# HY-WiFi SSH 연결 시도 기록

## 시도 목적
핸드폰 핫스팟 없이 학교 와이파이(HY-WiFi)만으로 노트북 ↔ 라즈베리파이 SSH 연결

---

## 네트워크 환경

| 기기 | 연결 | IP |
|---|---|---|
| 노트북 | HY-WiFi (wlan) | 172.16.136.221 |
| 라즈베리파이 | HY-WiFi (wlan0) | 172.16.136.171 |
| 라즈베리파이 | 유선 랜 (eth0) | 192.168.0.6 |

---

## 시도한 것들

### 1. SSH 직접 시도
```bash
ssh laba@172.16.136.171
```
결과: `Connection timed out`

### 2. ping 테스트 (노트북 → 라파)
```bash
ping 172.16.136.171
```
결과:
```
172.16.136.221의 응답: 대상 호스트에 연결할 수 없습니다.
```
노트북 자신(`221`)이 응답 → 패킷이 라파까지 도달 못함

### 3. ping 테스트 (라파 → 노트북)
```bash
ping 172.16.136.221
```
결과: `Destination Host Unreachable` 반복

### 4. 노트북 라우팅 테이블 확인
```bash
route print
```
결과: `172.16.136.0/24` 대역이 Wi-Fi 인터페이스로 정상 연결되어 있음 → 라우팅 문제 아님

### 5. SSH 서비스 상태 확인 (라파)
```bash
sudo systemctl status ssh
```
결과: `active (running)` → SSH 서버 정상 작동 중

### 6. 노트북 Windows 방화벽 ICMP 허용
```bash
# 관리자 권한 cmd에서
netsh advfirewall firewall add rule name="Allow ICMP" protocol=icmpv4 dir=in action=allow
```
결과: 확인됨 — 그래도 ping 안 됨

### 7. 라파 iptables 확인
```bash
sudo iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT
```
적용했으나 ping 여전히 안 됨

---

## 학교 담당자 문의 결과

- "기기 간 통신을 막아둔 것 없다"
- "같은 랜을 사용하는 공유기를 사용해보라" → 핫스팟과 같은 개념
- 노트북 ICMP 규칙 추가 후 노트북 ping은 열린 것 확인
- "기기 간의 문제일 것"이라고 답변

---

## 결론 및 원인 추정

핫스팟은 되고 학교 와이파이는 안 되는 이유:

```
핫스팟: 핸드폰(소규모 공유기) 아래 두 기기 직접 연결 → 통신 자유
학교 와이파이: 기업/학교용 AP 장비 사용 → AP Isolation 또는
              장비 기본 설정으로 기기 간 직접 통신 제한 가능성
```

담당자가 인지하지 못한 **AP Isolation** 설정이 원인일 가능성이 가장 높음.

---

## 열어뒀던 Windows 방화벽 규칙 제거 (작업 종료 시)

```bash
# 관리자 권한 cmd에서
netsh advfirewall firewall delete rule name="Allow ICMP"
```

---

## 최종 결론

학교 와이파이로 SSH 연결 불가. **핸드폰 핫스팟 사용**으로 결정.
