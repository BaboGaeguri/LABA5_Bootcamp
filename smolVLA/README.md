# smolVLA 디렉토리 가이드

`LABA5_Bootcamp/smolVLA` 하위 구조와 문서 역할을 정리한 안내 파일입니다.

## 디렉토리 구조

```text
smolVLA/
├── CLAUDE.md                        # Claude Code 자동 참조 컨텍스트
├── README.md
├── arm_2week_plan.md                # 2주 실행 계획 및 마일스톤
├── .github/
│   └── copilot-instructions.md     # GitHub Copilot 컨텍스트
├── repository/                      # lerobot 코드 구조 분석 문서
│   ├── lerobot_repo_overview.md
│   ├── lerobot_root_structure.md
│   └── lerobot_src_structure.md
├── soarm/                           # 실제 커스터마이징 대상 코드 (lerobot 기반)
│   ├── pyproject.toml
│   ├── examples/
│   └── lerobot/
└── storage/                         # 환경/장비 기록 문서 및 스냅샷 로그
    ├── 01_smolvla_arm_env_requirements.md
    ├── 02_hardware.md
    ├── 03_software.md
    ├── 04_devnetwork.md
    └── orin_*_snapshot_*.txt
```

## 폴더별 용도

- `arm_2week_plan.md`: 2주 실행 계획, 고려사항 결론, 마일스톤
- `repository/`: lerobot 레포 구조 분석 문서
- `soarm/`: SO-ARM 타겟 커스터마이징 코드 (lerobot 기반)
- `storage/`: 환경/장비 실측 기록 문서 및 스냅샷 로그

## `storage/` 문서 역할 분리

| 파일 | 역할 |
|---|---|
| `01_smolvla_arm_env_requirements.md` | 요구사항 정의 (What is required) |
| `02_hardware.md` | 하드웨어 실측값 (devPC / Orin / DGX Spark / SO-ARM BOM) |
| `03_software.md` | 소프트웨어 실측값 (OS, CUDA, conda env, 패키지 버전) |
| `04_devnetwork.md` | devPC ↔ Orin ↔ DGX Spark WiFi SSH 연결 설정 |

## AI 어시스턴트 컨텍스트 파일

| 파일 | 대상 도구 |
|---|---|
| `CLAUDE.md` | Claude Code |
| `.github/copilot-instructions.md` | GitHub Copilot |

## 참고

- Orin/스토리지 실측 로그는 `storage/orin_*_snapshot_*.txt`에 누적합니다.
- 구조가 변경되면 이 README도 함께 갱신합니다.
