# smolVLA 소프트웨어 현황 (현재 설정/실측)

> 작성일: 2026-04-21  
> 목적: 실제 설정된 소프트웨어 환경 값을 기록

## 1) 기본 개발 환경

- 개발 기준 OS: `Ubuntu 22.04`
- Python 기준: `3.12`
- 사용 의존성 그룹:
  - `smolvla`
  - `training`
  - `feetech`

## 2) Orin 실측 소프트웨어 정보

- 스냅샷 파일: `devices_snapshot/orin_env_snapshot_2026-04-22_0043.txt`
- OS: `Ubuntu 22.04.5 LTS`
- L4T: `R36.5.0`
- 커널: `5.15.185-tegra`
- CUDA:
  - `nvcc`: PATH에 미탐지 (패키지로 설치됨, SDK `12.6.11`)
  - cudart: `12.6.68`
- cuDNN: `9.3.0.75-1` (for CUDA 12.6)
- TensorRT: `10.3.0.30-1+cuda12.5`
- GPU 드라이버: `540.5.0`
- nvpmodel 현재 모드: `25W` (mode id `1`)

## 3) 컨테이너/ML 런타임 상태

- Docker 실행 중 컨테이너: 없음 (스냅샷 시점)
- PyTorch 설치 방식: 미확정
  - `python3 -c 'import torch ...'` 출력이 스냅샷에 기록되지 않음
  - 추가 확인 필요: `python3 -m pip show torch`

## 4) 노트북 의존성 실측 결과 (기록용)

- 점검일: `2026-04-21`
- 환경명: `lerobot` (conda)
- Python: `3.10.20`
- pip 경로: `/home/babogaeguri/miniconda3/envs/lerobot/lib/python3.10/site-packages/pip`

| 항목 | 설치 여부 | 버전 | 비고 |
|---|---|---|---|
| lerobot | 설치됨 | `0.4.4` | editable project location: `/home/babogaeguri/lerobot` |
| torch | 설치됨 | `2.7.1` |  |
| torchvision | 설치됨 | `0.22.1` |  |
| transformers | 미설치 | - | `pip show`에서 not found |
| accelerate | 설치됨 | `1.13.0` |  |
| opencv-python-headless | 설치됨 | `4.12.0.88` |  |
| feetech-servo-sdk | 설치됨 | `1.0.0` |  |

점검 메모:
- 같은 날 `base` 환경(`Python 3.13.12`)에서는 핵심 패키지들이 미설치로 확인됨.
- 실제 텔레옵/실행에 사용된 환경은 `lerobot` conda env로 판단됨.
- 현재 실행 환경 Python은 `3.10.20`이며, 문서 상 요구사항(`3.12`)과 불일치가 있어 추후 정리 필요.
- `transformers`가 `pip show` 기준 미설치 상태이므로 smolVLA 실행 전 재확인/설치 필요.

## 5) DGX Spark 실측 소프트웨어 정보

- 스냅샷 파일: `devices_snapshot/dgx_spark_env_snapshot_2026-04-22_0043.txt`
- OS: `Ubuntu 24.04.4 LTS`
- 커널: `6.17.0-1014-nvidia`
- CUDA:
  - `nvcc`: PATH에 미탐지 (패키지로 설치됨, SDK `13.0.2`)
  - GPU 드라이버: `580.142`
- cuDNN: 미탐지 (별도 설치 필요)
- TensorRT: 미탐지 (별도 설치 필요)
- PyTorch: 미설치
- Python: `3.12.3` (pip3 미탐지)
- conda: 미설치
- Docker: 미탐지
- ROS2: 미설치
- 특이사항: 포트 `11434` 리슨 중 (Ollama 실행 중인 것으로 추정)

## 6) 추가 확인 필요 항목

- [ ] PyTorch 설치 방식 확정 — Orin: NVIDIA wheel vs container / DGX: pip 직접 설치 여부
- [ ] DGX cuDNN / TensorRT 설치 필요 여부 확인
- [ ] 학습 PC(DGX)와 Orin 간 모델 반입/실행 절차 확정
- [ ] 외장 SSD 사용 시 데이터셋/체크포인트 경로 확정
