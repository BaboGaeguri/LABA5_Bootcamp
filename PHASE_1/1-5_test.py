import cv2
import time
import os
import threading
from flask import Flask, Response
from picamera2 import Picamera2
from gpiozero import AngularServo

app = Flask(__name__)

# ===== Haar Cascade (1-4 방식: 로컬 xml, 에러 체크) =====
xml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(xml_path)

if face_cascade.empty():
    print("ERROR: Could not load Haar Cascade.")
    exit()

# ===== 서보 설정 (1-5와 동일) =====
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
dead_zone = 25
max_step = 4
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
    config = picam2.create_preview_configuration(   # 1-4 방식
        main={"size": (WIDTH, HEIGHT)}
    )
    picam2.configure(config)
    picam2.start()
    time.sleep(2)
    print("Face tracking start")

    try:
        while True:
            frame = picam2.capture_array()
            display = frame.copy()

            center_x = WIDTH // 2

            # 1-4 방식: COLOR_RGB2GRAY, minNeighbors=5, minSize=(60,60)
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(60, 60)
            )

            if len(faces) > 0:
                x, y, w, h = max(faces, key=lambda r: r[2] * r[3])
                face_center_x = x + w // 2
                error = face_center_x - center_x

                if abs(error) > dead_zone:
                    movement = clamp(error * Kp, -max_step, max_step)
                    current_angle = clamp(current_angle + movement, ANGLE_MIN, ANGLE_MAX)
                    servo.angle = current_angle

                print(f"error: {error}  angle: {current_angle:.1f}")

                cv2.rectangle(display, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(display, f"Error: {error:.0f}px", (10, 55),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

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
