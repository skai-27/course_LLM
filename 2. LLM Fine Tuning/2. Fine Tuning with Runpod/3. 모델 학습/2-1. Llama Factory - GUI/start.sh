#!/bin/bash
# =====================================================
# LLaMA-Factory WebUI 시작 스크립트
# GUI를 통해 브라우저에서 파인튜닝을 진행합니다.
# =====================================================

# set -e 제거: 선택적 로그인 실패 시 컨테이너가 종료되지 않도록 합니다.

echo "================================================"
echo "  LLaMA-Factory WebUI 시작"
echo "  모드: GUI (브라우저에서 학습 설정)"
echo "  접속 주소: http://0.0.0.0:7860"
echo "================================================"

# WandB 로그인 (API 키가 있는 경우 - WebUI 모니터링에 활용)
# || true: 로그인 실패해도 스크립트를 계속 진행합니다.
if [ -n "$WANDB_API_KEY" ]; then
    echo "[INFO] WandB 로그인 중..."
    wandb login "$WANDB_API_KEY" || true
else
    echo "[INFO] WANDB_API_KEY 없음 - WandB 로그인 건너뜀"
    wandb disabled || true
fi

# HuggingFace 로그인 (모델/데이터셋 다운로드에 필요)
# || true: 로그인 실패해도 스크립트를 계속 진행합니다.
if [ -n "$HF_TOKEN" ]; then
    echo "[INFO] HuggingFace 로그인 중..."
    huggingface-cli login --token "$HF_TOKEN" || true
else
    echo "[INFO] HF_TOKEN 없음 - HuggingFace 로그인 건너뜀"
fi

# Gradio 환경변수 설정 (export로 subprocess에도 전달)
# GRADIO_SERVER_NAME=0.0.0.0: RunPod 프록시가 접근할 수 있도록 모든 인터페이스에 바인딩
# GRADIO_SERVER_PORT=7860: RunPod에 노출된 포트와 일치
# GRADIO_SHARE=False: 공개 터널(share link) 비활성화
export GRADIO_SERVER_NAME="0.0.0.0"
export GRADIO_SERVER_PORT="7860"
export GRADIO_SHARE="False"

# LLaMA-Factory WebUI 실행
cd /app/LLaMA-Factory
echo "[INFO] WebUI 시작 중... (server_name=${GRADIO_SERVER_NAME}, port=${GRADIO_SERVER_PORT})"
exec llamafactory-cli webui
