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

current_angle = 90.0
servo.angle = current_angle

# P제어 파라미터
Kp = 0.06
dead_zone = 25
max_step = 4
ANGLE_MIN = 10
ANGLE_MAX = 170

# ✅ 좌표 스무딩 파라미터
SMOOTH_ALPHA = 0.2          # 낮을수록 더 부드러움 (0.1 ~ 0.3 권장)
smoothed_x = None           # 첫 프레임 전까지 None으로 초기화

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

# -----------------------------
# 카메라 설정
# -----------------------------
WIDTH, HEIGHT = 640, 480

output_frame = None
frame_lock = threading.Lock()

def camera_thread():
    global output_frame, current_angle, smoothed_x

    picam2 = Picamera2()
    config = picam2.create_video_configuration(
        main={"size": (WIDTH, HEIGHT), "format": "RGB888"}
    )
    picam2.configure(config)
    picam2.start()
    time.sleep(2)
    print("Face tracking start")

    frame_count = 0  # ✅ print 빈도 조절용

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

            if len(faces) > 0:
                x, y, w, h = max(faces, key=lambda r: r[2] * r[3])
                raw_x = x + w // 2

                # ✅ 지수 이동 평균(EMA) 스무딩
                if smoothed_x is None:
                    smoothed_x = float(raw_x)   # 첫 프레임은 raw값으로 초기화
                else:
                    smoothed_x = SMOOTH_ALPHA * raw_x + (1 - SMOOTH_ALPHA) * smoothed_x

                error = smoothed_x - center_x

                # ✅ 각도 실제 변화 있을 때만 서보 명령 전송
                if abs(error) > dead_zone:
                    movement = clamp(error * Kp, -max_step, max_step)
                    new_angle = clamp(current_angle + movement, ANGLE_MIN, ANGLE_MAX)

                    if abs(new_angle - current_angle) > 0.3:  # ✅ 미세 변화 무시
                        current_angle = new_angle
                        servo.angle = current_angle

                # ✅ 30프레임마다만 print (터미널 출력 부하 감소)
                if frame_count % 30 == 0:
                    print(f"raw_x: {raw_x} | smoothed_x: {smoothed_x:.1f} | "
                          f"error: {error:.1f} | angle: {current_angle:.1f}")

                cv2.rectangle(display, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(display, f"Error: {error:.0f}px", (10, 55),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                # ✅ 스무딩된 중심점 표시
                cv2.circle(display, (int(smoothed_x), height // 2), 8, (0, 255, 255), -1)

            else:
                # ✅ 얼굴 없으면 smoothed_x 유지 (None 리셋 안 함 → 재등장 시 튀지 않음)
                if frame_count % 30 == 0:
                    print("No face detected")

            frame_count += 1

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