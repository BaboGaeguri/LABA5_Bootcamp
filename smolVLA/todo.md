# smolVLA Orin 환경 개선 TODO

> 작성일: 2026-04-23
> 범위: Orin(JetPack 6.2.2) 상에서 lerobot smolVLA 실행 환경 점검
> 근거: 관련 공식 문서·실측 기록·현재 설치 스크립트 교차 분석

---

## 배경

현재 Orin 환경은 **실행 동작 확인** 상태. 초기에는 "PyTorch 버전이 불필요하게 낮다"고 판단했으나,
NVIDIA 공식 JP 6.2 배포가 **컨테이너 전용**으로 전환된 점과 우리 개발/배포 방식이 겹치면서
**현재의 JP 6.0 wheel 이식 전략이 오히려 합리적**이라는 재평가가 나옴. 아래 §1 참고.

---

## 1. PyTorch 버전 경로 재평가 — 현재 유지로 확정 권장

### 현재 상태

- 설치된 wheel: `torch 2.5.0a0+872d972e41.nv24.08` (JP 6.0용)
- 설치 경로: `developer.download.nvidia.com/compute/redist/jp/v61/pytorch/`
- 근거: [orin/scripts/setup_env.sh:58](orin/scripts/setup_env.sh#L58),
  [docs/storage/05_env_setting.md:55-67](docs/storage/05_env_setting.md#L55-L67)

### NVIDIA 공식 호환 매트릭스

[docs/reference/nvidia_official/Install-PyTorch-Jetson-Platform-Release-Notes.md:38-66](docs/reference/nvidia_official/Install-PyTorch-Jetson-Platform-Release-Notes.md#L38-L66)

| PyTorch | **Container** | **Wheel** | JetPack |
|---|---|---|---|
| 2.8.0a0 | **25.06 / 25.05** ✅ | **— (공급 안 함)** | 6.2 |
| 2.7.0a0 | **25.02–25.04** ✅ | **— (공급 안 함)** | 6.2 |
| 2.5.0a0+b465a5843b | 24.09 | **24.09** ✅ | 6.1 |
| **2.5.0a0+872d972e41** | 24.08 | **— (공급 안 함)** | **6.0** ← 현재 이식 사용 중 |
| 2.4.0a0 | 24.05–24.07 | **24.05–24.07** ✅ | 6.0 |

**JP 6.2 행은 Wheel 컬럼이 전부 `-`, Container 컬럼만 채워짐 = NVIDIA의 JP 6.2 공식 배포 = Docker 컨테이너.**

### 왜 컨테이너 경로를 선택하지 않는가 — 6가지 복잡도

우리 개발 환경은 네이티브 venv + lerobot editable + SO-ARM UART + USB 카메라 조합이며,
컨테이너로 전환하면 아래 문제가 한꺼번에 발생함.

1. **L4T 버전 mismatch**
   - JP 6.2 PyTorch 컨테이너(`25.02`–`25.06`)는 **L4T R36.4 기반** 빌드
   - 우리 Orin은 **L4T R36.5.0 / JetPack 6.2.2** ([docs/storage/03_software.md:21](docs/storage/03_software.md#L21))
   - 드라이버 minor 차이로 CUDA/cuDNN/TensorRT mismatch 경고 및 일부 기능 오동작 가능

2. **하드웨어 통과(passthrough) 복잡도**
   - SO-ARM 제어를 위해 컨테이너에서 호스트 장치 접근 필요:
     - `/dev/ttyACM*` (Feetech 서보 USB 시리얼 2개: 리더·팔로워)
     - `/dev/video*` (카메라)
     - `/dev/bus/usb/*` (RealSense/Orbbec 사용 시)
   - `--device=` 단순 나열로는 USB hotplug 대응 불가 → `--privileged` 또는 `/dev` 바인드
     마운트 필요. udev 이벤트 전파·보안 면에서 venv보다 훨씬 번거로움

3. **GPU/그래픽 스택 추가 설정**
   - `nvidia-container-toolkit` 또는 `--runtime nvidia` 설정
   - Jetson 컨테이너는 `/etc/nvidia-container-runtime/host-files-for-container.d/`의
     CSV 목록을 통해 호스트 라이브러리를 바인드 마운트 — JP 6.2.2 경로와 컨테이너 base의
     `/usr/lib/aarch64-linux-gnu` 기대 경로가 다르면 `libnvinfer.so.x` 로드 실패

4. **lerobot editable 설치와의 충돌**
   - 현재 `pip install -e ${SMOLVLA_DIR}[smolvla,hardware,feetech]` ([orin/scripts/setup_env.sh:49](orin/scripts/setup_env.sh#L49))로
     호스트 `~/smolvla/`를 editable 참조
   - 컨테이너 전환 시 소스 디렉토리 bind mount, 컨테이너 내부 Python path 동기화, editable
     재설치 필요 → 코드 수정/컨테이너 재시작 루프로 개발 속도 저하

5. **디스크/메모리 비용**
   - `l4t-pytorch` 이미지는 **10–20GB** 수준
   - Orin NVMe는 256GB급 ([docs/storage/02_hardware.md:37](docs/storage/02_hardware.md#L37)) —
     SmolVLM 체크포인트·데이터셋과 경쟁
   - Unified Memory 환경에서 컨테이너 오버헤드가 추론 지연에 직접 영향

6. **배포 스크립트와의 충돌**
   - `deploy_orin.sh`는 호스트 파일시스템(`~/smolvla/`) 대상 rsync 구조 ([README.md:85-90](README.md#L85-L90))
   - 컨테이너 전환 시 배포 방식을 이미지 빌드/푸시/풀로 재설계 필요

### NVIDIA의 결정적 경고

[Release Notes L30](docs/reference/nvidia_official/Install-PyTorch-Jetson-Platform-Release-Notes.md#L30):
> **26.03 release (Note)**: NVIDIA will **no longer produce** the standalone iGPU containers starting from this release.

NVIDIA 자체도 **2026-03부터 Jetson용 standalone iGPU 컨테이너 생산 중단**. 지금 시점에
컨테이너 기반으로 전환하는 것은 **수명이 짧은 선택**.

### 선택지 전체 비교

| 경로 | PyTorch | 배포 방식 | 우리 환경 적합성 |
|---|---|---|---|
| NVIDIA 공식 JP 6.2 | 2.7 / 2.8 | **컨테이너 only** | ❌ SO-ARM hotplug·editable dev·rsync 배포와 충돌, 2026-03 생산 중단 |
| NVIDIA JP 6.1 nv24.09 | 2.5.0a0+b465a5843b | wheel | ⚠️ JP 6.1용 — JP 6.2.2에서 cusparselt 이슈 동일하게 발생 |
| **NVIDIA JP 6.0 nv24.08 (현재)** | **2.5.0a0+872d972e41** | **wheel** | ✅ **동작 검증 완료** |
| **Seeed SharePoint JP 6.1 & 6.2 (L4T R36.4)** | **2.7 / 2.5** (JP 6.2 재빌드) | **wheel** | 🔍 **미시도** — 같은 2.5라도 JP 6.2용 빌드면 cusparselt 이슈 해소 가능성. [Seeed 가이드](docs/reference/reComputer-Jetson-for-Beginners/3-Basic-Tools-and-Getting-Started/3.5-Pytorch/README.md#L50-L63) L50-63 공식 제시 |
| Jetson AI Lab `jp6/cu126` | 2.8–2.11 | wheel | ❌ libcudss/libcusparseLt 결손 ([docs/storage/05_env_setting.md:46-49](docs/storage/05_env_setting.md#L46-L49)) |
| 소스 컴파일 | 2.7 / 2.8 | 자체 빌드 wheel | ⚠️ 6–12시간 빌드, 유지보수 부담, smolVLA가 2.7+ 전용 기능 필요할 때만 정당화 |

### 결론 및 할 일

**현재 JP 6.0 wheel 경로를 의도적 선택으로 확정.** 단, 선택 근거를 문서에 남겨야 함.

- [ ] [orin/scripts/setup_env.sh:7-10](orin/scripts/setup_env.sh#L7-L10) 주석 정정
  - 현재: "JP 6.2부터 NVIDIA 공식 standalone wheel 공급 중단"
  - 수정: "JP 6.2 공식 배포는 컨테이너 전용. 네이티브 venv + SO-ARM UART hotplug +
    lerobot editable dev 조합과 맞지 않아 **JP 6.0 wheel(nv24.08, cu12.6 forward-compatible)을
    의도적으로 선택**. 2026-03부터 NVIDIA도 iGPU 컨테이너 생산 중단 예정"
- [ ] [docs/storage/05_env_setting.md](docs/storage/05_env_setting.md)에 본 §1의
  선택 근거 요약 추가 (컨테이너 회피 6가지 이유 + NVIDIA 컨테이너 단종 예정)
- [ ] smolVLA가 PyTorch 2.7+ 전용 기능(예: torch.compile 신규 기능, FlashAttention 3 등)에
  의존하지 않는지 확인. 의존 시에만 소스 컴파일 경로 재검토
- [ ] **Seeed SharePoint 재빌드 wheel 시도 가치 평가**
  - JP 6.2용 2.5 wheel을 받아 파일명·빌드 태그 확인 (R36.4 빌드 여부 / cusparselt 번들 여부)
  - R36.4 기반 재빌드면 현재의 `v61/nv24.08` (JP 6.0 R36.2) 이식보다 **플랫폼 버전 격차 적음**
  - 2.7로 업그레이드 가능 여부까지 함께 검증 (smolVLA extras 호환성 체크 필요)
  - 결정 기준: **cusparselt LD 패치 없이 동작하면 교체**, 그렇지 않으면 현 상태 유지
- [ ] (장기) NVIDIA의 2026-03 이후 Jetson PyTorch 배포 방식 변경 공지 모니터링

---

## 2. 설치 방식이 NVIDIA 공식 문서와 다름

### 공식 설치 절차

**NVIDIA 공식 문서**
[docs/reference/nvidia_official/Install-PyTorch-Jetson-Platform.md:76-107](docs/reference/nvidia_official/Install-PyTorch-Jetson-Platform.md#L76-L107)

1. `sudo apt-get install libopenblas-dev` (현재 스크립트엔 없음)
2. 24.06 이상 wheel 설치 시 **cusparselt를 시스템에 먼저 설치** (옵션 A — 스크립트):
   ```bash
   wget raw.githubusercontent.com/pytorch/pytorch/.../install_cusparselt.sh
   export CUDA_VERSION=12.6
   bash ./install_cusparselt.sh
   ```
3. `numpy==1.26.x` 고정 후 torch 설치

**Seeed 가이드 권장** (옵션 B — NVIDIA deb local 패키지)

[Seeed 가이드 L58](docs/reference/reComputer-Jetson-for-Beginners/3-Basic-Tools-and-Getting-Started/3.5-Pytorch/README.md#L58)은 `ImportError: libcusparseLt.so.0` 발생 시 다음을 설치하라고 제시:

- **cuSPARSELt 0.8.1 (aarch64-jetson / Ubuntu 22.04 / deb Local)**: https://developer.nvidia.com/cusparselt-downloads
- **CUDA 12.6 deb local (aarch64-jetson / Ubuntu 22.04)**: https://developer.nvidia.com/cuda-12-6-0-download-archive

**두 옵션 비교:**

| 옵션 | 장점 | 단점 |
|---|---|---|
| A. `install_cusparselt.sh` | 자동화, `setup_env.sh`에 통합 용이 | 스크립트 URL이 PyTorch repo commit에 고정됨 |
| B. NVIDIA deb local | **공식 배포 경로, 재현성 높음, apt 관리** | 사전 다운로드 필요 |

→ **Orin 단일 장비에선 옵션 B(deb) 권장**. 이미지 자동화/CI에선 옵션 A.

### 현재 setup_env.sh

[orin/scripts/setup_env.sh:51-74](orin/scripts/setup_env.sh#L51-L74)

- ❌ `libopenblas-dev`, `libopenmpi-dev`, `libomp-dev` 사전 설치 없음
- ❌ cusparselt **시스템 설치 없음**
- 🔁 대안으로 venv activate에 `LD_LIBRARY_PATH` 추가하여 pip 번들
  (`nvidia/cusparselt/lib`) 경로로 우회
- ✅ numpy `<2` 고정은 반영됨

### 우회 방식(LD_LIBRARY_PATH)의 리스크

- venv 바깥의 터미널/프로세스에서 실행 시 `libcusparseLt.so.0 not found`
- `nvidia-cusparselt-cu12` pip 패키지 메이저 버전 변경 시 경로 깨짐
- systemd 서비스·외부 launcher에서 라이브러리 로드 실패 가능

### 할 일

- [ ] `sudo apt install libopenblas-dev libopenmpi-dev libomp-dev` 추가
- [ ] cusparselt 시스템 설치 — **옵션 B (NVIDIA deb local) 우선 시도**
  - NVIDIA cuSPARSELt 0.8.1 deb(aarch64-jetson, Ubuntu 22.04) 다운로드 후 `sudo dpkg -i` 로 설치
  - 실패 시 옵션 A (`install_cusparselt.sh` 스크립트)로 fallback
- [ ] `setup_env.sh`의 `LD_LIBRARY_PATH` 패치 블록 제거 및 주석 갱신
- [ ] 검증: venv activate 없이 `python -c "import torch; torch.cuda.FloatTensor(2).zero_()"` 성공 확인
  (단순 import가 아니라 **실제 cuda 텐서 생성 까지** 통과해야 cusparselt lazy load 이슈 조기 발견)

---

## 3. torchvision을 완전히 포기하지 않아도 됐음

### 현재 판단

[docs/storage/05_env_setting.md:26](docs/storage/05_env_setting.md#L26)

> `torchvision: 미설치 — Orin 호환 버전 없음 (smolVLA 추론 경로에서 미사용)`

### 반박 근거

- **Seeed / NVIDIA 양쪽 모두 torchvision wheel을 제공**
  - JP 6.1 & 6.2: torchvision **0.22.0** (Seeed SharePoint)
  - JP 6.0: torchvision **0.20** (Seeed SharePoint, 필요 시 소스 빌드)
  - 근거: [docs/reference/seeedwiki/seeedwiki_so101.md:54](docs/reference/seeedwiki/seeedwiki_so101.md#L54),
    [docs/reference/reComputer-Jetson-for-Beginners/3-Basic-Tools-and-Getting-Started/3.5-Pytorch/README.md:50-62](docs/reference/reComputer-Jetson-for-Beginners/3-Basic-Tools-and-Getting-Started/3.5-Pytorch/README.md#L50-L62)
- 즉 **"Orin 호환 없음"이 아니라 "우리가 설치를 안 함"**이 정확.

### 실제 코드에서의 torchvision 사용처

| 파일 | 용도 | smolVLA 추론 영향 |
|---|---|---|
| [orin/lerobot/policies/smolvla/smolvlm_with_expert.py:46-47](orin/lerobot/policies/smolvla/smolvlm_with_expert.py#L46-L47) | SmolVLM `AutoProcessor`의 video processor가 torchvision 요구 → `_TokenizerOnlyProcessor`로 우회 중 | **있음 (우회 코드 존재)** |
| [orin/lerobot/processor/hil_processor.py:25](orin/lerobot/processor/hil_processor.py#L25) | `torchvision.transforms.functional` 직접 import | HIL 학습 경로, 추론엔 미사용 |
| [orin/lerobot/scripts/lerobot_imgtransform_viz.py](orin/lerobot/scripts/lerobot_imgtransform_viz.py) | 데이터 증강 시각화 | 추론엔 미사용 |

### torchvision 설치 시 효과

1. SmolVLM 공식 `AutoProcessor`를 그대로 사용 가능 → `_TokenizerOnlyProcessor` 우회 클래스 제거
2. Seeed 튜토리얼의 데이터 기록/시각화 명령(`lerobot-record`, `lerobot-dataset-viz`) Orin에서 직접 동작
3. `hil_processor` 경로가 필요해져도 import 에러 없음
4. upstream lerobot과의 diff 감소 → 유지보수 부담 ↓

### 할 일

- [ ] PyTorch 버전 확정 후 매칭되는 torchvision 선택 (2.5 → 0.20, 2.7 → 0.22)
- [ ] Seeed SharePoint wheel 또는 소스 컴파일 경로 중 택일
- [ ] 설치 후 `_TokenizerOnlyProcessor` 우회 코드 제거 가능 여부 검증
- [ ] 제거 시 [docs/storage/lerobot_upstream_check/03_orin_lerobot_diff.md](docs/storage/lerobot_upstream_check/03_orin_lerobot_diff.md)에
  변경 이력 추가

---

## 4. 기타 정리 항목

### 4-1. nvcc PATH 미등록

- 근거: [docs/storage/03_software.md:23](docs/storage/03_software.md#L23)
  > `nvcc: PATH에 미탐지 (패키지로 설치됨, SDK 12.6.11)`
- Seeed 가이드 검증 절차 [3.5-Pytorch/README.md:34](docs/reference/reComputer-Jetson-for-Beginners/3-Basic-Tools-and-Getting-Started/3.5-Pytorch/README.md#L34)의
  `nvcc -V` 명령이 그대로 통과되지 않음
- 할 일:
  - [ ] `/usr/local/cuda/bin`을 `~/.bashrc` PATH에 등록
  - [ ] `/usr/local/cuda/lib64`를 `LD_LIBRARY_PATH`에 등록 (필요 시)

### 4-2. DGX Spark 쪽 미설치 (기존 open TODO)

[docs/storage/03_software.md:66-88](docs/storage/03_software.md#L66-L88)

- PyTorch, cuDNN, TensorRT, conda, Docker 모두 미설치
- 학습 서버로 사용하려면 최소한 PyTorch + cuDNN은 필요
- 할 일:
  - [ ] DGX cuDNN / TensorRT 설치 필요 여부 확정
  - [ ] 학습 PC(DGX) ↔ Orin 간 모델 반입/실행 절차 확정
  - [ ] 외장 SSD 사용 시 데이터셋/체크포인트 경로 확정

---

## 5. 설치 검증 스크립트 강화

### 현재 검증 수준

[orin/scripts/setup_env.sh:78-82](orin/scripts/setup_env.sh#L78-L82):

```bash
python -c "import torch; print(torch.__version__)"
python -c "import torch; print(torch.cuda.is_available())"
```

### 문제점

- `torch.__version__`과 `torch.cuda.is_available()`은 **GPU 연산 능력을 보장하지 않음**
- `libcusparseLt.so.0`는 **lazy load** — 실제 tensor 연산 시점에야 로드됨
- 현재 검증은 통과하고 smolVLA 실행 시 `libcusparseLt not found` 가 터지는 시나리오 가능

### Seeed 가이드의 검증 절차

[3.5-Pytorch/README.md:107-120](docs/reference/reComputer-Jetson-for-Beginners/3-Basic-Tools-and-Getting-Started/3.5-Pytorch/README.md#L107-L120):

```python
import torch
print(torch.__version__)
print('CUDA available: ' + str(torch.cuda.is_available()))
print('cuDNN version: ' + str(torch.backends.cudnn.version()))
a = torch.cuda.FloatTensor(2).zero_()      # 실제 cuda 텐서 할당
print('Tensor a = ' + str(a))
b = torch.randn(2).cuda()                  # CPU→GPU 복사
print('Tensor b = ' + str(b))
c = a + b                                  # cuda 연산
print('Tensor c = ' + str(c))
```

**할당 + 복사 + 연산** 3단계를 모두 실행해야 cusparselt·cuDNN 로드까지 검증됨.

### 할 일

- [ ] `setup_env.sh` 마지막에 Seeed 스타일 실제 연산 검증 블록 추가
  - `torch.cuda.FloatTensor(2).zero_()` — cusparselt lazy load 트리거
  - `torch.randn(2).cuda()` — CPU→GPU 메모리 전송
  - `a + b` — GEMM 수준 연산 (cuDNN 로드 유도는 아니지만 기본 커널 동작 확인)
- [ ] 검증 실패 시 `set -e`로 스크립트 중단되도록 구성
- [ ] (선택) cuDNN 검증용으로 `torch.backends.cudnn.version()` 추가 호출
- [ ] 이 검증이 통과해야 §2의 "cusparselt LD 패치 제거" 작업 결과를 신뢰할 수 있음 — §2와 묶어서 진행

---

## 잘 된 부분 (변경 불필요)

- Python 3.10 (cp310 wheel에 정확히 일치)
- numpy `<2.0.0` 고정 (torch 2.5.0a0 NumPy 1.x ABI 요건)
- venv 구조 (conda env 폐기 결정 타당)
- [orin/pyproject.toml](orin/pyproject.toml)에서 torch/torchvision을 의존성에서 빼고
  setup_env.sh에서 직접 설치 (pip CPU-only wheel 덮어쓰기 방지)
- `-e [smolvla,hardware,feetech]` extras 구성

---

## 우선순위 요약

| # | 조치 | 대응 §   | 예상 효과 | 위험도 |
|---|---|---|---|---|
| 1 | setup_env.sh 주석 정정 + 05_env_setting.md에 JP 6.0 wheel 선택 근거 기록 | §1 | 판단 근거 보존, 다음 담당자에 맥락 전달 | 없음 |
| 2 | **Seeed SharePoint JP 6.2용 2.5/2.7 wheel 시도** (파일명 확인 → cusparselt 번들 여부 판단) | §1 | cusparselt LD 패치 제거 + 플랫폼 버전 격차 축소 가능성 | 낮음 (조사 우선) |
| 3 | `libopenblas-dev / libopenmpi-dev / libomp-dev` 설치 | §2 | 공식 가이드 준수 | 낮음 |
| 4 | cusparselt 시스템 설치 (NVIDIA deb local 우선) → LD 패치 제거 | §2 | 표준 설치, 외부 런처 호환, cusparselt lazy load 안정화 | 중간 |
| 5 | 검증 스크립트 강화 (실제 cuda 텐서 연산) | §5 | cusparselt/cuDNN 로드 조기 검증, §4와 묶어 진행 | 낮음 |
| 6 | torchvision 설치 검토 → `_TokenizerOnlyProcessor` 제거 | §3 | upstream diff 감소, Seeed 튜토리얼 명령 동작 | 낮음 (Orin 데이터 수집 수행 시에만) |
| 7 | `nvcc` PATH 등록 | §4-1 | 진단 용이 | 낮음 |
| 8 | DGX 학습 스택 설치 전략 확정 | §4-2 | 학습 파이프라인 가동 | 중간 |

---

## 가장 먼저 할 한 가지

§1 재평가 결과에 따라 NVIDIA v62 URL 조사는 불필요. 대신 두 축으로 움직임:

**축 1 — 선택 근거 문서화 (빠른 승리)**
- [ ] [orin/scripts/setup_env.sh](orin/scripts/setup_env.sh) 상단 주석 정정 (§1 결론 참조)
- [ ] [docs/storage/05_env_setting.md](docs/storage/05_env_setting.md)에 "JP 6.0 wheel 의도적 선택" 배경 추가

**축 2 — Seeed SharePoint wheel 조사 (새로 발견된 경로)**
- [ ] Seeed 가이드 [3.5-Pytorch/README.md L50-L63](docs/reference/reComputer-Jetson-for-Beginners/3-Basic-Tools-and-Getting-Started/3.5-Pytorch/README.md#L50-L63)의
  JP 6.2용 2.5 / 2.7 wheel을 받아 파일명·빌드 태그 확인 (R36.4 재빌드 여부)
- [ ] 테스트 venv에 설치 → cusparselt LD 패치 없이 `torch.cuda.FloatTensor(2).zero_()` 통과 여부 확인
- [ ] 통과 시 §1 표의 "현재 사용 중" 행을 교체 후보로 승격

---

## 부록 A. 자주 올라온 설계 질문과 답변 (2026-04-23)

세 가지 환경 선택에 대한 검증. 각 항목은 **결정 + 근거 + 조치** 구조.

### A-1. PyTorch 버전을 올려도 Python 3.10 고정인가?

**답: 그렇다. Python 3.10 고정은 PyTorch 버전과 무관한 플랫폼 제약.**

근거:

1. **JetPack 6.x 시스템 Python이 3.10**
   - Ubuntu 22.04 기반 → 기본 파이썬 3.10
   - [orin/scripts/setup_env.sh:17-22](orin/scripts/setup_env.sh#L17-L22) — venv 생성 시
     `python3.10` 우선 선택

2. **NVIDIA 공식 JP 6.x용 PyTorch wheel은 전부 `cp310`만 제공**
   - 현재 wheel 파일명: `torch-2.5.0a0+872d972e41.nv24.08.17622132-cp310-cp310-linux_aarch64.whl`
   - JP 6.0 / 6.1 / 6.2 대응 wheel 모두 cp310 (파일명의 `cp310-cp310` 부분)
   - Seeed 가이드 [3.5-Pytorch/README.md:69-70](docs/reference/reComputer-Jetson-for-Beginners/3-Basic-Tools-and-Getting-Started/3.5-Pytorch/README.md#L69-L70)도
     `torch-2.3.0-cp310-cp310-linux_aarch64.whl` 명시

3. **PyTorch 버전을 올려도 JP 6.x + cp310 조합은 유지**
   - JP 6.2 컨테이너 경로(2.7/2.8) — 컨테이너 내부 Python도 3.10
   - Python 3.11/3.12로 가려면 **JetPack 7.x로 OS 전체 재설치** 필요
     (JP 7.x는 L4T R38 기반 — 하드웨어 지원 매트릭스 상이)

4. **Seeed 튜토리얼도 Python 3.10 명시**
   - [so101.md:72](docs/reference/seeedwiki/seeedwiki_so101.md#L72) — `conda create -y -n lerobot python=3.10`
   - [so101.md:66-67](docs/reference/seeedwiki/seeedwiki_so101.md#L66-L67) — "Jetson Orin: Python 3.10"

결론:
- ✅ Python 3.10 사용은 **lerobot 제약이 아니라 JetPack 6.x 플랫폼 제약**
- PyTorch 버전과 Python 버전은 **독립적인 두 축**
- 3.11/3.12 사용은 현 시점 권장 안 함 (JP 7.x 전환은 별도 과제)

조치:
- [ ] 현재 Python 3.10 유지. 추가 작업 없음
- [ ] (장기) JetPack 7.x 전환 시 Python 버전 정책 재검토

---

### A-2. 학습을 DGX에서 한다면 Orin에 torchvision이 정말 필요 없는가?

**답: "순수 추론 전용"이면 지금 판단 유지 가능하나, 사실은 torchvision이 추론 경로에서 필요하며
현재는 우회 코드로 대체 중임을 문서에 명시해야 한다.**

Orin 내 torchvision 사용처 (실측):

| 파일 | 경로 | 추론 필수? | 현재 처리 |
|---|---|---|---|
| [orin/lerobot/policies/smolvla/smolvlm_with_expert.py:46-47](orin/lerobot/policies/smolvla/smolvlm_with_expert.py#L46-L47) | SmolVLM `AutoProcessor`의 video processor가 torchvision 요구 | ✅ **추론 핵심** | `_TokenizerOnlyProcessor` 우회 클래스 사용 |
| [orin/lerobot/processor/hil_processor.py:25](orin/lerobot/processor/hil_processor.py#L25) | `torchvision.transforms.functional` | ❌ HIL 학습 전용 | Orin에서 미사용 |
| [orin/lerobot/scripts/lerobot_imgtransform_viz.py](orin/lerobot/scripts/lerobot_imgtransform_viz.py) | 이미지 증강 시각화 | ❌ 학습/디버깅 | Orin에서 미사용 |

핵심: **`_TokenizerOnlyProcessor`의 존재 자체가 "torchvision이 smolVLA 추론 경로에서 필요하다"는 증거**.
우리가 우회 클래스를 만들어 회피하고 있을 뿐.

```python
# smolvlm_with_expert.py:41-51
class _TokenizerOnlyProcessor:
    """AutoProcessor 대신 tokenizer만 로드하는 최소 래퍼.
    ...
    AutoProcessor는 video_processing_smolvlm을 통해 torchvision을 요구하므로,
    Orin(torchvision 미지원) 환경에서는 tokenizer만 로드해 우회한다.
    """
```

양측 관점:

**"미설치 유지" 측**
- 학습은 DGX에서 → `hil_processor`, `lerobot_imgtransform_viz` 미사용
- 추론은 `_TokenizerOnlyProcessor`로 정상 동작
- aarch64 torchvision wheel 탐색/설치 추가 작업 회피

**"설치 권장" 측**
- upstream lerobot과의 diff 감소 → 우회 클래스 제거 가능 →
  [docs/storage/lerobot_upstream_check/03_orin_lerobot_diff.md](docs/storage/lerobot_upstream_check/03_orin_lerobot_diff.md)
  유지보수 부담 ↓
- SmolVLM upstream 업데이트 대응 — 향후 video processor가 다른 기능
  (비디오 전처리, 프레임 샘플링 등) 추가 시 우회 클래스로 감당 불가
- Seeed 튜토리얼의 `lerobot-record`, `lerobot-dataset-viz` 명령이 Orin에서 직접 동작
  (Orin에서 데이터 수집할 경우 필요)
- 설치 난이도 낮음 — Seeed SharePoint에 JP 6.0/6.1/6.2용 wheel 제공
  ([so101.md:54-60](docs/reference/seeedwiki/seeedwiki_so101.md#L54-L60))

결정 기준:

| 질문 | Yes | No |
|---|---|---|
| Orin에서 **데이터 수집**(teleop 녹화) 수행? | 설치 권장 | 설치 불요 |
| SmolVLM upstream 업데이트를 꾸준히 따라갈 것? | 설치 권장 | 설치 불요 |

현재 답변: **학습 DGX / Orin은 추론 전용** 전제로 "미설치" 유지 가능. 단, 문서 표현 정정 필요.

조치:
- [ ] [docs/storage/05_env_setting.md:26](docs/storage/05_env_setting.md#L26) 표현 수정
  - 현재: `torchvision: 미설치 — "Orin 호환 버전 없음"`
  - 수정: `torchvision: 미설치 — "우회 구현(_TokenizerOnlyProcessor)으로 회피 중,
    Seeed SharePoint에 JP 6.x용 wheel 존재하나 추론 전용 환경이므로 설치 보류"`
- [ ] Orin에서 데이터 수집을 수행하기로 결정되면 §A-2 재검토 후 torchvision 설치
- [ ] 설치 결정 시 `_TokenizerOnlyProcessor` 제거 및
  [docs/storage/lerobot_upstream_check/03_orin_lerobot_diff.md](docs/storage/lerobot_upstream_check/03_orin_lerobot_diff.md)
  변경 이력 추가

---

### A-3. venv 사용이 잘못되었는가? Seeed는 conda를 권장하는데?

**답: 틀리지 않았다. 우리 환경에서는 venv가 더 적합하다.**

Seeed가 conda를 쓰는 실제 이유:

[so101.md:69-75, 80-90](docs/reference/seeedwiki/seeedwiki_so101.md#L69-L90)
```bash
conda create -y -n lerobot python=3.10
conda install ffmpeg -c conda-forge
conda install -y -c conda-forge "opencv>=4.10.0.84"
```

- `ffmpeg=7.1.1`을 pip로 설치하기 어려움 → conda-forge의 prebuilt binary 사용
- aarch64용 `opencv>=4.10.0.84`를 conda-forge에서 한 번에 확보하기 위함

우리가 venv로 갈 수 있던 이유:

1. **opencv는 pip wheel로 해결**
   - [orin/pyproject.toml:15](orin/pyproject.toml#L15): `opencv-python-headless>=4.9.0,<4.14.0`
   - PyPI의 aarch64 manylinux wheel 정상 설치

2. **ffmpeg Python 바인딩 불필요**
   - Orin은 추론 전용 → 비디오 인코딩/디코딩은 학습/기록 시점 작업
   - ffmpeg CLI만 필요하며 JetPack이 시스템 패키지로 제공

3. **NVIDIA 공식 PyTorch wheel은 pip 기반 설치 전제**
   - [Install-PyTorch-Jetson-Platform.md:104-107](docs/reference/nvidia_official/Install-PyTorch-Jetson-Platform.md#L104-L107):
     `python3 -m pip install --no-cache $TORCH_INSTALL`
   - pip이 공식 경로이며, conda는 선택적 wrapper

4. **Jetson 상 conda의 단점**
   - conda-forge aarch64 채널의 패키지 커버리지가 불완전 (특히 NVIDIA 쪽)
   - conda env의 Python이 시스템 Python과 분리되어 **JetPack 번들 라이브러리
     호출 시 경로 이슈** 발생 가능
   - Miniconda 자체가 수백 MB → Orin NVMe 공간 비용
   - conda + pip 혼용 시 의존성 충돌 (ffmpeg가 대표적 사례)

프로젝트 내 선행 검증:

[docs/storage/05_env_setting.md:12-14](docs/storage/05_env_setting.md#L12-L14)
> "conda env 방식은 폐기. setup_env.sh가 생성하는 venv를 사용."

devPC에 conda `lerobot` env가 이미 있음
([docs/storage/03_software.md:46-48](docs/storage/03_software.md#L46-L48))에도 불구하고
Orin에선 venv를 새로 만든 결정 — 위 4번 단점이 실제 경험으로 축적됨.

결론:
- ✅ venv 선택 타당. Seeed의 conda 절차는 "처음 접하는 사용자에게 ffmpeg/opencv 설치
  허들을 낮추기 위한 간편 경로"이며, 기술적 우위 때문이 아님
- 우리는 NVIDIA 공식 pip 설치 경로 + opencv-headless wheel로 충분 → venv가 자연스러움

조치:
- [ ] Orin에 `ffmpeg` 시스템 패키지 설치 여부 확인 (`ffmpeg -version`). 없으면
  `sudo apt install ffmpeg`
- [ ] Seeed의 `pip install 'Cython<3'` 사전 설치는 **torchvision 소스 컴파일 시에만
  필요** — torchvision 미설치 방침이면 건너뛰어도 무방
- [ ] venv 방침을 [docs/storage/05_env_setting.md](docs/storage/05_env_setting.md) 상단
  "개요" 섹션에 근거와 함께 명시 (Seeed conda 권장에 대한 해명 포함)

이 결과에 따라 1번 항목의 실행 여부가 결정됨.
