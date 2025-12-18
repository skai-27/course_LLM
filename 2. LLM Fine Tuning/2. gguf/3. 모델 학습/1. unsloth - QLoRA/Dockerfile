# ==================================================
# 1. Base Image
# ==================================================
FROM runpod/pytorch:2.8.0-py3.11-cuda12.8.1-cudnn-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    CUDA_HOME=/usr/local/cuda \
    # 파이썬 실행 경로를 명시적으로 설정
    PYTHON_EXE=/usr/bin/python3.11 

WORKDIR /workspace

# ==================================================
# 2. System Packages & Python Link
# ==================================================
RUN apt-get update && apt-get install -y \
    git curl wget vim build-essential ninja-build libaio-dev \
    python3.11 python3.11-dev python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 시스템 기본 파이썬을 3.11로 완전히 고정 (혼선 방지 핵심)
RUN ln -sf /usr/bin/python3.11 /usr/bin/python3 && \
    ln -sf /usr/bin/python3.11 /usr/bin/python && \
    python -m pip install --upgrade pip

# ==================================================
# 3. AI Libraries (명시적 파이썬 호출)
# ==================================================
# python -m pip을 사용하면 현재 /usr/bin/python이 가리키는 3.11에만 설치됩니다.
RUN python -m pip install --no-cache-dir --upgrade setuptools wheel

RUN python -m pip install --no-cache-dir \
    transformers==4.57.3 \
    accelerate==1.12.0 \
    datasets==4.3.0 \
    sentencepiece==0.2.1 \
    protobuf==6.33.2 \
    scipy==1.16.3 \
    einops==0.8.1 \
    packaging==24.2 \
    safetensors==0.7.0

RUN python -m pip install --no-cache-dir \
    unsloth==2025.12.5 \
    unsloth-zoo==2025.12.4 \
    trl==0.24.0 \
    peft==0.18.0 \
    bitsandbytes==0.49.0 \
    xformers==0.0.33

RUN python -m pip install --no-cache-dir \
    wandb==0.23.1 tensorboard==2.20.0 rich==14.2.0 \
    ipykernel==6.29.5 jupyter-client==8.6.3 nbformat==5.10.4

# 커널 등록 시에도 정확한 경로 지정
RUN /usr/bin/python3.11 -m ipykernel install --name unsloth --display-name "Python (Unsloth)"

# ==================================================
# 4. VSCode Server & Extensions
# ==================================================
ENV HOME=/root

RUN curl -fsSL https://code-server.dev/install.sh | sh
RUN mkdir -p /root/.local/share/code-server
RUN code-server --install-extension ms-python.python --force && \
    code-server --install-extension ms-toolsai.jupyter --force

# ==================================================
# 5. Environment & Content
# ==================================================
ENV HF_HOME=/workspace/.cache/huggingface \
    XDG_DATA_HOME=/workspace/.vscode

COPY lectures/ /opt/lectures/

EXPOSE 8080

CMD ["bash", "-c", "\
if [ ! -d /workspace/lectures ]; then cp -r /opt/lectures /workspace/lectures; fi && \
code-server /workspace --bind-addr 0.0.0.0:8080 --auth none --disable-telemetry \
"]