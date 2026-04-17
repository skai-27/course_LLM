#!/bin/bash
# =====================================================================
# LLaMA-Factory WebUI 시작 스크립트
# GUI를 통해 브라우저에서 파인튜닝을 진행합니다.
# =====================================================================

echo "================================================"
echo "  LLaMA-Factory WebUI 시작"
echo "  모드: GUI (브라우저에서 학습 설정)"
echo "  접속 주소: http://0.0.0.0:7860"
echo "================================================"

# WandB 로그인 (WANDB_API_KEY 환경변수가 설정된 경우)
if [ -n "$WANDB_API_KEY" ]; then
    echo "[INFO] WandB 로그인 중..."
    wandb login "$WANDB_API_KEY" || true
else
    wandb disabled 2>/dev/null || true
fi

# HuggingFace 로그인 (HF_TOKEN 환경변수가 설정된 경우)
if [ -n "$HF_TOKEN" ]; then
    echo "[INFO] HuggingFace 로그인 중..."
    huggingface-cli login --token "$HF_TOKEN" || true
fi

# Gradio 서버 설정
# GRADIO_SERVER_NAME=0.0.0.0: RunPod 프록시가 접근할 수 있도록 모든 인터페이스에 바인딩
export GRADIO_SERVER_NAME="0.0.0.0"
export GRADIO_SERVER_PORT="7860"

# LLaMA-Factory WebUI 실행
cd /app/LLaMA-Factory
echo "[INFO] WebUI 시작 중... 브라우저에서 포트 7860에 접속하세요."
exec llamafactory-cli webui
