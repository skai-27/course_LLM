# vLLM + Hugging Face (Hub에서 MODEL_NAME으로 가중치 로드)
# 베이스 이미지에 CUDA·vLLM이 포함되어 있음 → 핸들러만 추가
FROM vllm/vllm-openai:v0.7.2

# 기존 설치된 충돌 유발 패키지 제거
RUN pip uninstall -y transformers vllm huggingface_hub

# 캐시를 무시하고 최신 안정 버전으로 재설치
# --force-reinstall 옵션을 통해 기존 찌꺼기를 완전히 덮어씁니다.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --force-reinstall \
    transformers==4.49.0 \
    huggingface_hub==0.28.1 \
    vllm==0.7.2

WORKDIR /

ENV PYTHONUNBUFFERED=1
# 배포 시 RunPod 엔드포인트 환경 변수로 덮어쓰기 (예: Qwen/Qwen2.5-0.5B-Instruct)
ENV MODEL_NAME=good593/unsloth-gemma3-1b-finetune-diseases

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY handler.py .
COPY test_input.json /test_input.json

# OpenAI 서버 기본 진입점 대신 RunPod Serverless 핸들러 실행
ENTRYPOINT []
CMD ["python3", "-u", "/handler.py"]
