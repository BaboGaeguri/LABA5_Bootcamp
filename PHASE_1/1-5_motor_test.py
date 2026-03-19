import sys
import tty
import termios
import time
from gpiozero import AngularServo

# ===== 서보 설정 =====
servo = AngularServo(
    18,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.0005,
    max_pulse_width=0.0025
)

current_angle = 90
servo.angle = current_angle
STEP = 5        # 한 번에 움직이는 각도
ANGLE_MIN = 0
ANGLE_MAX = 180

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def getch():
    """키 하나 읽기 (Enter 없이)"""
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        # 방향키: ESC [ A/B/C/D
        if ch == '\x1b':
            ch2 = sys.stdin.read(1)
            ch3 = sys.stdin.read(1)
            return ch + ch2 + ch3
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

print("===== 서보 모터 키보드 테스트 =====")
print(f"  ← / a  : 왼쪽  ({STEP}도)")
print(f"  → / d  : 오른쪽 ({STEP}도)")
print(f"  c      : 중앙 (90도)")
print(f"  q      : 종료")
print(f"현재 각도: {current_angle}")
print("==================================")

try:
    while True:
        key = getch()

        if key in ('\x1b[D', 'a', 'A'):    # 왼쪽
            current_angle = clamp(current_angle - STEP, ANGLE_MIN, ANGLE_MAX)
        elif key in ('\x1b[C', 'd', 'D'):  # 오른쪽
            current_angle = clamp(current_angle + STEP, ANGLE_MIN, ANGLE_MAX)
        elif key in ('c', 'C'):             # 중앙
            current_angle = 90
        elif key in ('q', 'Q', '\x03'):     # 종료 (q 또는 Ctrl+C)
            break
        else:
            continue

        servo.angle = current_angle
        print(f"각도: {current_angle:5.1f}도", end='\r')
        time.sleep(0.05)

finally:
    servo.detach()
    print("\n종료.")
