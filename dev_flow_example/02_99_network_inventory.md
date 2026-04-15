# Network Inventory (PC / Orin / NUC)

> 목적: 배포 전에 필요한 네트워크 정보를 한 문서에 기록한다.
> 작성 기준: `02_01_network_setting.md`

---

## 1. 공통 기록 항목

각 장비마다 아래를 기록한다.

- 장비 역할 (`Dev PC` / `Orin` / `NUC`)
- 호스트명 (`hostname`)
- 관리망 인터페이스/ IP (SSH용)
- 운영망 인터페이스/ IP (Orin-NUC ROS2용)
- 서브넷 (`/24` 등)
- 기본 게이트웨이 (`ip route`의 `default via`)
- DNS 서버
- SSH 사용자명
- `ROS_DOMAIN_ID`
- 비고 (DHCP/Static, 케이블 연결 상태 등)

---

## 2. 현재 기록 (초안)

### 2-1. Dev PC

- 역할: Dev PC
- 호스트명: `babogaeguri-950QED`
- 관리망 인터페이스: `wlo1`
- 관리망 IP: `172.16.139.236/24` (DHCP)
- 운영망 인터페이스: `N/A` (추후 Orin/NUC 운영망 분리 시 기록)
- 기본 게이트웨이: `172.16.139.254` (dev=`wlo1`)
- DNS: `168.126.63.1`, `8.8.8.8`
- SSH 사용자: `babogaeguri`
- ROS_DOMAIN_ID: `미기록`
- 비고:
  - Docker 브리지: `docker0=172.17.0.1/16`, `br-6f1c98e5b438=172.18.0.1/16`

### 2-2. Orin

- 역할: Orin
- 호스트명: `ubuntu`
- 관리망 인터페이스/IP (SSH): `wlp1s0`, `172.16.132.204/24` (DHCP)
- 운영망 인터페이스/IP (ROS2): `미기록`
- 기본 게이트웨이: `미기록`
- DNS: `미기록`
- SSH 사용자: `laba` (확정)
- ROS_DOMAIN_ID: `미기록`
- 비고:
  - 개발 PC에서 `ping 172.16.132.204` 통신 확인됨
  - 최초 SSH 시도에서 사용자명 `babogaeguri`는 인증 실패, `laba`로 교정 필요
  - `docker info` Server 출력 확인 (Docker 권한 이슈 해결)
  - 컨테이너 GUI 실행 확인 (`DISPLAY=:1`)
  - 현재 ROS2 발행 이슈: `No module named 'rclpy'`

### 2-3. NUC

- 역할: NUC
- 호스트명: `미기록`
- 관리망 인터페이스/IP (SSH): `미기록`
- 운영망 인터페이스/IP (ROS2): `미기록`
- 기본 게이트웨이: `미기록`
- DNS: `미기록`
- SSH 사용자: `babogaeguri` (예정)
- ROS_DOMAIN_ID: `미기록`
- 비고: `미기록`

---

## 3. Orin/NUC에서 실행할 수집 명령

아래를 각 장비에서 실행한 뒤 값을 위 섹션에 반영한다.

```bash
hostname
ip -4 addr show scope global
ip route
resolvectl dns || cat /etc/resolv.conf
echo "ROS_DOMAIN_ID=${ROS_DOMAIN_ID}"
```

추가 확인 (개발 PC에서 실행):

```bash
ssh laba@<orin_mgmt_ip> "hostname"
ssh <nuc_user>@<nuc_mgmt_ip> "hostname"
```

---

## 4. 고정 정책 (권장)

- 운영망(Orin-NUC 유선): Static IP 고정
- 관리망(SSH): DHCP 예약 또는 Static
- 배포 전: `scripts/preflight_check.sh <orin_mgmt_ip> <nuc_mgmt_ip> <ssh_user>`

---

## 5. 완료 조건

- [ ] Dev PC / Orin / NUC 항목 모두 기록 완료
- [ ] 관리망 IP와 운영망 IP를 구분해 기록 완료
- [ ] `ROS_DOMAIN_ID` 양쪽 동일 값 기록 완료
- [ ] preflight 결과 `FAIL : 0`

---

## 관련 실행 로그

- `02_97_orin_run_log.md`
