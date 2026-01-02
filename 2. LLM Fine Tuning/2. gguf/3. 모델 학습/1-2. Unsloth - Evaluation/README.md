# Docker Hub에 배포하는 명령어
```shell
docker build -t goodwon593/unsloth-deepeval-runpod:3.7.6 .
docker push goodwon593/unsloth-deepeval-runpod:3.7.6

# CPU용
docker run -it --rm -p 8080:8080 -v ./workspace:/workspace goodwon593/unsloth-deepeval-runpod:3.7.6
```

---
# lm-evaluation-harness vs 다른 평가 모듈 
| 항목                    | lm-evaluation-harness | Custom Eval (GPT-Judge 등) | HELM      | LightEval | 단순 예제 평가 |
| --------------------- | --------------------- | ------------------------- | --------- | --------- | -------- |
| 핵심 목적                 | **표준 성능 비교**          | 실사용 품질 검증                 | 연구용 종합 분석 | 경량 벤치마크   | 데모 확인    |
| 객관성                   | ⭐⭐⭐⭐⭐                 | ⭐⭐                        | ⭐⭐⭐⭐⭐     | ⭐⭐⭐⭐      | ⭐        |
| 외부 비교 가능성             | ⭐⭐⭐⭐⭐                 | ❌                         | ⭐⭐⭐⭐      | ⭐⭐⭐       | ❌        |
| 태스크 수                 | 매우 많음                 | 직접 정의                     | 매우 많음     | 중간        | 매우 적음    |
| 자동 채점                 | ✅                     | 부분적                       | ✅         | ✅         | ❌        |
| 파인튜닝 효과 분석            | ⭐⭐⭐                   | ⭐⭐⭐⭐⭐                     | ⭐⭐⭐       | ⭐⭐⭐       | ⭐        |
| Instruction / Chat 평가 | ❌ (제한적)               | ⭐⭐⭐⭐⭐                     | ⭐⭐⭐       | ⭐⭐        | ⭐⭐       |
| 한국어 확장                | 커스텀 필요                | 매우 쉬움                     | 어려움       | 제한적       | 가능       |
| 속도 / 경량성              | ⭐⭐⭐⭐                  | ⭐⭐⭐                       | ⭐         | ⭐⭐⭐⭐⭐     | ⭐⭐⭐⭐⭐    |
| 실무 친화성                | ⭐⭐⭐⭐                  | ⭐⭐⭐⭐⭐                     | ⭐         | ⭐⭐⭐       | ⭐⭐       |


---
# lm-evaluation-harness + 한국어 특화 평가

| 구분        | lm-evaluation-harness | 한국어 특화 평가                       | 이 조합의 의미          |
| --------- | --------------------- | ------------------------------- | ----------------- |
| 평가 목적     | **표준 성능 비교**          | **실사용 적합성 검증**                  | “점수 + 실력”을 동시에 증명 |
| 평가 대상     | 일반 LLM 능력             | 한국어 이해·지시 이행                    | 튜닝 목적이 명확해짐       |
| 대표 태스크    | HellaSwag, ARC, MMLU  | KMMLU, 한국어 QA, Instruction Eval | 범용 + 로컬 도메인       |
| 평가 방식     | 자동 채점 (MCQ 중심)        | 정답 기반 + Judge 기반                | 객관성 + 품질 평가       |
| 비교 가능성    | ⭐⭐⭐⭐⭐                 | ⭐⭐                              | 외부 모델과 공정 비교      |
| 서비스 연관성   | ⭐⭐                    | ⭐⭐⭐⭐⭐                           | 실제 배포 판단 가능       |
| 튜닝 효과 가시성 | ⭐⭐                    | ⭐⭐⭐⭐⭐                           | 파인튜닝 의미를 설명 가능    |
| 재현성       | ⭐⭐⭐⭐⭐                 | ⭐⭐⭐                             | 논문·강의·Hub에 적합     |
| 자동화 용이성   | 매우 쉬움                 | 중간                              | CI/스크립트화 가능       |

---
# lm-eval + 한국어 특화 vs lm-eval + DeepEval

| 평가 관점                    | lm-eval + 한국어 특화     | lm-eval + DeepEval   |
| ------------------------ | -------------------- | -------------------- |
| 평가 대상                    | **모델 능력 (언어·지식 중심)** | **응답 품질 (행동·추론 중심)** |
| 한국어 이해력                  | ⭐⭐⭐⭐⭐                | ⭐⭐⭐⭐                 |
| Fine-tuning 효과           | ⭐⭐⭐⭐                 | ⭐⭐⭐⭐⭐                |
| Instruction tuning 검증    | ⭐⭐                   | ⭐⭐⭐⭐⭐                |
| Chain-of-Thought / 추론 평가 | ⭐⭐                   | ⭐⭐⭐⭐⭐                |
| RAG / Tool 사용 적합성        | ⭐                    | ⭐⭐⭐⭐⭐                |
| 평가 지표 해석 용이성             | ⭐⭐⭐⭐⭐                | ⭐⭐⭐                  |
| 객관성                      | ⭐⭐⭐⭐⭐                | ⭐⭐⭐                  |
| 재현성                      | ⭐⭐⭐⭐⭐                | ⭐⭐⭐                  |
| 커스터마이징 난이도               | 낮음                   | 중간~높음                |
| 외부 비교 가능성                | ⭐⭐⭐⭐                 | ⭐⭐                   |
| 실무 적합성                   | ⭐⭐⭐                  | ⭐⭐⭐⭐⭐                |
| Hub 공개 설득력               | ⭐⭐⭐⭐⭐                | ⭐⭐⭐                  |
| 난이도                      | 쉬움                   | 중간                   |
| 비용                       | 낮음                   | 중간 (Self-host 가능)    |

---
# 참고 싸이트 
### lm-evaluation-harness
- https://github.com/EleutherAI/lm-evaluation-harness
- https://devocean.sk.com/blog/techBoardDetail.do?ID=166716&boardType=techBlog
- https://techblog.lycorp.co.jp/ko/automating-llm-application-evaluation-with-harness

### DeepEval
- https://deepeval.com/
- https://github.com/confident-ai/deepeval


