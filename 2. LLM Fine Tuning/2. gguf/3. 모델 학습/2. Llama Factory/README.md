# Docker Hub에 배포하는 명령어
```shell
docker build -t goodwon593/llamafactory-runpod:0.9.1 .
docker push goodwon593/llamafactory-runpod:0.9.1

# GPU용
docker run -it --rm --gpus all -p 8080:8080 -v ./workspace:/workspace goodwon593/llamafactory-runpod:0.9.1
# CPU용
docker run -it --rm -p 8080:8080 -v ./workspace:/workspace goodwon593/llamafactory-runpod:0.9.1
```



# LLaMA Factory를 이용한 sLLM 파인튜닝

## 📖 LLaMA Factory란?

**LLaMA Factory**는 대규모 언어 모델(LLM)을 손쉽게 파인튜닝할 수 있는 통합 프레임워크입니다. 100개 이상의 사전 학습된 모델을 지원하며, 코드 작성 없이도 GUI를 통해 모델을 학습할 수 있는 강력한 도구입니다.

### 주요 특징

- **🎯 다양한 모델 지원**: LLaMA, Mistral, Qwen, Gemma, Phi 등 100+ 모델 지원
- **🚀 효율적인 학습 방식**: LoRA, QLoRA, Full Fine-tuning 등 다양한 학습 방법 제공
- **🖥️ 직관적인 Web UI**: Gradio 기반의 사용자 친화적 인터페이스
- **📊 다양한 학습 알고리즘**: 
  - Supervised Fine-Tuning (SFT)
  - Reward Modeling (RM)
  - PPO (Proximal Policy Optimization)
  - DPO (Direct Preference Optimization)
  - KTO (Kahneman-Tversky Optimization)
- **💾 메모리 최적화**: FlashAttention-2, Unsloth 통합 지원
- **📁 데이터셋 관리**: 손쉬운 데이터셋 포맷팅 및 관리
- **🔄 모델 내보내기**: GGUF, AWQ, GPTQ 등 다양한 형식으로 변환 가능

### 지원하는 학습 방식

| 방식 | 메모리 효율 | 학습 속도 | 성능 | 용도 |
|------|------------|----------|------|------|
| **Full Fine-tuning** | ❌ 낮음 | 🐌 느림 | ⭐⭐⭐ 최고 | 대규모 리소스 환경 |
| **LoRA** | ✅ 중간 | 🚀 빠름 | ⭐⭐ 우수 | 일반적인 파인튜닝 |
| **QLoRA** | ✅✅ 높음 | 🚀 빠름 | ⭐⭐ 우수 | 제한된 GPU 환경 |
| **DoRA** | ✅ 중간 | 🚀 빠름 | ⭐⭐⭐ 매우 우수 | LoRA 개선 버전 |

---

## 🆚 LLaMA Factory vs Unsloth

### 개요 비교

| 특징 | LLaMA Factory | Unsloth |
|------|--------------|---------|
| **주요 목적** | 통합 파인튜닝 플랫폼 | 초고속 메모리 최적화 |
| **사용 난이도** | ⭐⭐ 쉬움 (GUI 제공) | ⭐⭐⭐ 중간 (코드 기반) |
| **모델 지원** | 100+ 모델 | 주요 모델 (LLaMA, Mistral, Gemma 등) |
| **학습 속도** | 빠름 | 2-5배 더 빠름 |
| **메모리 사용** | 효율적 | 최대 80% 감소 |
| **확장성** | 매우 높음 | 중간 |

### 🎨 LLaMA Factory의 장점

#### 1. **통합 플랫폼**
```
✅ 웹 UI를 통한 직관적인 작업 흐름
✅ 데이터 전처리부터 모델 배포까지 원스톱
✅ 다양한 학습 알고리즘 실험 가능
✅ 설정 파일(YAML) 기반 재현 가능한 실험
```

#### 2. **초보자 친화적**
- 코드 작성 없이 GUI로 모든 작업 가능
- 템플릿과 예제 데이터셋 제공
- 상세한 로깅 및 시각화

#### 3. **프로덕션 준비**
- 다양한 형식으로 모델 내보내기
- API 서버 배포 기능
- 벤치마크 및 평가 도구 내장

#### 4. **교육 및 연구에 최적**
- 다양한 실험을 빠르게 수행 가능
- 하이퍼파라미터 비교가 용이
- 팀 협업에 유리한 구조

### ⚡ Unsloth의 장점

#### 1. **극한의 속도 최적화**
```python
# Unsloth는 커스텀 CUDA 커널로 최적화
✅ 학습 속도: 2-5배 빠름
✅ 추론 속도: 2-3배 빠름
✅ 메모리 사용: 최대 80% 감소
✅ FlashAttention-2를 넘어서는 최적화
```

#### 2. **제한된 GPU 환경에 최적**
- 24GB GPU에서 70B 모델 학습 가능
- QLoRA + Unsloth 조합으로 극한의 효율성
- 무료 Colab에서도 대형 모델 학습 가능

#### 3. **세밀한 제어**
- 파이썬 코드로 모든 것을 제어
- 커스텀 학습 로직 구현 용이
- 고급 최적화 기법 적용 가능

#### 4. **경량성**
- 핵심 기능에만 집중
- 적은 의존성
- 빠른 설치 및 실행

### 🤔 어떤 것을 선택해야 할까?

#### LLaMA Factory를 선택하세요:
```
✅ 다양한 모델과 학습 방법을 실험하고 싶을 때
✅ GUI로 편리하게 작업하고 싶을 때
✅ 팀 프로젝트나 교육 목적일 때
✅ 데이터 관리와 실험 추적이 중요할 때
✅ DPO, PPO, KTO 등 고급 알고리즘을 사용할 때
✅ 프로덕션 배포까지 고려할 때
```

#### Unsloth를 선택하세요:
```
✅ 최대한 빠른 학습 속도가 필요할 때
✅ GPU 메모리가 부족할 때
✅ 코드 레벨의 세밀한 제어가 필요할 때
✅ 간단한 LoRA/QLoRA 학습만 필요할 때
✅ Jupyter Notebook 환경에서 빠르게 실험할 때
✅ 최소한의 설정으로 빠르게 시작하고 싶을 때
```

#### 두 가지를 함께 사용하세요:
```
💡 LLaMA Factory는 Unsloth를 백엔드로 통합할 수 있습니다!
   - LLaMA Factory의 편리한 UI
   + Unsloth의 빠른 속도
   = 최고의 조합 🚀
```

---

## 🚀 이 프로젝트에서의 사용

이 프로젝트는 **LLaMA Factory**를 사용하여 의료 데이터셋으로 sLLM을 파인튜닝합니다.

### 환경 구성
- **베이스 이미지**: RunPod PyTorch 2.8.0 + CUDA 12.8.1
- **파이썬 버전**: 3.11
- **주요 라이브러리**:
  - LLaMA Factory 0.8.3
  - PEFT 0.18.0 (LoRA/QLoRA)
  - TRL 0.26.2 (강화학습)
  - BitsAndBytes 0.49.0 (양자화)

### 학습 방법
- **QLoRA**: 4-bit 양자화를 통한 메모리 효율적 학습
- **데이터셋**: 의료 상담 데이터 (illnesses.csv)
- **목표**: 의료 도메인 특화 sLLM 개발

---

## 📖 강의 자료

### 🎓 LLaMA Factory QLoRA 파인튜닝 가이드

`lectures/` 폴더에서 **LLaMA Factory**를 이용한 QLoRA 파인튜닝 강의 자료를 확인하세요!

#### 📁 강의 구성

```
lectures/
├── Fine Tuning - QLoRA.ipynb    # 📓 메인 강의 노트북 (22개 셀)
├── README.md                     # 📚 상세 가이드
└── data/
    ├── illnesses.csv             # 📊 의료 상담 데이터셋 (794개)
    ├── medical_train.json        # 🎯 학습 데이터 (생성됨)
    ├── medical_val.json          # ✅ 검증 데이터 (생성됨)
    └── dataset_info.json         # ℹ️ LLaMA Factory 데이터셋 정보
```

#### 📚 강의 내용

1. **LLaMA Factory 소개**
   - No-Code LLM 파인튜닝 프레임워크
   - CLI, Web UI, Python API 지원
   - 100+ 모델 지원

2. **QLoRA 이론**
   - 4-bit 양자화 + LoRA 결합
   - 메모리 효율성 비교
   - 주요 하이퍼파라미터

3. **환경 설정**
   - 패키지 확인
   - LLaMA Factory CLI 확인

4. **데이터셋 준비**
   - CSV → Alpaca 형식 변환
   - dataset_info.json 등록

5. **LLaMA Factory CLI로 학습**
   - 학습 명령어 상세 설명
   - 파라미터 가이드

6. **Web UI 사용법**
   - Web UI 실행 방법
   - Train 탭 설정
   - Chat 탭 테스트

7. **추론 및 평가**
   - CLI로 추론 실행
   - 실시간 대화 테스트

8. **모델 내보내기**
   - LoRA 어댑터 병합
   - 모델 배포

9. **실전 팁**
   - 하이퍼파라미터 튜닝
   - 메모리 최적화
   - 문제 해결

10. **요약**
   - 학습 내용 정리
   - 빠른 시작 체크리스트
   - 다음 단계

#### 🚀 빠른 시작

```bash
# 1. 패키지 설치
pip install -r requirements.txt

# 2. 강의 노트북 실행
cd lectures
jupyter lab
# Fine Tuning - QLoRA.ipynb 열기

# 3. 데이터 준비 (노트북에서 실행)
# - CSV → Alpaca 형식 변환
# - dataset_info.json 생성

# 4. 학습 실행 (둘 중 하나)
# CLI 방식:
llamafactory-cli train --model_name_or_path Qwen/Qwen2.5-1.5B-Instruct ...

# Web UI 방식:
llamafactory-cli webui
# http://localhost:7860 접속
```

#### 💡 주요 특징

- ✅ **실전 중심**: 실제 의료 데이터로 실습
- ✅ **단계별 설명**: 초보자도 따라할 수 있는 상세한 설명
- ✅ **다양한 방법**: Notebook, 스크립트, CLI 모두 제공
- ✅ **한국어 지원**: 모든 설명과 주석이 한국어
- ✅ **문제 해결**: 자주 발생하는 문제와 해결 방법 포함

#### 📊 데이터셋 정보

**소아청소년과 의료 상담 데이터셋**
- 총 794개의 질문-답변 쌍
- 부모들의 실제 질문과 전문의 답변
- 다양한 질문 스타일과 길이
- 학습/검증 데이터 8:2 분할

#### 🎯 학습 결과

- **프레임워크**: LLaMA Factory 0.8.3
- **베이스 모델**: Qwen2.5-1.5B-Instruct
- **학습 방법**: QLoRA (4-bit)
- **GPU 메모리**: ~6-8GB
- **학습 시간**: ~30-60분 (A100 기준)
- **어댑터 크기**: ~30-50MB

#### 📋 LLaMA Factory 주요 명령어

```bash
llamafactory-cli train    # 학습
llamafactory-cli chat     # 추론
llamafactory-cli webui    # Web UI
llamafactory-cli export   # 모델 내보내기
llamafactory-cli eval     # 평가
```

#### 📖 참고 자료

강의에서 참조한 자료:
- [LLaMA Factory 공식 문서](https://llamafactory.readthedocs.io/)
- [SK Devocean - No-Code LLM 파인튜닝](https://devocean.sk.com/blog/techBoardDetail.do?ID=166098)
- [QLoRA 논문](https://arxiv.org/abs/2305.14314)
- [LoRA 논문](https://arxiv.org/abs/2106.09685)

---

## 📝 실습 2: Multi GPU Full Fine-tuning

### 개요

**EXAONE-3.5-2.4B-Instruct** 모델을 **DeepSpeed**를 사용하여 Multi GPU 환경에서 Full Fine-tuning하는 실습입니다.

📓 **노트북**: `lectures/2. Multi GPU - Full FT.ipynb`

### 핵심 내용

```
1. Multi GPU 분산 학습 개념
   ├─ DeepSpeed ZeRO 단계 이해
   ├─ Optimizer/Gradient 분산
   └─ 메모리 효율 최적화

2. EXAONE 모델 파인튜닝
   ├─ 한국어 특화 sLLM
   ├─ Full Fine-tuning 수행
   └─ 의료 도메인 적용

3. LLaMA Factory CLI
   ├─ 쉘 스크립트 자동화
   ├─ DeepSpeed 통합
   └─ WandB 모니터링

4. RunPod 환경 활용
   ├─ 클라우드 GPU 설정
   ├─ 비용 효율적 학습
   └─ 실전 배포 준비
```

### 💡 주요 특징

- ✅ **Multi GPU**: DeepSpeed ZeRO-2로 효율적 분산 학습
- ✅ **Full Fine-tuning**: 모든 파라미터 학습으로 최고 성능
- ✅ **자동화**: 쉘 스크립트로 간편한 실행
- ✅ **확장성**: 2/4/8 GPU로 유연하게 확장
- ✅ **모니터링**: WandB로 실시간 학습 추적

### 📊 성능 비교

| 구성 | GPU 메모리 | 학습 시간 | 배치 크기 |
|------|-----------|----------|----------|
| Single GPU | 24GB | 기준 (100%) | 제한적 |
| 2x GPU (DeepSpeed) | 24GB × 2 | ~60% | 2배 |
| 4x GPU (DeepSpeed) | 24GB × 4 | ~35% | 4배 |

### 🎯 학습 결과

- **프레임워크**: LLaMA Factory 0.9.1 + DeepSpeed 0.18.4
- **베이스 모델**: EXAONE-3.5-2.4B-Instruct
- **학습 방법**: Full Fine-tuning (ZeRO-2)
- **GPU 메모리**: 2x 24GB (최소)
- **학습 시간**: ~2-3시간 (2x A100 기준)
- **모델 크기**: ~5GB

### 🚀 실행 방법

#### 1. 환경 설정

```bash
# 패키지 설치
pip install -r requirements.txt

# 환경 확인
python -c "import deepspeed; print(deepspeed.__version__)"
```

#### 2. 데이터 준비

```bash
# 노트북의 데이터 준비 섹션 실행
# - data/medical_train.json
# - data/medical_val.json
# - data/dataset_info.json
```

#### 3. 학습 실행

```bash
# 스크립트 실행 권한 부여
chmod +x scripts/train_multi_gpu.sh

# 학습 시작
bash scripts/train_multi_gpu.sh
```

#### 4. 추론 테스트

```bash
# 대화형 추론
bash scripts/inference.sh

# 또는 Python API 사용
# 노트북의 추론 섹션 참고
```

### 📋 생성되는 파일

```
configs/
  └─ ds_config_zero2.json        # DeepSpeed 설정

scripts/
  ├─ train_multi_gpu.sh          # 학습 스크립트
  ├─ inference.sh                # 추론 스크립트
  └─ export_model.sh             # 모델 내보내기

outputs/
  └─ exaone_medical_multigpu/    # 학습된 모델
```

### 🔧 하이퍼파라미터

| 파라미터 | 값 | 설명 |
|---------|-------|------|
| `num_train_epochs` | 5.0 | 전체 데이터 5회 반복 |
| `per_device_train_batch_size` | 2 | GPU당 배치 크기 |
| `gradient_accumulation_steps` | 8 | 실질 배치 = 2×8×GPU수 |
| `learning_rate` | 5e-5 | Full FT 최적 학습률 |
| `deepspeed` | ZeRO-2 | Optimizer+Gradient 분산 |

### 📖 참고 자료

강의에서 참조한 자료:
- [LLaMA Factory Distributed Training](https://llamafactory.readthedocs.io/en/latest/advanced/distributed.html)
- [EXAONE-3.5 Model Card](https://huggingface.co/LGAI-EXAONE/EXAONE-3.5-2.4B-Instruct)
- [DeepSpeed Documentation](https://www.deepspeed.ai/docs/config-json/)
- [DeepSpeed ZeRO Paper](https://arxiv.org/abs/1910.02054)

---

## 📚 참고 자료

- [LLaMA Factory GitHub](https://github.com/hiyouga/LLaMA-Factory)
- [LLaMA Factory 문서](https://llamafactory.readthedocs.io/)
- [Unsloth GitHub](https://github.com/unslothai/unsloth)
- [PEFT 문서](https://huggingface.co/docs/peft/)
- [TRL 문서](https://huggingface.co/docs/trl/)
- [DeepSpeed 문서](https://www.deepspeed.ai/)

