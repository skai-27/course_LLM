# =====================================================================
# LLaMA Factory - WebUI (GUI) Fine-tuning Docker Image
#
# Base: LLaMA-Factory v0.9.4 공식 이미지
#   - CUDA / Ubuntu 22.04 / Python 3.10 / PyTorch
#   - 모든 의존성이 검증된 호환 버전으로 사전 설치됨
#
# 학습모델: Qwen/Qwen3.5-2B
# 학습방법: DoRA (GUI에서 설정)
# 학습데이터: good593/illnesses-dataset (GUI 드롭다운으로 선택)
# =====================================================================
FROM hiyouga/llamafactory:0.9.4

# 작업 디렉토리 (공식 이미지 기본 경로)
WORKDIR /app/LLaMA-Factory

# -----------------------------------------------
# illnesses-dataset을 GUI 드롭다운에 표시하기 위해
# dataset_info.json에 데이터셋 정보를 등록합니다.
# -----------------------------------------------
COPY dataset_info.json /app/LLaMA-Factory/data/dataset_info.json

# WebUI 포트 개방
EXPOSE 7860

# 시작 스크립트
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# -----------------------------------------------
# 학습 완료 후 HuggingFace 업로드 스크립트
# [사용법] 학습 완료 후 SSH 터미널에서:
#   bash /app/upload_model.sh
# -----------------------------------------------
COPY upload_model.sh /app/upload_model.sh
RUN chmod +x /app/upload_model.sh

ENTRYPOINT ["/app/start.sh"]
