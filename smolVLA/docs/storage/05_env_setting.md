## 05. Environment Setting Notes

이 문서는 `lerobot/pyproject.toml`(upstream)과 `orin/pyproject.toml`(Orin 배포용)의 의존성 정책 차이를 정리한다.

### 목적

- `lerobot/pyproject.toml`: upstream 기본 정책. 다양한 기능/플랫폼을 포괄하는 범용 의존성 집합.
- `orin/pyproject.toml`: Jetson Orin 실행 안정성을 우선한 배포 정책. 실제 추론/하드웨어 제어에 필요한 범위로 축소.

### 핵심 차이

| 항목 | `lerobot/pyproject.toml` | `orin/pyproject.toml` | 운영상 의미 |
|---|---|---|---|
| Python 기준 | `>=3.12` | `>=3.10` | Orin 기본 Python(3.10) 환경을 직접 지원하기 위한 차이 |
| PyTorch 범위 | `torch>=2.7,<2.11.0` | `torch>=2.5` | Orin에서는 JetPack/NVIDIA wheel 호환성이 우선 |
| TorchVision 범위 | `torchvision>=0.22.0,<0.26.0` | `torchvision>=0.20.0` | ARM64/JetPack 조합에서 설치 가능성 확보 |
| optional extras 범위 | dataset/training/sim/dev 포함 폭넓음 | `smolvla`, `hardware`, `feetech`, `zmq` 중심 | Orin 실행에 필요한 기능 위주로 최소화 |
| 플랫폼 예외 처리 | 일부 패키지에 플랫폼 marker 포함(예: 특정 환경에서 `torchcodec` 제외) | marker보다 curated 의존성 축소를 우선 | 설치 실패 가능성이 높은 경로를 사전 차단 |

### 왜 분리 관리가 필요한가

- Orin은 `aarch64`(ARM64) + JetPack(CUDA/cuDNN 묶음) 환경이므로, 개발 PC(`x86_64`) 기준 의존성을 그대로 적용하면 설치/실행 실패 가능성이 높다.
- upstream의 범용 의존성은 기능 커버리지가 넓은 대신 Orin 현장 실행에는 과할 수 있다.
- `orin/pyproject.toml`은 "실행 가능성"과 "재현성"을 우선해 의존성을 조정한 파일이다.

### 운영 원칙

- Orin 배포/실행은 `orin/pyproject.toml`을 기준으로 본다.
- upstream 동기화 시 코드는 `sync_lerobot.sh`로 맞추되, 의존성 정책은 Orin 기준을 유지하며 검증한다.
- 의존성 이슈가 발생하면 먼저 "upstream 범위 문제"인지 "Orin 정책 문제"인지 분리해서 진단한다.

### Upstream Tracking Log

upstream 변화를 점검할 때 아래 항목을 누적 기록한다.

| Date (KST) | lerobot commit | Describe | Recent cadence (30/90/180d) | Impact note | Action |
|---|---|---|---|---|---|
| 2026-04-22 | `ba27aab79c731a6b503b2dbdd4c601e78e285048` | `v0.5.1-42-gba27aab7` | `70 / 185 / 314` | upstream 변경 빈도 높음. Orin 의존성 drift 리스크 존재 | `orin/pyproject.toml` 기준 유지, 다음 동기화 시 설치/실행 재검증 |

#### Snapshot Notes (2026-04-22)

- Latest commit subject: `fix(robotwin): pin compatible curobo in benchmark image (#3427)`
- Current smolVLA pointer state: `-ba27aab79c731a6b503b2dbdd4c601e78e285048 lerobot`
- 해석: `-` 접두는 submodule이 현재 워킹트리에서 미초기화/불일치 상태일 수 있음을 의미하므로, 실제 동기화 작업 전 상태 확인이 필요하다.

