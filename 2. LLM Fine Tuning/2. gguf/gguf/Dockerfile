FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /workspace

# ===============================
# System packages (OS pin)
# ===============================
RUN apt-get update && apt-get install -y \
    git=1:2.34.1-1ubuntu1.10 \
    cmake=3.22.1-1ubuntu1.22.04.2 \
    build-essential \
    python3=3.10.6-1~22.04 \
    python3-pip \
    python3-dev \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

# ===============================
# llama.cpp (commit pin)
# ===============================
RUN git clone https://github.com/ggerganov/llama.cpp.git /opt/llama.cpp
WORKDIR /opt/llama.cpp

# 강의용으로 안정 검증된 커밋
RUN git checkout 3a6d4e9

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

