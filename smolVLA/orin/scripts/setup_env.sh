#!/bin/bash
# Jetson Orin (L4T R36.x / JetPack 6.2.2) 독립 Python 환경 구성 스크립트
# 실행 위치: Orin (~/smolvla/scripts/setup_env.sh)
#
# JetPack 6.2.2 (R36.5.0) 기준:
#   CUDA 12.6, Python 3.10 (cp310)
#   PyTorch: NVIDIA JP 6.0 공식 wheel (nv24.08, cu12.6 forward-compatible)
#   - JP 6.2부터 NVIDIA 공식 standalone wheel 공급 중단
#   - jp6/cu126 Jetson AI Lab 인덱스 wheel은 libcudss/libcusparseLt 미설치로 동작 불가
#   - JP 6.0 wheel (2.5.0a0+872d972e41.nv24.08) + cusparselt LD_LIBRARY_PATH 패치로 동작 확인

set -e

SMOLVLA_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV_DIR="${SMOLVLA_DIR}/.venv"

# Python 3.10 우선 (jp6/cu126 wheel이 cp310만 제공)
if command -v python3.10 &>/dev/null; then
    PYTHON=python3.10
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
    if "$PYTHON" -m venv "$VENV_DIR"; then
        echo "[setup] venv 생성 완료"
    else
        echo "[setup] python -m venv 실패. python3-venv 미설치 환경으로 판단되어 virtualenv fallback을 시도합니다."
        "$PYTHON" -m pip install --user --quiet virtualenv
        "$PYTHON" -m virtualenv "$VENV_DIR"
        echo "[setup] virtualenv 생성 완료"
    fi
fi

source "${VENV_DIR}/bin/activate"
pip install --upgrade pip --quiet

# ── 2. lerobot[smolvla,hardware,feetech] 설치 ─────────────────────────────────
# torch/torchvision 을 먼저 설치하면 lerobot 설치 시 pip 가 PyPI CPU-only wheel 로
# 덮어쓰므로, lerobot 을 먼저 설치한 뒤 torch 를 force-reinstall 한다.
echo "[setup] lerobot 설치 중 (${SMOLVLA_DIR})..."
pip install -e "${SMOLVLA_DIR}[smolvla,hardware,feetech]" --quiet

# ── 3. PyTorch (Jetson AI Lab jp6/cu126 인덱스, CUDA 12.6 전용) ───────────────
# JP 6.2부터 NVIDIA 공식 wheel 없음. Jetson AI Lab 준공식 인덱스 사용.
# lerobot 설치 이후에 실행해야 PyPI CPU-only wheel 에 의한 덮어쓰기를 막을 수 있음.
echo "[setup] PyTorch 설치 중 (NVIDIA JP 6.0 wheel — CUDA 12.6 forward-compatible)..."
# jp6/cu126 인덱스 wheel은 libcudss/libcusparseLt 미설치 문제로 동작 불가.
# JP 6.0 공식 wheel(nv24.08, cu12.6, cp310)이 JetPack 6.2.2 CUDA 12.6에서 동작 확인됨.
pip install \
    "https://developer.download.nvidia.com/compute/redist/jp/v61/pytorch/torch-2.5.0a0+872d972e41.nv24.08.17622132-cp310-cp310-linux_aarch64.whl" \
    --force-reinstall --no-deps \
    --quiet

# numpy: torch 2.5.0a0 는 NumPy 1.x 로 컴파일됨 — 2.x 설치 시 ABI 불일치 경고 발생
echo "[setup] NumPy 1.x 고정 중..."
pip install "numpy>=1.24.0,<2" --force-reinstall --quiet

# ── 4. LD_LIBRARY_PATH 패치 (venv activate에 영구 적용) ──────────────────────
# torch 2.5.0a0 은 libcusparseLt.so.0 을 시스템 경로에서 찾으나 JetPack 6.2.2 미포함.
# pip 설치된 nvidia-cusparselt 패키지 경로를 activate 스크립트에 추가.
CUSPARSELT_LIB="${VENV_DIR}/lib/python3.10/site-packages/nvidia/cusparselt/lib"
ACTIVATE_SCRIPT="${VENV_DIR}/bin/activate"
if [ -d "$CUSPARSELT_LIB" ] && ! grep -q "cusparselt" "$ACTIVATE_SCRIPT"; then
    echo "export LD_LIBRARY_PATH=${CUSPARSELT_LIB}:\$LD_LIBRARY_PATH" >> "$ACTIVATE_SCRIPT"
    echo "[setup] cusparselt LD_LIBRARY_PATH 패치 적용"
fi

source "${VENV_DIR}/bin/activate"

TORCH_VER=$(python -c "import torch; print(torch.__version__)" 2>/dev/null || echo "설치 실패")
echo "[setup] torch 버전: ${TORCH_VER}"

CUDA_OK=$(python -c "import torch; print(torch.cuda.is_available())" 2>/dev/null || echo "false")
echo "[setup] CUDA 사용 가능: ${CUDA_OK}"

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