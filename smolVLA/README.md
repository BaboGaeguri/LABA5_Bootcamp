# smolVLA 디렉토리 가이드

`LABA5_Bootcamp/smolVLA` 하위 구조와 문서 역할을 정리한 안내 파일입니다.

## 디렉토리 구조

```text
smolVLA/
├── README.md
├── arm_2week_plan.md
├── repository/
│   ├── lerobot_repo_overview.md
│   ├── lerobot_root_structure.md
│   └── lerobot_src_structure.md
├── soarm/
│   ├── pyproject.toml
│   ├── examples/
│   │   └── tutorial/smolvla/using_smolvla_example.py
│   └── lerobot/
│       ├── cameras/
│       ├── common/
│       ├── configs/
│       ├── datasets/
│       ├── motors/
│       ├── policies/
│       ├── processor/
│       ├── robots/
│       ├── scripts/
│       ├── teleoperators/
│       ├── utils/
│       ├── __init__.py
│       ├── __version__.py
│       └── types.py
├── src/
└── storage/
    ├── smolvla_arm_env_requirements.md
    ├── hardware.md
    ├── software.md
    ├── orin_env_snapshot_2026-04-21_1316.txt
    └── orin_storage_snapshot_2026-04-21_1323.txt
```

## 폴더별 용도

- `arm_2week_plan.md`: 2주 실행 계획 문서
- `repository/`: lerobot 코드 구조 분석 문서
- `soarm/`: 실제 커스터마이징 대상 코드(lerobot 기반)
- `src/`: 추가 소스 작업용 폴더(현재 구조상 비중 낮음)
- `storage/`: 환경/장비 기록 문서 및 스냅샷 로그

## `storage/` 문서 역할 분리

- `smolvla_arm_env_requirements.md`: 요구사항 정의 문서
- `hardware.md`: 현재 보유 하드웨어/실측값
- `software.md`: 현재 소프트웨어 설정/실측값

## 참고

- Orin/스토리지 실측 로그는 `storage/orin_*_snapshot_*.txt`에 누적합니다.
- 구조가 변경되면 이 README도 함께 갱신합니다.
