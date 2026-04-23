# smolVLA Orin 환경 세팅 기록

> 작성일: 2026-04-21 (최초) / 2026-04-23 (업데이트)
> 목적: lerobot을 Orin에서 실행하기 위한 환경 구성 과정과 현재 상태를 기록

## 1) 개요

- 실행 대상: Orin (JetPack 6.2.2, L4T R36.5.0, CUDA 12.6)
- 환경 관리 방식: venv (`~/smolvla/.venv`)
- 소프트웨어 실측 현황 근거: `docs/storage/03_software.md`

## 2) venv 환경 구성 (2026-04-23 확정)

conda env 방식은 폐기. `setup_env.sh`가 생성하는 venv를 사용.

- venv 경로: `~/smolvla/.venv`
- Python 버전: `3.10` (JetPack 6.2.2 시스템 Python)
- 설치 스크립트: `~/smolvla/scripts/setup_env.sh`

**실측 설치 패키지 (2026-04-23 기준):**

| 패키지 | 버전 | 비고 |
|---|---|---|
| lerobot (smolVLA orin/) | editable | `~/smolvla/` — `[smolvla,hardware,feetech]` extras |
| torch | `2.5.0a0+872d972e41` | NVIDIA JP 6.0 nv24.08 wheel, CUDA avail: True (12.6) |
| torchvision | 미설치 | Orin 호환 버전 없음 (smolVLA 추론 경로에서 미사용) |
| numpy | `<2.0.0` | torch 2.5.0a0 NumPy 1.x ABI 요건으로 고정 |
| transformers | lerobot deps 포함 | smolVLA extras 설치 시 자동 설치 |
| accelerate | lerobot deps 포함 | |
| opencv-python-headless | lerobot deps 포함 | |
| feetech-servo-sdk | lerobot deps 포함 | |

## 3) PyTorch 설치 방식

### 배경

- JetPack 6.2부터 NVIDIA 공식 standalone wheel 공급 중단
- `docs/reference/Install-PyTorch-Jetson-Platform-Release-Notes.md` Compatibility Matrix 확인 결과, JP 6.2 전체 항목의 wheel 컬럼 `-` (공급 없음)

### 시도한 경로와 실패 사유

**1차 시도: Jetson AI Lab PyPI 인덱스 (`pypi.jetson-ai-lab.io/jp6/cu126`)**

NVIDIA 엔지니어(Dusty Franklin)가 관리하는 준공식 인덱스.

| 버전 | 실패 사유 |
|---|---|
| torch 2.11.0+cu130 | CUDA 13.0 빌드 — Orin CUDA 12.6 드라이버와 불일치, `CUDA avail: False` |
| torch 2.8.0 ~ 2.10.0 | `libcudss.so.0` 의존성 — JP 6.2.2에 libcudss 미설치, apt로도 설치 불가 |

**2차 시도: NVIDIA JP 6.1 공식 wheel (`nv24.09`)**

URL 404 — `v61` 디렉토리에는 `nv24.08` wheel만 존재, `nv24.09`는 제공 안 됨.

### 확정 설치 방식: NVIDIA JP 6.0 공식 redist wheel (2026-04-23)

`v61` 디렉토리의 `nv24.08` wheel이 JP 6.2.2에서도 정상 동작.

**wheel 정보:**

| 항목 | 값 |
|---|---|
| torch 버전 | `2.5.0a0+872d972e41` |
| 빌드 태그 | `nv24.08.17622132` |
| Python | cp310 |
| arch | aarch64 |
| CUDA avail | True (12.6) |

**설치 순서 (`setup_env.sh` 기준):**

1. lerobot (orin/) editable 먼저 설치 — pip가 CPU-only torch를 덮어쓰지 못하도록
2. torch wheel 설치 (`--force-reinstall --no-deps`)
3. numpy `<2` 재고정 (`--force-reinstall`)
4. venv activate 스크립트에 LD_LIBRARY_PATH 자동 패치

**LD_LIBRARY_PATH 패치 이유:**

torch 2.5.0a0 pip 설치 시 `nvidia-cusparselt-cu12` 패키지가 함께 설치되는데, `libcusparseLt.so.0`가 시스템 경로에 없음. venv activate 시 아래 경로를 자동 추가:

`{venv}/lib/python3.10/site-packages/nvidia/cusparselt/lib`

**근거 자료:**
- [NVIDIA Developer Forums — Installing Pytorch & Torchvision for JetPack 6.2 and CUDA 12.6](https://forums.developer.nvidia.com/t/installing-pytorch-torchvision-for-jetpack-6-2-and-cuda-12-6/346074)
- [NVIDIA Developer Forums — PyTorch for Jetson (공식 스레드)](https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048)
- `docs/reference/Install-PyTorch-Jetson-Platform-Release-Notes.md`
