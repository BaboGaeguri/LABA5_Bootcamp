# 블록 깨기 게임 — 개발 계획

> 목적: docker / config / factory 구조로 개발-배포를 분리하는 흐름을 체득한다.
> 대상: Orin (게임 로직 + 렌더링) + NUC (점수 서버)

---

## 개발 철학

> **"구조 먼저, 구현 나중"**
> 코드를 짜기 전에 인터페이스를 확정한다.
> config만 바꿔서 dev ↔ prod 전환이 되어야 한다.
> 하드웨어(화면, 키보드)가 없어도 Mock으로 개발할 수 있어야 한다.
> 성래 컴퓨터에서도 내가 동작한거를 딸깍으로 똑같이 동작할 수 있어야 한다.

---

## 전체 흐름 요약

```
1단계  전체 구조 설계        파일 구조 확정, 인터페이스 확정, config 초안
2단계  환경 연결 확인        display 확인, ROS2 확인
3단계  통신 확인             Orin → NUC 점수 토픽 end-to-end
4단계  개별 모듈 구현        engine, input, display, fsm, score_server
5단계  통합 테스트           dev → prod 전환 후 배포
```

---

## 프로젝트 파일 구조

```
dev_flow_example/
│
├── orin/                               # Orin에서 실행되는 코드 (게임)
│   ├── game/
│   │   ├── engine.py                   # 게임 로직: 공/블록/패들 물리 연산
│   │   ├── input.py                    # 실제 키보드 입력 (prod용)
│   │   ├── mock_input.py               # 자동조작 입력 (dev용 - 키보드 없이 테스트)
│   │   └── factory.py                  # config 읽어서 input.py / mock_input.py 선택
│   │
│   ├── display/
│   │   ├── screen.py                   # 실제 pygame 화면 출력 (prod용)
│   │   ├── mock_screen.py              # 헤드리스 출력 - 터미널에 상태 프린트 (dev용)
│   │   └── factory.py                  # config 읽어서 screen.py / mock_screen.py 선택
│   │
│   ├── state_machine/
│   │   └── fsm.py                      # 상태 머신: IDLE → PLAYING → PAUSED → GAME_OVER / CLEAR
│   │
│   └── core/
│       └── coordinator.py              # 진입점: config 로드 → 모듈 조립 → 게임 루프 실행
│
├── nuc/                                # NUC에서 실행되는 코드 (점수 서버)
│   ├── score_server.py                 # ROS2로 점수 수신 후 터미널 출력 (prod용)
│   ├── mock_score_server.py            # 로컬에서 점수 출력만 (dev용)
│   └── factory.py                      # config 읽어서 score_server / mock 선택
│
├── ros2_ws/                            # Orin ↔ NUC 통신 (양쪽 모두 설치)
│   └── src/
│       └── breakout_bridge_pkg/
│           └── breakout_bridge_pkg/
│               ├── orin_pub.py         # Orin → NUC: /game/score 발행 (Int32)
│               ├── orin_sub.py         # NUC → Orin: /game/status 수신 (String)
│               ├── nuc_pub.py          # NUC → Orin: /game/status 발행
│               ├── nuc_sub.py          # Orin → NUC: /game/score 수신
│               └── launch/
│                   ├── orin.launch.py  # Orin에서 실행할 노드 묶음
│                   └── nuc.launch.py   # NUC에서 실행할 노드 묶음
│
├── configs/
│   ├── dev.yaml                        # Mock 입력 + 헤드리스 + 로컬 점수 출력
│   └── prod.yaml                       # 실제 키보드 + pygame 화면 + NUC 점수 전송
│
├── docker/
│   ├── docker-compose.dev.yml          # 개발용 컨테이너 (pygame 없음, mock 동작)
│   └── docker-compose.prod.yml         # 배포용 컨테이너 (Orin용 / NUC용 서비스 분리)
│
├── tests/
│   ├── 2_hw_connection/
│   │   ├── check_display.py            # pygame 화면 뜨는지 확인
│   │   └── check_ros2.sh               # ROS2 토픽 통신 살아있는지 확인
│   ├── 3_interface/
│   │   └── test_score_topic.py         # /game/score 발행 → NUC 수신 end-to-end
│   ├── 4_unit/
│   │   ├── test_engine.py              # 공 물리, 블록 충돌, 점수 계산 단위 테스트
│   │   ├── test_fsm.py                 # 상태 전환 규칙 단위 테스트
│   │   └── test_input.py               # MockInput 자동조작 동작 확인
│   └── 5_integration/
│       └── test_full_game.py           # dev 모드로 게임 전체 시나리오 자동 실행
│
├── scripts/
│   ├── deploy_orin.sh                  # Orin에 코드 복사 + docker 실행
│   └── deploy_nuc.sh                   # NUC에 코드 복사 + docker 실행
│
└── 00_breakout_plan.md                 # 이 파일
```

---

## 핵심 개념 설명

### factory 패턴
```
config['input']['type'] == 'real'  →  KeyboardInput()   # 실제 키보드
config['input']['type'] == 'mock'  →  MockInput()        # 자동조작
```
coordinator.py는 factory만 호출한다. Real인지 Mock인지 모른다.
config만 바꾸면 동작이 바뀐다.

### config 분리 (dev / prod)
| 항목 | dev.yaml | prod.yaml |
|------|----------|-----------|
| display | mock (터미널 출력) | real (pygame 화면) |
| input | mock (자동조작) | real (키보드) |
| score | mock (로컬 출력) | real (NUC 전송) |

### docker 분리
| 파일 | 용도 |
|------|------|
| docker-compose.dev.yml | 개발 PC에서 pygame 없이 헤드리스 실행 |
| docker-compose.prod.yml | Orin / NUC 각각 서비스로 분리해서 배포 |

### ROS2 토픽 인터페이스
| 토픽 | 방향 | 타입 | 내용 |
|------|------|------|------|
| `/game/score` | Orin → NUC | `std_msgs/Int32` | 게임 종료 시 최종 점수 |
| `/game/status` | NUC → Orin | `std_msgs/String` | `"received"` / `"error"` |

### 상태 머신 전환 규칙
1. dev로 로직 검증
| 현재 상태 | 이벤트 | 다음 상태 |
|----------|--------|----------|
| IDLE | 게임 시작 | PLAYING |
| PLAYING | ESC 키 | PAUSED |
| PAUSED | 재개 | PLAYING |
| PLAYING | 목숨 0 | GAME_OVER |
| PLAYING | 블록 전부 제거 | CLEAR |
| GAME_OVER / CLEAR | 재시작 | IDLE |

---

## TODO

### 1단계 — 전체 구조 설계
- [x] 파일 구조 확정
- [x] ROS2 토픽 인터페이스 확정
- [x] 상태 머신 전환 규칙 확정
- [x] configs/dev.yaml 초안 작성
- [x] configs/prod.yaml 초안 작성

### 2단계 — 환경 연결 확인
- [x] pygame 설치 및 화면 출력 확인 (prod 모드로 직접 플레이)
- [x] ROS2 환경 확인 (ROS2 Humble, Python 3.10)

### 3단계 — 통신 확인
- [x] `/game/score` Orin 발행 → NUC 수신 end-to-end 확인
  - 터미널 2개로 로컬 테스트 완료 (NUC 역할 / Orin 역할)
  - coordinator 게임 종료 시 자동 발행 연동 완료

### 4단계 — 개별 모듈 구현
- [x] `orin/game/engine.py` — 게임 로직
- [x] `orin/game/input.py` — 키보드 입력
- [x] `orin/game/mock_input.py` — 자동조작
- [x] `orin/game/factory.py`
- [x] `orin/display/screen.py` — pygame 렌더링
- [x] `orin/display/mock_screen.py` — 헤드리스 출력
- [x] `orin/display/factory.py`
- [x] `orin/state_machine/fsm.py`
- [x] `orin/core/coordinator.py` (ROS2 발행 연동 포함)
- [x] `ros2_ws/` 노드 구현 (orin_pub, nuc_sub, orin_sub, nuc_pub)

### 5단계 — 통합 테스트 및 배포
- [x] dev 모드 로컬 실행 확인
- [x] dev 모드 docker 실행 확인 (docker-compose.dev.yml)
- [x] prod 모드 pygame 화면 확인 (직접 플레이)
- [x] prod 모드 ROS2 점수 전송 확인
- [x] `scripts/deploy_orin.sh`, `scripts/deploy_nuc.sh` 작성 및 실행 권한 부여
- [ ] Orin/NUC 실물 배포 (SSH 연결 후 스크립트 실행)

> **prod docker 방향 결정:**
> Orin은 헤드리스 운용 → docker-compose.dev.yml을 배포용으로 사용
> CONFIG_PATH=configs/prod.yaml 로 실행하면 ROS2 점수 전송 활성화됨

### 실물 배포 전 체크리스트
- [ ] Orin에 Docker 설치 (`sudo apt install docker.io docker-compose-v2`)
- [ ] NUC에 ROS2 Humble 설치 확인 (`/opt/ros/humble` 존재 여부)
- [ ] SSH 키 설정 (`ssh-copy-id` 로 비밀번호 없이 접속)
- [ ] Orin/NUC IP 확정 후 스크립트 실행

---

## 배운 점

### dev / prod 분리
1. dev로 로직 검증
2. prod로 실제 환경 연결
- 문제를 분리해서 디버깅 가능 (dev에서 로직 버그를 잡고 나면, prod에서 이상할 때 로직 문제는 아니고 연결 문제라는걸 특정할 수 있음)

### factory 패턴
- coordinator는 Real/Mock을 몰라도 됨
- config만 바꾸면 동작이 바뀜 → 코드 수정 없이 환경 전환 가능

### docker
- 환경을 이미지로 고정 → 어느 머신에서든 동일하게 실행
- Orin은 헤드리스 → docker-compose.dev.yml을 배포용으로 재사용 가능
- prod docker (X11 화면) 는 Orin 헤드리스 구조상 불필요

### ROS2 통신
- 같은 PC 터미널 2개로 Orin/NUC 통신 구조 검증 가능
- Python 버전 주의: ROS2 Humble은 Python 3.10 기준 → conda 환경과 충돌
- conda deactivate 후 시스템 Python으로 실행해야 rclpy 동작