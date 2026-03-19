# BaboGaeguri 개발 환경 세팅

## 시스템 구성

### 방법 A — 박상윤 노트북 + 핫스팟 (기존)
```
박상윤 핸드폰 핫스팟
    ├── 박상윤 노트북 (Windows 11) — VSCode에서 작업
    └── 라즈베리파이 (laba@10.168.238.107) — 실행 환경
```

### 방법 B — 희승 컴퓨터 + 학교 유선 랜 (현재)
```
학교 유선 LAN (공유기)
    ├── 희승 컴퓨터 (192.168.0.13) — VSCode에서 작업
    └── 라즈베리파이 (laba@192.168.0.6) — 실행 환경
```

---

## 1. 네트워크 연결

### 방법 A — 핫스팟
1. 핸드폰에서 핫스팟 활성화
2. 노트북 → 핫스팟 Wi-Fi 연결
3. 라즈베리파이 → 같은 핫스팟 Wi-Fi 연결
4. 라파 IP 확인 방법:
   - 핸드폰 핫스팟 앱 "연결된 기기" 목록 확인
   - 또는 라파 터미널에서: `hostname -I`
   - 또는 노트북 터미널에서: `arp -a`

> 라파 IP (핫스팟): `10.168.238.107` / 라파 계정: `laba`

### 방법 B — 학교 유선 랜
1. 희승 컴퓨터 → 유선 랜 연결
2. 라즈베리파이 → 유선 랜 연결 (이더넷 케이블)
3. 라파 IP 확인 방법:
   - `arp -a` 로 목록 확인 (본인 PC IP 제외한 나머지)
   - 또는 `ping raspberrypi.local`

> 라파 IP (학교 랜): `192.168.0.6` / 희승 PC IP: `192.168.0.13` / 라파 계정: `laba`

---

## 2. SSH 연결

### 방법 A — 핫스팟 환경 (박상윤 노트북)
```bash
ssh laba@10.168.238.107
```

### 방법 B — 학교 유선 랜 환경 (희승 컴퓨터)
```bash
ssh laba@192.168.0.6
```

> 첫 번째 비밀번호 입력 시 오타 발생 가능 → 두 번째 시도에서 정상 입력

- 연결 성공 후 터미널에서 입력하는 모든 명령어는 **라파에서 실행**됨
- SSH 연결 중인 터미널 ≠ 로컬 터미널 (혼동 주의)

---

## 3. Remote-SSH 설정 (VSCode)

라파 파일을 VSCode GUI로 직접 보고 편집하기 위한 확장.

1. `Ctrl+Shift+X` → **Remote - SSH** 설치
2. `Ctrl+Shift+P` → **Remote-SSH: Connect to Host**
3. 환경에 맞는 주소 입력 → 비밀번호 입력
   - 핫스팟: `laba@10.168.238.107`
   - 학교 랜: `laba@192.168.0.6`
4. 플랫폼 선택창 뜨면 **Linux** 선택
5. **Open Folder** → `/home/laba/LABA5_Bootcamp`

---

## 4. 작업 흐름 (Workflow)

```
노트북 VSCode (로컬)
    └── Claude Code로 코드 작성/수정
            ↓ git push (노트북 터미널)
GitHub (BaboGaeguri/LABA5_Bootcamp)
            ↓ git pull (라파 SSH 터미널)
라즈베리파이 ~/LABA5_Bootcamp
    └── SSH 터미널에서 python3 실행
            ↓ 확인
Remote-SSH VSCode
    └── 라파 파일 탐색/확인 (GUI)
```

### Git push (노트북 터미널에서)

```bash
cd c:/Users/박상윤/Desktop/LABA5_Bootcamp
git add .
git commit -m "커밋 메시지"
git push
```

### Git pull (라파 SSH 터미널에서)

```bash
cd ~/LABA5_Bootcamp
git pull
```

### 왜 이 흐름이 최선인가?

| 방법 | 문제점 |
|---|---|
| 라파 VSCode 직접 사용 | 라파 저사양으로 버벅임, 불안정 |
| Remote-SSH에서 Claude Code 사용 | 라파에 팀원 Claude Code 계정이 로그인되어 있어 덮어쓸 위험 |
| scp 직접 전송 | 매번 수동 전송 필요, 번거로움 |
| **노트북 Claude Code + GitHub push/pull** | 버전 관리 + 자동 동기화, 가장 효율적 |

**결론:** 노트북 Claude Code로 코드 작성 → git push → 라파에서 git pull → 실행. GitHub가 중간 다리 역할을 하므로 scp 없이도 동기화 가능.

---

## 5. Git 초기 설정 (라파 최초 1회)

라파에서 커밋 작성자 정보 설정:

```bash
git config --global user.email "깃허브_이메일"
git config --global user.name "BaboGaeguri"
```

> Claude Code 계정과 무관함. git 커밋에 표시되는 이름/이메일 설정일 뿐.

---

## 6. 라파 저장소 현황

- 저장장치: **microSD 카드** (SSD 없음)
- 전체 용량: 58GB / 사용 중: 9.3GB (17%) / 여유: 47GB
- 주의: 전원을 갑자기 뽑으면 SD카드 손상 가능 → 반드시 `sudo shutdown -h now` 후 전원 차단

```bash
df -h  # 용량 확인
```

---

## 7. 작업 중단 및 재시작

### 작업 중단 시 종료 순서
1. 실행 중인 python 스크립트 종료 → `Ctrl+C`
2. 라파 안전 종료 (SSH 터미널에서):
```bash
sudo shutdown -h now
```
3. 라파 LED가 완전히 꺼진 후 전원 차단
4. 노트북 SSH / Remote-SSH 연결 닫기

> 전원을 그냥 뽑으면 SD카드 파일시스템 손상 가능 — 반드시 shutdown 먼저.

### 작업 재시작 시 순서 — 방법 A (핫스팟)
1. 핸드폰 핫스팟 활성화
2. 노트북 → 핫스팟 Wi-Fi 연결
3. 전원 케이블 꽂기 → 라파 자동 부팅 (전원 버튼 없음, 케이블 꽂으면 바로 켜짐)
4. **라파 IP 확인** (IP가 바뀔 수 있음):
   - 핸드폰 핫스팟 앱 "연결된 기기" 목록 확인
   - 라파 모니터 터미널에서: `hostname -I`
5. SSH 재연결: `ssh laba@<확인된 IP>`
6. Remote-SSH 재연결: `Ctrl+Shift+P` → **Remote-SSH: Connect to Host** → `laba@<확인된 IP>`

> 핫스팟을 껐다 켜면 IP가 바뀔 수 있으므로 매번 확인 권장.

### 작업 재시작 시 순서 — 방법 B (학교 유선 랜)
1. 희승 컴퓨터 → 유선 랜 연결 확인
2. 전원 케이블 꽂기 → 라파 자동 부팅
3. **라파 IP 확인**:
   - `arp -a` 로 확인 (보통 고정됨: `192.168.0.6`)
4. SSH 재연결: `ssh laba@192.168.0.6`
5. Remote-SSH 재연결: `Ctrl+Shift+P` → **Remote-SSH: Connect to Host** → `laba@192.168.0.6`

> 유선 랜은 IP가 비교적 안정적이지만 공유기 재시작 시 바뀔 수 있음.

---

## 8. 트러블슈팅

### Permission denied (비밀번호 입력 후)
첫 번째 비밀번호 입력에서 오타 발생 가능. 두 번째 시도에서 정상 입력하면 됨.

### git push 인증 오류
GitHub 비밀번호 대신 **Personal Access Token** 사용 필요.
GitHub → Settings → Developer settings → Personal access tokens에서 발급.
