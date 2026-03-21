"""
강의 예제: Tools만 등록한 최소 MCP 서버.

실행: 프로젝트 루트에서
  python examples/example_tools.py
"""

from __future__ import annotations

from fastmcp import FastMCP

mcp = FastMCP("Course — Tools only")


@mcp.tool
def add_integers(a: int, b: int) -> int:
    """두 정수를 더한다. 타입 힌트가 도구 입력 스키마로 노출된다."""
    return a + b


@mcp.tool
def summarize_text(text: str, max_sentences: int = 2) -> str:
    """
    (데모) 긴 텍스트를 짧게 자른다. 실제 요약은 LLM이 하도록 Resource/Tool을 나눌 수도 있다.
    """
    parts = [p.strip() for p in text.replace("\n", " ").split(".") if p.strip()]
    selected = parts[: max(1, max_sentences)]
    return ". ".join(selected) + ("." if selected else "")


if __name__ == "__main__":
    mcp.run()
