# ==================================================
# Base Image (CPU Runtime)
# ==================================================
FROM runpod/base:1.0.2-ubuntu2204

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    CUDA_HOME=/usr/local/cuda \
    PYTHON_EXE=/usr/bin/python3.11

WORKDIR /workspace

# ==================================================
# 2. System Packages & Python Link
# ==================================================
RUN apt-get update && apt-get install -y \
    git curl wget vim build-essential \
    python3.11 python3.11-dev python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 시스템 기본 파이썬 3.11로 고정
RUN ln -sf /usr/bin/python3.11 /usr/bin/python3 && \
    ln -sf /usr/bin/python3.11 /usr/bin/python && \
    python -m pip install --upgrade pip setuptools wheel

# ==================================================
# 3. DeepEval & QA 평가용 Libraries
# ==================================================
COPY requirements.txt /workspace/requirements.txt

RUN python -m pip install --no-cache-dir --upgrade pip
RUN python -m pip install --no-cache-dir \
    -r /workspace/requirements.txt

# RUN python -m pip install --no-cache-dir \
#     deepeval==3.7.6 \
#     openai==2.14.0 \
#     pandas==2.3.3 \
#     sentence-transformers==5.2.0 \
#     evaluate==0.4.6 \
#     tqdm==4.67.1 \
#     python-dotenv==1.2.1 \
#     lm-eval==0.4.9.2

# RUN python -m pip install --no-cache-dir \
#     ipykernel==6.29.5 jupyter-client==8.6.3

# 커널 등록 (--sys-prefix로 Python 환경 내에 설치)
RUN python -m ipykernel install --sys-prefix --name DeepEval --display-name "Python (DeepEval)"

# ==================================================
# 4. VSCode Server (선택)
# ==================================================

RUN curl -fsSL https://code-server.dev/install.sh | sh

# ==================================================
# 5. Workspace Content
# ==================================================
COPY lectures/ /opt/lectures/

EXPOSE 8080

CMD ["bash", "-c", "\
if [ ! -d /workspace/lectures ]; then cp -r /opt/lectures /workspace/lectures; fi && \
code-server /workspace \
    --bind-addr 0.0.0.0:8080 \
    --auth none \
    --disable-telemetry \
"]
