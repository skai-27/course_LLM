import asyncio
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI

logging.basicConfig(level=logging.INFO)

_ROOT = Path(__file__).resolve().parent
load_dotenv(_ROOT / ".env")

MCP_SERVER_SCRIPT = _ROOT / "mcp_servers.py"


def _base_url() -> str:
    host = os.environ.get("MCP_HTTP_HOST", "127.0.0.1").strip()
    port = os.environ.get("MCP_HTTP_PORT", "8766").strip()
    return f"http://{host}:{port}"


def _mcp_connections() -> dict[str, Any]:
    """MCP 연결 설정. 기본은 상시 구동형 SSE(URL). MCP_USE_STDIO=1 이면 stdio."""
    if not MCP_SERVER_SCRIPT.is_file():
        raise FileNotFoundError(f"MCP 서버 스크립트 없음: {MCP_SERVER_SCRIPT}")

    use_stdio = os.environ.get("MCP_USE_STDIO", "").lower() in ("1", "true", "yes")
    if use_stdio:
        return {
            "course_rag": {
                "command": sys.executable,
                "args": [str(MCP_SERVER_SCRIPT)],
                "transport": "stdio",
            }
        }

    mode = os.environ.get("MCP_CLIENT_TRANSPORT", "sse").lower().strip()
    base = _base_url()

    if mode in ("streamable-http", "streamable_http", "http"):
        raw = os.environ.get("MCP_STREAMABLE_HTTP_URL", "").strip()
        if raw:
            url = raw
        else:
            path = (os.environ.get("MCP_STREAMABLE_HTTP_PATH") or "/mcp").strip() or "/mcp"
            if not path.startswith("/"):
                path = "/" + path
            url = urljoin(base + "/", path.lstrip("/"))
        return {"course_rag": {"transport": "http", "url": url}}

    raw = os.environ.get("MCP_SSE_URL", "").strip()
    if raw:
        url = raw
    else:
        path = (os.environ.get("MCP_SSE_PATH") or "/sse").strip() or "/sse"
        if not path.startswith("/"):
            path = "/" + path
        url = urljoin(base + "/", path.lstrip("/"))
    return {"course_rag": {"transport": "sse", "url": url}}


_MCP_SERVER_NAME = "course_rag"


async def run_once(question: str) -> str:
    """질문 한 번에 대해 MCP 도구를 쓸 수 있는 에이전트를 돌리고, 최종 답 문자열을 반환한다.

    기본은 SSE/HTTP URL로 이미 떠 있는 MCP 서버에 붙는다(상시 프로세스).
    stdio는 MCP_USE_STDIO=1 일 때만 사용한다.

    도구 목록과 도구 호출이 같은 세션을 쓰도록 session + load_mcp_tools(session)을 사용한다.
    """
    connections = _mcp_connections()
    client = MultiServerMCPClient(connections)
    conn = connections[_MCP_SERVER_NAME]
    transport = conn.get("transport", "?")
    endpoint = conn.get("url") or f"{sys.executable} {MCP_SERVER_SCRIPT}"

    t_session = time.perf_counter()
    async with client.session(_MCP_SERVER_NAME) as session:
        t_tools = time.perf_counter()
        tools = await load_mcp_tools(session, server_name=_MCP_SERVER_NAME)
        logging.info(
            "MCP 도구 목록 로드(%s, 동일 세션): %.3fs, 도구 %d개, endpoint=%s",
            transport,
            time.perf_counter() - t_tools,
            len(tools),
            endpoint,
        )
        logging.debug(
            "도구 목록: %s",
            [(t.name, (t.description or "")[:80]) for t in tools],
        )

        model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        agent = create_agent(
            model,
            tools,
            system_prompt="""너는 강의 보조 에이전트다.
- 수업 용어·개념 질문은 반드시 rag_vector_search로 근거를 찾은 뒤, 검색 결과를 바탕으로 답한다.
- 학생 메모·실습 파일·요약 저장은 workspace_* 도구만 사용한다(허용 루트: mcp_workspace).
- 검색 결과에 없는 내용은 추측하지 말고, 검색 쿼리를 바꿔 다시 시도하거나 솔직히 모른다고 말한다.""",
        )

        t_agent = time.perf_counter()
        result = await agent.ainvoke(
            {"messages": [HumanMessage(content=question)]},
            config={"recursion_limit": 40},
        )
        logging.info("에이전트 실행(ainvoke): %.3fs", time.perf_counter() - t_agent)

    logging.info(
        "MCP 세션 전체(연결~종료): %.3fs",
        time.perf_counter() - t_session,
    )
    messages = result.get("messages", [])
    if not messages:
        return ""
    return str(messages[-1].content)


def main() -> None:
    if len(sys.argv) < 2:
        print(
            '사용법: python agent_with_mcp.py "질문"\n'
            "예: python agent_with_mcp.py 임베딩이 뭐야?\n\n"
            "먼저 다른 터미널에서 MCP 서버를 띄운다:\n"
            "  python mcp_servers.py --sse\n"
            "  또는: python mcp_servers.py --streamable-http\n"
            "그다음 MCP_CLIENT_TRANSPORT(sse|streamable-http), MCP_HTTP_HOST, MCP_HTTP_PORT 등 .env 확인.\n"
            "stdio만 쓸 때: MCP_USE_STDIO=1",
            file=sys.stderr,
        )
        sys.exit(1)
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        print("질문이 비어 있습니다.", file=sys.stderr)
        sys.exit(1)

    logging.info(f"Question: {question}")
    answer = asyncio.run(run_once(question))
    logging.info(f"Answer: {answer}")

if __name__ == "__main__":
    main()
