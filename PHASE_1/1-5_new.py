import cv2
import time
import os
import threading
import RPi.GPIO as GPIO
from flask import Flask, Response
from picamera2 import Picamera2
from gpiozero import AngularServo

app = Flask(__name__)

# ===== 파란색 HSV 범위 =====
# 조명에 따라 조정 필요
BLUE_LOWER = (105, 140, 80)
BLUE_UPPER = (125, 255, 255)
MIN_AREA = 15000  # 카드 크기 이상만 반응

# ===== 부저 =====
BUZZER_PIN = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
buzzer_pwm = GPIO.PWM(BUZZER_PIN, 1000)
buzzer_active = False

def buzzer_on():
    global buzzer_active
    if not buzzer_active:
        buzzer_pwm.start(50)
        buzzer_active = True

def buzzer_off():
    global buzzer_active
    if buzzer_active:
        buzzer_pwm.stop()
        buzzer_active = False

# ===== 서보 (gpiozero) =====
servo = AngularServo(
    18,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.0005,
    max_pulse_width=0.0025
)

current_angle = 90
servo.angle = current_angle

Kp = 0.02
DEAD_ZONE = 50
MAX_STEP = 2
ANGLE_MIN = 10
ANGLE_MAX = 170

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

# ===== 카메라 =====
WIDTH, HEIGHT = 640, 480

output_frame = None
frame_lock = threading.Lock()

def camera_thread():
    global output_frame, current_angle

    picam2 = Picamera2()
    config = picam2.create_preview_configuration(
        main={"size": (WIDTH, HEIGHT)}
    )
    picam2.configure(config)
    picam2.start()
    time.sleep(2)
    print("Blue card tracking start")

    try:
        while True:
            frame = picam2.capture_array()
            display = frame.copy()

            center_x = WIDTH // 2

            # RGB → HSV 변환 후 파란색 마스크
            hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
            mask = cv2.inRange(hsv, BLUE_LOWER, BLUE_UPPER)

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            detected = False
            if contours:
                largest = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(largest)
                if area > MIN_AREA:
                    detected = True
                    x, y, w, h = cv2.boundingRect(largest)
                    obj_center_x = x + w // 2
                    error = obj_center_x - center_x

                    if abs(error) > DEAD_ZONE:
                        movement = clamp(-error * Kp, -MAX_STEP, MAX_STEP)
                        current_angle = clamp(current_angle + movement, ANGLE_MIN, ANGLE_MAX)
                        servo.angle = current_angle

                    print(f"area: {int(area)}  error: {error}  angle: {current_angle:.1f}  HSV_lower: {BLUE_LOWER}")

                    cv2.rectangle(display, (x, y), (x + w, y + h), (255, 128, 0), 2)
                    cv2.putText(display, f"Area:{int(area)} Error:{error:.0f}px", (10, 55),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 128, 0), 2)

            if detected:
                buzzer_on()
            else:
                buzzer_off()
                if current_angle != 90:
                    current_angle = 90
                    servo.angle = current_angle

            cv2.line(display, (center_x, 0), (center_x, HEIGHT), (255, 0, 0), 2)
            cv2.putText(display, f"Angle: {current_angle:.1f} deg", (10, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            display_bgr = cv2.cvtColor(display, cv2.COLOR_RGB2BGR)
            ok, jpeg = cv2.imencode(".jpg", display_bgr, [cv2.IMWRITE_JPEG_QUALITY, 75])
            if ok:
                with frame_lock:
                    output_frame = jpeg.tobytes()

    finally:
        picam2.stop()
        servo.detach()
        buzzer_off()
        GPIO.cleanup()
        print("Exited cleanly.")


# ===== Flask =====
@app.route("/")
def index():
    return '<img src="/video_feed">'

@app.route("/video_feed")
def video_feed():
    def generate():
        while True:
            with frame_lock:
                frame = output_frame
            if frame is None:
                time.sleep(0.03)
                continue
            yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
            time.sleep(0.03)
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    t = threading.Thread(target=camera_thread, daemon=True)
    t.start()
    print("Server running at http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, threaded=True)