# smolVLA 하드웨어 현황 (현재 보유/실측)

> 작성일: 2026-04-21  
> 목적: 실제 보유 장비와 실측 하드웨어 값을 기록

## 1) 컴퓨팅 장치

- 개발 PC: Ubuntu 환경 사용 중
- 엣지 장치: `Jetson Orin Nano Super Developer Kit`
- 학습/파인튜닝 서버: `NVIDIA DGX Spark`

## 2) devPC 사양 확인 방법 및 실측

### 실측 결과 (2026-04-21)

- 호스트명: `babogaeguri-950QED`
- OS: `Ubuntu 22.04.5 LTS`
- 커널: `6.8.0-106-generic`
- CPU: `12th Gen Intel(R) Core(TM) i7-1260P`
  - 논리 코어: `16`
  - 소켓당 코어: `12`
- 메모리: 총 `15Gi` (가용 약 `8.1Gi`, 점검 시점)
- GPU:
  - `nvidia-smi not found` (NVIDIA 드라이버/CLI 미탐지 상태)
- 저장장치:
  - 내장 NVMe: `SAMSUNG MZVL2512HCJQ-00B` `476.9G`
  - Linux 루트(`/`): `nvme0n1p5` (`ext4`, `200G`)
  - EFI: `nvme0n1p1` (`vfat`, `200M`)
  - 추가 USB mass storage 디바이스(`sda`, `sdb`)가 보이지만 크기 `0B`로 인식됨

## 3) Orin 저장장치 실측

- 스냅샷 파일:
  - `smolVLA/storage/orin_env_snapshot_2026-04-21_1316.txt`
  - `smolVLA/storage/orin_storage_snapshot_2026-04-21_1323.txt`
- 확인된 디스크:
  - `nvme0n1` `SAMSUNG MZVL2256HCHQ-00B` (256GB급)
  - 루트(`/`) 마운트: `nvme0n1p1` (`ext4`)
  - EFI 마운트: `nvme0n1p10` (`vfat`)
- 메모:
  - 외장 SSD 별도 장치는 스냅샷 시점에서 식별되지 않음 (`/dev/sdX` 또는 추가 `nvmeXnY` 미검출)

## 4) DGX Spark 실측

> 스냅샷: `devices_snapshot/dgx_spark_env_snapshot_2026-04-22_0043.txt`

| 항목 | 실측값 | 비고 |
|---|---|---|
| 호스트명 | `spark-8434` | |
| OS | `Ubuntu 24.04.4 LTS` | |
| 커널 | `6.17.0-1014-nvidia` | |
| CPU | `aarch64` 20코어 | NUMA 1노드, Max 3900 / 2808 MHz (클러스터별) |
| 메모리 | `121Gi` | 가용 약 110Gi (스냅샷 시점) |
| GPU 모델 | `NVIDIA GB10` | Grace Blackwell |
| GPU 메모리 | Unified Memory | nvidia-smi에서 별도 VRAM 값 미제공 |
| GPU 드라이버 | `580.142` | CUDA 13.0 지원 |
| 저장장치 | NVMe `3.7T` | SAMSUNG MZALC4T0HBL1-00B07, 사용 215G / 3.7T |

---

## 5) SO-ARM 핵심 부품 (BOM 기준)

- 모터 계열: `Feetech STS3215`

| 구성 | 상세 모델 | 수량 |
|---|---|---|
| SO-101 follower (팔 1개) | `STS3215 7.4V, 1/345 gear (C001)` | x6 |
| SO-101 leader (팔 1개) | `STS3215 7.4V, 1/345 (C001)` | x1 |
| SO-101 leader (팔 1개) | `STS3215 7.4V, 1/191 (C044)` | x2 |
| SO-101 leader (팔 1개) | `STS3215 7.4V, 1/147 (C046)` | x3 |

leader + follower(현재 보유 1쌍) 합계:
- `C001 x7`, `C044 x2`, `C046 x3`

## 6) 모터 드라이버 보드 / 케이블

- 모터 드라이버(컨트롤 보드):
  - `Serial Bus Servo Driver Board, for ST/SC Series Serial Bus Servos`
  - 유통명 예시: `Waveshare Bus Servo Adapter (A)`
  - BOM 링크 ASIN 예시: `B0CTMM4LWK`
  - 수량 기준: 팔 1개당 보드 1개

- 보드-PC 연결 USB 케이블:
  - USB-A to USB-C 케이블
  - 상품 예시: `etguuds USB A to USB C Cable 6.6ft, 2-Pack, 3A`
  - ASIN 예시: `B0B8NWLLW2`

## 7) 로봇 구성 수량

- Follower arm: 1대
- Leader arm: 1대
