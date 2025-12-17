# ==================================================
# Base Image (CUDA pin)
# ==================================================
# RunPod 공식 PyTorch 2.8.0 이미지
FROM runpod/pytorch:2.8.0-py3.11-cuda12.8.1-cudnn-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV CUDA_HOME=/usr/local/cuda
ENV TORCH_CUDA_ARCH_LIST="8.0 8.6 8.9 9.0"

WORKDIR /workspace

# ==================================================
# System packages
# ==================================================
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    vim \
    build-essential \
    ninja-build \
    libaio-dev \
    python3.11 \
    python3-pip \
    python3.11-dev \
    && rm -rf /var/lib/apt/lists/*

RUN ln -sf /usr/bin/python3 /usr/bin/python

# ==================================================
# Python base
# ==================================================
RUN pip install --upgrade \
    pip \
    setuptools \
    wheel

# ==================================================
# PyTorch (CUDA 12.1 공식 wheel)
# ==================================================
# RUN pip install \
#     torch==2.8.0 \
#     torchvision==0.23.0 \
#     torchaudio==2.8.0 \
#     --index-url https://download.pytorch.org/whl/cu128

# ==================================================
# HuggingFace core stack
# ==================================================
RUN pip install \
    transformers==4.57.3 \
    accelerate==1.12.0 \
    datasets==4.3.0 \
    sentencepiece==0.2.1 \
    protobuf==6.33.2 \
    scipy==1.16.3 \
    einops==0.8.1 \
    packaging==24.2 \
    safetensors==0.7.0

# ==================================================
# Unsloth stack
# ==================================================
RUN pip install \
    unsloth==2025.12.5 \
    unsloth-zoo==2025.12.4 \
    trl==0.24.0 \
    peft==0.18.0 \
    bitsandbytes==0.49.0 \
    xformers==0.0.33

# ==================================================
# Optional (강의 편의)
# ==================================================
RUN pip install \
    wandb==0.23.1 \
    tensorboard==2.20.0 \
    rich==14.2.0

# ==================================================
# Jupyter kernel only (NOT server)
# ==================================================
RUN pip install \
    ipykernel==6.29.5 \
    jupyter-client==8.6.3 \
    nbformat==5.10.4

# Python 커널 등록
RUN python -m ipykernel install \
    --name unsloth \
    --display-name "Python (Unsloth)"

# ==================================================
# VSCode Server (code-server)
# ==================================================
ENV HOME=/root

RUN curl -fsSL https://code-server.dev/install.sh | sh \
    && /usr/bin/code-server --version

# ==================================================
# VSCode extensions
# ==================================================
# RUN mkdir -p /root/.local/share/code-server && \
#     /usr/bin/code-server \
#     --user-data-dir /root/.local/share/code-server \
#     --install-extension ms-python.python || true && \
#     /usr/bin/code-server \
#     --user-data-dir /root/.local/share/code-server \
#     --install-extension ms-toolsai.jupyter || true && \
#     /usr/bin/code-server \
#     --user-data-dir /root/.local/share/code-server \
#     --install-extension ms-python.vscode-pylance || true

# ==================================================
# Runtime cache (RunPod Volume friendly)
# ==================================================
ENV HF_HOME=/workspace/.cache/huggingface
ENV TRANSFORMERS_CACHE=/workspace/.cache/huggingface
ENV WANDB_DIR=/workspace/.cache/wandb

ENV XDG_DATA_HOME=/workspace/.vscode
ENV XDG_CONFIG_HOME=/workspace/.config
ENV XDG_CACHE_HOME=/workspace/.cache

# ==================================================
# Permissions
# ==================================================
RUN chmod -R 777 /workspace

# ==================================================
# Expose VSCode Server
# ==================================================
EXPOSE 8080

# ==================================================
# 강의자료 복사
# ==================================================
COPY lectures/ /opt/lectures/

# ==================================================
# Entrypoint
# ==================================================
CMD ["bash", "-c", "\
if [ ! -d /workspace/lectures ]; then \
  cp -r /opt/lectures /workspace/lectures; \
fi && \
code-server /workspace \
  --bind-addr 0.0.0.0:8080 \
  --auth none \
  --disable-telemetry \
"]
