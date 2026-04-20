# Orin / NUC 연결 시작 프로세스

> 목적: Dev 노트북에서 Orin과 NUC에 SSH로 연결하기까지의 과정을 단계별로 기록한다.
> 이 문서만 보고 처음부터 다시 해도 성공할 수 있도록 작성한다.

---

## 환경 정보 (2026-04-16 기준)

| 장비 | 호스트명 | SSH 유저 | WiFi 인터페이스 | WiFi IP | LAN 인터페이스 |
|------|---------|---------|----------------|---------|--------------|
| Dev PC | `babogaeguri-950QED` | `babogaeguri` | `wlo1` | `172.16.139.236/24` | - |
| Orin | `ubuntu` | `laba` | `wlp1p1s0` | `172.16.128.97/24` | `eno1` |
| NUC | `laba-desktop` | `laba` | 없음 | - | `enp1s0` |

> NUC는 WiFi 없음. Orin의 LAN을 통해 인터넷 공유.

---

## Step 1. 각 장비 IP 확인

각 장비에서 실행:

```bash
ip a | grep "inet "
```

- `127.0.0.1` : 루프백 (무시)
- `172.17/18.x.x` : Docker 브리지 (무시)
- 실제 WiFi IP만 확인 (`wlo1`, `wlp*` 등 무선 인터페이스)

Dev PC에서 Orin으로 ping 확인:

```bash
ping -c 3 172.16.128.97
```

> 서브넷이 달라도(`172.16.139.x` vs `172.16.128.x`) 라우터가 중계해주면 ping이 된다.

---

## Step 2. Orin ↔ NUC LAN 케이블 연결

LAN 케이블로 Orin `eno1` ↔ NUC `enp1s0` 직결.

연결 후 Orin에서 확인:

```bash
ip a
```

`eno1`이 `state UP`이면 케이블 연결 성공. (IP는 아직 없어도 됨)

---

## Step 3. Orin ↔ NUC Static IP 설정

**Orin에서:**

```bash
sudo ip addr add 192.168.50.1/24 dev eno1
sudo ip link set eno1 up
```

**NUC에서:**

```bash
sudo ip addr add 192.168.50.2/24 dev enp1s0
sudo ip link set enp1s0 up
```

**Orin에서 NUC ping 확인:**

```bash
ping -c 3 192.168.50.2
```

0% packet loss 확인.

---

## Step 4. Orin에서 NUC로 인터넷 공유 설정 (NetworkManager)

> NUC에 SSH 서버를 설치하려면 인터넷이 필요하다.
> Orin의 WiFi를 NUC에 공유한다.

**Orin에서:**

```bash
sudo sysctl -w net.ipv4.ip_forward=1
nmcli connection add type ethernet ifname eno1 con-name "share-to-nuc" ipv4.method shared
nmcli connection up "share-to-nuc"
```

> `iptables` 수동 설정 하지 말 것. NetworkManager가 NAT/DHCP를 자동으로 처리한다.

---

## Step 5. NUC IP / 라우팅 / DNS 설정

**NUC에서** DHCP로 IP 받기:

```bash
sudo dhclient enp1s0
ip a | grep "inet "
```

NetworkManager가 `10.42.0.x` 대역으로 IP를 할당한다. (예: `10.42.0.221`)

**NUC에서** 라우팅 수정 (기존 default 삭제 후 Orin 게이트웨이로 변경):

```bash
sudo ip route del default
sudo ip route add default via 10.42.0.1 dev enp1s0
```

**NUC에서** DNS 설정:

```bash
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
```

**NUC에서** 인터넷 확인:

```bash
ping -c 3 8.8.8.8
```

0% packet loss 확인.

---

## Step 6. NUC에 SSH 서버 설치

**NUC에서:**

```bash
sudo apt install openssh-server -y
```

설치 완료 시 `sshd` 서비스가 자동으로 시작된다.

---

## Step 7. Dev PC에서 SSH 연결

**Orin SSH:**

```bash
ssh laba@172.16.128.97
```

**NUC SSH (Orin 경유 점프):**

```bash
ssh -J laba@172.16.128.97 laba@10.42.0.221
```

> NUC IP(`10.42.0.221`)는 DHCP라 재부팅 시 바뀔 수 있다.
> 재접속 전에 Orin에서 `ip neigh show dev eno1` 또는 NUC에서 `ip a`로 현재 IP 확인.

---

## 주의사항

- Orin/NUC의 Static IP 설정(`ip addr add`)은 재부팅 시 초기화된다.
- NetworkManager `share-to-nuc` 연결은 재부팅 후 `nmcli connection up "share-to-nuc"`로 다시 올려야 할 수 있다.
- NUC의 라우팅(`ip route`)과 DNS(`/etc/resolv.conf`)도 재부팅 시 초기화된다.
- 영구 설정이 필요하면 `netplan` 또는 `nmcli` 설정 파일로 고정해야 한다.
