# PHASE_1 — 스마트 경비 시스템

> 환경 세팅은 `babogaeguri_setting.md` 참고

---

## 미션 개요

라즈베리파이 하나로 작동하는 스마트 경비 시스템.
카메라가 얼굴을 감지하면 서보모터로 추적하고, 침입자 판단 시 LED 경고 + 자동 촬영.

| 서브미션 | 기능 |
|---|---|
| 1-1 | 카메라 촬영 (사진 저장) |
| 1-2 | GPIO 경고 (침입자/인가자 LED) |
| 1-3 | 증거 촬영 (자동 저장) |
| 1-4 | 라이브 모니터링 |
| 1-5 | 움직임 감지 → 경계 모드 전환 |
| 1-6 | 얼굴 인식 + 서보 추적 + 색상 기반 침입자 판단 (통합) |

---

## 라파 프로젝트 디렉토리 구조

```
/home/laba/LABA5_Bootcamp/PHASE_1/
├── 1-1.py                          ← 카메라 촬영
├── 1-2.py
├── 1-3.py
├── 1-4.py
├── 1-5.py
├── 1-6.py                          ← 통합 보안 시스템 (cv2.imshow 버전)
├── 1-6(revised).py                 ← Flask 웹스트리밍 버전
├── 1-6(html_source).py
├── haarcascade_frontalface_default.xml
├── python_test.jpg                 ← 1-1 실행 시 저장되는 사진
└── templates/
    └── index.html                  ← 1-6 Flask용 웹 UI (반드시 templates/ 하위)
```

> `templates/` 폴더는 Flask의 `render_template("index.html")`이 자동으로 탐색하므로 삭제 불가.

---

## 실행 방법

### 공통: 노트북 수정 후 라파 반영

```bash
# 노트북 터미널
git add . && git commit -m "메시지" && git push

# 라파 SSH 터미널
cd ~/LABA5_Bootcamp && git pull
```

### 1-1 실행 (카메라 촬영)

```bash
python3 ~/LABA5_Bootcamp/PHASE_1/1-1.py
```

- 저장 경로: `PHASE_1/python_test.jpg` (스크립트 위치 기준으로 자동 저장)
- 실행 시 `img.show()` 에러는 GUI 뷰어 없어서 발생 → 무시해도 됨, 사진은 정상 저장

### 1-6 Flask 버전 실행

```bash
cd ~/LABA5_Bootcamp/PHASE_1
python3 1-6\(revised\).py
```

노트북 브라우저에서 라이브 모니터링:
```
http://10.168.238.107:5000
```

### 실행 시 터미널 로그 예시
```
[HH:MM:SS] Camera started
[HH:MM:SS] Motion detected -> GUARD MODE
[HH:MM:SS] Authorized person detected
[HH:MM:SS] Intruder detected
[HH:MM:SS] INTRUDER CAPTURED -> /home/laba/intruder_YYYYMMDD_HHMMSS.jpg
[HH:MM:SS] No motion for 5 sec -> STANDBY MODE
```

---

## 주요 설정값 (1-6 revised)

| 항목 | 값 | 설명 |
|---|---|---|
| `MOTION_DIFF_THRESH` | 40 | 프레임 차이 임계값 |
| `MOTION_PIXEL_THRESHOLD` | 500 | 움직임 판정 최소 픽셀 수 |
| `NO_MOTION_TIMEOUT` | 5.0초 | 대기 모드 복귀 시간 |
| `SERVO_P_GAIN` | 0.12 | 서보 추적 P 게인 |
| `SERVO_DEADZONE` | 20px | 서보 미동작 허용 범위 |
| `INTRUDER_CAPTURE_COOLDOWN` | 5.0초 | 중복 촬영 방지 쿨다운 |
| `BLUE_RATIO_THRESHOLD` | 0.02 | 파란 카드 인식 최소 비율 |

---

## GPIO 핀 배치

| 기능 | GPIO 핀 (BCM) |
|---|---|
| 초록 LED (인가자) | GPIO 17 |
| 빨간 LED (침입자) | GPIO 27 |
| 서보모터 | GPIO 18 |

---

## 트러블슈팅

### img.show() 에러 (1-1)
```
Error: no "view" rule for type "image/png"
```
라파 GUI 이미지 뷰어를 찾지 못해서 발생. 사진은 정상 저장됨. 무시해도 됨.

### PermissionError: '/home/pi'
`CAPTURE_DIR`이 `/home/pi`로 설정되어 있으나 라파 계정이 `laba`라서 권한 오류 발생.
현재 코드에서는 이미 수정 완료.
