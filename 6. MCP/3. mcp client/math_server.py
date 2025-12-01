# MCP(Machine Control Protocol) 서버 구현을 위한 FastMCP 임포트
from mcp.server.fastmcp import FastMCP 

# "Math"라는 이름으로 MCP 서버 인스턴스 생성
mcp = FastMCP("Math") 

# 덧셈 연산을 수행하는 도구 함수
# @mcp.tool() 데코레이터를 사용하여 MCP 도구로 등록
@mcp.tool()
def add(a: int, b: int) -> int:
    """두 정수를 입력받아 합을 반환합니다.
    Args:
        a (int): 첫 번째 정수
        b (int): 두 번째 정수
    Returns:
        int: 두 정수의 합
    """
    return a + b

# 곱셈 연산을 수행하는 도구 함수
# @mcp.tool() 데코레이터를 사용하여 MCP 도구로 등록
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """두 정수를 입력받아 곱을 반환합니다.
    Args:
        a (int): 첫 번째 정수
        b (int): 두 번째 정수
    Returns:
        int: 두 정수의 곱
    """
    return a * b

# 메인 프로그램으로 실행될 때
if __name__ == "__main__":
    # stdio(표준 입출력)를 통신 방식으로 사용하여 MCP 서버 실행
    mcp.run(transport="stdio")

