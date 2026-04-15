#!/bin/bash
# Orin 배포 스크립트
# 사용법: ./scripts/deploy_orin.sh <orin_ip>
# 예시:   ./scripts/deploy_orin.sh 192.168.1.10

set -e  # 에러 발생 시 즉시 중단

ORIN_IP=$1
ORIN_USER="babogaeguri"
REMOTE_DIR="/home/$ORIN_USER/breakout"
LOCAL_DIR="$(cd "$(dirname "$0")/.." && pwd)"  # dev_flow_example/ 절대경로

if [ -z "$ORIN_IP" ]; then
  echo "[deploy_orin] 사용법: $0 <orin_ip>"
  exit 1
fi

echo "=============================="
echo " Orin 배포 시작"
echo " 대상: $ORIN_USER@$ORIN_IP:$REMOTE_DIR"
echo "=============================="

# 1. 원격 디렉토리 생성
echo "[1/4] 원격 디렉토리 준비..."
ssh $ORIN_USER@$ORIN_IP "mkdir -p $REMOTE_DIR"

# 2. 코드 복사 (docker, configs, orin, ros2_ws, scripts, Dockerfile, requirements.txt)
echo "[2/4] 코드 복사..."
rsync -avz --exclude='__pycache__' \
  $LOCAL_DIR/orin \
  $LOCAL_DIR/configs \
  $LOCAL_DIR/ros2_ws \
  $LOCAL_DIR/docker \
  $LOCAL_DIR/Dockerfile \
  $LOCAL_DIR/requirements.txt \
  $ORIN_USER@$ORIN_IP:$REMOTE_DIR/

# 3. Docker 이미지 빌드
echo "[3/4] Docker 이미지 빌드..."
ssh $ORIN_USER@$ORIN_IP "cd $REMOTE_DIR && docker build -t breakout-game ."

# 4. 실행 (prod 모드 - ROS2 점수 전송 활성화)
echo "[4/4] 게임 실행 (prod 모드)..."
ssh $ORIN_USER@$ORIN_IP "cd $REMOTE_DIR/docker && \
  docker compose -f docker-compose.dev.yml run \
  -e CONFIG_PATH=configs/prod.yaml orin"

echo "=============================="
echo " Orin 배포 완료"
echo "=============================="
