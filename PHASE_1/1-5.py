import cv2
import time
import os
import urllib.request
from picamera2 import Picamera2
from gpiozero import AngularServo

# -----------------------------
# Haar 다운로드
# -----------------------------
xml_filename = 'haarcascade_frontalface_default.xml'
if not os.path.exists(xml_filename):
    url = 'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml'
    urllib.request.urlretrieve(url, xml_filename)

face_cascade = cv2.CascadeClassifier(xml_filename)

# -----------------------------
# 서보 설정
# -----------------------------
servo = AngularServo(
    18,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.0005,
    max_pulse_width=0.0025
)

current_angle = 90
servo.angle = current_angle

# P제어 파라미터
Kp = 0.06
dead_zone = 25
max_step = 4
ANGLE_MIN = 10
ANGLE_MAX = 170

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

# -----------------------------
# 카메라 설정
# -----------------------------
WIDTH, HEIGHT = 640, 480

picam2 = Picamera2()
config = picam2.create_video_configuration(
    main={"size": (WIDTH, HEIGHT), "format": "RGB888"}
)
picam2.configure(config)
picam2.start()

time.sleep(2)
print("Face tracking start")

try:
    while True:
        frame = picam2.capture_array("main")  # RGB 그대로 사용

        height, width, _ = frame.shape
        center_x = width // 2

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(60, 60)
        )

        if len(faces) > 0:
            x, y, w, h = max(faces, key=lambda r: r[2] * r[3])
            face_center_x = x + w // 2

            error = face_center_x - center_x

            if abs(error) > dead_zone:
                movement = clamp(error * Kp, -max_step, max_step)
                current_angle = clamp(current_angle + movement,
                                      ANGLE_MIN, ANGLE_MAX)
                servo.angle = current_angle
               
            print("error:", error,
                "movement:", movement,
                 "angle:", current_angle)

                

            cv2.rectangle(frame, (x, y),
                          (x + w, y + h), (0, 255, 0), 2)

        cv2.line(frame,
                 (center_x, 0),
                 (center_x, height),
                 (255, 0, 0), 2)

        cv2.imshow("Face Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    picam2.stop()
    picam2.close()
    cv2.destroyAllWindows()
    servo.detach()
    print("Program terminated safely.")