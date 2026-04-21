# smolVLA 디렉토리 가이드

`LABA5_Bootcamp/smolVLA` 하위 구조와 문서 역할을 정리한 안내 파일입니다.

## 디렉토리 구조

```text
smolVLA/
├── CLAUDE.md                            # Claude Code 자동 참조 컨텍스트
├── README.md
├── arm_2week_plan.md                    # 2주 실행 계획 및 마일스톤
├── dev-connect.sh                       # VS Code Remote SSH로 Orin/DGX 동시 연결
├── .github/
│   └── copilot-instructions.md         # GitHub Copilot 컨텍스트
├── docs/
│   ├── repository/                      # lerobot 코드 구조 분석 문서
│   │   ├── lerobot_repo_overview.md
│   │   ├── lerobot_root_structure.md
│   │   └── lerobot_src_structure.md
│   └── storage/                         # 환경/장비 기록 문서 및 스냅샷 스크립트
│       ├── 01_smolvla_arm_env_requirements.md
│       ├── 02_hardware.md
│       ├── 03_software.md
│       ├── 04_devnetwork.md
│       ├── collect_snapshot.sh          # 원격 디바이스에서 실행되는 수집 payload
│       ├── run_snapshots.sh             # 로컬에서 Orin/DGX 동시 수집 실행
│       └── devices_snapshot/            # 디바이스별 스냅샷 로그 누적
│           ├── orin_env_snapshot_*.txt
│           └── dgx_spark_env_snapshot_*.txt
├── soarm/                               # 커스터마이징 대상 코드 (lerobot 기반)
│   ├── pyproject.toml
│   ├── examples/
│   │   └── tutorial/smolvla/
│   │       └── using_smolvla_example.py
│   └── lerobot/
│       ├── cameras/                     # OpenCV / RealSense / ZMQ 카메라
│       ├── common/                      # 학습/제어 공통 유틸
│       ├── configs/                     # 학습·평가 설정
│       ├── datasets/                    # LeRobot 데이터셋 I/O
│       ├── motors/                      # Feetech / Dynamixel 드라이버
│       ├── policies/
│       │   └── smolvla/                 # SmolVLA 모델 (modeling / processor / config)
│       ├── processor/                   # 관측·행동 전처리 파이프라인
│       ├── robots/
│       │   └── so_follower/             # SO-101 follower 로봇 인터페이스
│       ├── scripts/                     # 텔레옵 / 녹화 / 평가 실행 스크립트
│       │   ├── lerobot_teleoperate.py
│       │   ├── lerobot_record.py
│       │   └── lerobot_eval.py
│       ├── teleoperators/
│       │   ├── so_leader/               # SO-101 leader 텔레오퍼레이터
│       │   └── keyboard/
│       └── utils/
└── src/                                 # (미사용, 예약)
```

## 폴더별 용도

- `arm_2week_plan.md`: 2주 실행 계획, 고려사항 결론, 마일스톤
- `docs/repository/`: lerobot 레포 구조 분석 문서
- `docs/storage/`: 환경/장비 실측 기록 문서 및 스냅샷 수집 스크립트
- `soarm/`: SO-ARM 타겟 커스터마이징 코드 (lerobot 기반)

## `docs/storage/` 문서 역할 분리

| 파일 | 역할 |
|---|---|
| `01_smolvla_arm_env_requirements.md` | 요구사항 정의 (What is required) |
| `02_hardware.md` | 하드웨어 실측값 (devPC / Orin / DGX Spark / SO-ARM BOM) |
| `03_software.md` | 소프트웨어 실측값 (OS, CUDA, conda env, 패키지 버전) |
| `04_devnetwork.md` | devPC ↔ Orin ↔ DGX Spark WiFi SSH 연결 설정 |
| `collect_snapshot.sh` | Orin/DGX 자동 감지 후 환경 정보 수집 (원격 실행용 payload) |
| `run_snapshots.sh` | 로컬에서 SSH로 두 디바이스 동시 수집 후 `devices_snapshot/`에 저장 |

## AI 어시스턴트 컨텍스트 파일

| 파일 | 대상 도구 |
|---|---|
| `CLAUDE.md` | Claude Code |
| `.github/copilot-instructions.md` | GitHub Copilot |

## 참고

- 디바이스 스냅샷은 `docs/storage/devices_snapshot/`에 누적합니다.
- 스냅샷 수집: `bash docs/storage/run_snapshots.sh` (SSH alias `orin` / `dgx` 필요)
- 구조가 변경되면 이 README도 함께 갱신합니다.
