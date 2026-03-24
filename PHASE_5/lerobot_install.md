# LeRobot 설치 가이드 (Ubuntu 22.04 / 24.04 x86) — 텔레오퍼레이션용

## Ubuntu 버전 호환성

| 환경 | 판단 | 비고 |
|---|---|---|
| 네이티브 Ubuntu 22.04 | ✅ 정상 | Seeed 가이드 기준 환경 |
| 네이티브 Ubuntu 24.04 | ✅ 공식 지원 | LeRobot 공식 팀 개발 환경 |
| WSL2 + Ubuntu 24.04 | ⚠️ 주의 | evdev 빌드 이슈 가능 (아래 참고) |

> LeRobot 공식 GitHub의 `requirements.in` 주석에 `requirements-ubuntu.txt`가 **Ubuntu 24.04.4 LTS x86_64** 기준으로 생성되었다고 명시되어 있음. Seeed 가이드가 22.04 기준이지만 실제 동작에는 영향 없음.

### WSL2 + Ubuntu 24.04 환경에서 evdev 빌드 실패 시

```bash
# 방법 1: 커널 헤더 설치
sudo apt-get install linux-headers-$(uname -r)

# 방법 2: evdev-binary 패키지 사용
pip install evdev-binary
```

### 빌드 오류 발생 시 추가 패키지

```bash
sudo apt-get install cmake build-essential python3-dev pkg-config \
  libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev \
  libswscale-dev libswresample-dev libavfilter-dev
```

---

---

## 1단계. Miniconda 설치

```bash
mkdir -p ~/miniconda3
cd ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
source ~/miniconda3/bin/activate
conda init --all
```

> `conda init --all` 실행 후 **터미널을 재시작**해야 conda가 정상 활성화됨.

---

## 2단계. LeRobot용 conda 환경 생성 및 활성화

### Anaconda Terms of Service 동의 (최초 1회)

`conda create` 실행 시 아래 오류가 발생하면 ToS에 먼저 동의해야 함:

```
CondaToSNonInteractiveError: Terms of Service have not been accepted...
```

```bash
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
```

### 환경 생성

```bash
conda create -y -n lerobot python=3.10
conda activate lerobot
```

---

## 3단계. LeRobot 소스코드 클론

```bash
git clone https://github.com/Seeed-Projects/lerobot.git ~/lerobot
```

---

## 4단계. ffmpeg 설치 (텔레오퍼레이션 시 불필요)

> **ffmpeg란?** 영상 인코딩/디코딩 라이브러리로, LeRobot에서 데이터셋 녹화 및 영상 저장 시 사용됨.
> 텔레오퍼레이션만 진행할 경우 이 단계는 **생략 가능**.

```bash
conda install ffmpeg -c conda-forge
```

### 문제 발생 시 — libsvtav1 인코더 지원 확인

```bash
ffmpeg -encoders | grep svt
```

지원 안 될 경우 버전 명시해서 설치:

```bash
conda install ffmpeg=7.1.1 -c conda-forge
```

---

## 5단계. LeRobot + feetech 모터 의존성 설치
이 작업이 생각보다 오래걸림

```bash
cd ~/lerobot && pip install -e ".[feetech]"
```

---

## 6단계. PyTorch GPU 확인 (텔레오퍼레이션 시 불필요)

> GPU는 학습(training) 시에만 필요. 텔레오퍼레이션은 CPU만으로 충분하므로 **생략 가능**.

`pip install` 과정에서 CPU 버전 PyTorch로 교체될 수 있으므로 학습 시에는 반드시 확인:

```python
import torch
print(torch.cuda.is_available())
```

- `True` → 정상, GPU 사용 가능
- `False` → PyTorch GPU 버전 재설치 필요

### GPU 버전 재설치 (CUDA 버전에 맞게 공식 사이트 확인 후)

```bash
# 예시: CUDA 12.1 기준
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

> CUDA 버전 확인: `nvcc --version` 또는 `nvidia-smi`

---

## 설치 완료 체크리스트

| 단계 | 항목 | 확인 |
|---|---|---|
| 1 | Miniconda 설치 & 터미널 재시작 | ☐ |
| 2 | lerobot conda 환경 활성화 | ☐ |
| 3 | GitHub 클론 완료 | ☐ |
| 4 | ffmpeg 설치 완료 | ☐ |
| 5 | pip install 완료 | ☐ |
| 6 | `torch.cuda.is_available()` → True (텔레옵 시 불필요) | ☐ |

---

## 터미널 재시작 후 빠른 시작

터미널을 새로 열었을 때 아래 순서대로 실행:

```bash
# 1. 환경 활성화
conda activate lerobot
cd ~/lerobot

# 2. 포트 확인 (연결 순서에 따라 매번 바뀔 수 있음)
ls /dev/ttyACM*

# 3. 포트 권한 부여
sudo chmod 666 /dev/ttyACM0
sudo chmod 666 /dev/ttyACM1  # 두 드라이버 모두 연결된 경우
```

`(lerobot)` 프롬프트가 표시되면 준비 완료.

---

## 텔레오퍼레이션 (SO-ARM 101 Pro)

> 모터 설정 및 캘리브레이션은 **최초 1회만** 진행. 이후에는 텔레옵 실행 단계만 반복.

### 1단계. USB 포트 확인

리더/팔로워 드라이버 보드를 **둘 다 PC에 연결한 상태**에서 실행:

```bash
lerobot-find-port
```

> **포트 확인 방법:** 스크립트 실행 후 팔로워 드라이버 USB만 뽑고 Enter.
> 사라진 포트 = 팔로워, 나머지 = 리더.
>
> **주의:** 포트 번호(ttyACM0, ttyACM1)는 연결 순서에 따라 동적으로 할당되므로 매번 바뀔 수 있음. 항상 `lerobot-find-port` 또는 `ls /dev/ttyACM*`로 확인 후 진행.

> **주의:** 드라이버 보드는 전원 어댑터와 USB 케이블을 **둘 다** 연결해야 인식됨.

포트 접근 권한 부여:

```bash
sudo chmod 666 /dev/ttyACM0
sudo chmod 666 /dev/ttyACM1
```

### 2단계. 모터 ID 설정 (최초 1회)

> **전원 전압 주의 (중요!)**
> - 팔로워 암 **Pro 버전** (ST-3215-C047/C018): **12V 전원**
> - 팔로워 암 **Kit 버전** (ST-3215-C001): **5V 전원**
> - 리더 암 (ST-3215-C044/C046/C001, 7.4V 모터): **항상 5V 전원**
>
> 전압이 틀리면 모터를 찾지 못하거나 모터가 손상될 수 있음!

> **연결 방법:** 모터를 **한 개씩** 드라이버 보드에 연결해서 설정. 데이지체인 연결 상태에서는 진행 불가.

**팔로워 암:**
```bash
lerobot-setup-motors \
    --robot.type=so101_follower \
    --robot.port=/dev/ttyACM0
```

순서: gripper(6) → wrist_roll(5) → wrist_flex(4) → elbow_flex(3) → shoulder_lift(2) → shoulder_pan(1)

**리더 암:**
```bash
lerobot-setup-motors \
    --teleop.type=so101_leader \
    --teleop.port=/dev/ttyACM1
```

### 3단계. 캘리브레이션 (최초 1회)

**팔로워 암:**
```bash
lerobot-calibrate \
    --robot.type=so101_follower \
    --robot.port=/dev/ttyACM0 \
    --robot.id=my_follower
```

**리더 암:**
```bash
lerobot-calibrate \
    --teleop.type=so101_leader \
    --teleop.port=/dev/ttyACM1 \
    --teleop.id=my_leader
```

### 4단계. 텔레옵 실행

```bash
lerobot-teleoperate \
    --robot.type=so101_follower \
    --robot.port=/dev/ttyACM0 \
    --robot.id=my_follower \
    --teleop.type=so101_leader \
    --teleop.port=/dev/ttyACM1 \
    --teleop.id=my_leader
```

---

## 드라이버 재연결 후 텔레옵 재개 (빠른 실행)

> 모터 ID 설정과 캘리브레이션은 **최초 1회만** 하면 됨. 드라이버를 뽑았다 꽂아도 다시 할 필요 없음.
> 캘리브레이션 파일은 `~/.cache/huggingface/lerobot/calibration/` 에 영구 저장되어 있음.

### 1단계. 하드웨어 연결 확인

드라이버 보드 2개 모두:
- **전원 어댑터** 연결 (팔로워 Pro: 12V / 리더: 5V)
- **USB 케이블** PC에 연결

> 전원 어댑터 없이 USB만 연결하면 포트가 인식되지 않음.

### 2단계. 포트 식별

두 드라이버를 **모두 연결한 상태**에서:

```bash
conda activate lerobot
cd ~/lerobot

lerobot-find-port
```

실행 후 **팔로워 드라이버 USB만 뽑고** Enter → 사라진 포트가 팔로워, 남은 포트가 리더.

```
# 예시 출력
Ports before: ['/dev/ttyACM0', '/dev/ttyACM1']
Ports after:  ['/dev/ttyACM0']
→ 팔로워: /dev/ttyACM1, 리더: /dev/ttyACM0
```

> 포트 번호는 연결 순서에 따라 매번 바뀜. 반드시 매번 확인.

뽑았던 팔로워 USB를 다시 꽂은 후 진행.

### 3단계. 포트 권한 부여

```bash
sudo chmod 666 /dev/ttyACM0
sudo chmod 666 /dev/ttyACM1
```

### 4단계. 텔레옵 실행

아래 명령에서 `--robot.port`와 `--teleop.port`를 2단계에서 확인한 포트로 교체:

```bash
lerobot-teleoperate \
    --robot.type=so101_follower \
    --robot.port=/dev/ttyACM1 \
    --robot.id=my_follower \
    --teleop.type=so101_leader \
    --teleop.port=/dev/ttyACM0 \
    --teleop.id=my_leader
```

---

### 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| `ls /dev/ttyACM*` 아무것도 없음 | 전원 어댑터 미연결 | 전원 어댑터 확인 후 재연결 |
| `PermissionError` | 포트 권한 없음 | `sudo chmod 666 /dev/ttyACM*` |
| `Missing motor IDs` | 잘못된 포트에 연결 | `lerobot-find-port`로 포트 재확인 |
| 팔로워가 리더 움직임 안 따라옴 | 포트 반대로 입력 | `--robot.port`와 `--teleop.port` 교체 |