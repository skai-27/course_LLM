## vLLM 마스터 클래스: 고성능 LLM 서빙 구축
### 1. vLLM 핵심 원리 이해 (오전)
vLLM이 왜 빠른지, 기존 추론 방식과 무엇이 다른지 기술적 근거를 학습합니다.

PagedAttention 메커니즘: OS의 가상 메모리 관리 기법을 응용한 KV 캐시 관리 이해.

연속 일괄 처리(Continuous Batching): 정적 배칭의 한계를 극복하는 동적 요청 처리 방식.

아키텍처 구조: Engine, Worker, 그리고 Ray를 활용한 분산 처리 구조.

### 2. 환경 구성 및 기본 서빙 (오전)
다양한 인프라 환경에서 vLLM을 안정적으로 구동하는 방법을 실습합니다.

도커 기반 배포: CUDA 버전 및 종속성 문제를 해결하기 위한 최적화된 Dockerfile 작성.

OpenAI 호환 서버: vllm.entrypoints.openai.api_server를 활용한 API 엔드포인트 생성.

런타임 설정: GPU 메모리 점유율(gpu_memory_utilization) 및 최대 컨텍스트 길이 설정.

### 3. 분산 추론 및 가속화 기법 (오후)
대규모 모델을 여러 개의 GPU에서 효율적으로 구동하는 고급 기술을 다룹니다.

분산 추론(Distributed Inference):

Tensor Parallelism (TP): 모델의 가중치를 나누어 병렬 연산하는 법.

Pipeline Parallelism (PP): 레이어 단위로 나누어 처리하는 기법.

양자화(Quantization) 적용: AWQ, GPTQ, FP8 등 다양한 양자화 모델 로드 및 성능 비교.

LoRA 어댑터 서빙: 하나의 엔진 인스턴스에서 여러 개의 LoRA 어댑터를 동시에 서빙하는 Multi-LoRA 설정.

### 4. 성능 모니터링 및 최적화 (오후)
실제 서비스 운영 환경에서 반드시 확인해야 할 지표와 튜닝 포인트를 학습합니다.

벤치마킹 도구: vLLM에서 제공하는 benchmark_serving.py를 활용한 처리량(Throughput) 측정.

지연 시간(Latency) 관리: TTFT(Time To First Token)와 TPOT(Time Per Output Token)의 개념 및 개선 전략.

프로덕션 가이드: Prometheus와 Grafana를 연동한 실시간 GPU 및 요청 상태 모니터링.

### 학습 목표 및 기대 효과
기술적 깊이: 단순 사용법을 넘어 PagedAttention 등 내부 알고리즘을 설명할 수 있습니다.

실무 적응력: 기업용 LLM 서비스 구축 시 비용 효율적인 GPU 자원 할당 능력을 갖춥니다.

환경 독립성: 클라우드(RunPod 등)와 온프레미스 환경 모두에 대응 가능한 배포 역량을 확보합니다.