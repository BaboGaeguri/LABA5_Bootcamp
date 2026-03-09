import cv2
import time
import os
import urllib.request
import numpy as np
from datetime import datetime
from picamera2 import Picamera2
import RPi.GPIO as GPIO
from gpiozero import AngularServo



print("=== SMART SECURITY SYSTEM STARTING ===")

# =============================
# GPIO SETUP
# =============================
RED_LED = 17
GREEN_LED = 27
SERVO_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)

GPIO.output(RED_LED, False)
GPIO.output(GREEN_LED, False)

# =============================
# SERVO SETUP
# =============================
servo = AngularServo(
    18,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.0005,
    max_pulse_width=0.0025
)
current_angle = 90
servo.angle = current_angle

Kp = 0.06
dead_zone = 80
max_step = 5
ANGLE_MIN = 10
ANGLE_MAX = 170

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

# =============================
# HAAR CASCADE
# =============================
xml_filename = "haarcascade_frontalface_default.xml"
if not os.path.exists(xml_filename):
    url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
    urllib.request.urlretrieve(url, xml_filename)

face_cascade = cv2.CascadeClassifier(xml_filename)

# =============================
# CAMERA SETUP
# =============================
WIDTH, HEIGHT = 640, 480

picam2 = Picamera2()
config = picam2.create_video_configuration(
    main={"size": (WIDTH, HEIGHT), "format": "RGB888"}
)
picam2.configure(config)
picam2.start()
time.sleep(2)

# =============================
# MOTION DETECTION 초기화
# =============================
frame1 = picam2.capture_array("main")
prev_gray = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)
prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)

THRESH_VAL = 60
MOTION_PIXELS = 20000

motion_mode = False
last_motion_time = 0
last_capture_time = 0
CAPTURE_COOLDOWN = 10
face_x_list = []
face_detect_count = 0


print("[SYSTEM READY]")

# =============================
# MAIN LOOP
# =============================
try:
    while True:
        frame = picam2.capture_array("main")

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        gray = cv2.equalizeHist(gray)
        gray_blur = cv2.GaussianBlur(gray, (21, 21), 0)

        # ===== Motion Detection =====
        diff = cv2.absdiff(prev_gray, gray_blur)
        _, thresh = cv2.threshold(diff, THRESH_VAL, 255, cv2.THRESH_BINARY)
        motion_score = cv2.countNonZero(thresh)

        if motion_score > MOTION_PIXELS:
            motion_mode = True
            last_motion_time = time.time()

        if motion_mode and time.time() - last_motion_time > 5:
            motion_mode = False
            GPIO.output(RED_LED, False)
            GPIO.output(GREEN_LED, False)

        prev_gray = gray_blur
        status_text = "STANDBY"

        if motion_mode:
            status_text = "MOTION DETECTED"

            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=3,
                minSize=(40, 40)
            )

            if len(faces) > 0:
                face_detect_count += 1
            else:
                face_detect_count = 0
                face_x_list = []  # ← 얼굴 없으면 즉시 초기화

            if face_detect_count >= 8:
                x, y, w, h = max(faces, key=lambda r: r[2]*r[3])
                if (w*h) > 5000:
                    face_center_x = x + w // 2
                    center_x = WIDTH // 2

                    # ===== BLUE CARD AUTH =====
                    roi = frame[y:y+h, x:min(x+w*2, WIDTH)]
                    hsv = cv2.cvtColor(roi, cv2.COLOR_RGB2HSV)

                    lower_blue = np.array([100, 120, 70])
                    upper_blue = np.array([130, 255, 255])

                    mask = cv2.inRange(hsv, lower_blue, upper_blue)

                    kernel = np.ones((5, 5), np.uint8)
                    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
                    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

                    blue_pixels = cv2.countNonZero(mask)
                    roi_area = w * h
                    blue_ratio = blue_pixels / roi_area

                    if blue_pixels > 800 and blue_ratio > 0.10:
                        status_text = "AUTHORIZED"
                        GPIO.output(GREEN_LED, True)
                        GPIO.output(RED_LED, False)
                    else:
                        status_text = "INTRUDER"
                        GPIO.output(RED_LED, True)
                        GPIO.output(GREEN_LED, False)

                        if time.time() - last_capture_time > CAPTURE_COOLDOWN:
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            filename = f"/home/pi/intruder_{timestamp}.jpg"
                            cv2.imwrite(filename, frame)
                            last_capture_time = time.time()

                    cv2.rectangle(frame, (x, y),
                                (x+w, y+h), (0, 255, 0), 2)

                    # ===== SERVO TRACKING =====
                    face_x_list.append(face_center_x)

                    if len(face_x_list) > 5:
                        face_x_list.pop(0)

                    smooth_x = sum(face_x_list) / len(face_x_list)
                    error = center_x - smooth_x

                    if abs(error) > dead_zone:
                        movement = clamp(error * Kp, -max_step, max_step)
                        current_angle = clamp(current_angle + movement,
                                            ANGLE_MIN, ANGLE_MAX)
                        servo.angle = current_angle

                else:
                    face_x_list = []  # ← 얼굴 크기 미달 시 초기화

        cv2.putText(frame, status_text, (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 0, 0) if "INTRUDER" in status_text else (0, 255, 0),
                    2)

        cv2.imshow("Smart Security System", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    GPIO.cleanup()
    picam2.stop()
    cv2.destroyAllWindows()
    print("=== SYSTEM SHUTDOWN COMPLETE ===")