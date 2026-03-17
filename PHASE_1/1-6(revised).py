import cv2
import numpy as np
import threading
import time
import json
import os
from datetime import datetime
from flask import Flask, Response, render_template, request
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

# 마이크로 서보(SG90류) 기준 예시값
# 서보마다 조금씩 다를 수 있으니 필요하면 미세 조정
servo = AngularServo(
    SERVO_PIN,
    min_angle=-90,
    max_angle=90,
    min_pulse_width=0.0005,
    max_pulse_width=0.0024
)

# =========================
# Haar Cascade 로드
# =========================
CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

# =========================
# 저장 경로
# =========================
CAPTURE_DIR = "/home/pi"
os.makedirs(CAPTURE_DIR, exist_ok=True)

# =========================
# 설정값 (튜닝 가능)
# =========================
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

MOTION_DIFF_THRESH = 40          # 프레임 차이 threshold
MOTION_PIXEL_THRESHOLD = 500     # 움직임 판정 픽셀 수
NO_MOTION_TIMEOUT = 5.0          # 5초 동안 움직임 없으면 대기 모드

FACE_MIN_SIZE = (60, 60)

# 파란색 카드 검출 HSV 범위
# 조명에 따라 조정 가능
BLUE_LOWER = np.array([90, 80, 50])
BLUE_UPPER = np.array([130, 255, 255])

BLUE_RATIO_THRESHOLD = 0.02      # ROI 안에서 파란색 비율 2% 이상이면 인가자

# 서보 추적 설정
SERVO_P_GAIN = 0.12              # 비례제어 게인
SERVO_DEADZONE = 20              # 중앙 오차 허용 범위(px)
SERVO_DIRECTION = 1              # 반대로 움직이면 -1로 바꿔라
SERVO_UPDATE_INTERVAL = 0.05     # 너무 자주 움직이지 않게

# 같은 침입자 반복 촬영 방지
INTRUDER_CAPTURE_COOLDOWN = 5.0  # 초

# =========================
# 공유 상태
# =========================
state = {
    "mode": "standby",           # standby / guard
    "motion": False,
    "pixels": 0,
    "faces": 0,
    "auth": "NONE",              # NONE / AUTHORIZED / INTRUDER
    "last_capture": "",
    "servo_angle": 0.0,
}

state_lock = threading.Lock()
frame_lock = threading.Lock()
output_frame = None

# 내부 제어용
last_motion_time = 0
last_intruder_capture_time = 0
last_servo_update_time = 0
current_servo_angle = 0.0


# =========================
# 유틸 함수
# =========================
def log_event(message):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")


def clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))


# 색 보정 계수 (파란 화면이면 blue_scale 낮추고 red_scale 높여라)
# 기본값 1.0 = 보정 없음
COLOR_RED_SCALE = 1.0
COLOR_GREEN_SCALE = 1.0
COLOR_BLUE_SCALE = 1.0   # 파란 치우침이면 0.7~0.85 정도로 낮춰라


def apply_color_correction(rgb_frame):
    """RGB 채널별 스케일 보정"""
    if COLOR_RED_SCALE == 1.0 and COLOR_GREEN_SCALE == 1.0 and COLOR_BLUE_SCALE == 1.0:
        return rgb_frame
    result = rgb_frame.astype(np.float32)
    result[:, :, 0] = np.clip(result[:, :, 0] * COLOR_RED_SCALE, 0, 255)
    result[:, :, 1] = np.clip(result[:, :, 1] * COLOR_GREEN_SCALE, 0, 255)
    result[:, :, 2] = np.clip(result[:, :, 2] * COLOR_BLUE_SCALE, 0, 255)
    return result.astype(np.uint8)


def set_mode_standby():
    global current_servo_angle
    green_led.off()
    red_led.off()

    # 원하면 대기 시 중앙 복귀
    current_servo_angle = 0.0
    servo.angle = current_servo_angle

    with state_lock:
        state["mode"] = "standby"
        state["motion"] = False
        state["auth"] = "NONE"
        state["servo_angle"] = current_servo_angle


def set_authorized():
    green_led.on()
    red_led.off()
    with state_lock:
        state["auth"] = "AUTHORIZED"


def set_intruder():
    green_led.off()
    red_led.on()
    with state_lock:
        state["auth"] = "INTRUDER"


def detect_blue_card(rgb_frame, face):
    """
    얼굴 주변 확장 영역에서 파란색 카드가 있는지 검사
    """
    x, y, w, h = face
    h_img, w_img, _ = rgb_frame.shape

    # 얼굴 주변을 조금 넓게 본다
    pad_x = int(w * 0.8)
    pad_y = int(h * 1.0)

    x1 = max(0, x - pad_x)
    y1 = max(0, y - pad_y)
    x2 = min(w_img, x + w + pad_x)
    y2 = min(h_img, y + h + pad_y)

    roi = rgb_frame[y1:y2, x1:x2]
    if roi.size == 0:
        return False, 0.0, (x1, y1, x2, y2)

    hsv = cv2.cvtColor(roi, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, BLUE_LOWER, BLUE_UPPER)

    blue_pixels = cv2.countNonZero(mask)
    total_pixels = roi.shape[0] * roi.shape[1]
    blue_ratio = blue_pixels / total_pixels if total_pixels > 0 else 0.0

    authorized = blue_ratio >= BLUE_RATIO_THRESHOLD
    return authorized, blue_ratio, (x1, y1, x2, y2)


def track_face_with_servo(face_center_x, frame_center_x):
    """
    얼굴 x좌표를 기준으로 좌우 추적
    """
    global current_servo_angle, last_servo_update_time

    now = time.time()
    if now - last_servo_update_time < SERVO_UPDATE_INTERVAL:
        return

    error = face_center_x - frame_center_x

    # 중앙 근처면 굳이 안 움직임
    if abs(error) < SERVO_DEADZONE:
        return

    normalized_error = error / frame_center_x  # 대략 -1 ~ +1
    delta = SERVO_DIRECTION * SERVO_P_GAIN * normalized_error * 90.0

    current_servo_angle += delta
    current_servo_angle = clamp(current_servo_angle, -90, 90)

    servo.angle = current_servo_angle
    last_servo_update_time = now

    with state_lock:
        state["servo_angle"] = round(current_servo_angle, 1)


def save_intruder_frame(display_bgr):
    global last_intruder_capture_time

    now = time.time()
    if now - last_intruder_capture_time < INTRUDER_CAPTURE_COOLDOWN:
        return None

    filename = datetime.now().strftime("intruder_%Y%m%d_%H%M%S.jpg")
    filepath = os.path.join(CAPTURE_DIR, filename)
    cv2.imwrite(filepath, display_bgr)

    last_intruder_capture_time = now

    with state_lock:
        state["last_capture"] = filename

    log_event(f"INTRUDER CAPTURED -> {filepath}")
    return filename


# =========================
# 카메라 스레드
# =========================
def camera_thread():
    global output_frame, last_motion_time

    picam2 = Picamera2()
    config = picam2.create_preview_configuration(
        main={"format": "RGB888", "size": (FRAME_WIDTH, FRAME_HEIGHT)}
    )
    picam2.configure(config)
    picam2.start()
    time.sleep(2)  # AWB 수렴 대기 시간 늘림

    # AWB 안정화 후 현재 게인 고정 (파란색 치우침 방지)
    metadata = picam2.capture_metadata()
    colour_gains = metadata.get("ColourGains", (2.0, 1.5))  # (red_gain, blue_gain)
    # blue_gain을 낮추거나 red_gain을 높여서 파란 치우침 보정
    # 기본값보다 파란 화면이면 blue_gain을 줄여라 (예: 1.2~1.5)
    picam2.set_controls({"ColourGains": (colour_gains[0], colour_gains[1])})

    prev_gray_blur = None
    current_mode = "standby"
    last_auth_state = "NONE"

    log_event("Camera started")
    set_mode_standby()

    try:
        while True:
            frame = picam2.capture_array()  # RGB
            frame = apply_color_correction(frame)
            display = frame.copy()

            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            gray_blur = cv2.GaussianBlur(gray, (21, 21), 0)

            if prev_gray_blur is None:
                prev_gray_blur = gray_blur
                continue

            # -------------------------
            # 1) 움직임 감지
            # -------------------------
            diff = cv2.absdiff(prev_gray_blur, gray_blur)
            _, thresh = cv2.threshold(diff, MOTION_DIFF_THRESH, 255, cv2.THRESH_BINARY)
            motion_pixels = cv2.countNonZero(thresh)
            motion_detected = motion_pixels > MOTION_PIXEL_THRESHOLD

            now = time.time()

            if motion_detected:
                last_motion_time = now
                if current_mode != "guard":
                    current_mode = "guard"
                    log_event("Motion detected -> GUARD MODE")

            # 5초 동안 움직임 없으면 standby
            if current_mode == "guard" and (now - last_motion_time > NO_MOTION_TIMEOUT):
                current_mode = "standby"
                set_mode_standby()
                last_auth_state = "NONE"
                log_event("No motion for 5 sec -> STANDBY MODE")

            # 상태 반영
            with state_lock:
                state["mode"] = current_mode
                state["motion"] = motion_detected
                state["pixels"] = motion_pixels

            # -------------------------
            # 2) 기본 오버레이
            # -------------------------
            mode_text = f"MODE: {current_mode.upper()}"
            cv2.putText(display, mode_text, (10, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            cv2.putText(display, f"Motion Pixels: {motion_pixels}", (10, 55),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            if current_mode == "guard":
                cv2.putText(display, "!! MOTION DETECTED", (10, 85),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

            # -------------------------
            # 3) 경계 모드일 때만 얼굴 검출
            # -------------------------
            face_count = 0
            auth_state = "NONE"

            if current_mode == "guard":
                faces = face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=FACE_MIN_SIZE
                )

                face_count = len(faces)

                with state_lock:
                    state["faces"] = face_count

                if face_count > 0:
                    # 가장 큰 얼굴 선택 -> 서보 추적 기준
                    largest_face = max(faces, key=lambda f: f[2] * f[3])
                    face_center_x = largest_face[0] + largest_face[2] // 2
                    frame_center_x = FRAME_WIDTH // 2

                    # 서보 추적
                    track_face_with_servo(face_center_x, frame_center_x)

                    # 얼굴들 표시
                    for (x, y, w, h) in faces:
                        cv2.rectangle(display, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    # 가장 큰 얼굴 주변에서 파란 카드 검사
                    authorized, blue_ratio, roi_box = detect_blue_card(frame, largest_face)
                    rx1, ry1, rx2, ry2 = roi_box

                    cv2.rectangle(display, (rx1, ry1), (rx2, ry2), (255, 255, 0), 2)
                    cv2.putText(display, f"Blue Ratio: {blue_ratio:.3f}", (rx1, max(20, ry1 - 10)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 0), 2)

                    if authorized:
                        auth_state = "AUTHORIZED"
                        set_authorized()

                        cv2.putText(display, "AUTHORIZED", (10, 115),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                        if last_auth_state != "AUTHORIZED":
                            log_event("Authorized person detected")
                    else:
                        auth_state = "INTRUDER"
                        set_intruder()

                        cv2.putText(display, "INTRUDER", (10, 115),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

                        if last_auth_state != "INTRUDER":
                            log_event("Intruder detected")

                        # 침입자 자동 촬영
                        display_bgr_for_save = cv2.cvtColor(display, cv2.COLOR_RGB2BGR)
                        save_intruder_frame(display_bgr_for_save)

                else:
                    # 경계 모드인데 얼굴이 없으면 LED는 끄고 대기
                    green_led.off()
                    red_led.off()
                    auth_state = "NONE"

            else:
                with state_lock:
                    state["faces"] = 0

            with state_lock:
                state["auth"] = auth_state

            last_auth_state = auth_state

            # 서보 각도 표시
            with state_lock:
                angle_text = state["servo_angle"]
            cv2.putText(display, f"Servo: {angle_text} deg", (10, 145),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # 스트리밍용 JPEG 변환
            display_bgr = cv2.cvtColor(display, cv2.COLOR_RGB2BGR)
            ok, jpeg = cv2.imencode(".jpg", display_bgr, [cv2.IMWRITE_JPEG_QUALITY, 75])

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
# Flask 라우팅
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
                frame = output_frame
            if frame is None:
                time.sleep(0.03)
                continue

            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
            time.sleep(0.03)

    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/snapshot")
def snapshot():
    with frame_lock:
        frame = output_frame
    if frame is None:
        return "", 503
    return Response(frame, mimetype="image/jpeg")


@app.route("/status")
def status_poll():
    with state_lock:
        data = {
            "mode": state["mode"],
            "motion": state["motion"],
            "pixels": state["pixels"],
            "faces": state["faces"],
            "auth": state["auth"],
            "last_capture": state["last_capture"],
            "servo_angle": state["servo_angle"],
        }
    return json.dumps(data), 200, {"Content-Type": "application/json"}


@app.route("/set_motion_threshold", methods=["POST"])
def set_motion_threshold():
    global MOTION_PIXEL_THRESHOLD
    data = request.get_json()
    if data and "threshold" in data:
        MOTION_PIXEL_THRESHOLD = int(data["threshold"])
        log_event(f"Motion threshold changed -> {MOTION_PIXEL_THRESHOLD}")
    return "", 204


@app.route("/set_p_gain", methods=["POST"])
def set_p_gain():
    global SERVO_P_GAIN
    data = request.get_json()
    if data and "p_gain" in data:
        SERVO_P_GAIN = float(data["p_gain"])
        log_event(f"Servo P gain changed -> {SERVO_P_GAIN}")
    return "", 204


# =========================
# 실행
# =========================
if __name__ == "__main__":
    t = threading.Thread(target=camera_thread, daemon=True)
    t.start()

    log_event("Starting server on http://0.0.0.0:5000")
    log_event(f"Intruder captures saved to: {CAPTURE_DIR}")
    app.run(host="0.0.0.0", port=5000, threaded=True)