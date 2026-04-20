# Orin/NUC Network Connection Guide

> 목적: 배포 전에 Orin과 NUC 네트워크를 먼저 안정화한다.
> 기준: 개발 PC에서 SSH 가능 + Orin/NUC 간 ROS2 통신 가능

---

## 1. 권장 구성 (처음 성공용)

가장 먼저는 아래 구성을 권장한다.

- 개발 PC, Orin, NUC를 같은 공유기/스위치에 연결
- 가능하면 3대 모두 유선 LAN 사용
- 최소한 Orin/NUC는 유선 LAN 우선

이 구성이 좋은 이유:

- IP 확인이 쉽고, 라우팅 혼선이 적다
- SSH/배포/ROS2를 한 네트워크에서 동시에 검증 가능

---

## 2. 대안 구성 (직결 + Wi-Fi 관리)

필요하면 아래도 가능하다.

- Orin <-> NUC: 유선 직결 (ROS2 전용)
- 개발 PC <-> Orin/NUC: Wi-Fi SSH (배포/관리)

주의:

- 유선/무선 멀티 NIC로 인해 ROS2 discovery와 라우팅이 꼬일 수 있다
- 첫 성공 전에는 권장하지 않는다

---

## 3. 네트워크 점검 체크리스트

### 3-1. 장비 전원/물리 연결

- [ ] Orin 전원 ON
- [ ] NUC 전원 ON
- [ ] LAN 케이블 링크 LED 확인
- [ ] 공유기/스위치 연결 상태 확인

### 3-2. IP 주소 확인

각 장비에서 IP 확인:

```bash
ip a
```

- [ ] Orin IP 확인 (예: `192.168.1.10`)
- [ ] NUC IP 확인 (예: `192.168.1.20`)
- [ ] 개발 PC와 같은 대역인지 확인 (`192.168.1.x/24`)

### 3-3. SSH 접속 확인

개발 PC에서:

```bash
ssh babogaeguri@192.168.1.10
ssh babogaeguri@192.168.1.20
```

- [ ] Orin SSH 접속 성공
- [ ] NUC SSH 접속 성공

무비번 설정:

```bash
ssh-copy-id babogaeguri@192.168.1.10
ssh-copy-id babogaeguri@192.168.1.20
```

- [ ] Orin 무비번 SSH 성공
- [ ] NUC 무비번 SSH 성공

### 3-4. ROS2 기본 조건 확인

Orin/NUC 양쪽에서:

```bash
echo $ROS_DOMAIN_ID
```

- [ ] 동일한 `ROS_DOMAIN_ID` 사용

필요 시 동일하게 설정:

```bash
export ROS_DOMAIN_ID=0
```

---

## 4. 직결(Orin<->NUC) 사용할 때 권장 IP 예시

유선 인터페이스에 고정 IP를 준다.

- Orin eth: `192.168.50.10/24`
- NUC eth: `192.168.50.20/24`

개발 PC에서는 이 IP로는 직접 접속이 안 될 수 있으므로,
Wi-Fi IP를 별도로 확인해 SSH 대상으로 사용한다.

예시:

- ROS2 통신 대상: `192.168.50.x` (유선)
- SSH/배포 대상: `192.168.1.x` (Wi-Fi)

---

## 5. Preflight로 최종 판정

네트워크/SSH 정리 후 아래를 실행한다.

```bash
cd /home/babogaeguri/ros2_ws/src/LABA5_Bootcamp/dev_flow_example
./scripts/preflight_check.sh 192.168.1.10 192.168.1.20 babogaeguri
```

판정:

- `FAIL : 0` -> 배포 진행
- `FAIL : 1 이상` -> 실패 항목 해결 후 재실행

---

## 6. 다음 단계

preflight 통과 후 배포:

```bash
./scripts/deploy_nuc.sh 192.168.1.20
./scripts/deploy_orin.sh 192.168.1.10
```

---

## 관련 문서

- `00_breakout_plan.md`
- `01_docker_guide.md`
- `02_edge_deploy_checklist.md`
- `scripts/preflight_check.sh`
