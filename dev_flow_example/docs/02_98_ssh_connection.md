1. 같은 와이파이 네트워크에 연결되어 있는지 확인 (예: 핫스팟, 학교 랜)
2. Orin/NUC IP 주소 확인 (관리망 SSH용 IP 기준)
3. SSH 포트(22)가 열려 있는지 확인
4. SSH 접속 시도 (Orin 사용자명 확인됨: `laba`)
	- 예시: `ssh laba@<orin_ip>`
5. SSH 접속 시 비밀번호 입력 (첫 시도에서 오타 가능성 있음)
6. SSH 연결 성공 후 터미널에서 명령어 입력 시 원격 장비에서 실행됨
7. SSH 연결 중인 터미널과 로컬 터미널 구분 주의

## 보류 메모

- 무비번 SSH 설정(`ssh-keygen`, `ssh-copy-id`)은 나중에 진행
- `~/.ssh/config` 호스트 등록(`Host orin`)도 나중에 진행
- 시점: `sh` 파일 자동화/배포 스크립트 학습 단계에서 함께 적용

## remote_ssh_extension_setting_guide

VS Code에서 `Remote - SSH` 확장을 사용하면, 터미널 SSH보다 시각적으로 작업하기 편하다.

### 1. 확장 설치

- VS Code Extensions에서 `Remote - SSH` 설치
- 확장 ID: `ms-vscode-remote.remote-ssh`

### 2. SSH 접속 설정(편의 기)

터미널에서 `~/.ssh/config` 파일에 Orin 호스트를 등록한다.

```sshconfig
Host orin
	HostName 172.16.132.204
	User laba
	Port 22
```

### 3. VS Code에서 원격 접속

1. `F1` 입력
2. `Remote-SSH: Connect to Host...` 실행
3. `orin` 선택
4. 비밀번호 입력 후 접속

### 4. 원격 폴더 열기

- `File > Open Folder...`에서 Orin 경로 선택
- 예시: `/home/laba`

### 5. 확인 포인트

- VS Code 좌측 하단에 `SSH: orin` 표시 확인
- VS Code 터미널에서 `whoami` 실행 시 `laba` 출력 확인
- VS Code 터미널에서 `hostname` 실행 시 `ubuntu` 출력 확인

### 6. 문제 발생 시

- 비밀번호 오류: 사용자명/비밀번호 재확인 (`laba`)
- 접속 불가: PC와 Orin 네트워크 도달성 확인 (`ping 172.16.132.204`)
- Host key 충돌: `~/.ssh/known_hosts`에서 해당 IP 항목 정리 후 재접속