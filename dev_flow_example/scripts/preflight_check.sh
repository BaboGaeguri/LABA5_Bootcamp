#!/bin/bash
# 배포 전 사전 점검 스크립트
# 사용법: ./scripts/preflight_check.sh <orin_ip> <nuc_ip> [remote_user]
# 예시:   ./scripts/preflight_check.sh 192.168.1.10 192.168.1.20 babogaeguri

set -u
set -o pipefail

ORIN_IP="${1:-}"
NUC_IP="${2:-}"
REMOTE_USER="${3:-babogaeguri}"

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

PASS_COUNT=0
FAIL_COUNT=0
WARN_COUNT=0

print_header() {
  echo "=============================================="
  echo " Breakout Preflight Check"
  echo " 대상 Orin: ${REMOTE_USER}@${ORIN_IP}"
  echo " 대상 NUC : ${REMOTE_USER}@${NUC_IP}"
  echo " 프로젝트 : ${PROJECT_ROOT}"
  echo "=============================================="
}

pass() {
  echo "[PASS] $1"
  PASS_COUNT=$((PASS_COUNT + 1))
}

fail() {
  echo "[FAIL] $1"
  FAIL_COUNT=$((FAIL_COUNT + 1))
}

warn() {
  echo "[WARN] $1"
  WARN_COUNT=$((WARN_COUNT + 1))
}

check_local_cmd() {
  local cmd="$1"
  local label="$2"
  if command -v "$cmd" >/dev/null 2>&1; then
    pass "로컬 명령어 확인: ${label}"
  else
    fail "로컬 명령어 없음: ${label} (설치 필요)"
  fi
}

check_local_file() {
  local path="$1"
  local label="$2"
  if [ -e "$path" ]; then
    pass "로컬 파일 확인: ${label}"
  else
    fail "로컬 파일 누락: ${label} (${path})"
  fi
}

check_ping() {
  local ip="$1"
  local label="$2"
  if ping -c 1 -W 1 "$ip" >/dev/null 2>&1; then
    pass "네트워크 ping 성공: ${label} (${ip})"
  else
    warn "네트워크 ping 실패: ${label} (${ip}) - ICMP 차단일 수 있음"
  fi
}

check_ssh() {
  local ip="$1"
  local label="$2"
  if ssh -o BatchMode=yes -o ConnectTimeout=5 "${REMOTE_USER}@${ip}" "echo ok" >/dev/null 2>&1; then
    pass "SSH 무비번 접속 확인: ${label}"
  else
    fail "SSH 무비번 접속 실패: ${label} (${REMOTE_USER}@${ip})"
    echo "       해결: ssh-copy-id ${REMOTE_USER}@${ip}"
  fi
}

check_remote_orin() {
  local ip="$1"
  local target="${REMOTE_USER}@${ip}"

  if ssh -o BatchMode=yes -o ConnectTimeout=5 "$target" "command -v docker >/dev/null" >/dev/null 2>&1; then
    pass "Orin docker 설치 확인"
  else
    fail "Orin docker 미설치"
    echo "       해결: sudo apt install docker.io"
  fi

  if ssh -o BatchMode=yes -o ConnectTimeout=5 "$target" "docker compose version >/dev/null" >/dev/null 2>&1; then
    pass "Orin docker compose(v2) 확인"
  else
    fail "Orin docker compose(v2) 미확인"
    echo "       해결: sudo apt install docker-compose-v2"
  fi

  if ssh -o BatchMode=yes -o ConnectTimeout=5 "$target" "docker info >/dev/null" >/dev/null 2>&1; then
    pass "Orin docker 권한 확인 (sudo 없이 실행 가능)"
  else
    warn "Orin docker 권한 문제 가능성 (docker info 실패)"
    echo "       해결: sudo usermod -aG docker $REMOTE_USER && newgrp docker"
  fi
}

check_remote_nuc() {
  local ip="$1"
  local target="${REMOTE_USER}@${ip}"

  if ssh -o BatchMode=yes -o ConnectTimeout=5 "$target" "test -d /opt/ros/humble" >/dev/null 2>&1; then
    pass "NUC ROS2 Humble 경로 확인 (/opt/ros/humble)"
  else
    fail "NUC ROS2 Humble 경로 없음 (/opt/ros/humble)"
  fi

  if ssh -o BatchMode=yes -o ConnectTimeout=5 "$target" "bash -lc 'source /opt/ros/humble/setup.bash >/dev/null 2>&1 && command -v ros2 >/dev/null'" >/dev/null 2>&1; then
    pass "NUC ros2 명령어 확인"
  else
    fail "NUC ros2 명령어 사용 불가"
  fi

  if ssh -o BatchMode=yes -o ConnectTimeout=5 "$target" "command -v colcon >/dev/null" >/dev/null 2>&1; then
    pass "NUC colcon 설치 확인"
  else
    warn "NUC colcon 미설치 가능성"
    echo "       해결: sudo apt install python3-colcon-common-extensions"
  fi
}

print_summary() {
  echo
  echo "--------------- 요약 ---------------"
  echo "PASS : ${PASS_COUNT}"
  echo "WARN : ${WARN_COUNT}"
  echo "FAIL : ${FAIL_COUNT}"

  if [ "$FAIL_COUNT" -eq 0 ]; then
    echo "결과: 배포 진행 가능"
    return 0
  fi

  echo "결과: FAIL 항목 해결 후 재실행 필요"
  return 1
}

if [ -z "$ORIN_IP" ] || [ -z "$NUC_IP" ]; then
  echo "사용법: $0 <orin_ip> <nuc_ip> [remote_user]"
  exit 1
fi

print_header

echo "[1/5] 로컬 도구 점검"
check_local_cmd ssh "ssh"
check_local_cmd rsync "rsync"
check_local_cmd docker "docker"

echo
echo "[2/5] 로컬 파일 점검"
check_local_file "${PROJECT_ROOT}/Dockerfile" "Dockerfile"
check_local_file "${PROJECT_ROOT}/docker/docker-compose.dev.yml" "docker-compose.dev.yml"
check_local_file "${PROJECT_ROOT}/configs/prod.yaml" "configs/prod.yaml"
check_local_file "${PROJECT_ROOT}/ros2_ws/src/breakout_bridge_pkg" "ROS2 패키지 경로"

echo
echo "[3/5] 네트워크 점검"
check_ping "$ORIN_IP" "Orin"
check_ping "$NUC_IP" "NUC"

echo
echo "[4/5] SSH 점검"
check_ssh "$ORIN_IP" "Orin"
check_ssh "$NUC_IP" "NUC"

echo
echo "[5/5] 원격 런타임 점검"
check_remote_orin "$ORIN_IP"
check_remote_nuc "$NUC_IP"

print_summary
