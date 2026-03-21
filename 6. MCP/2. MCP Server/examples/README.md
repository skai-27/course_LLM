# 예제 스크립트

| 파일 | 내용 |
|------|------|
| `example_resources.py` | `@mcp.resource` — URI·템플릿 URI |
| `example_tools.py` | `@mcp.tool` — 인자 스키마·기본값 |
| `example_prompts.py` | `@mcp.prompt` — 재사용 메시지 템플릿 |
| `example_full.py` | 위 세 가지를 한 서버에 통합 |

각 파일은 동일하게 `mcp.run()`으로 **stdio** 서버를 띄웁니다. 단독 실행 시 터미널에 프롬프트가 뜨지 않는 것이 정상이며, MCP 클라이언트가 프로세스에 연결해야 동작이 보입니다.

설명 문서는 상위 폴더의 [docs/](../docs/)를 참고하세요.
