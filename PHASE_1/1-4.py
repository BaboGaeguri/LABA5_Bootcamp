from picamera2 import Picamera2
from flask import Flask, Response
import cv2
import RPi.GPIO as GPIO
import os
import time

app = Flask(__name__)

# ===== Haar Cascade =====
xml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(xml_path)

if face_cascade.empty():
    print("ERROR: Could not load Haar Cascade.")
    exit()

# ===== GPIO 설정 =====
LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, False)

# ===== Picamera2 설정 =====
picam2 = Picamera2()
picam2.configure(
    picam2.create_preview_configuration(
        main={"size": (640, 480)}
    )
)
picam2.start()
time.sleep(2)

print("FACE DETECTION STARTED")

def generate():
    while True:
        frame = picam2.capture_array()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60)
        )

        if len(faces) > 0:
            GPIO.output(LED_PIN, True)
            status = "FACE DETECTED"
        else:
            GPIO.output(LED_PIN, False)
            status = "NO FACE"

        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.putText(
            frame_bgr, status, (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX, 1,
            (0, 0, 255) if len(faces) > 0 else (0, 255, 0), 2
        )

        _, buffer = cv2.imencode('.jpg', frame_bgr)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    return '<img src="/video_feed">'

@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("Server running at http://0.0.0.0:5000")
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        GPIO.output(LED_PIN, False)
        GPIO.cleanup()
        picam2.stop()
        print("EXITED CLEANLY")
