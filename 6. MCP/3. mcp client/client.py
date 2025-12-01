from dotenv import load_dotenv 
# MCP 클라이언트 관련 모듈 임포트
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
# LangChain MCP 어댑터 도구 임포트
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.tools import load_mcp_tools
# ReAct 에이전트 생성을 위한 모듈 임포트
from langgraph.prebuilt import create_react_agent
# 비동기 작업을 위한 asyncio 임포트
import asyncio

load_dotenv()  # 환경 변수 로드

# OpenAI GPT-4 모델 초기화
from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-4o-mini")

# math_server.py를 실행하기 위한 서버 파라미터 설정
server_params = StdioServerParameters(
    command="python",
    args=["math_server.py"]
)

async def run_agent():
    # stdio 클라이언트를 사용하여 서버와 통신 설정
    async with stdio_client(server_params) as (read, write):
        # 클라이언트 세션 생성 및 초기화
        async with ClientSession(read, write) as session:
            await session.initialize()
            # MCP 도구 로드
            tools=await load_mcp_tools(session)
            # ReAct 에이전트 생성
            agent = create_react_agent(model, tools)
            # 에이전트에 수학 문제 전달 및 응답 수신
            agent_response = await agent.ainvoke(
                {"messages":"what's (4+6)x14?"}
            )
            for message in agent_response["messages"]:
                message.pretty_print()

            # 에이전트의 응답 중 실제 답변 부분만 반환
            return agent_response["messages"][3].content
        
# 메인 프로그램으로 실행될 때
if __name__ == "__main__":
    # 비동기 함수 실행 및 결과 출력
    result = asyncio.run(run_agent())
    print(f"Result: {result}")