import RPi.GPIO as GPIO
import time

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

print("=== GPIO 테스트 스크립트 ===")
print("  l : LED 토글 (켜기/끄기)")
print("  b : 부저 토글 (켜기/끄기)")
print("  a : LED + 부저 동시 토글")
print("  q : 종료")
print("===========================")

led_on = False

try:
    while True:
        cmd = input("명령 입력 > ").strip().lower()

        if cmd == 'l':
            led_on = not led_on
            GPIO.output(LED_PIN, led_on)
            print(f"LED {'ON' if led_on else 'OFF'}")

        elif cmd == 'b':
            if not pwm_started:
                pwm.start(BUZZER_DUTY)
                pwm_started = True
                print("부저 ON")
            else:
                pwm.stop()
                pwm_started = False
                print("부저 OFF")

        elif cmd == 'a':
            led_on = not led_on
            GPIO.output(LED_PIN, led_on)
            if not pwm_started:
                pwm.start(BUZZER_DUTY)
                pwm_started = True
            else:
                pwm.stop()
                pwm_started = False
            print(f"LED {'ON' if led_on else 'OFF'} / 부저 {'ON' if pwm_started else 'OFF'}")

        elif cmd == 'q':
            print("종료합니다.")
            break

        else:
            print("알 수 없는 명령입니다. (l / b / a / q)")

finally:
    if pwm_started:
        pwm.stop()
    GPIO.output(LED_PIN, False)
    GPIO.output(BUZZER_PIN, False)
    GPIO.cleanup()
    print("EXITED CLEANLY")