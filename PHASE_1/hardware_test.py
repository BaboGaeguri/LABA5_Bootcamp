import sys
import tty
import termios
import time
from gpiozero import AngularServo, LED, Buzzer

# ===== 핀 설정 =====
green_led = LED(17)
red_led   = LED(27)
buzzer    = Buzzer(22)
servo = AngularServo(
    18,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.001,
    max_pulse_width=0.002
)

current_angle = 90
servo.angle = current_angle
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
            buzzer.toggle()
            print(f"부저: {'ON' if buzzer.is_active else 'OFF'}          ")

        elif key in ('\x1b[D', 'a', 'A'):
            current_angle = clamp(current_angle - STEP, ANGLE_MIN, ANGLE_MAX)
            servo.angle = current_angle
            print(f"서보: {current_angle:.1f}도          ")

        elif key in ('\x1b[C', 'd', 'D'):
            current_angle = clamp(current_angle + STEP, ANGLE_MIN, ANGLE_MAX)
            servo.angle = current_angle
            print(f"서보: {current_angle:.1f}도          ")

        elif key in ('c', 'C'):
            current_angle = 90
            servo.angle = current_angle
            print(f"서보: 중앙 ({current_angle:.1f}도)          ")

        elif key in ('q', 'Q', '\x03'):
            break

finally:
    green_led.off()
    red_led.off()
    buzzer.off()
    servo.detach()
    print("\n종료.")
