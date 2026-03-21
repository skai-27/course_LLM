"""
강의 예제: Prompts만 등록한 최소 MCP 서버.

실행: 프로젝트 루트에서
  python examples/example_prompts.py
"""

from __future__ import annotations

from fastmcp import FastMCP

mcp = FastMCP("Course — Prompts only")


@mcp.prompt
def explain_for_beginner(topic: str) -> str:
    """초보자용 설명을 요청하는 사용자 메시지 템플릿."""
    return (
        f"'{topic}'을(를) 비유와 짧은 예시를 들어 초보자도 이해할 수 있게 설명해 줘. "
        "필요하면 단계별로 나눠서 말해 줘."
    )


@mcp.prompt
def code_review_request(language: str, code_snippet: str) -> str:
    """코드 리뷰를 요청하는 템플릿."""
    return (
        f"다음 {language} 코드를 리뷰해 줘. "
        "버그 가능성, 가독성, 성능, 보안 관점에서 피드백을 줘.\n\n"
        f"```{language}\n{code_snippet}\n```"
    )


if __name__ == "__main__":
    mcp.run()
