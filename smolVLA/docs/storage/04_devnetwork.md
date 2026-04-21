# Dev Network 설정 (WiFi SSH)

> 작성일: 2026-04-21  
> 목적: devPC ↔ Jetson Orin ↔ DGX Spark 간 WiFi SSH 연결 설정 기록

---

## 1) 장비 개요

| 장비 | 역할 | OS | 호스트명 |
|---|---|---|---|
| devPC | 코드 정리/문서화/배포 관리 | Ubuntu 22.04 | `babogaeguri-950QED` |
| Jetson Orin Nano Super | 실행/검증 (SO-ARM 연결) | Ubuntu 22.04 (L4T R36.5.0) | 확인 필요 |
| DGX Spark | 학습/파인튜닝 전용 | Ubuntu (확인 필요) | 확인 필요 |

---

## 2) 네트워크 정보 수집

| 장비 | WiFi IP | 비고 |
|---|---|---|
| devPC | — | 확인 후 기재 |
| Jetson Orin | — | 확인 후 기재 |
| DGX Spark | — | 확인 후 기재 |

> **접속 방식**: 학교 WiFi 환경이므로 IP 고정이 불가능하다. **mDNS(hostname.local) 방식**으로 접속한다.

---

## 3) SSH 서버 설치/활성화 확인

### Jetson Orin (확인됨)
- `openssh-server` 설치됨
- `ssh.service`: `active`, `enabled`
- `0.0.0.0:22`, `[::]:22` 리슨 확인 → 별도 설정 불필요

### DGX Spark (확인 필요)

---

## 4) SSH 키 기반 인증 설정 (패스워드 없이 접속)

- devPC에서 ed25519 키 생성 후 각 장비에 공개키 배포
- 기본 키 경로: `~/.ssh/id_ed25519`

---

## 5) SSH Config 설정 (`~/.ssh/config`)

devPC의 `~/.ssh/config`에 Orin / DGX Spark 항목 추가:

| 항목 | Orin | DGX Spark |
|---|---|---|
| Host alias | `orin` | `dgx` |
| HostName | `<orin-hostname>.local` | `<dgx-hostname>.local` |
| User | `babogaeguri` | 확인 후 기재 |
| IdentityFile | `~/.ssh/id_ed25519` | `~/.ssh/id_ed25519` |
| ServerAliveInterval | `30` | `30` |
| ServerAliveCountMax | `5` | `5` |

> `ServerAliveInterval` / `ServerAliveCountMax`: WiFi 환경에서 idle 세션 끊김 방지

---

## 6) VS Code Remote SSH 설정

1. VS Code 확장 설치: `Remote - SSH` (`ms-vscode-remote.remote-ssh`)
2. `F1` → `Remote-SSH: Connect to Host...`
3. `~/.ssh/config`에 등록된 `orin` 또는 `dgx` 선택
4. 처음 연결 시 플랫폼 선택: `Linux`

### 권장 워크스페이스 경로

| 장비 | Remote 워크스페이스 경로 |
|---|---|
| Orin | `/home/babogaeguri/lerobot` |
| DGX Spark | 확인 후 기재 |

---

## 7) 파일 전송 (devPC ↔ Orin/DGX)

- 소규모: `scp -r`
- 대용량/증분: `rsync -avz --progress` 권장

---

## 8) 포트 포워딩 (Jupyter 등 원격 UI 접근)

- Orin Jupyter → devPC `localhost:8888`로 터널링
- DGX Spark Jupyter → devPC `localhost:8889`로 터널링
- VS Code Remote-SSH 연결 시 포트 포워딩 탭에서 자동 처리 가능

---

## 9) 자주 쓰는 원격 명령

| 목적 | 명령 |
|---|---|
| Orin GPU 상태 | `ssh orin "tegrastats --interval 1000"` |
| Orin nvpmodel 확인 | `ssh orin "sudo nvpmodel -q"` |
| DGX GPU 상태 | `ssh dgx "nvidia-smi"` |

---

## 10) 확인 필요 항목

- [ ] Orin 호스트명 확인 (`hostname`) → `<orin-hostname>.local`로 접속 테스트
- [ ] devPC에서 `avahi-daemon` 설치/동작 확인
- [ ] Orin에서 `avahi-daemon` 설치/동작 확인
- [ ] `ssh babogaeguri@<orin-hostname>.local` 접속 성공 확인
- [ ] DGX Spark 호스트명, 유저명 확인 후 동일 방식 적용
- [ ] 같은 WiFi AP에 3대 모두 연결 가능한지 확인 (공유기 AP isolation 비활성화 여부)
