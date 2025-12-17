FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /workspace

# ===============================
# System packages (OS pin)
# ===============================
RUN apt-get update && apt-get install -y \
    git=1:2.34.* \
    cmake=3.22.* \
    build-essential \
    python3.10 \
    python3-pip \
    python3.10-dev \
    wget \
    curl \
    libcurl4-openssl-dev \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

# ===============================
# llama.cpp (latest stable)
# ===============================
RUN git clone https://github.com/ggerganov/llama.cpp.git /opt/llama.cpp
WORKDIR /opt/llama.cpp

# 최신 안정 버전 사용 (gguf 0.6.0 호환)
# git checkout 생략하여 최신 master 사용

RUN cmake -B build \
    && cmake --build build --config Release

# ===============================
# Python GGUF stack (version pin)
# ===============================
RUN pip install --upgrade pip==24.0

RUN pip install \
    gguf==0.6.0 \
    transformers==4.40.2 \
    sentencepiece==0.1.99 \
    safetensors==0.4.3

WORKDIR /workspace

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

