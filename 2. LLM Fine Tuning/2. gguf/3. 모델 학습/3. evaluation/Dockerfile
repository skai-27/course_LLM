# ==================================================
# Base Image (CUDA Runtime)
# ==================================================
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV CUDA_HOME=/usr/local/cuda

WORKDIR /workspace

# ==================================================
# System packages (Eval minimal)
# ==================================================
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    vim \
    build-essential \
    python3.10 \
    python3-pip \
    python3.10-dev \
    openjdk-11-jdk \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

# ==================================================
# Python base (pin)
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
# Hugging Face inference stack
# ==================================================
RUN pip install \
    transformers==4.40.2 \
    accelerate==0.30.1 \
    datasets==2.19.0 \
    sentencepiece==0.1.99 \
    protobuf==4.25.3 \
    safetensors==0.4.3 \
    einops==0.7.0 \
    packaging==24.0

# ==================================================
# lm-evaluation-harness (표준 평가)
# ==================================================
RUN pip install \
    lm-eval==0.4.3 \
    evaluate==0.4.2 \
    rouge-score==0.1.2 \
    sacrebleu==2.4.2

# ==================================================
# Korean-specific Evaluation stack
# ==================================================
RUN pip install \
    konlpy==0.6.0 \
    nltk==3.8.1 \
    pandas==2.2.2 \
    scikit-learn==1.4.2 \
    tqdm==4.66.4

# ==================================================
# Deep Eval stack (LLM-as-a-Judge)
# ==================================================
RUN pip install \
    openai==1.30.1 \
    deepeval==0.21.73 \
    pytest==8.2.0 \
    pytest-asyncio==0.23.6

# ==================================================
# Hugging Face Hub
# ==================================================
RUN pip install \
    huggingface_hub==0.23.2

# ==================================================
# Jupyter kernel ONLY (server 실행 안 함)
# ==================================================
RUN pip install \
    ipykernel==6.29.4 \
    jupyter-client==8.6.1 \
    nbformat==5.10.4

RUN python -m ipykernel install \
    --name eval \
    --display-name "Python (Eval)"

# ==================================================
# VSCode Server (code-server)
# ==================================================
ENV HOME=/root

RUN curl -fsSL https://code-server.dev/install.sh | sh \
    && /usr/bin/code-server --version

# ==================================================
# Runtime cache (Volume friendly)
# ==================================================
ENV HF_HOME=/workspace/.cache/huggingface
ENV TRANSFORMERS_CACHE=/workspace/.cache/huggingface
ENV HF_DATASETS_CACHE=/workspace/.cache/huggingface/datasets

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
