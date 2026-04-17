# LLaMA-Factory GUI - DoRA Fine-tuning 예제

## 개요

| 항목 | 내용 |
|------|------|
| 학습 방법 | **DoRA** (DoRA = LoRA + `use_dora: true`, GUI에서 체크박스로 활성화) |
| 학습 데이터 | [good593/illnesses-dataset](https://huggingface.co/datasets/good593/illnesses-dataset) (793건) |
| 학습 모델 | [Qwen/Qwen2.5-2B-Instruct](https://huggingface.co/Qwen/Qwen2.5-2B-Instruct) |
| 학습 방식 | **LLaMA-Factory WebUI (GUI)** 로 브라우저에서 클릭하여 학습 |
| 베이스 이미지 | `nvidia/cuda:12.1.1-devel-ubuntu22.04` |

> 💡 이 예제는 **CLI 없이 브라우저 GUI만으로** 파인튜닝을 수행합니다.

---

## DoRA (Weight-Decomposed LoRA)란?

| 항목 | LoRA | DoRA |
|------|------|------|
| 방식 | 저랭크 행렬 추가 | 가중치를 크기(magnitude) + 방향(direction)으로 분해 |
| 성능 | 효율적이지만 Full FT와 차이 있음 | Full Fine-tuning에 더 근접 |
| GUI 설정 | Fine-tuning Method: LoRA | LoRA 선택 후 **"Use DoRA" 체크** |

---

## 파일 구조

```
2-1. Llama Factory - GUI/
├── Dockerfile           # Docker 이미지 빌드 (WebUI 자동 실행)
├── start.sh             # WebUI 시작 스크립트
├── dataset_info.json    # illnesses-dataset을 GUI 드롭다운에 등록
├── train_config.yaml    # [참고용] GUI에서 생성되는 YAML 예시
├── requirements.txt     # Python 패키지 목록
├── .env.example         # 환경변수 예제 (HF_TOKEN, WANDB_API_KEY)
└── README.md            # 이 파일
```

---

## 사용 방법

### 1단계: Docker 이미지 빌드

```bash
docker build -t llamafactory-gui .
```

### 2단계: 컨테이너 실행 (RunPod에서)

```bash
docker run --gpus all --shm-size 32G \
  -p 7860:7860 \
  -e HF_TOKEN="your_hf_token_here" \
  -e WANDB_API_KEY="your_wandb_key_here" \
  -v $(pwd)/output:/app/LLaMA-Factory/saves \
  llamafactory-gui
```

> RunPod에서는 환경변수와 포트를 RunPod 대시보드에서 직접 설정할 수 있습니다.

### 3단계: 브라우저로 WebUI 접속

```
http://<RunPod IP>:7860
```

---

## WebUI에서 DoRA 파인튜닝 설정 순서

컨테이너 실행 후 브라우저에서 아래 순서대로 GUI를 설정합니다.

### 📋 Train 탭 설정

#### [모델 선택]
| 항목 | 설정값 |
|------|--------|
| Model Name | `Qwen/Qwen2.5-2B-Instruct` |
| Finetuning Method | `lora` |
| ✅ **Use DoRA** | **체크** ← DoRA 핵심 설정 |

#### [데이터셋 선택]
| 항목 | 설정값 |
|------|--------|
| Dataset | `illnesses_dataset` (드롭다운에서 선택) |
| Max Samples | `793` (전체 사용) |
| Cutoff Length | `1024` |

#### [하이퍼파라미터]
| 항목 | 설정값 |
|------|--------|
| Learning Rate | `5e-5` |
| Epochs | `3.0` |
| Batch Size (per device) | `2` |
| Gradient Accumulation | `8` |
| LR Scheduler | `cosine` |
| Warmup Ratio | `0.1` |

#### [LoRA 설정]
| 항목 | 설정값 |
|------|--------|
| LoRA Rank (r) | `16` |
| LoRA Alpha | `32` |
| LoRA Dropout | `0.05` |
| LoRA Target | `all` |

#### [고급 설정]
| 항목 | 설정값 |
|------|--------|
| Flash Attention | `fa2` |
| BF16 | ✅ 체크 (A100/H100) |
| FP16 | ✅ 체크 (RTX 30xx/40xx) |
| Val Size | `0.1` |

### ▶ Start 버튼 클릭 → 학습 시작!

학습 로그와 Loss 그래프가 GUI 하단에 실시간으로 표시됩니다.

---

## 데이터셋 등록 방식 (dataset_info.json)

GUI 드롭다운에 `illnesses_dataset`이 표시되도록 `dataset_info.json`을 LLaMA-Factory `data/` 폴더에 등록합니다.

```json
{
  "illnesses_dataset": {
    "hf_hub_url": "good593/illnesses-dataset",
    "split": "train",
    "columns": {
      "prompt": "instruction",
      "query": "input",
      "response": "output"
    }
  }
}
```

---

## 환경 변수 설정 (.env.example 참고)

| 변수명 | 설명 | 필수 |
|--------|------|------|
| `HF_TOKEN` | HuggingFace API 토큰 (모델 다운로드 필요) | ✅ |
| `WANDB_API_KEY` | WandB API 키 (GUI에서 학습 곡선 모니터링) | 선택 |
| `WANDB_PROJECT` | WandB 프로젝트 이름 | 선택 |

---

## 권장 GPU 사양

| GPU | VRAM | 배치크기 | 예상 학습 시간 (3 epoch) |
|-----|------|---------|-------------------------|
| RTX 3090 / 4090 | 24GB | 2 | ~20분 |
| A100 40GB | 40GB | 4 | ~10분 |
| A100 80GB | 80GB | 8 | ~7분 |

> ⚡ **RTX 시리즈 사용 시**: GUI에서 BF16 해제 → FP16 체크

---

## 학습 완료 후 - Merge & Export

학습 완료 후 **Export 탭**에서 LoRA 가중치를 베이스 모델에 병합할 수 있습니다.

1. Export 탭 이동
2. Export Dir 설정 (예: `merged_model/`)
3. **Export model** 클릭

---

## 참고 링크

- [LLaMA-Factory GitHub](https://github.com/hiyouga/LLaMA-Factory)
- [DoRA 논문 (arXiv)](https://arxiv.org/abs/2402.09353)
- [Qwen2.5-2B-Instruct (HuggingFace)](https://huggingface.co/Qwen/Qwen2.5-2B-Instruct)
- [illnesses-dataset (HuggingFace)](https://huggingface.co/datasets/good593/illnesses-dataset)
- [WandB 학습 모니터링](https://wandb.ai)
