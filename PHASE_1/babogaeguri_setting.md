# BaboGaeguri 개발 환경 세팅

## 시스템 구성

```
핸드폰 핫스팟
    ├── 노트북 (Windows 11) — VSCode에서 작업
    └── 라즈베리파이 (laba@10.168.238.107) — 실행 환경
```

---

## 1. 핫스팟 연결

1. 핸드폰에서 핫스팟 활성화
2. 노트북 → 핫스팟 Wi-Fi 연결
3. 라즈베리파이 → 같은 핫스팟 Wi-Fi 연결
4. 라파 IP 확인 방법:
   - 핸드폰 핫스팟 앱 "연결된 기기" 목록 확인
   - 또는 라파 터미널에서: `hostname -I`
   - 또는 노트북 터미널에서: `arp -a`

> 현재 라파 IP: `10.168.238.107`
> 라파 계정: `laba`

---

## 2. SSH 연결 (노트북 → 라파)

VSCode 터미널 또는 PowerShell에서:

```bash
ssh laba@10.168.238.107
```

- 연결 성공 후 터미널에서 입력하는 모든 명령어는 **라파에서 실행**됨
- SSH 연결 중인 터미널 ≠ 노트북 터미널 (혼동 주의)

---

## 3. Remote-SSH 설정 (VSCode)

노트북 VSCode에서 라파 파일을 GUI로 직접 보고 편집하기 위한 확장.

1. `Ctrl+Shift+X` → **Remote - SSH** 설치
2. `Ctrl+Shift+P` → **Remote-SSH: Connect to Host**
3. `laba@10.168.238.107` 입력 → 비밀번호 입력
4. **Open Folder** → `/home/laba/security_system`

---

## 4. 작업 흐름 (Workflow)

```
노트북 VSCode (로컬)
    └── Claude Code로 코드 작성/수정
            ↓ scp로 전송
라즈베리파이
    └── SSH 터미널에서 python3 실행
            ↓ 확인
Remote-SSH VSCode
    └── 라파 파일 탐색/확인 (GUI)
```

### 파일 전송 명령어 (노트북 일반 터미널에서 실행)

```bash
scp "c:/Users/박상윤/Desktop/LABA5_Bootcamp/PHASE_1/<파일명>" laba@10.168.238.107:~/security_system/<대상경로>
```

### 왜 이 흐름이 최선인가?

| 방법 | 문제점 |
|---|---|
| 라파 VSCode 직접 사용 | 라파 저사양으로 버벅임, 불안정 |
| Remote-SSH에서 Claude Code 사용 | 라파에 팀원 Claude Code 계정이 로그인되어 있어 덮어쓸 위험 |
| 노트북 Claude Code + scp 전송 | 약간 번거롭지만 안전하고 안정적 |

**결론:** 노트북 Claude Code(Pro 계정)로 코드 작성 → scp 전송 → Remote-SSH로 결과 확인이 현재 환경에서 가장 안전하고 효율적인 방법.

---

## 5. 라파 저장소 현황

- 저장장치: **microSD 카드** (SSD 없음)
- 전체 용량: 58GB / 사용 중: 9.3GB (17%) / 여유: 47GB
- 주의: 전원을 갑자기 뽑으면 SD카드 손상 가능 → 반드시 `sudo shutdown -h now` 후 전원 차단

```bash
df -h  # 용량 확인
```

---

## 6. 트러블슈팅

### scp 전송 실패 (No such file or directory)
라파에 폴더가 없는 상태에서 scp 실행 시 실패.
**해결:** SSH 터미널에서 `mkdir` 먼저 실행 후 scp 진행.

```bash
mkdir -p ~/security_system/templates
```

### Permission denied (비밀번호 입력 후)
첫 번째 비밀번호 입력에서 오타 발생 가능. 두 번째 시도에서 정상 입력하면 됨.
