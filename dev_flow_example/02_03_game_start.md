# 블록 깨기 게임 — 실물 배포 시작 프로세스

> 목적: Dev PC에서 Orin/NUC에 게임을 빌드·배포하고 실행하기까지의 과정을 단계별로 기록한다.
> 전제: `02_96_start_process.md` 완료 (Dev PC → Orin/NUC SSH 연결 성공)

---

## 환경 정보

| 장비 | SSH 유저 | IP | 역할 |
|------|---------|-----|------|
| Dev PC | `babogaeguri` | `172.16.139.236` | 코드 작성 / 배포 실행 |
| Orin | `laba` | `172.16.128.97` | 게임 로직 + 렌더링 + ROS2 발행 |
| NUC | `laba` | `10.42.0.221` (DHCP) | 점수 서버 + ROS2 수신 |

> NUC 접속은 Orin 경유 점프: `ssh -J laba@172.16.128.97 laba@10.42.0.221`

---

## Step 0. Preflight Check

배포 전 환경 점검 스크립트 실행.

```bash
[Dev PC] cd ~/ros2_ws/src/LABA5_Bootcamp/dev_flow_example
[Dev PC] ./scripts/preflight_check.sh 172.16.128.97 10.42.0.221
```

> NUC ping WARN은 정상. NUC는 Orin 뒤에 있어 직접 ping 불가.

---

## Step 1. Orin — Docker 설치

> Orin은 게임을 Docker 컨테이너 안에서 실행한다.

설치 확인:

```bash
[Orin] docker --version
# Docker version 29.3.1, build c2be9cc
[Orin] docker compose version
# Docker Compose version v5.1.1
```

→ 이미 설치되어 있음. 별도 설치 불필요.

---

## Step 2. NUC — ROS2 Humble + colcon 확인

> NUC는 ROS2로 점수 토픽을 수신한다.

설치 확인:

```bash
[NUC] ros2 --help | head -3
# → ros2 명령 정상 동작 확인

[NUC] ls /opt/ros/
# humble

[NUC] colcon --version
# colcon: command not found → 설치 필요
```

colcon 설치:

```bash
[NUC] sudo apt install -y python3-colcon-common-extensions
```

→ ROS2 Humble 기설치, colcon 신규 설치 완료.

---

## Step 3. 게임 배포 — Orin

```bash
[Dev PC] ./scripts/deploy_orin.sh 172.16.128.97
```

결과:
- 코드 rsync 완료
- Docker 이미지 빌드 완료 (`breakout-game:latest`)
- 게임 실행 → `GAME OVER score=30` 확인
- **ROS2 발행 실패: `No module named 'rclpy'`**

**원인:** Docker 컨테이너(`python:3.11-slim`) 안에 ROS2가 없음.
Orin 호스트에는 ROS2 Humble이 설치되어 있으나 컨테이너는 호스트 환경을 격리함.

```
Orin 컴퓨터
├── 호스트: ROS2 Humble 설치됨
└── Docker 컨테이너: python:3.11-slim (ROS2 없음) ← 여기서 실행 중
```

---

## Step 3-A. ROS2 문제 해결 — 방법 A: 호스트에서 직접 실행 ✅

> Docker 없이 Orin 호스트에서 직접 coordinator.py 실행.
> 호스트에 ROS2가 있으므로 rclpy 사용 가능.

```bash
[Orin] source /opt/ros/humble/setup.bash
[Orin] cd ~/breakout
[Orin] pip install -r requirements.txt
[Orin] PYTHONPATH=/home/laba/breakout:$PYTHONPATH CONFIG_PATH=configs/prod.yaml python3 orin/core/coordinator.py
```

> `PYTHONPATH`에 `/home/laba/breakout`를 추가해야 `orin` 모듈을 찾을 수 있다.
> `PYTHONPATH=...` 단독으로 쓰면 ROS2 경로가 날아가므로 반드시 `:$PYTHONPATH`로 이어붙일 것.

장점: 간단, ROS2 바로 사용 가능
단점: 의존성이 호스트에 직접 설치됨 (환경 오염 가능)

### 실제 키보드 + 화면으로 플레이

Orin에 모니터가 연결되어 있는 경우 DISPLAY 번호 확인:

```bash
[Orin] ls /tmp/.X11-unix/
# X1 → DISPLAY=:1
```

실행:

```bash
[Orin] DISPLAY=:1 PYTHONPATH=/home/laba/breakout:$PYTHONPATH CONFIG_PATH=configs/prod.yaml python3 orin/core/coordinator.py
```

→ pygame 화면 + 실제 키보드(← →)로 게임 플레이 성공 ✅

---

## Step 3-B. ROS2 문제 해결 — 방법 B: Dockerfile에 ROS2 추가

> 컨테이너 안에 ROS2를 포함시켜 격리 환경 유지.

Dockerfile 수정 — `python:3.11-slim` 대신 ROS2 공식 이미지 베이스 사용:

```dockerfile
FROM ros:humble

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-rclpy \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY orin/ ./orin/
COPY configs/ ./configs/

CMD ["python3", "orin/core/coordinator.py"]
```

재빌드:

```bash
[Dev PC] ./scripts/deploy_orin.sh 172.16.128.97
```

장점: 환경 완전 격리, 어디서든 동일하게 실행
단점: 이미지 크기 증가, 빌드 시간 길어짐

---

## Step 4. NUC 배포 및 실행

```bash
[Dev PC] ./scripts/deploy_nuc.sh 10.42.0.221
```

`deploy_nuc.sh`는 코드 복사 → colcon 빌드 → `nuc_sub` 실행까지 자동으로 진행한다.
Dev PC 터미널에 NUC에서 실행 중인 로그가 출력된다.

NUC 터미널에서 직접 확인하고 싶을 때:

```bash
[NUC] source /opt/ros/humble/setup.bash
[NUC] cd ~/breakout/ros2_ws
[NUC] source install/setup.bash
[NUC] ros2 run breakout_bridge_pkg nuc_sub
```

---

## Step 5. 동작 확인 ✅

**실행 순서:**

1. NUC에서 `nuc_sub` 대기 시작 (Step 4)
2. Orin에서 게임 실행 (Step 3-A)
3. 게임 종료 시 Orin이 `/game/score` 토픽 발행
4. NUC가 수신 후 로그 출력

**확인된 로그:**

```
[Orin] [orin_pub]: Orin publisher ready
[Orin] [orin_pub]: [Orin] score 발행: 30

[NUC]  [nuc_sub]: NUC subscriber ready — /game/score 대기 중...
[NUC]  [nuc_sub]: [NUC] 점수 수신: 30
```

→ Orin ↔ NUC ROS2 통신 end-to-end 성공 ✅

---

## 주의사항

- NUC IP(`10.42.0.221`)는 DHCP라 재부팅 시 바뀔 수 있다.
  재접속 전 Orin에서 확인: `ip neigh show dev eno1`
