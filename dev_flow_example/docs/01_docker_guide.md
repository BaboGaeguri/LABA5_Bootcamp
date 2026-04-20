# Docker 가이드 — 블록 깨기 게임 기준

> 작성일: 2026.04.08
> 목적: docker로 게임 환경을 격리하고, 어느 머신에서든 동일하게 실행하기

---

## 핵심 개념

### 3가지만 알면 된다

| 개념 | 설명 | 비유 |
|------|------|------|
| **Image** | 환경의 스냅샷 (Python 버전, 라이브러리, 코드 전부 포함) | 설계도 |
| **Container** | Image를 실제로 실행한 것 | 설계도로 지은 집 |
| **Registry** | Image를 저장하고 공유하는 저장소 (Docker Hub) | GitHub |

### 전체 흐름

```
Dockerfile → (build) → Image → (push) → Registry → (pull) → Image → (run) → Container
  설계도              스냅샷           저장소              스냅샷            실행 환경
```

### Git과 비교

| | Git | Docker |
|--|-----|--------|
| 로컬 저장 | git commit | docker build |
| 원격 저장소 | GitHub | Docker Hub |
| 올리기 | git push | docker push |
| 받기 | git pull | docker pull |

---

## 설치

### Docker 설치 (Ubuntu 22.04)

```bash
sudo apt install docker.io
```

### sudo 없이 사용하기 위한 권한 설정

```bash
sudo usermod -aG docker $USER
# 터미널 재시작 후 적용
newgrp docker   # 재시작 없이 즉시 적용할 때
```

### docker-compose 플러그인 설치

```bash
sudo apt install docker-compose-v2
```

### 설치 확인

```bash
docker --version
```

---

## Dockerfile

Image를 어떻게 만들지 정의하는 파일. 프로젝트 루트(`dev_flow_example/`)에 위치.

```dockerfile
# 1. 베이스 이미지: Python 3.11 (슬림 버전)
FROM python:3.11-slim

# 2. 컨테이너 안에서 작업할 디렉토리 지정
WORKDIR /app

# 3. 의존성 먼저 설치 (코드보다 먼저 — 캐시 활용)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 게임 코드 복사
COPY orin/ ./orin/
COPY configs/ ./configs/

# 5. 기본 실행 명령
CMD ["python3", "-m", "orin.core.coordinator"]
```

**왜 requirements.txt를 코드보다 먼저 복사하나?**
Docker는 변경된 레이어부터 다시 빌드한다. 코드만 바꿨을 때 pip install을 다시 하지 않으려면 의존성을 먼저 설치해두는 게 유리하다.

---

## requirements.txt

컨테이너 안에 설치할 라이브러리 목록.

```
pyyaml==6.0.2
pygame==2.6.1
```

버전을 고정해두는 이유: 나중에 다른 머신(Orin 등)에서 빌드할 때도 동일한 버전이 설치되도록.

---

## 주요 명령어

### 이미지 빌드

```bash
docker build -t breakout-game .
# -t : 이미지 이름 지정
# .  : 현재 디렉토리의 Dockerfile 사용
```

### 컨테이너 직접 실행

```bash
docker run --rm -e CONFIG_PATH=configs/dev.yaml breakout-game
# --rm : 종료 후 컨테이너 자동 삭제
# -e   : 환경변수 주입 (CONFIG_PATH로 dev/prod 전환)
```

### 이미지 / 컨테이너 목록 확인

```bash
docker images       # 이미지 목록
docker ps -a        # 컨테이너 목록 (실행 중 + 종료된 것 전부)
```

---

## docker-compose

`docker run` 명령어를 파일로 관리하는 도구.
긴 명령어를 매번 치는 대신, yml 파일 하나로 실행 설정을 관리한다.

### docker/docker-compose.dev.yml

```yaml
services:
  orin:
    build:
      context: ..          # Dockerfile이 있는 위치
      dockerfile: Dockerfile
    image: breakout-game:dev
    environment:
      - CONFIG_PATH=configs/dev.yaml   # dev 모드로 실행
```

### 실행

```bash
cd docker/
docker compose -f docker-compose.dev.yml up
```

### docker run vs docker compose 비교

```bash
# 직접 실행
docker run --rm -e CONFIG_PATH=configs/dev.yaml breakout-game

# compose로 실행 (같은 내용, 파일로 관리)
docker compose -f docker-compose.dev.yml up
```

---

## dev 모드에서 Docker가 의미있는 이유

| | Docker 없이 | Docker 있이 |
|--|------------|------------|
| Orin에 배포 | Python 설치, pip install, 경로 설정... | `docker compose up` 한 줄 |
| 환경 충돌 | Python 버전, 라이브러리 버전 충돌 가능 | 이미지 안에 버전 고정 |
| 재현성 | "내 PC에서는 되는데..." | 어디서든 동일하게 동작 |

> **"성래 컴퓨터에서도 내가 동작한거를 딸깍으로 똑같이 동작할 수 있어야 한다"**

---

## 확인된 실행 결과

```
# 로컬 직접 실행
python3 -m orin.core.coordinator              → CLEAR! score=240 ✅

# docker run
docker run --rm -e CONFIG_PATH=configs/dev.yaml breakout-game  → CLEAR! score=240 ✅

# docker compose
docker compose -f docker-compose.dev.yml up   → CLEAR! score=240 ✅
```

세 가지 방법 전부 동일한 결과. 환경이 달라도 동작이 같다.

---

## 실물 배포 (Orin / NUC)

사전점검 체크리스트 문서: `02_edge_deploy_checklist.md`

### 사전 준비

**Orin에 Docker 설치**
```bash
sudo apt install docker.io docker-compose-v2
sudo usermod -aG docker $USER
newgrp docker
```

**NUC에 ROS2 Humble 설치 확인**
```bash
ls /opt/ros/humble   # 존재하면 OK
```

**SSH 키 설정 (비밀번호 없이 접속)**
```bash
ssh-keygen
ssh-copy-id babogaeguri@192.168.1.10   # Orin
ssh-copy-id babogaeguri@192.168.1.20   # NUC
```

### 배포 전 자동 점검 (preflight)

실배포 전에 아래 스크립트로 필수 조건을 한 번에 검사한다.

```bash
./scripts/preflight_check.sh 192.168.1.10 192.168.1.20
# 또는 사용자 지정
./scripts/preflight_check.sh 192.168.1.10 192.168.1.20 babogaeguri
```

점검 항목:

- 로컬 명령어 확인: `ssh`, `rsync`, `docker`
- 로컬 파일 확인: `Dockerfile`, `docker/docker-compose.dev.yml`, `configs/prod.yaml`, `ros2_ws/src/breakout_bridge_pkg`
- 네트워크 확인: Orin/NUC `ping` (ICMP 차단 시 `WARN` 가능)
- SSH 확인: Orin/NUC 무비번 접속 가능 여부
- 원격 런타임 확인: Orin `docker`, `docker compose`, NUC `ROS2 Humble`, `ros2`, `colcon`

결과 해석:

- `FAIL=0` 이면 배포 진행 가능
- `FAIL>0` 이면 해결 후 재실행
- `WARN`은 배포 가능할 수 있으나 환경 점검 권장

### 배포 실행

```bash
# NUC 먼저 — 점수 수신 대기 상태로 만들기
./scripts/deploy_nuc.sh 192.168.1.20

# Orin — 게임 실행 + 점수 발행
./scripts/deploy_orin.sh 192.168.1.10
```

### 배포 흐름 요약

```
deploy_orin.sh 실행
  → SSH로 Orin 접속
  → 코드 복사 (rsync)
  → docker build
  → CONFIG_PATH=configs/prod.yaml 로 컨테이너 실행
  → 게임 종료 시 /game/score ROS2 발행

deploy_nuc.sh 실행
  → SSH로 NUC 접속
  → ros2_ws 복사
  → colcon build
  → ros2 run breakout_bridge_pkg nuc_sub 실행
  → /game/score 수신 → 터미널 출력
```

### prod docker를 만들지 않은 이유

Orin은 헤드리스(화면 없음) 운용 → pygame 창을 docker 안에서 띄울 필요 없음.
`docker-compose.dev.yml` + `CONFIG_PATH=configs/prod.yaml` 조합으로 충분히 배포 가능.

| 환경 | docker-compose 파일 | CONFIG_PATH |
|------|---------------------|-------------|
| 개발 PC (테스트) | docker-compose.dev.yml | configs/dev.yaml |
| Orin (실물 배포) | docker-compose.dev.yml | configs/prod.yaml |
