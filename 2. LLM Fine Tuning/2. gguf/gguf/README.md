
# Dockerfile에 포함된 필수 요소
> HF Hub 모델 → GGUF 변환

| 기능           | 라이브러리 / 도구                         | 상태 |
| ------------ | ---------------------------------- | -- |
| HF 모델 다운로드   | `huggingface-cli` / `transformers` | ✅  |
| HF → GGUF 변환 | `llama.cpp`                        | ✅  |
| GGUF 메타 처리   | `gguf`                             | ✅  |
| Quantization | `llama-quantize`                   | ✅  |


