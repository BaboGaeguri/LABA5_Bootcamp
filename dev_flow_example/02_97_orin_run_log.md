# Orin Run Log

> 목적: Orin 실행/배포 과정에서 발생한 시행착오와 해결 내용을 시간순으로 기록한다.
> 범위: Orin 단독 실행 검증 (NUC 연동 전)

---

## 1. 현재 결론 요약

- Orin SSH 접속 사용자명은 `laba`로 확정 (`babogaeguri` 아님).
- Orin 관리망 Wi-Fi IP는 `172.16.132.204/24`.
- Docker/Compose 설치 및 권한 문제는 해결됨 (`newgrp docker` 이후 `docker info` 정상).
- 컨테이너에서 pygame 게임 실행 자체는 성공.
- 현재 미해결 이슈는 ROS2 발행(`rclpy`) 누락으로 인한 점수 발행 실패.

---

## 2. 수행 기록

### 2-1. 네트워크/SSH

- PC -> Orin `ping 172.16.132.204` 성공.
- 초기 접속 시 `ssh babogaeguri@172.16.132.204`는 인증 실패.
- Orin 로컬 확인 결과:
  - `hostname`: `ubuntu`
  - `whoami`: `laba`
- 이후 접속 계정은 `laba`로 교정.

### 2-2. 코드 전송

로컬 PC에서 아래 명령으로 Orin으로 코드 전송 완료:

```bash
rsync -avz --exclude='__pycache__' \
  orin configs docker Dockerfile requirements.txt \
  laba@172.16.132.204:/home/laba/breakout/
```

### 2-3. Docker 권한 이슈

증상:

- `permission denied while trying to connect to the docker API at unix:///var/run/docker.sock`

해결:

```bash
sudo usermod -aG docker laba
newgrp docker
docker info
```

결과:

- `docker info` Server 정보 출력 확인 (권한 해결).

### 2-4. GUI(X11) 관련 이슈

증상:

- `xhost: unable to open display ":0"`
- `~/.Xauthority` 파일 없음.

확인:

- `/tmp/.X11-unix/X1` 존재 -> 유효 DISPLAY는 `:1`.
- X 서버 프로세스의 `-auth` 경로 확인:
  - `/run/user/1000/gdm/Xauthority`

대응:

- `gdm` auth 파일을 `/tmp/orin.xauth`로 복사해 컨테이너에 마운트.

### 2-5. 컨테이너 실행 결과

실행 시 출력:

- `pygame ... Hello from the pygame community...`
- `[coordinator] GAME OVER score=30`
- `[coordinator] ROS2 발행 실패: No module named 'rclpy'`

해석:

- 게임 실행/렌더링은 성공.
- ROS2 점수 발행 단계에서 `rclpy`가 없어 실패.

---

## 3. 남은 작업

- NUC 정보(SSH 계정/IP/ROS2 상태) 수집 후 연동 준비.
- ROS2 발행을 위해 아래 중 하나 선택:
  - Docker 이미지를 ROS2 Humble 기반으로 재구성
  - 게임 컨테이너와 ROS2 발행 경로를 분리

---

## 4. 다음 실행 시 체크

1. `docker info`가 현재 세션에서 Server까지 출력되는지
2. `DISPLAY`가 실제 X 소켓(`X0`/`X1`)과 일치하는지
3. 점수 발행 테스트가 필요한 런에서 `rclpy` 사용 가능 여부
