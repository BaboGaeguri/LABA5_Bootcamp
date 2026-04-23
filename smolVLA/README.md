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
├── .github/
│   └── copilot-instructions.md         # GitHub Copilot 컨텍스트
├── docs/
│   ├── repository/                      # lerobot 코드 구조 분석 문서
│   ├── reference/                       # 외부 참조 문서 + 읽기 전용 서브모듈
│   │   ├── lerobot/                     # HuggingFace lerobot upstream submodule
│   │   ├── reComputer-Jetson-for-Beginners/ # Seeed Jetson beginner reference submodule
│   │   ├── reference.md
│   │   └── so101.md
│   └── storage/                         # 환경/장비 기록 문서
│       ├── 01_smolvla_arm_env_requirements.md   # 요구사항 + 문서 네비게이션
│       ├── 02_hardware.md
│       ├── 03_software.md
│       ├── 04_devnetwork.md
│       ├── 05_env_setting.md
│       ├── devices_snapshot/            # 장치 점검 스크립트 + 수집 결과
│       │   ├── collect_snapshot.sh
│       │   ├── run_snapshots.sh
│       │   └── *_snapshot_*.txt
│       └── lerobot_upstream_check/      # lerobot upstream 추적 및 충돌 점검
│           ├── 01_compatibility_check.md
│           ├── 99_lerobot_upstream_Tracking.md
│           └── check_update_diff.sh
└── orin/                                # Jetson Orin 배포 패키지
    ├── pyproject.toml                   # Orin용 (torch>=2.5, Python>=3.10, smolvla extras)
    ├── lerobot/                         # curated 추론 필수 모듈
    │   ├── cameras/{opencv,realsense,zmq}
    │   ├── configs/
    │   ├── envs/
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

---

## lerobot 업데이트 워크플로우

lerobot upstream이 업데이트되면 아래 순서로 진행합니다.

**0. 의존성 충돌 사전 점검**

`docs/storage/lerobot_upstream_check/check_update_diff.sh` 로 변경 내용을 확인한 후,
`docs/storage/lerobot_upstream_check/01_compatibility_check.md` 에 점검 결과를 기록합니다.

주요 확인 항목: Python 3.12 전용 문법 추가 여부, pyproject.toml 의존성 범위 변경, 신규 패키지의 aarch64/cp310 빌드 존재 여부.

**1. submodule pull**

```bash
git submodule update --remote smolVLA/docs/reference/lerobot
```

**2. orin/lerobot/ 수동 갱신**

`smolVLA/docs/reference/lerobot/src/lerobot/` 에서 필요한 파일을 `smolVLA/orin/lerobot/` 로 직접 복사합니다.  
(자동 동기화 스크립트는 제거됨 — 필요 시 재작성)

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
| `docs/reference/lerobot/` | upstream submodule (수정 금지) |
| `docs/reference/reComputer-Jetson-for-Beginners/` | Seeed Jetson beginner reference submodule |
| `orin/` | Orin 배포 패키지 — curated lerobot + 예제 + 설치 스크립트 |
| `deploy_orin.sh` | orin/ → Orin rsync (devPC에서 실행) |
| `docs/storage/` | 환경/장비 실측 기록 문서 |
| `docs/reference/` | 외부 참조 PDF/MD + 읽기 전용 참고 서브모듈 |
| `arm_2week_plan.md` | 2주 실행 계획, 마일스톤 |

---

## `docs/storage/` 문서 역할

| 파일 | 역할 |
|---|---|
| `01_smolvla_arm_env_requirements.md` | 요구사항 정의 + 하위 문서 네비게이션 |
| `02_hardware.md` | 하드웨어 실측값 (devPC / Orin / DGX Spark / SO-ARM BOM) |
| `03_software.md` | 소프트웨어 실측값 (OS, JetPack, CUDA, 패키지 버전) |
| `04_devnetwork.md` | devPC ↔ Orin ↔ DGX Spark 네트워크/SSH 연결 설정 |
| `05_env_setting.md` | Orin lerobot 환경 세팅 기록 (conda env, PyTorch 설치 방식) |

### `devices_snapshot/`

| 파일 | 역할 |
|---|---|
| `collect_snapshot.sh` | Orin/DGX 환경 정보 수집 payload (원격 실행용) |
| `run_snapshots.sh` | 두 디바이스 동시 수집 후 `devices_snapshot/` 저장 |
| `*_snapshot_*.txt` | 수집된 스냅샷 결과 |

### `lerobot_upstream_check/`

| 파일 | 역할 |
|---|---|
| `check_update_diff.sh` | upstream 업데이트 비교 스크립트 (`HEAD@{1} -> HEAD`) |
| `01_compatibility_check.md` | 의존성 충돌 점검 기록 (Python 버전, 신규 문법, 패키지 변경) |
| `02_orin_pyproject_diff.md` | upstream vs orin/pyproject.toml 변경 이력 누적 기록 |
| `03_orin_lerobot_diff.md` | upstream vs orin/lerobot/ 코드 변경 이력 누적 기록 |
| `99_lerobot_upstream_Tracking.md` | lerobot 동기화 이력 누적 기록 |

---

## AI 어시스턴트 컨텍스트 파일

| 파일 | 대상 도구 |
|---|---|
| `CLAUDE.md` | Claude Code |
| `.github/copilot-instructions.md` | GitHub Copilot |

---

## 참고

- 장치 스냅샷 수집: `bash docs/storage/devices_snapshot/run_snapshots.sh` (SSH alias `orin` / `dgx` 필요)
- upstream 변경 비교: `bash docs/storage/lerobot_upstream_check/check_update_diff.sh`
- PyTorch 설치 경로 (Orin): `https://pypi.jetson-ai-lab.io/jp6/cu126` (torch 2.11.0, cp310, cu126)
- 구조가 변경되면 이 README도 함께 갱신합니다.
