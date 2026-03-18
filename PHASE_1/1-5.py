import cv2
import time
import os
import threading
import urllib.request
from flask import Flask, Response
from picamera2 import Picamera2
from gpiozero import AngularServo

app = Flask(__name__)

# -----------------------------
# Haar 다운로드
# -----------------------------
PHASE1_DIR = os.path.dirname(os.path.abspath(__file__))
xml_filename = os.path.join(PHASE1_DIR, 'haarcascade_frontalface_default.xml')
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

output_frame = None
frame_lock = threading.Lock()

def camera_thread():
    global output_frame, current_angle

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
            frame = picam2.capture_array("main")
            display = frame.copy()

            height, width, _ = frame.shape
            center_x = width // 2

            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=10,
                minSize=(80, 80)
            )

            movement = 0
            if len(faces) > 0:
                x, y, w, h = max(faces, key=lambda r: r[2] * r[3])
                face_center_x = x + w // 2

                error = face_center_x - center_x

                if abs(error) > dead_zone:
                    movement = clamp(error * Kp, -max_step, max_step)
                    current_angle = clamp(current_angle + movement, ANGLE_MIN, ANGLE_MAX)
                    servo.angle = current_angle

                print("error:", error, "movement:", movement, "angle:", current_angle)

                cv2.rectangle(display, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(display, f"Error: {error:.0f}px", (10, 55),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # 중앙선
            cv2.line(display, (center_x, 0), (center_x, height), (255, 0, 0), 2)

            # 각도 오버레이
            cv2.putText(display, f"Angle: {current_angle:.1f} deg", (10, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # JPEG 변환
            display_bgr = cv2.cvtColor(display, cv2.COLOR_RGB2BGR)
            ok, jpeg = cv2.imencode(".jpg", display_bgr, [cv2.IMWRITE_JPEG_QUALITY, 75])
            if ok:
                with frame_lock:
                    output_frame = jpeg.tobytes()

    finally:
        picam2.stop()
        picam2.close()
        servo.detach()
        print("Program terminated safely.")


# -----------------------------
# Flask 스트리밍
# -----------------------------
@app.route("/")
def index():
    return """
    <html><body style="background:#111;color:#fff;text-align:center;">
    <h2>Face Tracking - Live</h2>
    <img src="/video_feed" width="640" height="480">
    </body></html>
    """

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


# -----------------------------
# 실행
# -----------------------------
if __name__ == "__main__":
    t = threading.Thread(target=camera_thread, daemon=True)
    t.start()
    print("Server running at http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, threaded=True)
