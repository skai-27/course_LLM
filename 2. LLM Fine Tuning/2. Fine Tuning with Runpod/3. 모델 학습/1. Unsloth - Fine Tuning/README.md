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
# Docker Hub에 배포하는 명령어
> Docker Image 생성
```shell
docker build -t <Docker ID>/unsloth-runpod:2025.12.5 .
```

> Docker Container 실행 
```shell
# GPU용
docker run -it --rm --gpus all -p 8080:8080 -v ./workspace:/workspace <Docker ID>/unsloth-runpod:2025.12.5
# CPU용
docker run -it --rm -p 8080:8080 -v ./workspace:/workspace <Docker ID>/unsloth-runpod:2025.12.5
```

> Docker Hub 배포 
```shell
docker push <Docker ID>/unsloth-runpod:2025.12.5
```

---
# Dockerfile에 포함된 필수 요소
> RunPod에서 모델 학습 → Hugging Face Hub 저장

| 기능       | 라이브러리             | 상태 |
| -------- | ----------------- | -- |
| 모델 로딩/학습 | `unsloth`         | ✅  |
| HF 모델 구조 | `transformers`    | ✅  |
| QLoRA    | `bitsandbytes`    | ✅  |
| Trainer  | `trl`, `peft`     | ✅  |
| Hub 업로드  | `transformers` 내부 | ✅  |

---
# Unsloth LoRA / QLoRA 장점

| 관점           | 장점                  | 설명                                  |
| ------------ | ------------------- | ----------------------------------- |
| 속도        | **학습 속도 매우 빠름**     | 커스텀 CUDA 커널 + 최적화된 forward/backward |
| 메모리       | **VRAM 사용량 최소**     | 4bit 로딩 + QLoRA 기본 설계               |
| 난이도       | **설정이 단순함**         | YAML 없음, Python 몇 줄로 끝              |
| 실험        | **빠른 반복 실험 가능**     | 하이퍼파라미터 변경 부담 낮음                    |
| 하드웨어      | **단일 GPU로 충분**      | 24GB GPU에서도 7B~13B 가능               |
| 통합        | **Transformers 호환** | HF Trainer / PEFT 생태계 그대로 사용        |
| 저장        | **HF Hub 업로드 간단**   | `push_to_hub()` 바로 가능               |
| 디버깅       | **에러 지점 명확**        | 분산/ZeRO 개념 없음                       |

