#!/bin/bash
# NUC 배포 스크립트
# 사용법: ./scripts/deploy_nuc.sh <nuc_ip>
# 예시:   ./scripts/deploy_nuc.sh 192.168.1.20

set -e  # 에러 발생 시 즉시 중단

NUC_IP=$1
NUC_USER="laba"
ORIN_IP="172.16.128.97"
ORIN_USER="laba"
REMOTE_DIR="/home/$NUC_USER/breakout"
LOCAL_DIR="$(cd "$(dirname "$0")/.." && pwd)"  # dev_flow_example/ 절대경로

JUMP="-J $ORIN_USER@$ORIN_IP"

if [ -z "$NUC_IP" ]; then
  echo "[deploy_nuc] 사용법: $0 <nuc_ip>"
  echo "             예시:   $0 10.42.0.221"
  exit 1
fi

echo "=============================="
echo " NUC 배포 시작"
echo " 경로: Dev PC → Orin($ORIN_IP) → NUC($NUC_IP)"
echo " 대상: $NUC_USER@$NUC_IP:$REMOTE_DIR"
echo "=============================="

# 1. 원격 디렉토리 생성
echo "[1/3] 원격 디렉토리 준비..."
ssh $JUMP $NUC_USER@$NUC_IP "mkdir -p $REMOTE_DIR"

# 2. ROS2 패키지 복사 (Orin 경유 rsync)
echo "[2/3] ROS2 패키지 복사..."
rsync -avz -e "ssh -J $ORIN_USER@$ORIN_IP" \
  --exclude='__pycache__' --exclude='build' --exclude='install' --exclude='log' \
  $LOCAL_DIR/ros2_ws \
  $NUC_USER@$NUC_IP:$REMOTE_DIR/

# 3. ROS2 패키지 빌드 및 nuc_sub 실행
echo "[3/3] ROS2 패키지 빌드 및 실행..."
ssh $JUMP $NUC_USER@$NUC_IP "
  source /opt/ros/humble/setup.bash &&
  cd $REMOTE_DIR/ros2_ws &&
  colcon build --packages-select breakout_bridge_pkg &&
  source install/setup.bash &&
  ros2 run breakout_bridge_pkg nuc_sub
"

echo "=============================="
echo " NUC 배포 완료"
echo "=============================="
