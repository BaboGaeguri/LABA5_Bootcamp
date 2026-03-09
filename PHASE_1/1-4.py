import cv2
import time
import RPi.GPIO as GPIO
import os
import urllib.request
from picamera2 import Picamera2

print("FACE DETECTION STARTED")

# -----------------------------
# 0️⃣ Haar Cascade 자동 다운로드
# -----------------------------
xml_filename = 'haarcascade_frontalface_default.xml'

if not os.path.exists(xml_filename):
    print("Downloading Haar Cascade...")
    url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
    urllib.request.urlretrieve(url, xml_filename)
    print("Download complete!")

face_cascade = cv2.CascadeClassifier(xml_filename)

if face_cascade.empty():
    print("ERROR: Could not load Haar Cascade.")
    exit()

# -----------------------------
# 1️⃣ GPIO 설정
# -----------------------------
LED_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, False)

# -----------------------------
# 2️⃣ Picamera2 설정 (RGB 기본 유지)
# -----------------------------
picam2 = Picamera2()
picam2.configure(
    picam2.create_preview_configuration(
        main={"size": (640, 480)}
    )
)
picam2.start()

time.sleep(2)

print("Press 'q' to quit.")

try:
    while True:
        # 📷 RGB 프레임 받기
        frame = picam2.capture_array()

        # 1️⃣ 그레이스케일 변환 (RGB 기준)
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # 2️⃣ 얼굴 검출
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60)
        )

        # 3️⃣ LED 제어
        if len(faces) > 0:
            GPIO.output(LED_PIN, True)
            status = "FACE DETECTED"
        else:
            GPIO.output(LED_PIN, False)
            status = "NO FACE"

        # 4️⃣ 화면 출력용 RGB → BGR 변환
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # 5️⃣ 얼굴 박스 그리기
        for (x, y, w, h) in faces:
            cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 상태 텍스트 표시
        cv2.putText(
            frame_bgr,
            status,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255) if len(faces) > 0 else (0, 255, 0),
            2
        )

        cv2.imshow("Face Detection", frame_bgr)

        # 종료 키
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break

finally:
    GPIO.output(LED_PIN, False)
    GPIO.cleanup()
    picam2.stop()
    cv2.destroyAllWindows()
    print("EXITED CLEANLY")