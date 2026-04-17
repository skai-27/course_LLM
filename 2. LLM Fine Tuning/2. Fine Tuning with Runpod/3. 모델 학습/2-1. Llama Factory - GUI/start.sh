#!/bin/bash
# =====================================================
# LLaMA-Factory WebUI 시작 스크립트
# GUI를 통해 브라우저에서 파인튜닝을 진행합니다.
# =====================================================

set -e

echo "================================================"
echo "  LLaMA-Factory WebUI 시작"
echo "  모드: GUI (브라우저에서 학습 설정)"
echo "  접속 주소: http://0.0.0.0:7860"
echo "================================================"

# WandB 로그인 (API 키가 있는 경우 - WebUI 모니터링에 활용)
if [ -n "$WANDB_API_KEY" ]; then
    echo "[INFO] WandB 로그인 중..."
    wandb login "$WANDB_API_KEY"
fi

# HuggingFace 로그인 (모델/데이터셋 다운로드에 필요)
if [ -n "$HF_TOKEN" ]; then
    echo "[INFO] HuggingFace 로그인 중..."
    huggingface-cli login --token "$HF_TOKEN"
fi

# LLaMA-Factory WebUI 실행
# 브라우저에서 http://<RunPod IP>:7860 으로 접속하여 GUI로 파인튜닝 설정
cd /app/LLaMA-Factory
echo "[INFO] WebUI 시작 중... 브라우저에서 포트 7860에 접속하세요."
llamafactory-cli webui
