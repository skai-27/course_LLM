# Deep Agents 
- 공식 싸이트: https://docs.langchain.com/oss/python/deepagents/overview
- 학생들은 이미 LangChain, LangGraph 등을 이용해서 Multi Agents 강의를 들었음.
- 그런 학생들에게 아래 커리큘럼에 맞게 주피터파일을 만들어서 Deep Agents 강의자료를 만들어줘.

# 커리큘럼
## Deep Agents 개요  
- 파일이름: `1. Quickstart.ipynb`
- "첫 DeepAgent" 실행 경험 — 코드 + 입출력 + 간단한 플로우 체험

## Subagents & Workflow 분리 / 구조화
- 파일이름: `2. Subagents & Workflow.ipynb`
- 복잡한 작업을 모듈화 하는 법을 익히고, 작은 규모 프로젝트 구조 설계해보기
- Subagent 정의 방법 (dictionary-based, CompiledSubAgent)
- Subagent를 활용한 context isolation, 역할 분리

## Backend, Memory, Persistence 다루기
- 파일이름: `3. Backend & Persistent Storage.ipynb`
- "한 번 실행하고 끝"이 아닌, 지속 동작하는 agent 설계 실습
- 기본 backend (StateBackend) vs. persistent storage (StoreBackend / CompositeBackend)
- 장기 메모리, 세션 간 정보 유지
- 파일 시스템 활용법, 파일 입출력, 상태 관리

## Middleware & 고급 설정
- 파일이름: `4. Middleware.ipynb`
- Middleware의 의미와 효과 이해 + 커스텀 agent 설계 실습
- Middleware 구조 (TodoListMiddleware, FilesystemMiddleware, SubAgentMiddleware 등) 
- 커스텀 system_prompt 작성
- Human-in-the-loop 설정 (interrupt_on) 등 고급 옵션

