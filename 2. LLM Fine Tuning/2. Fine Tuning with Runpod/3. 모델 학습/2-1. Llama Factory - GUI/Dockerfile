# =====================================================
# LLaMA Factory - WebUI (GUI) Fine-tuning Docker Image
# 학습모델: Qwen/Qwen3.5-2B
# 학습방법: DoRA (GUI에서 설정)
# 학습데이터: good593/illnesses-dataset (GUI 드롭다운으로 선택)
# =====================================================
FROM nvidia/cuda:12.1.1-devel-ubuntu22.04

# 환경 변수 설정
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV CUDA_HOME=/usr/local/cuda-12.1

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3-dev \
    git \
    wget \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# python3 -> python 심볼릭 링크
RUN ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip

# 작업 디렉토리 설정
WORKDIR /app

# pip 업그레이드
RUN pip install --upgrade pip

# PyTorch 설치 (CUDA 12.1 호환)
RUN pip install torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 \
    --index-url https://download.pytorch.org/whl/cu121

# LLaMA-Factory 설치
RUN git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory.git /app/LLaMA-Factory

WORKDIR /app/LLaMA-Factory

# LLaMA-Factory 의존성 설치 (metrics, 웹UI 포함)
RUN pip install -e ".[torch,metrics]"

# requirements.txt 복사 및 의존성 설치
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt --no-build-isolation

# -----------------------------------------------
# illnesses-dataset을 GUI 드롭다운에 표시하기 위해
# dataset_info.json에 데이터셋 정보를 등록합니다.
# -----------------------------------------------
COPY dataset_info.json /app/LLaMA-Factory/data/dataset_info.json

# WebUI 포트 개방
EXPOSE 7860

# 시작 스크립트 복사 및 실행 권한 부여
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

ENTRYPOINT ["/app/start.sh"]
