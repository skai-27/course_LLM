FROM nvidia/cuda:12.1.1-devel-ubuntu22.04

# 환경 변수 설정: Multi-GPU 통신(NCCL) 및 Python 최적화
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    NCCL_P2P_DISABLE=0 \
    NCCL_IB_DISABLE=1 \
    UCX_TLS=tcp,self

WORKDIR /workspace

# 1. 시스템 패키지 및 Python 3.11 설치
RUN apt-get update && apt-get install -y \
    software-properties-common git curl wget vim build-essential && \
    add-apt-repository ppa:deadsnakes/ppa && apt-get update && \
    apt-get install -y python3.11 python3.11-dev python3.11-distutils && \
    rm -rf /var/lib/apt/lists/*

# 2. Pip 설치
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# 3. 라이브러리 설치 및 Multi-GPU 최적화
COPY requirements.txt /tmp/requirements.txt

RUN python3.11 -m pip install --no-cache-dir --upgrade pip setuptools wheel packaging ninja

# 핵심 torch 설치 (CUDA 12.1용)
RUN python3.11 -m pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Flash-Attention 설치 (빌드 환경 변수 추가 및 사전 요구사항 설치)
# MAX_JOBS를 지정하여 빌드 시 메모리 부족을 방지하고, --no-build-isolation으로 설치 속도 향상
RUN MAX_JOBS=4 python3.11 -m pip install --no-cache-dir flash-attn --no-build-isolation

# 나머지 패키지 설치
RUN python3.11 -m pip install --no-cache-dir -r /tmp/requirements.txt

# 4. 소스 코드 및 강의 자료 준비
COPY lectures/ /opt/lectures/
RUN curl -fsSL https://code-server.dev/install.sh | sh

EXPOSE 8080

# 5. 실행 스크립트 (2개 GPU 인식 및 커널 설정)
CMD ["bash", "-c", "\
    if [ ! -d /workspace/lectures ]; then \
        cp -r /opt/lectures /workspace/lectures && \
        python3.11 -m ipykernel install --user --name LLaMA --display-name 'Python 3.11 (LLaMA Factory)'; \
    fi && \
    code-server /workspace --bind-addr 0.0.0.0:8080 --auth none --disable-telemetry \
"]
