# 팔 모터 인식 불가 문제 해결 기록

## 증상
- `/dev/ttyACM0`, `/dev/ttyACM1` 포트는 정상 인식
- 모든 baudrate(57600, 115200, 1000000, 2000000, 4000000)에서 모터 응답 없음 (`{}`)
- `dynamixel_sdk` ping 결과 ID 1~19 전부 미응답

## 원인

### 1. ModemManager가 포트 점유
- 리눅스의 `ModemManager` 서비스가 U2D2 (Dynamixel USB 어댑터)를 모뎀 장치로 착각
- ttyACM 포트를 자동으로 점유해버려서 Python에서 열어도 모터와 실제 통신이 안 됨
- 특히 USB 재연결 직후 ModemManager가 먼저 포트를 잡아버리는 타이밍 문제 발생

### 2. dialout 그룹 미등록
- `laba` 계정이 `dialout` 그룹에 없어서 Permission denied 발생
- `sudo usermod -aG dialout laba` 로 해결
- 단, 그룹 적용은 SSH 재연결 후부터 유효

## 해결 방법

```bash
# 1. ModemManager 중지 및 재시작 방지
sudo systemctl stop ModemManager
sudo systemctl disable ModemManager

# 2. dialout 그룹 추가 (최초 1회)
sudo usermod -aG dialout laba
# 이후 SSH 재연결 필요

# 3. 포트 권한 임시 개방 (필요시)
sudo chmod 666 /dev/ttyACM0 /dev/ttyACM1
```

## 결과
- `ttyACM0` = **Leader** (xl330-m288 x6)
- `ttyACM1` = **Follower** (xl430-w250 x3 + xl330-m288 x3)
- 모든 모터 6개씩 정상 인식 확인

## 주의사항
- 재부팅 후에도 ModemManager가 다시 살아날 수 있으므로 `disable`까지 해야 영구 적용
- U2D2 USB 뽑았다 꽂을 때마다 ModemManager가 간섭할 수 있으니 재부팅 후 확인 권장
