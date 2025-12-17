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
    build-essential \
    python3.10 \
    python3-pip \
    python3.10-dev \
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
# - KMMLU
# - Korean QA / Instruction eval
RUN pip install \
    konlpy==0.6.0 \
    nltk==3.8.1 \
    pandas==2.2.2 \
    scikit-learn==1.4.2 \
    tqdm==4.66.4

# (Konlpy dependency)
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    && rm -rf /var/lib/apt/lists/*

# ==================================================
# OpenAI-style Eval stack (LLM-as-a-Judge)
# ==================================================
# - OpenAI / Azure OpenAI
# - Claude / Gemini 대응 가능
# - Judge 프롬프트 기반 평가
RUN pip install \
    openai==1.30.1 \
    litellm==1.38.3 \
    tiktoken==0.7.0 \
    pydantic==2.7.1

# ==================================================
# Hugging Face Hub (upload)
# ==================================================
RUN pip install \
    huggingface_hub==0.23.2

# ==================================================
# Runtime cache (Volume friendly)
# ==================================================
ENV HF_HOME=/workspace/.cache/huggingface
ENV TRANSFORMERS_CACHE=/workspace/.cache/huggingface
ENV HF_DATASETS_CACHE=/workspace/.cache/huggingface/datasets

# ==================================================
# Jupyter (강의/실험용)
# ==================================================
RUN pip install \
    jupyterlab==4.1.8 \
    notebook==7.1.3 \
    ipykernel==6.29.4

EXPOSE 8888

# ==================================================
# Entrypoint
# ==================================================
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]

