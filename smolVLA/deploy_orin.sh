#!/bin/bash
# devPC → Orin 배포 스크립트
# 실행 위치: devPC (smolVLA/ 디렉토리 내 어디서든)

ORIN_HOST="orin"
ORIN_DEST="/home/laba/smolvla"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC="${SCRIPT_DIR}/orin/"

echo "[deploy] ${SRC} → ${ORIN_HOST}:${ORIN_DEST}"

rsync -avz --delete \
    --exclude '.venv' \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude '*.egg-info' \
    --exclude '.git' \
    "$SRC" "${ORIN_HOST}:${ORIN_DEST}"

echo "[deploy] 완료. Orin에서 초기 설치가 필요하면:"
echo "  ssh orin"
echo "  bash ~/smolvla/scripts/setup_env.sh"