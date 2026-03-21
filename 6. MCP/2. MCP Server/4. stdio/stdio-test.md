---
style: |
  img {
    display: block;
    float: none;
    margin-left: auto;
    margin-right: auto;
  }
marp: true
paginate: true
---
# 04. stdio 배포와 로컬 테스트

## 학습 목표

- MCP 로컬 연결이 왜 **stdio(표준 입출력)** 를 쓰는지 설명할 수 있다.
- `python ...py`와 `fastmcp run ...` 두 가지 실행 방식의 차이를 안다.
- IDE(예: Cursor)에 MCP 서버를 등록할 때 **명령줄·작업 디렉터리**를 올바르게 쓴다.

## stdio가 의미하는 것

많은 MCP 클라이언트는 서버를 **자식 프로세스**로 실행하고, **stdin/stdout 파이프**로 JSON-RPC 메시지를 주고받습니다.

- 별도 포트 개방 없이 로컬에서 동작하기 쉽습니다.
- “서버 = 내 PC에서 도는 짧은 수명 프로세스”라는 멘탈 모델이 맞습니다.

## 이 레포에서 서버 실행

프로젝트 루트(`2. MCP Server 개발` 폴더)에서:

```bash
pip install -r requirements.txt
python examples/example_full.py
```

실행 후 **아무 터미널 출력도 기대하지 마세요.** stdio는 대화용 채널이라, 클라이언트가 붙어야 의미가 있습니다.

## FastMCP CLI

```bash
fastmcp run examples/example_full.py:mcp
```

- `파일경로:변수명` 형태로 **모듈에서 `FastMCP` 인스턴스**를 가리킵니다.
- CLI는 파일의 `if __name__ == "__main__":` 블록을 실행하지 않고 import 할 수 있습니다. ([Quickstart](https://gofastmcp.com/getting-started/quickstart))

## Cursor에 등록하는 예시

Cursor MCP 설정에 대략 다음과 같은 형태로 추가합니다(경로는 본인 환경에 맞게 수정).

```json
{
  "mcpServers": {
    "course-mcp-full": {
      "command": "python",
      "args": ["examples/example_full.py"],
      "cwd": "C:/develop/github/course_LLM/6. MCP/2. MCP Server 개발"
    }
  }
}
```

가상환경을 쓰면 `command`를 해당 `python.exe` 절대 경로로 바꾸는 것이 안전합니다.

## 디버깅 팁

- 서버 코드에 `print()`를 남발하면 **프로토콜 스트림을 오염**시킬 수 있습니다. 로그는 MCP `Context`의 로깅/알림 기능이나 파일 로거를 고려하세요.
- “연결이 안 된다”면 **cwd**, **Python 경로**, **의존성 설치 여부**를 먼저 확인합니다.

## 체크리스트

- [ ] `example_full.py`를 stdio로 띄운 상태에서 클라이언트가 도구/리소스를 본다.
- [ ] (선택) HTTP 전송(`mcp.run(transport="http", ...)`)과 stdio의 차이를 문서로 한 줄 요약해 본다.
