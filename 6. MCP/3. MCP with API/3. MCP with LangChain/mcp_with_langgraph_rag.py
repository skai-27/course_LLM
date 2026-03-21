import asyncio
import os
from pathlib import Path
from typing import Literal, TypedDict

from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.graph import END, START, StateGraph

from common.elasticsearch_vector import ElasticsearchVectorStore

load_dotenv()


class AgentState(TypedDict, total=False):
    question: str
    route: Literal["rag", "mcp"]
    context: str
    answer: str


def build_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0,
    )


def build_mcp_server_config() -> dict:
    """Configure stdio MCP server with file workspace defaults."""
    base_dir = Path(__file__).resolve().parent
    sql_mcp_dir = base_dir.parent / "2. MCP with SQL"
    sql_mcp_script = sql_mcp_dir / "example_sql_mcp.py"
    mcp_workspace_dir = base_dir / "mcp_workspace"
    mcp_workspace_dir.mkdir(parents=True, exist_ok=True)

    # Child MCP process inherits environment, so set practical defaults here.
    os.environ.setdefault(
        "DATABASE_URL", "postgresql://admin:admin123@localhost:5432/mcp_db"
    )
    os.environ.setdefault("MCP_FS_ROOT", str(mcp_workspace_dir))

    return {
        "transport": "stdio",
        "command": os.getenv("MCP_SERVER_PYTHON", "python"),
        "args": [os.getenv("MCP_SERVER_SCRIPT", str(sql_mcp_script))],
    }


def build_vector_store() -> ElasticsearchVectorStore:
    es = Elasticsearch(
        [os.getenv("ES_URL", "http://localhost:9200")],
        basic_auth=(
            os.getenv("ES_USER", "elastic"),
            os.getenv("ES_PASSWORD", "changeme123!"),
        ),
        verify_certs=False,
    )
    embeddings = OpenAIEmbeddings(
        model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    )
    return ElasticsearchVectorStore(
        es_client=es,
        index_name=os.getenv("ES_INDEX", "course_keywords"),
        embeddings=embeddings,
        k=3,
    )


def route_question(state: AgentState) -> AgentState:
    question = state["question"].lower()
    mcp_keywords = ["sql", "주문", "고객", "상품", "api", "jsonplaceholder", "db"]
    route = "mcp" if any(keyword in question for keyword in mcp_keywords) else "rag"
    return {"route": route}


def retrieve_rag_context(state: AgentState) -> AgentState:
    store = build_vector_store()
    docs = store.hybrid_search_with_score(state["question"], k=3)
    context = "\n\n".join(f"- {doc.page_content}" for doc, _ in docs)
    return {"context": context}


async def answer_from_mcp(state: AgentState) -> AgentState:
    llm = build_llm()
    client = MultiServerMCPClient(
        {
            "user-course-sql-mcp": build_mcp_server_config(),
        }
    )
    tools = await client.get_tools()
    tool_llm = llm.bind_tools(tools)
    messages = [
        SystemMessage(
            content=(
                "당신은 MCP 도구 호출 전문가입니다. "
                "질문에 맞는 도구를 선택해서 필요한 조회를 수행하고 결과를 설명하세요. "
                "파일 작업 요청이면 fs_write_text_file/fs_read_text_file을 사용하고, "
                "반드시 MCP_FS_ROOT(=mcp_workspace) 하위 경로만 사용하세요."
            )
        ),
        HumanMessage(content=state["question"]),
    ]
    response = await tool_llm.ainvoke(messages)
    return {"answer": response.content}


def answer_from_rag(state: AgentState) -> AgentState:
    llm = build_llm()
    messages = [
        SystemMessage(
            content=(
                "당신은 RAG 도우미입니다. 제공된 컨텍스트를 기반으로만 답변하고 "
                "근거가 없으면 모른다고 답하세요."
            )
        ),
        HumanMessage(
            content=f"질문: {state['question']}\n\n컨텍스트:\n{state.get('context', '')}"
        ),
    ]
    response = llm.invoke(messages)
    return {"answer": response.content}


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("route", route_question)
    graph.add_node("retrieve_rag", retrieve_rag_context)
    graph.add_node("answer_rag", answer_from_rag)
    graph.add_node("answer_mcp", answer_from_mcp)

    graph.add_edge(START, "route")
    graph.add_conditional_edges(
        "route",
        lambda state: state["route"],
        {"rag": "retrieve_rag", "mcp": "answer_mcp"},
    )
    graph.add_edge("retrieve_rag", "answer_rag")
    graph.add_edge("answer_rag", END)
    graph.add_edge("answer_mcp", END)
    return graph.compile()


async def run_graph(question: str) -> None:
    app = build_graph()
    result = await app.ainvoke({"question": question})
    print("route:", result.get("route"))
    print("answer:", result.get("answer"))


if __name__ == "__main__":
    asyncio.run(run_graph("Semantic Search와 Embedding 차이를 설명해줘"))
    asyncio.run(run_graph("고객별 주문 수를 SQL로 조회해줘"))
