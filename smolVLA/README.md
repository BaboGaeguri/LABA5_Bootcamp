# smolVLA 디렉토리 가이드

`LABA5_Bootcamp/smolVLA` 하위 구조와 문서 역할을 정리한 안내 파일입니다.

## 디렉토리 구조

```text
smolVLA/
├── CLAUDE.md                            # Claude Code 자동 참조 컨텍스트
├── README.md
├── arm_2week_plan.md                    # 2주 실행 계획 및 마일스톤
├── dev-connect.sh                       # VS Code Remote SSH로 Orin/DGX 동시 연결
├── deploy_orin.sh                       # devPC → Orin rsync 배포
├── sync_lerobot.sh                      # lerobot submodule → orin/lerobot/ 동기화
├── .github/
│   └── copilot-instructions.md         # GitHub Copilot 컨텍스트
├── docs/
│   ├── repository/                      # lerobot 코드 구조 분석 문서
│   └── storage/                         # 환경/장비 기록 문서 및 스냅샷 스크립트
│       ├── 01_smolvla_arm_env_requirements.md
│       ├── 02_hardware.md
│       ├── 03_software.md
│       ├── 04_devnetwork.md
│       ├── collect_snapshot.sh
│       ├── run_snapshots.sh
│       └── devices_snapshot/
├── lerobot/                             # ⚠️ upstream submodule — 절대 수정 금지
│                                        #   (huggingface/lerobot 원본)
└── orin/                                # Jetson Orin 배포 패키지
    ├── pyproject.toml                   # Orin용 (torch>=2.5, smolvla extras)
    ├── lerobot/                         # curated 추론 필수 모듈 (110 files)
    │   ├── cameras/{opencv,realsense,zmq}
    │   ├── configs/
    │   ├── envs/                        # 추론 필요 최소본
    │   ├── model/
    │   ├── motors/feetech/
    │   ├── optim/
    │   ├── policies/{smolvla,rtc}/
    │   ├── processor/
    │   ├── robots/so_follower/
    │   ├── scripts/{lerobot_eval,lerobot_teleoperate}
    │   ├── teleoperators/so_leader/
    │   └── utils/
    ├── examples/
    │   └── tutorial/smolvla/
    │       └── using_smolvla_example.py
    └── scripts/
        └── setup_env.sh                 # Orin에서 실행 — venv + pip install
```

## lerobot 업데이트 워크플로우

lerobot upstream이 업데이트되면 아래 순서로 진행합니다.

**1. submodule pull**

```bash
git submodule update --remote smolVLA/lerobot
```

**2. orin/ curated 재동기화**

```bash
./smolVLA/sync_lerobot.sh
```

`smolVLA/lerobot/src/lerobot/` 에서 추론 필수 파일만 `smolVLA/orin/lerobot/` 로 복사합니다.

**3. Orin에 배포**

```bash
./smolVLA/deploy_orin.sh
```

`smolVLA/orin/` 전체를 Orin의 `~/smolvla/` 로 rsync 합니다.

**4. Orin에서 환경 재설치 (의존성이 바뀐 경우)**

```bash
ssh orin
rm -rf ~/smolvla/.venv
bash ~/smolvla/scripts/setup_env.sh
```

---

## Orin 최초 설치

```bash
# devPC
./smolVLA/deploy_orin.sh

# Orin
ssh orin
bash ~/smolvla/scripts/setup_env.sh
source ~/smolvla/.venv/bin/activate
```

---

## 폴더별 용도

| 폴더/파일 | 용도 |
|---|---|
| `lerobot/` | upstream submodule (수정 금지) |
| `orin/` | Orin 배포 패키지 — curated lerobot + 예제 + 설치 스크립트 |
| `sync_lerobot.sh` | lerobot 업데이트 후 orin/ 갱신 (devPC에서 실행) |
| `deploy_orin.sh` | orin/ → Orin rsync (devPC에서 실행) |
| `docs/storage/` | 환경/장비 실측 기록 및 스냅샷 수집 스크립트 |
| `arm_2week_plan.md` | 2주 실행 계획, 마일스톤 |

## `docs/storage/` 문서 역할 분리

| 파일 | 역할 |
|---|---|
| `01_smolvla_arm_env_requirements.md` | 요구사항 정의 |
| `02_hardware.md` | 하드웨어 실측값 (devPC / Orin / DGX Spark / SO-ARM BOM) |
| `03_software.md` | 소프트웨어 실측값 (OS, CUDA, 패키지 버전) |
| `04_devnetwork.md` | devPC ↔ Orin ↔ DGX Spark WiFi SSH 연결 설정 |
| `collect_snapshot.sh` | Orin/DGX 환경 정보 수집 payload (원격 실행용) |
| `run_snapshots.sh` | 두 디바이스 동시 수집 후 `devices_snapshot/` 저장 |

## AI 어시스턴트 컨텍스트 파일

| 파일 | 대상 도구 |
|---|---|
| `CLAUDE.md` | Claude Code |
| `.github/copilot-instructions.md` | GitHub Copilot |

## 참고

- 디바이스 스냅샷은 `docs/storage/devices_snapshot/`에 누적합니다.
- 스냅샷 수집: `bash docs/storage/run_snapshots.sh` (SSH alias `orin` / `dgx` 필요)
- 구조가 변경되면 이 README도 함께 갱신합니다.