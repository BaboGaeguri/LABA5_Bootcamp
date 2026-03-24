# 하드웨어 사양 가이드 — ACT 학습 (SO-ARM 101 Pro + LeRobot)

> **기준:** ACT 모델 (~80M 파라미터, ResNet-18 백본), 카메라 1~3대, 에피소드 50~100개 데이터셋

---

## 사양 등급 한눈에 보기

| 등급 | 목적 | GPU VRAM | 예상 학습 시간 (100 epoch) |
|---|---|---|---|
| **최소** | 텔레옵 + 학습 가능 | 6GB | 8~12시간 |
| **권장** | 안정적 학습 | 10~12GB | 2~4시간 |
| **고성능** | 빠른 반복 실험 | 16~24GB | 30분~1시간 |
| **DGX Spark** | Production / 다중 실험 | 128GB 통합 | 10~20분 |

---

## 최소 사양 (Minimum)

> 학습은 가능하지만 느리고, 멀티 카메라 시 불안정할 수 있음

| 항목 | 최소 사양 | 비고 |
|---|---|---|
| **CPU** | 8코어 (Intel i7-10세대 / AMD Ryzen 7 3700X) | 카메라 3대 동시 처리 기준 |
| **RAM** | 16GB DDR4 | 데이터셋 로딩 시 병목 가능 |
| **GPU** | NVIDIA GTX 1660 Ti (6GB VRAM) | batch_size=4로 줄여서 실행 |
| **저장공간** | 256GB SSD (NVMe 권장) | HDD 사용 시 데이터 로딩 매우 느림 |
| **USB** | USB 3.0 포트 3개 이상 | 카메라 + 로봇 암 2대 |
| **OS** | Ubuntu 22.04 / 24.04 x86_64 | Windows/macOS 비권장 |
| **CUDA** | 11.8 이상 | `nvidia-smi`로 버전 확인 |

**최소 사양에서 필수 조정 사항:**
```bash
# batch_size를 4로 줄여야 VRAM 6GB에서 동작
lerobot-train \
    --policy.type=act \
    --dataset.repo_id=<your_username>/so101_task \
    --training.batch_size=4
```

---

## 권장 사양 (Recommended)

> 안정적이고 실용적인 학습 환경. 이 프로젝트의 **기본 타겟 사양**

| 항목 | 권장 사양 | 비고 |
|---|---|---|
| **CPU** | 12~16코어 (Intel i7-13세대 / AMD Ryzen 9 5900X) | 병렬 데이터 전처리 쾌적 |
| **RAM** | 32GB DDR4/DDR5 | 데이터셋 전체 메모리 로드 가능 |
| **GPU** | NVIDIA RTX 3080 (10GB) / RTX 4070 (12GB) | batch_size=8 기본값 그대로 사용 |
| **저장공간** | 512GB NVMe SSD | 여러 데이터셋 / 체크포인트 보관 |
| **USB** | USB 3.1 Gen1 포트 4개 이상 (개별 컨트롤러) | 허브 없이 직결 권장 |
| **전원** | 650W PSU 이상 | RTX 3080 TDP 320W 기준 |
| **CUDA** | 12.1 이상 | |

**권장 PyTorch 설치:**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

---

## 고성능 사양 (High-end)

> 빠른 반복 실험, 고해상도 멀티 카메라, 대규모 데이터셋

| 항목 | 고성능 사양 | 비고 |
|---|---|---|
| **CPU** | 16~24코어 (Intel i9-13세대 / AMD Ryzen 9 7950X) | |
| **RAM** | 64GB DDR5 | 대규모 데이터셋 완전 캐시 가능 |
| **GPU** | NVIDIA RTX 4090 (24GB VRAM) | batch_size=32 이상 가능 |
| **저장공간** | 1TB NVMe SSD (PCIe 4.0) | 빠른 데이터셋 I/O |
| **USB** | PCIe USB 확장 카드 추가 권장 | 카메라 3대 이상 안정 운용 |
| **전원** | 850W+ PSU | RTX 4090 TDP 450W |
| **CUDA** | 12.3 이상 | |

**고성능 배치 설정:**
```bash
lerobot-train \
    --policy.type=act \
    --dataset.repo_id=<your_username>/so101_task \
    --training.batch_size=32 \
    --training.num_workers=8
```

---

## DGX Spark 구성

> NVIDIA GB10 Grace Blackwell Superchip 기반 개인용 AI 슈퍼컴퓨터

### DGX Spark 주요 스펙

| 항목 | 사양 |
|---|---|
| **칩** | NVIDIA GB10 Grace Blackwell Superchip |
| **CPU** | 20코어 ARM Cortex-X925 (Grace) |
| **GPU** | Blackwell GPU (NVLink-C2C 연결) |
| **통합 메모리** | 128GB LPDDR5X (CPU/GPU 공유) |
| **AI 성능** | ~1 PFLOPS (FP8) |
| **스토리지** | 1TB NVMe SSD |
| **I/O** | USB4 × 3, Thunderbolt 4, PCIe 5.0 |
| **가격대** | 약 $3,000~4,000 USD (2025 기준) |

### ACT 학습에서 DGX Spark의 장점

| 항목 | 일반 RTX 4090 | DGX Spark |
|---|---|---|
| VRAM | 24GB (별도 GDDR) | 128GB (CPU와 통합) |
| 메모리 대역폭 | 1,008 GB/s | 3,200 GB/s (NVLink) |
| 모델 동시 실험 | 1~2개 | 4~8개 병렬 가능 |
| 데이터셋 캐시 | RAM↔VRAM 복사 필요 | 통합 메모리로 복사 Zero-copy |
| 전력 소비 | 약 500W+ (전체 시스템) | 60~170W |
| 폼팩터 | ATX 타워 | Mac Mini 크기 |

### DGX Spark 권장 학습 설정

```bash
# 128GB 통합 메모리를 활용한 대규모 배치
lerobot-train \
    --policy.type=act \
    --dataset.repo_id=<your_username>/so101_task \
    --training.batch_size=64 \
    --training.num_workers=16 \
    --training.num_epochs=200
```

### DGX Spark 구매 고려 시 체크포인트

| 체크포인트 | 내용 |
|---|---|
| **I/O** | USB4 포트 3개 → 카메라 2대 + 로봇 1대 직결 가능, 3대 이상 카메라는 허브 필요 |
| **OS** | Ubuntu 22.04 ARM 또는 DGX OS (x86 에뮬레이션 불필요, LeRobot ARM 지원 확인 필요) |
| **ROS2** | ARM64 네이티브 ROS2 Humble/Jazzy 지원 → 이 레포와 연동 가능 |
| **전력** | 가정용 콘센트(110/220V) 사용 가능, 서버실 불필요 |

> **주의:** DGX Spark는 ARM 아키텍처 기반. LeRobot 및 Feetech 모터 드라이버의 ARM64 호환성을 구매 전 확인 권장. 현재(2026년 기준) Seeed Projects fork는 x86_64 기준으로 테스트됨.

---

## 작업 단계별 최소 요구 GPU

| 단계 | GPU 필요 여부 | 최소 VRAM |
|---|---|---|
| 모터 설정 / 캘리브레이션 | ❌ 불필요 | — |
| 텔레옵 (카메라 없음) | ❌ 불필요 | — |
| 텔레옵 (카메라 포함) | ❌ 불필요 | — |
| 데이터셋 녹화 | ❌ 불필요 | — |
| 데이터셋 시각화 | ❌ 불필요 | — |
| **ACT 학습** | ✅ **필수** | **6GB** |
| **정책 평가 (추론)** | ⚠️ 권장 | 4GB (CPU도 가능하나 느림) |

---

## 현재 세팅 진단

```bash
# CPU 코어 수 확인
nproc

# RAM 용량 확인
free -h

# GPU 정보 확인
nvidia-smi

# GPU VRAM 확인
nvidia-smi --query-gpu=name,memory.total --format=csv
```

GPU가 없거나 VRAM이 부족한 경우 대안:

| 대안 | 방법 | 비용 |
|---|---|---|
| **Google Colab** | LeRobot 공식 Colab 노트북 사용 | 무료~월 $10 |
| **Vast.ai / RunPod** | RTX 4090 GPU 클라우드 임대 | 약 $0.3~0.5/시간 |
| **배치 크기 축소** | `--training.batch_size=2` | 학습 시간 2~3배 증가 |

---

## USB 대역폭 주의사항

카메라 3대를 안정적으로 운용하려면 USB 컨트롤러가 분리되어 있어야 합니다.

```bash
# USB 컨트롤러 확인
lsusb -t

# 카메라가 같은 버스(Bus)에 몰려있으면 USB PCIe 확장 카드 추가 권장
```

| 연결 방식 | 안정성 | 비고 |
|---|---|---|
| 카메라 직결 (별도 포트) | ✅ 최고 | 포트마다 다른 컨트롤러 이상적 |
| USB 3.0 허브 1대에 1대 | ⚠️ 보통 | MJPG라면 보통 동작 |
| USB 허브 1대에 2대 이상 | ❌ 비권장 | 프레임 드랍, 연결 끊김 가능 |
