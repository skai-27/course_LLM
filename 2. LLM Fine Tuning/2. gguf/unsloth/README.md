
# Dockerfile에 포함된 필수 요소
> RunPod에서 모델 학습 → Hugging Face Hub 저장

| 기능       | 라이브러리             | 상태 |
| -------- | ----------------- | -- |
| 모델 로딩/학습 | `unsloth`         | ✅  |
| HF 모델 구조 | `transformers`    | ✅  |
| QLoRA    | `bitsandbytes`    | ✅  |
| Trainer  | `trl`, `peft`     | ✅  |
| Hub 업로드  | `transformers` 내부 | ✅  |

