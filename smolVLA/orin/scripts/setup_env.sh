#!/bin/bash
# Jetson Orin (L4T R36.x / JetPack 6.x) 독립 Python 환경 구성 스크립트
# 실행 위치: Orin (~/smolvla/scripts/setup_env.sh)
#
# JetPack 6.x (R36.5.0) 기준:
#   CUDA 12.6, Python 3.10 기본 / 3.12 선택 가능
#   NVIDIA PyTorch 인덱스: https://developer.download.nvidia.com/compute/redist/jp/v62/

set -e

SMOLVLA_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV_DIR="${SMOLVLA_DIR}/.venv"

# Python 3.12 우선, 없으면 python3 사용
if command -v python3.12 &>/dev/null; then
    PYTHON=python3.12
else
    PYTHON=python3
fi

echo "[setup] smolVLA 경로: ${SMOLVLA_DIR}"
echo "[setup] venv 경로:    ${VENV_DIR}"
echo "[setup] Python:       $($PYTHON --version)"

# ── 1. venv 생성 ───────────────────────────────────────────────────────────────
if [ -d "$VENV_DIR" ]; then
    echo "[setup] 기존 venv 발견 — 재사용합니다. 완전히 새로 만들려면 .venv 디렉토리를 삭제 후 재실행하세요."
else
    "$PYTHON" -m venv "$VENV_DIR"
    echo "[setup] venv 생성 완료"
fi

source "${VENV_DIR}/bin/activate"
pip install --upgrade pip --quiet

# ── 2. PyTorch (NVIDIA JetPack 6.x aarch64/CUDA 전용) ─────────────────────────
# NVIDIA 인덱스에서 먼저 torch/torchvision 설치 후 lerobot을 --no-deps 없이 설치하면
# pip이 이미 설치된 torch를 재사용한다.
NVIDIA_INDEX="https://developer.download.nvidia.com/compute/redist/jp/v62/"

echo "[setup] PyTorch 설치 중 (NVIDIA JetPack 6.2 인덱스 사용)..."
pip install torch torchvision \
    --extra-index-url "$NVIDIA_INDEX" \
    --quiet

TORCH_VER=$(python -c "import torch; print(torch.__version__)" 2>/dev/null || echo "설치 실패")
echo "[setup] torch 버전: ${TORCH_VER}"

CUDA_OK=$(python -c "import torch; print(torch.cuda.is_available())" 2>/dev/null || echo "false")
echo "[setup] CUDA 사용 가능: ${CUDA_OK}"

# ── 3. lerobot[smolvla,hardware,feetech] 설치 ─────────────────────────────────
echo "[setup] lerobot 설치 중..."
pip install -e "${SMOLVLA_DIR}/lerobot[smolvla,hardware,feetech]" --quiet

echo ""
echo "══════════════════════════════════════════════════════"
echo " 환경 설치 완료!"
echo ""
echo " 활성화 방법:"
echo "   source ${VENV_DIR}/bin/activate"
echo ""
echo " 실행 예시:"
echo "   python ${SMOLVLA_DIR}/examples/tutorial/smolvla/using_smolvla_example.py"
echo "══════════════════════════════════════════════════════"