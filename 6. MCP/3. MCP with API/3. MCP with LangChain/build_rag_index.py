"""
data/*.txt 를 읽어 Elasticsearch에 벡터 인덱스를 구축한다.
실행 전: elasticsearch/docker-compose 로 ES 기동, OPENAI_API_KEY 설정.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

load_dotenv(_ROOT / ".env")

DEFAULT_INDEX = "course_rag_mcp"
EMBED_DIMS = 1536  # text-embedding-3-small 기본 차원
DATA_GLOB = ["rag-keywords.txt", "web-keywords.txt"]


def _chunk_text(text: str, max_chars: int = 1200, overlap: int = 150) -> list[str]:
    text = text.strip()
    if not text:
        return []
    chunks: list[str] = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + max_chars, n)
        chunks.append(text[start:end])
        if end >= n:
            break
        start = max(0, end - overlap)
    return chunks


def load_documents(data_dir: Path) -> list[Document]:
    docs: list[Document] = []
    for name in DATA_GLOB:
        path = data_dir / name
        if not path.is_file():
            continue
        raw = path.read_text(encoding="utf-8")
        for i, chunk in enumerate(_chunk_text(raw)):
            docs.append(
                Document(
                    page_content=chunk,
                    metadata={"source": name, "chunk": i},
                )
            )
    return docs


def ensure_index(es: Elasticsearch, index_name: str, *, delete_existing: bool) -> None:
    if delete_existing and es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)

    if es.indices.exists(index=index_name):
        return

    mapping = {
        "properties": {
            "text": {"type": "text"},
            "embedding": {
                "type": "dense_vector",
                "dims": EMBED_DIMS,
                "index": True,
                "similarity": "cosine",
            },
            "metadata": {"type": "object", "enabled": True},
        }
    }
    es.indices.create(index=index_name, mappings=mapping)


def main() -> None:
    parser = argparse.ArgumentParser(description="RAG용 Elasticsearch 인덱스 구축")
    parser.add_argument(
        "--recreate",
        action="store_true",
        help="기존 인덱스가 있으면 삭제 후 재생성",
    )
    parser.add_argument(
        "--index",
        default=os.environ.get("RAG_INDEX_NAME", DEFAULT_INDEX),
        help=f"인덱스 이름 (기본: 환경변수 RAG_INDEX_NAME 또는 {DEFAULT_INDEX})",
    )
    args = parser.parse_args()

    es_url = os.environ.get("ELASTICSEARCH_URL", "http://localhost:9200")
    es_user = os.environ.get("ELASTIC_USER", "elastic")
    es_password = os.environ.get("ELASTIC_PASSWORD", "changeme123!")

    es = Elasticsearch(
        es_url,
        basic_auth=(es_user, es_password),
        verify_certs=False,
        request_timeout=120,
    )
    if not es.ping():
        raise SystemExit("Elasticsearch ping 실패. docker-compose 기동과 인증 정보를 확인하세요.")

    data_dir = _ROOT / "data"
    documents = load_documents(data_dir)
    if not documents:
        raise SystemExit(f"{data_dir} 에서 문서를 찾지 못했습니다.")

    embedding_model = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    embeddings = OpenAIEmbeddings(model=embedding_model)

    ensure_index(es, args.index, delete_existing=args.recreate)

    texts = [d.page_content for d in documents]
    vectors = embeddings.embed_documents(texts)

    def actions():
        for doc, vec in zip(documents, vectors, strict=True):
            yield {
                "_index": args.index,
                "_source": {
                    "text": doc.page_content,
                    "embedding": vec,
                    "metadata": doc.metadata,
                },
            }

    n_ok, errors = bulk(es, actions(), refresh=True, raise_on_error=False)
    if errors:
        raise SystemExit(f"Bulk 인덱싱 오류: {errors}")

    count = es.count(index=args.index)["count"]
    print(f"인덱스 '{args.index}' 에 문서 {count}건 반영 완료 (bulk reports: {n_ok}).")


if __name__ == "__main__":
    main()
