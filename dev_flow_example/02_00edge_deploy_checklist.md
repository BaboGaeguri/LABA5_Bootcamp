# Edge Deploy Preflight Checklist

> 목적: 개발 PC에서 만든 프로그램을 실제 엣지 디바이스(Orin/NUC)에 안정적으로 배포하기 전, 실패 요인을 사전에 제거한다.
> 기준 스크립트: `scripts/preflight_check.sh`

---

## 0. 실행 원칙

- 배포 전에 반드시 `preflight_check.sh`를 먼저 실행한다.
- `FAIL : 0`이 아니면 배포를 시작하지 않는다.
- `WARN`은 진행 가능할 수 있지만, 원인을 알고 진행한다.

---

## 1. 사전 준비 체크

- [ ] Orin IP 확인 (`예: 192.168.1.10`)
- [ ] NUC IP 확인 (`예: 192.168.1.20`)
- [ ] 원격 사용자 확인 (`기본: babogaeguri`)
- [ ] 로컬 프로젝트 경로 확인 (`dev_flow_example`)

실행:

```bash
cd /home/babogaeguri/ros2_ws/src/LABA5_Bootcamp/dev_flow_example
./scripts/preflight_check.sh 192.168.1.10 192.168.1.20 babogaeguri
```

또는 사용자 기본값 사용:

```bash
./scripts/preflight_check.sh 192.168.1.10 192.168.1.20
```

---

## 2. Preflight 결과 판정

- [ ] `PASS` 항목 확인
- [ ] `WARN` 항목 원인 확인 (예: ping 차단)
- [ ] `FAIL` 항목 0개 확인

판정 기준:

- `FAIL : 0` -> 배포 진행 가능
- `FAIL : 1 이상` -> 실패 항목 해결 후 재실행

---

## 3. 실패 항목별 빠른 조치

### 3-1. SSH 무비번 접속 실패

- [ ] Orin 수동 접속 확인: `ssh babogaeguri@<orin_ip>`
- [ ] NUC 수동 접속 확인: `ssh babogaeguri@<nuc_ip>`
- [ ] SSH 키 배포

```bash
ssh-copy-id babogaeguri@192.168.1.10
ssh-copy-id babogaeguri@192.168.1.20
```

### 3-2. Orin Docker 관련 실패

- [ ] Docker 설치
- [ ] Compose v2 설치
- [ ] docker 그룹 권한 적용

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-v2
sudo usermod -aG docker $USER
newgrp docker
```

### 3-3. NUC ROS2 관련 실패

- [ ] `/opt/ros/humble` 존재 확인
- [ ] `ros2` 명령 확인
- [ ] `colcon` 설치 확인

```bash
ls /opt/ros/humble
source /opt/ros/humble/setup.bash
ros2 --help
sudo apt install -y python3-colcon-common-extensions
```

---

## 4. 배포 실행 체크

`preflight_check.sh` 재실행 후 `FAIL : 0`이면 진행:

- [ ] NUC 배포
- [ ] Orin 배포

```bash
./scripts/deploy_nuc.sh 192.168.1.20
./scripts/deploy_orin.sh 192.168.1.10
```

---

## 5. 배포 후 확인

- [ ] NUC에서 `/game/score` 수신 로그 확인
- [ ] Orin 게임 종료 후 점수 발행 확인
- [ ] 실패 시 preflight/배포 로그를 함께 저장

## 6. 느낀점
- 미리 발표장소 가서 네트워크 환경을 체크하는게 매우매우 중요할거라고 생각
- 도커파일을 jetson이나 x86에서 모두 빌드할 수 있도록 작성하는게 중요할거라고 생각

---

## 참고

- 상세 Docker/배포 설명: `01_docker_guide.md`
- 개발 전체 계획: `00_breakout_plan.md`
- 사전점검 스크립트: `scripts/preflight_check.sh`
