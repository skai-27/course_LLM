# MCP Server 개발 입문 (SDK 활용)

이 모듈은 **FastMCP**로 MCP 서버를 만들 때 반드게 거치는 네 가지 축—**Resources**, **Tools**, **Prompts**, **stdio 배포·테스트**—을 강의 순서에 맞춰 정리합니다.

## 사용 라이브러리

- [FastMCP](https://gofastmcp.com/) (Python MCP 서버 SDK)

## 환경 준비

```bash
pip install -r requirements.txt
```

## 핵심 컴포넌트와 자료 위치

| 컴포넌트 | 역할(한 줄) | 설명 문서 | 예제 코드 |
|----------|-------------|-----------|-----------|
| **Resources** | URI로 **읽기 전용** 데이터 노출 | [docs/01-resources.md](docs/01-resources.md) | [examples/example_resources.py](examples/example_resources.py) |
| **Tools** | LLM이 호출하는 **실행 가능한 함수** | [docs/02-tools.md](docs/02-tools.md) | [examples/example_tools.py](examples/example_tools.py) |
| **Prompts** | **재사용·파라미터화**된 메시지 템플릿 | [docs/03-prompts.md](docs/03-prompts.md) | [examples/example_prompts.py](examples/example_prompts.py) |
| **stdio** | 로컬 클라이언트와 **표준 입출력**으로 연결 | [docs/04-stdio-test.md](docs/04-stdio-test.md) | 아래 실행 방법 참고 |

**통합 예제**(세 컴포넌트를 한 서버에 묶음): [examples/example_full.py](examples/example_full.py)

## 권장 학습 순서

1. [docs/00-overview.md](docs/00-overview.md) — MCP가 무엇인지, 서버·클라이언트 관계
2. Resources → Tools → Prompts 순으로 문서 + 해당 `examples/*.py` 실행
3. [docs/04-stdio-test.md](docs/04-stdio-test.md)로 Cursor 등 클라이언트에 붙여 보기

## 서버 실행 (stdio)

프로젝트 루트(이 폴더)에서:

```bash
python examples/example_full.py
```

또는 FastMCP CLI:

```bash
fastmcp run examples/example_full.py:mcp
```

자세한 테스트 방법은 [docs/04-stdio-test.md](docs/04-stdio-test.md)를 참고하세요.

## 참고 링크

- [FastMCP 문서](https://gofastmcp.com/)
- [MCP 사양](https://modelcontextprotocol.io/)
