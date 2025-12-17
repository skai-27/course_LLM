# ==================================================
# Base Image (CUDA pin)
# ==================================================
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV CUDA_HOME=/usr/local/cuda
ENV TORCH_CUDA_ARCH_LIST="8.0 8.6 8.9 9.0"

WORKDIR /workspace

# ==================================================
# System packages (OS-level pin)
# ==================================================
RUN apt-get update && apt-get install -y \
    git=1:2.34.1-1ubuntu1.10 \
    curl \
    wget \
    vim \
    build-essential \
    python3=3.10.6-1~22.04 \
    python3-pip \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

# ==================================================
# Python base (pip pin)
# ==================================================
RUN pip install --upgrade \
    pip==24.0 \
    setuptools==69.5.1 \
    wheel==0.43.0

# ==================================================
# PyTorch (CUDA 12.1)
# ==================================================
RUN pip install \
    torch==2.2.2 \
    torchvision==0.17.2 \
    torchaudio==2.2.2 \
    --index-url https://download.pytorch.org/whl/cu121

# ==================================================
# HuggingFace core stack (Unsloth compatible)
# ==================================================
RUN pip install \
    transformers==4.40.2 \
    accelerate==0.30.1 \
    datasets==2.19.0 \
    sentencepiece==0.1.99 \
    protobuf==4.25.3 \
    scipy==1.11.4 \
    einops==0.7.0 \
    packaging==24.0 \
    safetensors==0.4.3

# ==================================================
# Unsloth stack (핵심)
# ==================================================
RUN pip install \
    unsloth==2024.6 \
    trl==0.8.6 \
    peft==0.10.0 \
    bitsandbytes==0.43.1 \
    xformers==0.0.25

# ==================================================
# Optional (강의/실험 편의)
# ==================================================
RUN pip install \
    wandb==0.17.0 \
    tensorboard==2.16.2 \
    rich==13.7.1

# ==================================================
# Runtime cache locations
# ==================================================
ENV HF_HOME=/workspace/.cache/huggingface
ENV TRANSFORMERS_CACHE=/workspace/.cache/huggingface
ENV WANDB_DIR=/workspace/.cache/wandb

# ===============================
# Jupyter
# ===============================
RUN pip install \
jupyterlab==4.1.8 \
notebook==7.1.3 \
ipykernel==6.29.4

EXPOSE 8888

# ==================================================
# Entrypoint
# ==================================================
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
