import sys
import tty
import termios
import time
import RPi.GPIO as GPIO
import pigpio
from gpiozero import LED

# ===== 핀 설정 =====
green_led = LED(17)
red_led   = LED(27)

BUZZER_PIN = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
pwm = GPIO.PWM(BUZZER_PIN, 1000)  # 1000Hz
buzzer_on = False

# ===== 서보 (gpiozero → pigpio 교체) =====
# servo = AngularServo(
#     18,
#     min_angle=0,
#     max_angle=180,
#     min_pulse_width=0.0005,
#     max_pulse_width=0.0025
# )
# servo.angle = current_angle

SERVO_PIN = 18
pi = pigpio.pi()
if not pi.connected:
    print("ERROR: pigpiod 가 실행중이지 않습니다. 'sudo pigpiod' 를 먼저 실행하세요.")
    exit()

# 각도 → 펄스폭 변환 (0도=500us, 90도=1500us, 180도=2000us)
def angle_to_pw(angle):
    return int(500 + (angle / 180.0) * 1500)

current_angle = 90
pi.set_servo_pulsewidth(SERVO_PIN, angle_to_pw(current_angle))
STEP = 10
ANGLE_MIN = 0
ANGLE_MAX = 180

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def getch():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            ch2 = sys.stdin.read(1)
            ch3 = sys.stdin.read(1)
            return ch + ch2 + ch3
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

print("===== 하드웨어 테스트 =====")
print("  g      : 초록 LED 토글")
print("  r      : 빨간 LED 토글")
print("  b      : 부저 토글")
print("  ← / a  : 서보 왼쪽")
print("  → / d  : 서보 오른쪽")
print("  c      : 서보 중앙 (90도)")
print("  q      : 종료")
print("===========================")

try:
    while True:
        key = getch()

        if key in ('g', 'G'):
            green_led.toggle()
            print(f"초록 LED: {'ON' if green_led.is_active else 'OFF'}          ")

        elif key in ('r', 'R'):
            red_led.toggle()
            print(f"빨간 LED: {'ON' if red_led.is_active else 'OFF'}          ")

        elif key in ('b', 'B'):
            buzzer_on = not buzzer_on
            if buzzer_on:
                pwm.start(50)
            else:
                pwm.stop()
            print(f"부저: {'ON' if buzzer_on else 'OFF'}          ")

        elif key in ('\x1b[D', 'a', 'A'):
            current_angle = clamp(current_angle - STEP, ANGLE_MIN, ANGLE_MAX)
            # servo.angle = current_angle
            pi.set_servo_pulsewidth(SERVO_PIN, angle_to_pw(current_angle))
            print(f"서보: {current_angle:.1f}도          ")

        elif key in ('\x1b[C', 'd', 'D'):
            current_angle = clamp(current_angle + STEP, ANGLE_MIN, ANGLE_MAX)
            # servo.angle = current_angle
            pi.set_servo_pulsewidth(SERVO_PIN, angle_to_pw(current_angle))
            print(f"서보: {current_angle:.1f}도          ")

        elif key in ('c', 'C'):
            current_angle = 90
            # servo.angle = current_angle
            pi.set_servo_pulsewidth(SERVO_PIN, angle_to_pw(current_angle))
            print(f"서보: 중앙 ({current_angle:.1f}도)          ")

        elif key in ('q', 'Q', '\x03'):
            break

finally:
    green_led.off()
    red_led.off()
    pwm.stop()
    GPIO.cleanup()
    # servo.detach()
    pi.set_servo_pulsewidth(SERVO_PIN, 0)
    pi.stop()
    print("\n종료.")