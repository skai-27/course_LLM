"""
MCP 도구(RAG·워크스페이스)를 붙인 LangChain 에이전트 데모.

langchain-mcp-adapters의 MultiServerMCPClient로 mcp_servers.py를 띄우고,
create_agent로 질의에 맞게 도구를 호출한다.

실행 예:
  python agent_with_mcp.py "임베딩이 뭐야?"

사전 준비:
  1) elasticsearch/docker-compose 기동
  2) python build_rag_index.py --recreate
  3) .env 에 OPENAI_API_KEY (필요 시 ELASTIC_* , RAG_INDEX_NAME)
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI

_ROOT = Path(__file__).resolve().parent
load_dotenv(_ROOT / ".env")

MCP_SERVER_SCRIPT = _ROOT / "mcp_servers.py"

SYSTEM_PROMPT = """너는 강의 보조 에이전트다.
- 수업 용어·개념 질문은 반드시 rag_vector_search로 근거를 찾은 뒤, 검색 결과를 바탕으로 답한다.
- 학생 메모·실습 파일·요약 저장은 workspace_* 도구만 사용한다(허용 루트: mcp_workspace).
- 검색 결과에 없는 내용은 추측하지 말고, 검색 쿼리를 바꿔 다시 시도하거나 솔직히 모른다고 말한다."""


def _mcp_connections() -> dict:
    if not MCP_SERVER_SCRIPT.is_file():
        raise FileNotFoundError(f"MCP 서버 스크립트 없음: {MCP_SERVER_SCRIPT}")
    return {
        "course_rag": {
            "command": sys.executable,
            "args": [str(MCP_SERVER_SCRIPT)],
            "transport": "stdio",
        }
    }


async def run_once(question: str) -> str:
    """질문 한 번에 대해 MCP 도구를 쓸 수 있는 에이전트를 돌리고, 최종 답 문자열을 반환한다."""
    client = MultiServerMCPClient(_mcp_connections())
    tools = await client.get_tools()
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    agent = create_agent(model, tools, system_prompt=SYSTEM_PROMPT)
    result = await agent.ainvoke(
        {"messages": [HumanMessage(content=question)]},
        config={"recursion_limit": 40},
    )
    messages = result.get("messages", [])
    if not messages:
        return ""
    return str(messages[-1].content)


def main() -> None:
    if len(sys.argv) < 2:
        print(
            '사용법: python agent_with_mcp.py "질문"\n'
            "예: python agent_with_mcp.py 임베딩이 뭐야?",
            file=sys.stderr,
        )
        sys.exit(1)
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        print("질문이 비어 있습니다.", file=sys.stderr)
        sys.exit(1)
    answer = asyncio.run(run_once(question))
    print(answer)


if __name__ == "__main__":
    main()
