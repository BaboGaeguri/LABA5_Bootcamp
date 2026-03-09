from picamera2 import Picamera2
import cv2
import RPi.GPIO as GPIO
import time

print("STARTED")

# ===== GPIO 핀 설정 (BCM 번호) =====
LED_PIN = 17
BUZZER_PIN = 27  # BCM 27 = 물리 핀 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

GPIO.output(LED_PIN, False)
GPIO.output(BUZZER_PIN, False)

# ===== 부저 PWM 설정 (Passive/피에조 대응) =====
BUZZER_FREQ_HZ = 4000   # 1000~4000 사이에서 가장 크게 들리는 지점 찾기
BUZZER_DUTY = 50        # 0~100 (듀티가 클수록 더 잘 들리는 경우가 많음)

pwm = GPIO.PWM(BUZZER_PIN, BUZZER_FREQ_HZ)
pwm_started = False

# ===== Picamera2 설정 =====
picam2 = Picamera2()
picam2.configure(
    picam2.create_preview_configuration(
        main={"size": (640, 480)}
    )
)
picam2.start()
time.sleep(2)

# 첫 프레임(이전 프레임) 준비
frame1 = picam2.capture_array()
prev_gray = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)
prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)

# ===== 움직임 감지 파라미터(필요시 튜닝) =====
THRESH_VAL = 25        # 픽셀 변화 임계값(낮을수록 민감)
MOTION_PIXELS = 4000   # 변화 픽셀 수 기준(낮을수록 민감)

try:
    while True:
        frame2 = picam2.capture_array()

        # 1) 그레이스케일 변환 (RGB 기준)
        gray = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # 2) 프레임 차이
        diff = cv2.absdiff(prev_gray, gray)

        # 3) 임계값 적용
        _, thresh = cv2.threshold(diff, THRESH_VAL, 255, cv2.THRESH_BINARY)

        # 4) 변화 픽셀 수로 움직임 판단
        motion_score = cv2.countNonZero(thresh)
        motion = motion_score > MOTION_PIXELS

        # GPIO + 부저(PWM) 제어
        if motion:
            status = f"MOTION DETECTED ({motion_score})"
            GPIO.output(LED_PIN, True)

            if not pwm_started:
                # 필요하면 주파수/듀티를 여기서 바꿔도 됨
                pwm.ChangeFrequency(BUZZER_FREQ_HZ)
                pwm.start(BUZZER_DUTY)
                pwm_started = True
        else:
            status = f"NO MOTION ({motion_score})"
            GPIO.output(LED_PIN, False)

            if pwm_started:
                pwm.stop()
                pwm_started = False

        # 화면 표시(OpenCV는 BGR이 자연스러움 → RGB->BGR 변환)
        frame2_bgr = cv2.cvtColor(frame2, cv2.COLOR_RGB2BGR)
        cv2.putText(
            frame2_bgr,
            status,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255) if motion else (0, 255, 0),
            2
        )

        cv2.imshow("Security Camera", frame2_bgr)

        # 다음 루프 대비
        prev_gray = gray

        # 종료 키
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:  # q 또는 ESC
            break

finally:
    # 정리
    if pwm_started:
        pwm.stop()
    GPIO.output(LED_PIN, False)
    GPIO.output(BUZZER_PIN, False)
    GPIO.cleanup()
    picam2.stop()
    cv2.destroyAllWindows()
    print("EXITED CLEANLY")