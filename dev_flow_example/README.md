# dev_flow_example

블록 깨기 게임을 예제로, Docker / Config / Factory 구조로 개발-배포를 분리하는 흐름을 체득하기 위한 프로젝트입니다.

- **대상 장비**: Orin (게임 로직 + 렌더링) + NUC (점수 서버)
- **핵심 원칙**: 구조 먼저, 구현 나중

---

## 디렉토리 구조

```
dev_flow_example/
├── README.md
├── Dockerfile
├── requirements.txt
├── configs/          # 환경별 설정 파일
├── docker/           # Docker 관련 파일
├── docs/             # 개발 문서 (아래 참고)
├── nuc/              # NUC 전용 코드
├── orin/             # Orin 전용 코드
├── ros2_ws/          # ROS2 워크스페이스
├── scripts/          # 유틸리티 스크립트
└── tests/            # 테스트 코드
```

---

## 문서 목록 (`docs/`)

### 00 - 프로젝트 계획

| 파일 | 설명 |
|------|------|
| [00_breakout_plan.md](docs/00_breakout_plan.md) | 블록 깨기 게임 전체 개발 계획. 개발 철학, 단계별 목표, 구조 설계 방향 정리 |
| [99_hylion_sw_dev_plan.md](docs/99_hylion_sw_dev_plan.md) | 하이리온 소프트웨어 전체 개발 계획. Orin Nano Super / NUC / SO-ARM101 / ESP32 대상 |

### 01 - Docker

| 파일 | 설명 |
|------|------|
| [01_docker_guide.md](docs/01_docker_guide.md) | Docker 기초 가이드. 게임 환경 격리 및 어느 머신에서든 동일 실행하는 방법 |

### 02 - 네트워크

| 파일 | 설명 |
|------|------|
| [02_00_네트워크관련정리.md](docs/02_00_네트워크관련정리.md) | 네트워크 작업 중 느낀점 및 추가로 확인할 사항 메모 |
| [02_01_network_setting.md](docs/02_01_network_setting.md) | 네트워크 기본 개념 정리. IP/인터페이스 확인 방법 (개발 PC, Orin, NUC 기준) |
| [02_02_network_connection.md](docs/02_02_network_connection.md) | Orin/NUC 네트워크 연결 가이드. SSH 접속 및 ROS2 통신 안정화 |
| [02_03_game_start.md](docs/02_03_game_start.md) | 실물 배포 시작 프로세스. Dev PC에서 Orin/NUC에 게임 빌드·배포 후 실행까지 |
| [02_96_start_process.md](docs/02_96_start_process.md) | Orin / NUC 연결 시작 프로세스. SSH 연결 성공까지 단계별 절차 |
| [02_97_orin_run_log.md](docs/02_97_orin_run_log.md) | Orin 실행/배포 과정의 시행착오 및 해결 내용 시간순 기록 |
| [02_98_ssh_connection.md](docs/02_98_ssh_connection.md) | SSH 연결 체크리스트 및 보류 메모 |
| [02_99_network_inventory.md](docs/02_99_network_inventory.md) | PC / Orin / NUC 네트워크 정보 인벤토리. 배포 전 필요한 IP·인터페이스 정보 기록 |

### 03 - 배포

| 파일 | 설명 |
|------|------|
| [03_01_deploy_flow.md](docs/03_01_deploy_flow.md) | 하이리온 배포 플로우. 환경 초기 세팅 후 코드/모델 변경을 반복 배포하는 흐름 |

---

## 문서 읽는 순서 (권장)

1. [00_breakout_plan.md](docs/00_breakout_plan.md) — 프로젝트 전체 구조와 목표 파악
2. [01_docker_guide.md](docs/01_docker_guide.md) — Docker 환경 이해
3. [02_01_network_setting.md](docs/02_01_network_setting.md) → [02_99_network_inventory.md](docs/02_99_network_inventory.md) — 네트워크 기본 개념 및 인벤토리 작성
4. [02_96_start_process.md](docs/02_96_start_process.md) → [02_02_network_connection.md](docs/02_02_network_connection.md) — SSH 연결 및 네트워크 안정화
5. [02_03_game_start.md](docs/02_03_game_start.md) — 실물 배포 시작
6. [03_01_deploy_flow.md](docs/03_01_deploy_flow.md) — 반복 배포 플로우
