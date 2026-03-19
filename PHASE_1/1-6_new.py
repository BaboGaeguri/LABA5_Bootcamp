import cv2
import time
import os
import threading
import RPi.GPIO as GPIO
from collections import deque
from datetime import datetime
from flask import Flask, Response
from picamera2 import Picamera2
from gpiozero import AngularServo, LED

app = Flask(__name__)

# ===== 핀 설정 =====
GREEN_LED = LED(17)
RED_LED   = LED(27)

BUZZER_PIN = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
buzzer_pwm = GPIO.PWM(BUZZER_PIN, 1000)
buzzer_active = False

# ===== 서보 =====
servo = AngularServo(
    18,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.0005,
    max_pulse_width=0.0025
)
current_angle = 90
servo.angle = current_angle

# ===== 서보 추적 파라미터 =====
Kp             = 0.02
DEAD_ZONE      = 100   # 중앙 ±100px 이내면 서보 정지
MAX_STEP       = 2
ANGLE_MIN      = 10
ANGLE_MAX      = 170
ERROR_SMOOTH   = 7
SERVO_INTERVAL = 0.5   # 서보 업데이트 최소 간격 (초)
error_history  = deque(maxlen=ERROR_SMOOTH)
last_servo_t   = 0.0

# ===== 색상 HSV 범위 =====
BLUE_LOWER  = (105, 180, 80)
BLUE_UPPER  = (125, 255, 255)
RED_LOWER1  = (0,   120, 80)
RED_UPPER1  = (10,  255, 255)
RED_LOWER2  = (170, 120, 80)
RED_UPPER2  = (180, 255, 255)
MIN_AREA    = 15000

# ===== 움직임 감지 파라미터 =====
MOTION_THRESHOLD  = 30    # 픽셀 diff 임계값
MOTION_MIN_PIXELS = 3000  # 변화 픽셀 수 최소값
STANDBY_TIMEOUT   = 5.0   # 움직임 없으면 대기 모드 복귀 (초)

# ===== 증거 촬영 파라미터 =====
CAPTURE_COOLDOWN  = 10.0  # 같은 침입자 반복 촬영 방지 (초)
CAPTURE_DIR       = "/home/laba"

# ===== 상태 =====
STATE_STANDBY    = "STANDBY"
STATE_ALERT      = "ALERT"
STATE_AUTHORIZED = "AUTHORIZED"
STATE_INTRUDER   = "INTRUDER"

# ===== 공유 변수 =====
output_frame   = None
frame_lock     = threading.Lock()

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

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

def all_leds_off():
    GREEN_LED.off()
    RED_LED.off()

def detect_card(hsv):
    """파란색/빨간색 카드 감지. (card_type, x, y, w, h) 반환. 없으면 (None, ...)"""
    # 파란색 우선 확인
    blue_mask = cv2.inRange(hsv, BLUE_LOWER, BLUE_UPPER)
    blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if blue_contours:
        largest = max(blue_contours, key=cv2.contourArea)
        if cv2.contourArea(largest) > MIN_AREA:
            x, y, w, h = cv2.boundingRect(largest)
            return "BLUE", x, y, w, h

    # 빨간색 확인
    red_mask = cv2.inRange(hsv, RED_LOWER1, RED_UPPER1) | cv2.inRange(hsv, RED_LOWER2, RED_UPPER2)
    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if red_contours:
        largest = max(red_contours, key=cv2.contourArea)
        if cv2.contourArea(largest) > MIN_AREA:
            x, y, w, h = cv2.boundingRect(largest)
            return "RED", x, y, w, h

    return None, 0, 0, 0, 0

def save_intruder_photo(frame_bgr):
    ts  = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(CAPTURE_DIR, f"intruder_{ts}.jpg")
    cv2.imwrite(path, frame_bgr)
    print(f"[CAPTURE] 증거 저장: {path}")
    return path

def camera_thread():
    global output_frame, current_angle

    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"size": (640, 480)})
    picam2.configure(config)
    picam2.start()
    time.sleep(2)

    WIDTH, HEIGHT = 640, 480
    center_x = WIDTH // 2

    prev_gray      = None
    state          = STATE_STANDBY
    last_motion_t  = time.time()
    last_capture_t = 0

    print("[INFO] Smart Guard System 시작")

    try:
        while True:
            frame   = picam2.capture_array()
            display = frame.copy()
            gray    = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            gray    = cv2.GaussianBlur(gray, (21, 21), 0)
            hsv     = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

            # ── 움직임 감지 ──
            motion_detected = False
            if prev_gray is not None:
                diff        = cv2.absdiff(prev_gray, gray)
                _, thresh   = cv2.threshold(diff, MOTION_THRESHOLD, 255, cv2.THRESH_BINARY)
                motion_px   = cv2.countNonZero(thresh)
                if motion_px > MOTION_MIN_PIXELS:
                    motion_detected = True
                    last_motion_t   = time.time()
            prev_gray = gray

            # ── 상태 전이 ──
            if motion_detected:
                if state == STATE_STANDBY:
                    state = STATE_ALERT
                    print("[EVENT] 움직임 감지 → 경계 모드")
            else:
                if state != STATE_STANDBY:
                    if time.time() - last_motion_t > STANDBY_TIMEOUT:
                        state = STATE_STANDBY
                        all_leds_off()
                        buzzer_off()
                        if current_angle != 90:
                            current_angle = 90
                            servo.angle   = current_angle
                        print("[EVENT] 대기 모드 복귀")

            # ── 카드 감지 및 추적 (경계 모드 이상일 때) ──
            card_type = None
            if state != STATE_STANDBY:
                card_type, cx, cy, cw, ch = detect_card(hsv)

                if card_type is not None:
                    # 서보 추적
                    obj_center_x = cx + cw // 2
                    error        = obj_center_x - center_x
                    error_history.append(error)
                    smooth_error = sum(error_history) / len(error_history)

                    now = time.time()
                    if abs(smooth_error) > DEAD_ZONE and now - last_servo_t > SERVO_INTERVAL:
                        movement      = clamp(-smooth_error * Kp, -MAX_STEP, MAX_STEP)
                        current_angle = clamp(current_angle + movement, ANGLE_MIN, ANGLE_MAX)
                        servo.angle   = current_angle
                        last_servo_t  = now

                    # 상태 결정
                    if card_type == "BLUE":
                        state = STATE_AUTHORIZED
                        GREEN_LED.on()
                        RED_LED.off()
                        buzzer_off()
                        color_box = (0, 200, 0)
                        label     = "AUTHORIZED"
                    else:  # RED
                        state = STATE_INTRUDER
                        RED_LED.on()
                        GREEN_LED.off()
                        buzzer_on()
                        color_box = (0, 0, 255)
                        label     = "INTRUDER"

                        # 증거 촬영 (쿨다운 적용)
                        if time.time() - last_capture_t > CAPTURE_COOLDOWN:
                            display_bgr = cv2.cvtColor(display, cv2.COLOR_RGB2BGR)
                            save_intruder_photo(display_bgr)
                            last_capture_t = time.time()

                    cv2.rectangle(display, (cx, cy), (cx + cw, cy + ch), color_box, 2)
                    cv2.putText(display, label, (cx, cy - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color_box, 2)
                    print(f"[{state}] card={card_type}  error={error}  angle={current_angle:.1f}")

                else:
                    # 카드 없음 → 경계 모드 유지
                    if state in (STATE_AUTHORIZED, STATE_INTRUDER):
                        state = STATE_ALERT
                    all_leds_off()
                    buzzer_off()
                    if current_angle != 90:
                        current_angle = 90
                        servo.angle   = current_angle
                    error_history.clear()

            # ── 화면 오버레이 ──
            cv2.line(display, (center_x, 0), (center_x, HEIGHT), (100, 100, 100), 1)

            state_color = {
                STATE_STANDBY:    (180, 180, 180),
                STATE_ALERT:      (0,   200, 255),
                STATE_AUTHORIZED: (0,   200, 0),
                STATE_INTRUDER:   (0,   0,   255),
            }
            cv2.putText(display, f"STATE: {state}", (10, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, state_color[state], 2)
            cv2.putText(display, f"Servo: {current_angle:.1f} deg", (10, 55),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            if state == STATE_ALERT:
                cv2.putText(display, "⚠ MOTION DETECTED", (WIDTH // 2 - 160, HEIGHT - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 200, 255), 2)

            display_bgr = cv2.cvtColor(display, cv2.COLOR_RGB2BGR)
            ok, jpeg    = cv2.imencode(".jpg", display_bgr, [cv2.IMWRITE_JPEG_QUALITY, 75])
            if ok:
                with frame_lock:
                    output_frame = jpeg.tobytes()

    finally:
        picam2.stop()
        servo.detach()
        buzzer_off()
        all_leds_off()
        GPIO.cleanup()
        print("[INFO] 종료")


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