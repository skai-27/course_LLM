# Docker Hub에 배포하는 명령어
```shell
docker build -t goodwon593/llamafactory-runpod:0.8.3 .
docker push goodwon593/llamafactory-runpod:0.8.3

# GPU용
docker run -it --rm --gpus all -p 8080:8080 -v ./workspace:/workspace goodwon593/llamafactory-runpod:0.8.3
# CPU용
docker run -it --rm -p 8080:8080 -v ./workspace:/workspace goodwon593/llamafactory-runpod:0.8.3
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

## 📚 참고 자료

- [LLaMA Factory GitHub](https://github.com/hiyouga/LLaMA-Factory)
- [LLaMA Factory 문서](https://llamafactory.readthedocs.io/)
- [Unsloth GitHub](https://github.com/unslothai/unsloth)
- [PEFT 문서](https://huggingface.co/docs/peft/)
- [TRL 문서](https://huggingface.co/docs/trl/)

