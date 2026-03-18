from picamera2 import Picamera2
from flask import Flask, Response
import cv2
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# ===== GPIO 설정 =====
LED_PIN = 17
BUZZER_PIN = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(LED_PIN, False)
GPIO.output(BUZZER_PIN, False)

BUZZER_FREQ_HZ = 4000
BUZZER_DUTY = 50
pwm = GPIO.PWM(BUZZER_PIN, BUZZER_FREQ_HZ)
pwm_started = False

# ===== 움직임 감지 파라미터 =====
THRESH_VAL = 25
MOTION_PIXELS = 4000

# ===== Picamera2 설정 =====
picam2 = Picamera2()
picam2.configure(
    picam2.create_preview_configuration(
        main={"size": (640, 480)}
    )
)
picam2.start()
time.sleep(2)

frame1 = picam2.capture_array()
prev_gray = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)
prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)

def generate():
    global prev_gray, pwm_started

    while True:
        frame2 = picam2.capture_array()

        gray = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        diff = cv2.absdiff(prev_gray, gray)
        _, thresh = cv2.threshold(diff, THRESH_VAL, 255, cv2.THRESH_BINARY)
        motion_score = cv2.countNonZero(thresh)
        motion = motion_score > MOTION_PIXELS

        if motion:
            status = f"MOTION DETECTED ({motion_score})"
            GPIO.output(LED_PIN, True)
            if not pwm_started:
                pwm.ChangeFrequency(BUZZER_FREQ_HZ)
                pwm.start(BUZZER_DUTY)
                pwm_started = True
        else:
            status = f"NO MOTION ({motion_score})"
            GPIO.output(LED_PIN, False)
            if pwm_started:
                pwm.stop()
                pwm_started = False

        frame_bgr = cv2.cvtColor(frame2, cv2.COLOR_RGB2BGR)
        cv2.putText(
            frame_bgr, status, (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX, 1,
            (0, 0, 255) if motion else (0, 255, 0), 2
        )

        prev_gray = gray

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
        if pwm_started:
            pwm.stop()
        GPIO.output(LED_PIN, False)
        GPIO.output(BUZZER_PIN, False)
        GPIO.cleanup()
        picam2.stop()
        print("EXITED CLEANLY")
