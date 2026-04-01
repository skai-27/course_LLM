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
    apt-get install -y libaio-dev && \
    rm -rf /var/lib/apt/lists/*

# 2. Pip 설치
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# 3. 라이브러리 설치 및 Multi-GPU 최적화
COPY requirements.txt /tmp/requirements.txt

# [1단계] 빌드 필수 도구 및 업그레이드
RUN python3.11 -m pip install --no-cache-dir --upgrade pip setuptools wheel packaging ninja

# [2단계] requirements.txt 먼저 설치 (PyTorch 2.3.1 및 모든 의존성 확정)
# 여기서 torch, transformers, accelerate 등이 모두 설치됩니다.
RUN python3.11 -m pip install --no-cache-dir -r /tmp/requirements.txt

# [3단계] 확정된 PyTorch 환경 위에서 flash-attn 빌드 및 설치
# 이미 requirements.txt에서 torch가 깔렸으므로, flash-attn은 이를 보고 올바르게 컴파일됩니다.
RUN MAX_JOBS=4 python3.11 -m pip install --no-cache-dir flash-attn --no-build-isolation

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
