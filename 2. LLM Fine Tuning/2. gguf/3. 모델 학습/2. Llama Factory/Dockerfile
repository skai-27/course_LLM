FROM nvidia/cuda:12.1.1-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

WORKDIR /workspace

# 1. 시스템 패키지 및 Python 3.11 설치
RUN apt-get update && apt-get install -y \
    software-properties-common git curl wget vim build-essential && \
    add-apt-repository ppa:deadsnakes/ppa && apt-get update && \
    apt-get install -y python3.11 python3.11-dev python3.11-distutils && \
    rm -rf /var/lib/apt/lists/*

# 2. Pip 설치 (가장 안정적인 bootstrap 방식)
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# 3. 라이브러리 설치
COPY requirements.txt /tmp/requirements.txt

# Pip 자체를 최신으로 유지하여 의존성 해결 능력 향상
RUN python3.11 -m pip install --no-cache-dir --upgrade pip setuptools wheel

# 핵심 torch 설치 (인덱스 명시)
RUN python3.11 -m pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 나머지 패키지 설치 (여기서 수정된 requirements.txt 사용)
RUN python3.11 -m pip install --no-cache-dir -r /tmp/requirements.txt

# 4. 소스 코드 및 강의 자료 준비
RUN git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory.git /opt/LLaMA-Factory
COPY lectures/ /opt/lectures/
RUN curl -fsSL https://code-server.dev/install.sh | sh

EXPOSE 8080 7860

# 5. 실행 스크립트 (RunPod 마운트 대응)
CMD ["bash", "-c", "\
    if [ ! -d /workspace/LLaMA-Factory ]; then \
        cp -r /opt/LLaMA-Factory /workspace/LLaMA-Factory && \
        cp -r /opt/lectures /workspace/lectures && \
        cd /workspace/LLaMA-Factory && python3.11 -m pip install -e .[metrics,bitsandbytes,qwen] && \
        python3.11 -m ipykernel install --user --name LLaMA --display-name 'Python 3.11 (LLaMA Factory)'; \
    fi && \
    code-server /workspace --bind-addr 0.0.0.0:8080 --auth none --disable-telemetry \
"]