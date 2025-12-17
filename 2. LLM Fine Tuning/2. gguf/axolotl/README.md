
# Dockerfile에 포함된 필수 요소
> 멀티 GPU Pod → 학습 → Hugging Face Hub 저장

| 기능        | 라이브러리          | 상태 |
| --------- | -------------- | -- |
| 멀티 GPU 실행 | `accelerate`   | ✅  |
| 분산 학습     | `deepspeed`    | ✅  |
| 모델 학습     | `axolotl`      | ✅  |
| HF Hub 저장 | `transformers` | ✅  |


