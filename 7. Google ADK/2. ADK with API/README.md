## Phase 2: 도구 연동 및 확장성 (2~3주)
- 에이전트가 외부 세계와 상호작용할 수 있도록 "손과 발"을 달아주는 과정입니다.
- 내장 도구 활용: Google Search, Code Interpreter 등 기본 도구 연결.
- 커스텀 도구(Custom Tools) 개발: Python 함수를 ADK 도구로 변환 (Docstring 기반 자동 파싱).
- API 통합: 외부 REST API를 호출하여 실시간 데이터를 가져오는 에이전트 설계.
- Model Context Protocol (MCP): MCP를 통한 표준화된 도구 서버 연결 및 확장.

# 실습 프로젝트 아이디어
- 지능형 여행 플래너: 날씨 확인(도구), 일정 생성(에이전트), 이메일 발송(API)을 결합.