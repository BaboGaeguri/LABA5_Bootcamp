# PHASE_1 — 스마트 경비 시스템

> 환경 세팅은 `babogaeguri_setting.md` 참고

---

## 미션 개요

라즈베리파이 하나로 작동하는 스마트 경비 시스템.
카메라가 얼굴을 감지하면 서보모터로 추적하고, 침입자 판단 시 LED 경고 + 자동 촬영.

| 서브미션 | 기능 | 브라우저 확인 |
|---|---|---|
| 1-1 | 카메라 촬영 (사진 저장) | X (파일 저장만) |
| 1-2 | 라이브 카메라 스트리밍 | O |
| 1-3 | 움직임 감지 + LED/부저 | O |
| 1-4 | 얼굴 인식 + LED | O |
| 1-5 | 얼굴 추적 서보모터 | O |
| 1-6 | 통합 보안 시스템 (얼굴+서보+색상+LED+촬영) | O |

---

## 라파 프로젝트 디렉토리 구조

```
/home/laba/LABA5_Bootcamp/PHASE_1/
├── 1-1.py                          ← 카메라 촬영 (사진 저장)
├── 1-2.py                          ← 라이브 스트리밍 (Flask)
├── 1-3.py                          ← 움직임 감지 + LED/부저 (Flask)
├── 1-4.py                          ← 얼굴 인식 + LED (Flask)
├── 1-5.py                          ← 얼굴 추적 서보모터 (Flask)
├── 1-6.py                          ← 통합 보안 시스템 (Flask)
├── 1-6(revised).py                 ← 1-6 초기 Flask 버전
├── 1-6(html_source).py             ← 1-6 HTML 소스
├── haarcascade_frontalface_default.xml  ← 얼굴 인식 모델 (1-4, 1-5, 1-6 공용)
├── python_test.jpg                 ← 1-1 실행 시 저장되는 사진
└── templates/
    └── index.html                  ← 1-6 Flask용 웹 UI
```

> `haarcascade_frontalface_default.xml`은 PHASE_1 폴더 기준 상대경로로 로드됨.
> `templates/` 폴더는 Flask `render_template()`이 자동 탐색하므로 삭제 불가.

---

## 실행 방법

### 공통: 노트북 수정 후 라파 반영

```bash
# 노트북 터미널
git add . && git commit -m "메시지" && git push

# 라파 SSH 터미널
cd ~/LABA5_Bootcamp && git pull
```

### 1-1 실행 — 카메라 촬영

```bash
python3 ~/LABA5_Bootcamp/PHASE_1/1-1.py
```

- 저장 경로: `PHASE_1/python_test.jpg`
- `img.show()` 에러는 무시해도 됨 → 사진은 정상 저장됨

### 1-2 실행 — 라이브 스트리밍

```bash
python3 ~/LABA5_Bootcamp/PHASE_1/1-2.py
```

- 브라우저: `http://<라파IP>:5000`

### 1-3 실행 — 움직임 감지 + LED/부저

```bash
python3 ~/LABA5_Bootcamp/PHASE_1/1-3.py
```

- 움직임 감지 시 LED 점등 + 부저 울림
- 브라우저 화면에 `MOTION DETECTED` / `NO MOTION` 오버레이 표시
- 브라우저: `http://<라파IP>:5000`

### 1-4 실행 — 얼굴 인식 + LED

```bash
python3 ~/LABA5_Bootcamp/PHASE_1/1-4.py
```

- 얼굴 감지 시 초록 박스 + LED 점등
- 브라우저: `http://<라파IP>:5000`

### 1-5 실행 — 얼굴 추적 서보모터

```bash
python3 ~/LABA5_Bootcamp/PHASE_1/1-5.py
```

- 얼굴 x좌표에 따라 서보 좌우 회전
- 브라우저: `http://<라파IP>:5000`

### 1-6 실행 — 통합 보안 시스템

```bash
cd ~/LABA5_Bootcamp/PHASE_1
python3 1-6\(revised\).py
```

- 브라우저: `http://<라파IP>:5000`

---

## 주요 설정값 (1-5, 1-6 공통)

| 항목 | 값 | 설명 |
|---|---|---|
| `minNeighbors` | 5 | 얼굴 감지 민감도 (높을수록 오탐지 감소) |
| `THRESH_VAL` | 25 | 움직임 픽셀 변화 임계값 |
| `MOTION_PIXELS` | 4000 | 움직임 판정 최소 픽셀 수 |
| `SERVO_P_GAIN` | 0.12 | 서보 추적 P 게인 |
| `SERVO_DEADZONE` | 20px | 서보 미동작 허용 범위 |
| `INTRUDER_CAPTURE_COOLDOWN` | 5.0초 | 중복 촬영 방지 쿨다운 |
| `BLUE_RATIO_THRESHOLD` | 0.02 | 파란 카드 인식 최소 비율 |

---

## GPIO 핀 배치

| 기능 | GPIO 핀 (BCM) |
|---|---|
| LED (1-3, 1-4) / 초록 LED 인가자 (1-6) | GPIO 17 |
| 부저 (1-3) / 빨간 LED 침입자 (1-6) | GPIO 27 |
| 서보모터 (1-5, 1-6) | GPIO 18 |

---

## 트러블슈팅

### img.show() 에러 (1-1)
```
Error: no "view" rule for type "image/png"
```
라파 GUI 이미지 뷰어를 찾지 못해서 발생. 사진은 정상 저장됨. 무시해도 됨.

### qt.qpa.xcb: could not connect to display (SSH 실행 시)
SSH 터미널은 GUI 디스플레이가 없어서 `cv2.imshow` 사용 불가.
1-2 ~ 1-6은 Flask 스트리밍으로 수정했으므로 SSH에서 실행해도 브라우저로 확인 가능.

### 서보모터 오탐지로 좌우 계속 움직임
Haar Cascade가 아무것도 없는 장면을 얼굴로 잘못 인식하는 오탐지 현상.
`minNeighbors` 값을 높여서 민감도를 낮추면 해결됨.

### PWMSoftwareFallback 경고
```
To reduce servo jitter, use the pigpio pin factory.
```
서보 지터를 줄이려면 pigpio 핀 팩토리 사용 필요. 기능에는 문제없으므로 무시 가능.

### PermissionError: '/home/pi'
`CAPTURE_DIR`이 `/home/pi`로 설정되어 있으나 라파 계정이 `laba`라서 권한 오류 발생.
현재 코드에서는 이미 `/home/laba`로 수정 완료.
