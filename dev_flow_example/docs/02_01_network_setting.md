# Network Setting Basics

> 목적: 연결 문제를 다루기 전에, 각 기기의 IP/인터페이스를 스스로 확인하고 해석할 수 있도록 기본 개념을 정리한다.
> 대상: 개발 PC, Orin, NUC (Linux 기준)

---

## 1. 꼭 알아야 하는 개념

- IP 주소: 네트워크에서 장비를 식별하는 주소
- 서브넷(대역): 같은 네트워크인지 판단하는 범위
- 인터페이스: `eth0`, `wlan0`처럼 네트워크 장치 이름
- 게이트웨이: 다른 네트워크로 나갈 때 거치는 기본 경로
- DNS: 도메인 이름을 IP로 바꿔주는 서버

예시:

- `192.168.1.10/24` -> 같은 대역은 `192.168.1.x`
- `/24`는 서브넷 마스크 `255.255.255.0`과 동일 의미

---

## 2. IP 확인 기본 명령어

### 2-1. 인터페이스와 IP 전체 보기

```bash
ip a
```

볼 포인트:

- `state UP`인지
- `inet` 항목이 있는지
- 유선은 보통 `eth0`, 무선은 보통 `wlan0`/`wlp*`

### 2-2. 특정 인터페이스만 보기

```bash
ip -4 addr show eth0
ip -4 addr show wlan0
```

### 2-3. 기본 라우팅(게이트웨이) 확인

```bash
ip route
```

볼 포인트:

- `default via ... dev ...` 줄이 있는지
- 기본 경로가 어떤 인터페이스로 나가는지

### 2-4. DNS 확인

```bash
resolvectl status
cat /etc/resolv.conf
```

---

## 3. 연결/도달성 확인 명령어

### 3-1. IP까지 닿는지 확인

```bash
ping -c 3 192.168.1.10
```

### 3-2. SSH 포트(22) 열림 확인

```bash
nc -zv 192.168.1.10 22
```

`nc`가 없으면:

```bash
telnet 192.168.1.10 22
```

### 3-3. 실제 SSH 접속 확인

```bash
ssh babogaeguri@192.168.1.10
```

---

## 4. Orin/NUC에서 가장 먼저 할 5개

각 장비에 직접 로그인해서 아래만 먼저 확인:

```bash
hostname
ip a
ip route
ping -c 3 8.8.8.8
ping -c 3 <상대장비_IP>
```

체크:

- [ ] 장비 이름(`hostname`) 확인
- [ ] IP 주소 확인
- [ ] 기본 게이트웨이 확인
- [ ] 인터넷 방향 ping 가능 여부
- [ ] 상대 장비 ping 가능 여부

---

## 5. IP 고정(Static) vs 자동(DHCP)

- DHCP: 공유기가 IP를 자동 할당 (쉽지만 IP가 바뀔 수 있음)
- Static: 직접 IP 고정 (안정적, 배포 스크립트에 유리)

배포 자동화에서는 고정 IP를 권장한다.

예시 고정 IP 정책:

- Orin: `192.168.1.10`
- NUC: `192.168.1.20`
- 개발 PC: `192.168.1.30`

---

## 6. 자주 헷갈리는 포인트

- `ping` 실패 = 무조건 네트워크 장애는 아님 (ICMP 차단 가능)
- `ssh` 실패는 실사용 관점에서 치명적
- Wi-Fi와 유선을 같이 쓰면 라우팅이 꼬일 수 있음
- IP가 바뀌면 배포 스크립트 인자도 반드시 변경해야 함

---

## 7. 다음 단계

기초 확인이 끝나면 아래로 진행:

1. `02_1_network_connection.md`에서 연결 토폴로지 선택
2. `scripts/preflight_check.sh` 실행
3. `FAIL : 0` 확인 후 배포 스크립트 실행

---

## 관련 문서

- `02_03_network_inventory.md`
- `02_1_network_connection.md`
- `02_edge_deploy_checklist.md`
- `01_docker_guide.md`
- `scripts/preflight_check.sh`
