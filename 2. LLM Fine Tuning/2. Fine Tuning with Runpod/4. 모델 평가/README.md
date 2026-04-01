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
### lm-evaluation-harness vs 다른 평가 모듈

| 항목 | lm-evaluation-harness | Custom Eval (GPT-Judge 등) | HELM | LightEval | 단순 예제 평가 |
|---|---|---|---|---|---|
| 목적 | 표준 성능 비교 | 실사용 품질 검증 | 연구용 종합 분석 | 경량 벤치마크 | 데모 확인 |
| 객관성 | 높음 | 낮음 | 높음 | 높음 | 매우 낮음 |
| 파인튜닝 | 중간 | 매우 높음 | 중간 | 중간 | 매우 낮음 |
| 한국어 | 커스텀 필요 | 매우 쉬움 | 어려움 | 제한적 | 가능 |
| 실무 친화성 | 높음 | 매우 높음 | 낮음 | 중간 | 낮음 |

---
### lm-evaluation-harness + 한국어 특화 평가

| 구분 | lm-evaluation-harness | 한국어 특화 평가 | 이 조합의 의미 |
|---|---|---|---|
| 평가 대상 | 일반 LLM 능력 | 한국어 이해·지시 이행 | 튜닝 목적이 명확해짐 |
| 평가 방식 | 자동 채점 (MCQ 중심) | 정답 기반 + Judge 기반 | 객관성 + 품질 평가 |
| 비교 가능성 | 매우 높음 | 낮음 | 외부 모델과 공정 비교 |
| 튜닝 효과 가시성 | 낮음 | 매우 높음 | 파인튜닝 의미를 설명 가능 |
| 재현성 | 매우 높음 | 중간 | 논문·강의·Hub에 적합 |


---
### lm-eval + 한국어 특화 vs lm-eval + DeepEval

| 평가 관점 | lm-eval + 한국어 특화 | lm-eval + DeepEval |
|---|---|---|
| 평가 대상 | 모델 능력 (언어·지식 중심) | 응답 품질 (행동·추론 중심) |
| 한국어 이해력 | 매우 높음 | 높음 |
| Fine-tuning 효과 | 높음 | 매우 높음 |
| RAG / Tool 사용 적합성 | 매우 낮음 | 매우 높음 |
| 평가 지표 해석 용이성 | 매우 높음 | 중간 |
| 커스터마이징 난이도 | 낮음 | 중간~높음 |
| 외부 비교 가능성 | 높음 | 낮음 |
| 실무 적합성 | 중간 | 매우 높음 |
| 난이도 | 쉬움 | 중간 |

---
# 참고 사이트

### lm-evaluation-harness
- https://github.com/EleutherAI/lm-evaluation-harness
- https://devocean.sk.com/blog/techBoardDetail.do?ID=166716&boardType=techBlog
- https://techblog.lycorp.co.jp/ko/automating-llm-application-evaluation-with-harness

### DeepEval
- https://deepeval.com/
- https://github.com/confident-ai/deepeval
