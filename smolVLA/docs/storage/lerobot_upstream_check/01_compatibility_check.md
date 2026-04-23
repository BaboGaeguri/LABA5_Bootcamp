# 01. lerobot 의존성 충돌 점검 기록

> 목적: lerobot upstream 업데이트 이후 Orin 환경(Python 3.10, CUDA 12.6)과의 의존성 충돌 가능성을 확인하고 기록한다.
> 관련 스크립트: `check_update_diff.sh`
> 추적 이력: `99_lerobot_upstream_Tracking.md`

---

## 점검 기준

Orin 환경 고정값 (변경 불가):

| 항목 | 값 | 제약 이유 |
|---|---|---|
| Python | `3.10` | Jetson AI Lab wheel(`jp6/cu126`)이 cp310만 제공 |
| CUDA | `12.6` | JetPack 6.2.2 고정 |
| arch | `aarch64` | Jetson Orin 하드웨어 |
| lerobot (Orin 설치) | `0.4.4` | editable, `/home/babogaeguri/lerobot` |

### Python 버전에 대한 공식 입장

| 항목 | 내용 |
|---|---|
| lerobot 공식 요구사항 | `requires-python = ">=3.12"` — Python 3.12 이상만 공식 지원 |
| Jetson 공식 지원 | [GitHub Issue #819](https://github.com/huggingface/lerobot/issues/819) "closed as not planned" — Jetson 지원 계획 없음 |
| Python 3.10 공식 근거 | **없음** — 커뮤니티 레벨 실사용 사례(lerobot 0.4.x)만 존재 |

**JetPack 버전을 낮추면 Python 3.12를 쓸 수 있을까?**

불가능. JetPack별 기본 Python 버전:
- JP 5.x → Python **3.8** (더 낮아짐)
- JP 6.x → Python **3.10** (현재)
- 어떤 JetPack에도 Python 3.12용 CUDA PyTorch wheel 없음

NVIDIA iGPU 컨테이너 방식도 26.03부터 공급 중단. ROS2 + 하드웨어 연동 복잡성 문제도 존재.

**결론: Python 3.10은 공식 지원이 아닌 하드웨어 제약으로 인한 유일한 경로이며, orin/ curated 환경에서 실제로 동작하는지는 직접 검증으로 확인한다.**

근거 자료:
- [lerobot pyproject.toml](https://github.com/huggingface/lerobot/blob/main/pyproject.toml)
- [lerobot Jetson support issue #819](https://github.com/huggingface/lerobot/issues/819)
- `docs/reference/Install-PyTorch-Jetson-Platform-Release-Notes.md` — JP별 wheel 공급 현황

---

## 점검 이력

### [2026-04-23] Python 3.12 전용 문법 사용 확인

**점검 대상 commit:** `ba27aab79c731a6b503b2dbdd4c601e78e285048` (v0.5.1-42)

**점검 항목 및 결과:**

| 기능 | 도입 버전 | 위험도 | 실제 사용 여부 | 비고 |
|---|---|---|---|---|
| `type` alias 문법 (`type X = ...`) | 3.12 | **높음** | **사용 중** | `motors/motors_bus.py:51-52` |
| `ExceptionGroup` / `except*` | 3.11 | 중간 | 미사용 | 코드 전체 검색 확인 |
| `tomllib` (stdlib) | 3.11 | 낮음 | 미사용 | 코드 전체 검색 확인 |
| `Self` type hint | 3.11 | 낮음 | 미사용 | 코드 전체 검색 확인 |
| `match` 문 | 3.10 | 없음 | — | 3.10에서 정상 동작 |
| `X \| Y` union 타입 힌트 | 3.10 | 없음 | — | 3.10에서 정상 동작 |

**상세: `type` alias 문법**

파일: `src/lerobot/motors/motors_bus.py`

```
type NameOrID = str | int   # line 51
type Value = int | float    # line 52
```

Python 3.10에서 이 파일을 import하면 즉시 `SyntaxError` 발생.

영향 경로:
```
motors_bus.py
  └── motors/__init__.py  (Motor, MotorCalibration, MotorNormMode import)
       ├── feetech/feetech.py       (NameOrID, Value import)
       ├── dynamixel/dynamixel.py   (NameOrID, Value import)
       ├── robots/robot.py          (MotorCalibration import)
       └── teleoperators/ 전체
```

**영향 범위 판단:**

| 기능 | 영향 |
|---|---|
| smolVLA policy 추론 (forward pass만) | 없음 — policy 코드는 `lerobot.motors` 미사용 |
| SO-ARM 모터 제어 (feetech) | **실행 불가** |
| 텔레옵 / 데이터 수집 | **실행 불가** |
| robot.py 기반 평가 루프 | **실행 불가** |

**결론:**
- 현재 Orin에 설치된 `lerobot 0.4.4`에는 이 문법이 없어 동작 중
- submodule 최신 commit(`ba27aab`)으로 동기화 시 Orin에서 실행 불가
- **동기화 전 이 파일의 해당 두 줄을 호환 문법으로 패치 필요**

대응 방안:
- `orin/` 레이어에서 `NameOrID = Union[str, int]` 형태로 재정의 래핑
- 또는 Orin의 editable install 경로에 직접 패치 (submodule 비변경)

---

## 향후 점검 체크리스트

upstream 동기화 전 아래 항목을 `check_update_diff.sh` 출력과 함께 확인한다.

- [ ] `pyproject.toml` `requires-python` 변경 여부
- [ ] `motors/motors_bus.py` 추가 3.12 문법 도입 여부
- [ ] `from __future__ import annotations` 미적용 파일에서 새 타입 힌트 추가 여부
- [ ] numpy, torch, torchvision 버전 범위 변경 → Orin wheel 호환성 재확인
- [ ] 신규 의존성 패키지 추가 → aarch64/cp310 빌드 존재 여부 확인
