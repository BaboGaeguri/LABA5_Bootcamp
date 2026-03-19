import cv2
import threading
import time
import json
from datetime import datetime
from flask import Flask, Response, render_template
from picamera2 import Picamera2
from gpiozero import LED, AngularServo


app = Flask(__name__)

# =========================
# GPIO 설정
# =========================
GREEN_LED_PIN = 17
RED_LED_PIN = 27
SERVO_PIN = 18

green_led = LED(GREEN_LED_PIN)
red_led = LED(RED_LED_PIN)

servo = AngularServo(
    SERVO_PIN,
    min_angle=-90,
    max_angle=90,
    min_pulse_width=0.0005,
    max_pulse_width=0.0024
)

# =========================
# Haar Cascade
# =========================
CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

# =========================
# 설정값
# =========================
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

MOTION_DIFF_THRESH = 40
MOTION_PIXEL_THRESHOLD = 500
NO_MOTION_TIMEOUT = 5.0

FACE_MIN_SIZE = (60, 60)
FACE_CONFIRM_SECONDS = 3       # 3초 연속 감지 후 서보 작동
FACE_LOCK_COOLDOWN = 5          # 얼굴 사라진 후 5초 대기

# 서보 추적
SERVO_P_GAIN = 0.12
SERVO_DEADZONE = 20
SERVO_DIRECTION = 1
SERVO_UPDATE_INTERVAL = 0.05

# =========================
# 공유 상태
# =========================
state = {
    "mode": "standby",
    "motion": False,
    "pixels": 0,
    "faces": 0,
    "servo_angle": 0.0,
}

state_lock = threading.Lock()
frame_lock = threading.Lock()
output_frame = None

# 내부 제어용
last_motion_time = 0
last_servo_update_time = 0
current_servo_angle = 0.0

# 얼굴 추적용
face_first_seen_time = 0
face_continuous = False
tracked_face_center = None
face_lost_time = 0


# =========================
# 유틸
# =========================
def log_event(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def clamp(val, lo, hi):
    return max(lo, min(hi, val))


def track_face_with_servo(face_cx, frame_cx):
    global current_servo_angle, last_servo_update_time

    now = time.time()
    if now - last_servo_update_time < SERVO_UPDATE_INTERVAL:
        return

    error = face_cx - frame_cx
    if abs(error) < SERVO_DEADZONE:
        return

    delta = SERVO_DIRECTION * SERVO_P_GAIN * (error / frame_cx) * 90.0
    current_servo_angle = clamp(current_servo_angle + delta, -90, 90)

    servo.angle = current_servo_angle
    last_servo_update_time = now

    with state_lock:
        state["servo_angle"] = round(current_servo_angle, 1)


# =========================
# 카메라 스레드
# =========================
def camera_thread():
    global output_frame, last_motion_time
    global face_continuous, face_first_seen_time
    global tracked_face_center, face_lost_time
    global current_servo_angle

    picam2 = Picamera2()
    config = picam2.create_preview_configuration(
        main={"format": "RGB888", "size": (FRAME_WIDTH, FRAME_HEIGHT)}
    )
    picam2.configure(config)
    picam2.start()
    time.sleep(2)
    picam2.set_controls({"AwbEnable": True})

    prev_gray_blur = None
    current_mode = "standby"

    # 서보 초기 위치 고정
    current_servo_angle = 0.0
    servo.angle = 0

    log_event("Camera started")

    try:
        while True:
            frame = picam2.capture_array()  # BGR로 취급
            display = frame.copy()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_blur = cv2.GaussianBlur(gray, (21, 21), 0)

            if prev_gray_blur is None:
                prev_gray_blur = gray_blur
                continue

            # 1) 움직임 감지
            diff = cv2.absdiff(prev_gray_blur, gray_blur)
            _, thresh = cv2.threshold(diff, MOTION_DIFF_THRESH, 255, cv2.THRESH_BINARY)
            motion_pixels = cv2.countNonZero(thresh)
            motion_detected = motion_pixels > MOTION_PIXEL_THRESHOLD
            now = time.time()

            if motion_detected:
                last_motion_time = now
                if current_mode != "guard":
                    current_mode = "guard"
                    log_event("Motion -> GUARD")

            if current_mode == "guard" and (now - last_motion_time > NO_MOTION_TIMEOUT):
                current_mode = "standby"
                current_servo_angle = 0.0
                servo.angle = 0
                face_continuous = False
                tracked_face_center = None
                face_lost_time = 0
                green_led.off()
                red_led.off()
                log_event("No motion -> STANDBY")

            with state_lock:
                state["mode"] = current_mode
                state["motion"] = motion_detected
                state["pixels"] = motion_pixels

            # 2) 오버레이
            cv2.putText(display, f"MODE: {current_mode.upper()}", (10, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # 3) 경계 모드 → 얼굴 검출 & 서보 추적
            face_count = 0

            if current_mode == "guard":
                faces = face_cascade.detectMultiScale(
                    gray, scaleFactor=1.1, minNeighbors=5, minSize=FACE_MIN_SIZE
                )
                face_count = len(faces)

                # 쿨다운 체크
                in_cooldown = (tracked_face_center is None
                               and face_lost_time > 0
                               and now - face_lost_time < FACE_LOCK_COOLDOWN)

                if face_count > 0 and not in_cooldown:
                    # 연속 감지 타이머
                    if not face_continuous:
                        face_first_seen_time = now
                        face_continuous = True

                    # 추적 대상 선택: 락온 중이면 가장 가까운 얼굴, 아니면 가장 큰 얼굴
                    if tracked_face_center is not None:
                        def dist(f):
                            cx = f[0] + f[2] // 2
                            cy = f[1] + f[3] // 2
                            return (cx - tracked_face_center[0])**2 + (cy - tracked_face_center[1])**2
                        target = min(faces, key=dist)
                    else:
                        target = max(faces, key=lambda f: f[2] * f[3])

                    tcx = target[0] + target[2] // 2
                    tcy = target[1] + target[3] // 2
                    tracked_face_center = (tcx, tcy)
                    face_lost_time = 0

                    # 3초 이상 연속 감지 시 서보 추적 시작
                    if now - face_first_seen_time >= FACE_CONFIRM_SECONDS:
                        track_face_with_servo(tcx, FRAME_WIDTH // 2)
                        red_led.on()
                        green_led.off()
                        cv2.putText(display, "TRACKING", (10, 85),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    else:
                        # 아직 확인 중
                        remaining = FACE_CONFIRM_SECONDS - (now - face_first_seen_time)
                        cv2.putText(display, f"Confirming... {remaining:.1f}s", (10, 85),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

                    # 얼굴 사각형 표시
                    for (x, y, w, h) in faces:
                        cv2.rectangle(display, (x, y), (x + w, y + h), (0, 255, 0), 2)

                else:
                    # 얼굴 없거나 쿨다운 중
                    face_continuous = False
                    if tracked_face_center is not None:
                        tracked_face_center = None
                        face_lost_time = time.time()
                    green_led.off()
                    red_led.off()

                    if in_cooldown:
                        remaining = FACE_LOCK_COOLDOWN - (now - face_lost_time)
                        cv2.putText(display, f"Cooldown {remaining:.1f}s", (10, 85),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 255), 2)

            with state_lock:
                state["faces"] = face_count

            # 서보 각도 표시
            cv2.putText(display, f"Servo: {current_servo_angle:.1f} deg", (10, FRAME_HEIGHT - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # JPEG 변환
            ok, jpeg = cv2.imencode(".jpg", display, [cv2.IMWRITE_JPEG_QUALITY, 75])
            if ok:
                with frame_lock:
                    output_frame = jpeg.tobytes()

            prev_gray_blur = gray_blur

    finally:
        log_event("Shutting down...")
        green_led.off()
        red_led.off()
        servo.angle = 0
        picam2.stop()


# =========================
# Flask
# =========================
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    def generate():
        global output_frame
        while True:
            with frame_lock:
                f = output_frame
            if f is None:
                time.sleep(0.03)
                continue
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" + f + b"\r\n")
            time.sleep(0.03)
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/status")
def status_poll():
    with state_lock:
        data = dict(state)
    return json.dumps(data), 200, {"Content-Type": "application/json"}


# =========================
# 실행
# =========================
if __name__ == "__main__":
    t = threading.Thread(target=camera_thread, daemon=True)
    t.start()
    log_event("Starting server on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, threaded=True)
