#!/bin/bash
# smolVLA/lerobot submodule → smolVLA/orin/lerobot/ curated 동기화
# 실행 위치: devPC (smolVLA/ 어디서든)
# 언제 실행: git submodule update --remote smolVLA/lerobot 후

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC="${SCRIPT_DIR}/lerobot/src/lerobot"
DST="${SCRIPT_DIR}/orin/lerobot"

if [ ! -f "${SRC}/__init__.py" ]; then
    echo "[sync] 오류: submodule이 초기화되지 않았습니다."
    echo "       git submodule update --init smolVLA/lerobot 을 먼저 실행하세요."
    exit 1
fi

echo "[sync] ${SRC} → ${DST}"
rm -rf "$DST"
mkdir -p "$DST"

copy_dir() {
    local rel="$1"
    mkdir -p "${DST}/${rel}"
    cp -r "${SRC}/${rel}/." "${DST}/${rel}/"
}

copy_files() {
    local dir="$1"; shift
    mkdir -p "${DST}/${dir}"
    for f in "$@"; do
        cp "${SRC}/${dir}/${f}" "${DST}/${dir}/${f}"
    done
}

# ── root ──────────────────────────────────────────────────────────────────────
copy_files "." "__init__.py" "__version__.py" "types.py"

# ── cameras (reachy2 제외) ────────────────────────────────────────────────────
copy_files "cameras" "__init__.py" "camera.py" "configs.py" "utils.py"
copy_dir "cameras/opencv"
copy_dir "cameras/realsense"
copy_dir "cameras/zmq"

# ── configs (전체) ────────────────────────────────────────────────────────────
copy_dir "configs"

# ── envs (시뮬레이션 백엔드 제외) ──────────────────────────────────────────────
copy_files "envs" "__init__.py" "configs.py" "factory.py" "utils.py"

# ── model ─────────────────────────────────────────────────────────────────────
copy_dir "model"

# ── motors (feetech만) ───────────────────────────────────────────────────────
copy_files "motors" "__init__.py" "motors_bus.py" "encoding_utils.py" "calibration_gui.py"
copy_dir "motors/feetech"

# ── optim ─────────────────────────────────────────────────────────────────────
copy_dir "optim"

# ── policies (smolvla + rtc) ─────────────────────────────────────────────────
copy_files "policies" "__init__.py" "pretrained.py" "factory.py" "utils.py"
copy_dir "policies/smolvla"
copy_dir "policies/rtc"

# ── processor (전체) ──────────────────────────────────────────────────────────
copy_dir "processor"

# ── robots (so_follower만) ───────────────────────────────────────────────────
copy_files "robots" "__init__.py" "robot.py" "config.py" "utils.py"
copy_dir "robots/so_follower"

# ── scripts (eval + teleoperate) ─────────────────────────────────────────────
copy_files "scripts" "lerobot_eval.py" "lerobot_teleoperate.py"

# ── teleoperators (so_leader만) ──────────────────────────────────────────────
copy_files "teleoperators" "__init__.py" "config.py" "teleoperator.py" "utils.py"
copy_dir "teleoperators/so_leader"

# ── utils (전체) ──────────────────────────────────────────────────────────────
copy_dir "utils"

echo "[sync] 완료"
echo "[sync] 파일 수: $(find "$DST" -name "*.py" | wc -l) 개"