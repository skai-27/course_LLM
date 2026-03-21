"""
강의 예제: Resources + Tools + Prompts를 한 서버에 묶은 통합 데모.

실행 (stdio, 기본):
  python examples/example_full.py

CLI:
  fastmcp run examples/example_full.py:mcp
"""

from __future__ import annotations

from fastmcp import FastMCP

mcp = FastMCP("Course — Full demo")


@mcp.resource("course://meta/server-info")
def server_info() -> dict:
    """이 서버가 노출하는 컴포넌트 요약."""
    return {
        "name": mcp.name,
        "components": ["resources", "tools", "prompts"],
    }


@mcp.tool()
def echo_message(message: str, times: int = 1) -> str:
    """(데모) 메시지를 여러 번 이어 붙인다. 부작용 없는 순수 함수 예시."""
    n = max(1, min(times, 5))
    return " | ".join([message] * n)


@mcp.prompt
def lesson_objectives(lesson_title: str) -> str:
    """강의 시작용 학습 목표 질문 템플릿."""
    return (
        f"강의 '{lesson_title}'의 맨 앞에 쓸 학습 목표를 3개 bullet로 작성해 줘. "
        "각 목표는 한 문장으로, 측정 가능하게 써 줘."
    )


if __name__ == "__main__":
    mcp.run()
