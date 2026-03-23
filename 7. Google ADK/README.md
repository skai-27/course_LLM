# Google ADK 마스터 커리큘럼

## Phase 1: ADK 기초 및 환경 구성 (1~2주)
- 에이전트의 기본 개념을 이해하고, 첫 번째 독립 실행형 에이전트를 구축합니다.
- ADK 아키텍처 이해: Agent(두뇌), Session(기억), Runner(실행기)의 삼각 구조 파악.
- 개발 환경 셋업: Python SDK 설치 및 Google Cloud Project(Vertex AI) 연동.
- 첫 번째 에이전트 생성: 간단한 페르소나와 지침(Instruction)을 가진 에이전트 실행.
- 디버깅 및 UI: ADK Web UI를 활용한 실시간 대화 및 상태 모니터링.

## Phase 2: 도구 연동 및 확장성 (2~3주)
- 에이전트가 외부 세계와 상호작용할 수 있도록 "손과 발"을 달아주는 과정입니다.
- 내장 도구 활용: Google Search, Code Interpreter 등 기본 도구 연결.
- 커스텀 도구(Custom Tools) 개발: Python 함수를 ADK 도구로 변환 (Docstring 기반 자동 파싱).
- API 통합: 외부 REST API를 호출하여 실시간 데이터를 가져오는 에이전트 설계.
- Model Context Protocol (MCP): MCP를 통한 표준화된 도구 서버 연결 및 확장.

## Phase 3: 세션 관리와 기억(Memory) (3~4주)
- 단발성 대화가 아닌, 맥락을 기억하고 사용자의 의도를 장기적으로 추적하는 에이전트를 만듭니다.
- Session State 활용: 대화 중 발생하는 가변적인 데이터(장바구니, 사용자 선택지 등) 관리.
- Context Window 최적화: 대화 이력 요약 및 필수 정보 유지 전략.
- RAG(Retrieval-Augmented Generation) 통합: Vertex AI Search 또는 벡터 DB를 연동한 장기 기억(Memory) 구현.

## Phase 4: 멀티 에이전트 오케스트레이션 (4~6주)
- 여러 전문 에이전트가 협업하여 복잡한 문제를 해결하는 시스템을 구축합니다.
- 협업 패턴 설계:
    - Sequential: 순차적으로 업무를 전달하는 파이프라인.
    - Parallel: 병렬로 작업을 수행하고 결과를 취합하는 구조.
    - Router: 사용자 요청에 따라 적절한 전문 에이전트에게 할당.
    - Hierarchical System: 관리자 에이전트(Manager)가 하위 에이전트(Worker)를 통제하는 계층 구조.
- 에이전트 간 통신: 데이터 교환 포맷 정의 및 상태 공유.

## Phase 5: 운영 및 배포 (Production Ready) (6~8주)
- 실제 서비스 환경에 적용하기 위한 안정성과 보안을 강화합니다.
- 평가(Evaluation) 및 가드레일: 에이전트의 응답 품질 측정 및 유해 콘텐츠 필터링.
- Docker 및 Cloud 배포: 에이전트를 컨테이너화하여 Cloud Run 또는 Vertex AI Agent Engine에 배포.
- 모니터링: OpenTelemetry 기반 로그 추적 및 성능 병목 현상 분석.

# 실습 프로젝트 아이디어
- 지능형 여행 플래너: 날씨 확인(도구), 일정 생성(에이전트), 이메일 발송(API)을 결합.
- 데이터 분석 자동화 에이전트: CSV 파일을 읽어 분석하고 시각화 차트를 생성하는 에이전트.
- 멀티 에이전트 고객 지원 시스템: 기술 문의, 결제 문의, 일반 문의를 구분하여 처리하는 협업 시스템.
