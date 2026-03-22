"""
강의용 MCP 서버 (단일 파일에 도구 모음).

- RAG: Elasticsearch 용어집 검색
- 워크스페이스: mcp_workspace 폴더 안의 파일 목록/읽기/쓰기

에이전트(`agent_with_mcp.py`)는 langchain-mcp-adapters로
이 스크립트를 stdio 서브프로세스로 실행해 도구를 호출한다.
"""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from fastmcp import FastMCP
from langchain_openai import OpenAIEmbeddings

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from common.elasticsearch_vector import ElasticsearchVectorStore

load_dotenv(_ROOT / ".env")

MAX_WS_READ = 256_000
MAX_WS_WRITE = 256_000

mcp = FastMCP(
    "Course — RAG & Workspace",
    instructions=(
        "강의용 지식베이스(RAG)는 rag_vector_search로 검색한다. "
        "메모·노트·실습 파일은 workspace_list_files, workspace_read_text, workspace_write_text로 "
        "mcp_workspace 폴더 안에서만 다룬다."
    ),
)

_store: ElasticsearchVectorStore | None = None


def _workspace_root() -> Path:
    raw = os.environ.get("MCP_WORKSPACE_ROOT")
    if raw:
        return Path(raw).resolve()
    return (_ROOT / "mcp_workspace").resolve()


def _safe_workspace_path(relative_path: str) -> Path:
    rel = relative_path.strip().replace("\\", "/").lstrip("/")
    root = _workspace_root()
    target = (root / rel).resolve()
    try:
        target.relative_to(root)
    except ValueError as e:
        raise RuntimeError("경로가 workspace 루트 밖을 가리킵니다.") from e
    return target


def _get_vector_store() -> ElasticsearchVectorStore:
    global _store
    if _store is not None:
        return _store

    es_url = os.environ.get("ELASTICSEARCH_URL", "http://localhost:9200")
    es_user = os.environ.get("ELASTIC_USER", "elastic")
    es_password = os.environ.get("ELASTIC_PASSWORD", "changeme123!")
    index_name = os.environ.get("RAG_INDEX_NAME", "course_rag_mcp")
    embed_model = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

    es = Elasticsearch(
        es_url,
        basic_auth=(es_user, es_password),
        verify_certs=False,
        request_timeout=60,
    )
    embeddings = OpenAIEmbeddings(model=embed_model)
    _store = ElasticsearchVectorStore(
        es_client=es,
        index_name=index_name,
        embeddings=embeddings,
        k=4,
    )
    return _store


@mcp.tool()
async def rag_vector_search(query: str, k: int = 4) -> str:
    """지식 용어집(RAG 인덱스)에서 의미 유사도 검색. 'OOO가 뭐야', '정의 알려줘' 등에 사용."""
    q = query.strip()
    if not q:
        raise RuntimeError("query가 비어 있습니다.")
    k = max(1, min(int(k), 20))
    store = _get_vector_store()
    store.k = k
    docs = store.similarity_search(q, k=k)
    if not docs:
        return "(검색 결과 없음)"
    lines = []
    for i, d in enumerate(docs, 1):
        meta = d.metadata or {}
        src = meta.get("source", "")
        lines.append(f"[{i}] (source={src})\n{d.page_content}")
    return "\n\n---\n\n".join(lines)


@mcp.tool()
async def workspace_list_files(relative_dir: str = "") -> str:
    """mcp_workspace 내 하위 디렉터리 목록과 파일 이름을 나열한다. relative_dir는 workspace 기준 상대 경로."""
    base = _safe_workspace_path(relative_dir or ".")
    if not base.exists():
        return "(경로 없음)"
    if base.is_file():
        return base.name
    rows = sorted(base.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
    if not rows:
        return "(비어 있음)"
    return "\n".join(f"{'[dir] ' if p.is_dir() else ''}{p.name}" for p in rows)


@mcp.tool()
async def workspace_read_text(relative_path: str) -> str:
    """mcp_workspace 아래 텍스트 파일을 읽는다."""
    path = _safe_workspace_path(relative_path)
    if not path.is_file():
        raise RuntimeError("파일이 없거나 파일이 아닙니다.")
    data = path.read_bytes()
    if len(data) > MAX_WS_READ:
        raise RuntimeError(f"파일이 너무 큽니다(최대 {MAX_WS_READ}바이트).")
    return data.decode("utf-8", errors="replace")


@mcp.tool()
async def workspace_write_text(
    relative_path: str,
    content: str,
    mode: Literal["create", "overwrite"] = "create",
) -> str:
    """mcp_workspace 아래에 텍스트를 쓴다. create는 기존 파일이 있으면 실패."""
    path = _safe_workspace_path(relative_path)
    raw = content.encode("utf-8")
    if len(raw) > MAX_WS_WRITE:
        raise RuntimeError(f"내용이 너무 큽니다(최대 {MAX_WS_WRITE}바이트).")
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and mode == "create":
        raise RuntimeError("파일이 이미 있어 create 모드로 쓸 수 없습니다.")
    path.write_bytes(raw)
    return f"저장 완료: {path.relative_to(_workspace_root())} ({len(raw)} bytes)"


def main() -> None:
    if "--sse" in sys.argv:
        asyncio.run(
            mcp.run_http_async(
                transport="sse",
                host=os.environ.get("MCP_HTTP_HOST", "127.0.0.1"),
                port=int(os.environ.get("MCP_HTTP_PORT", "8766")),
            )
        )
    else:
        mcp.run()


if __name__ == "__main__":
    main()
