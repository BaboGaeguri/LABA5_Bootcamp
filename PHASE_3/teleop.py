import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys, select, termios, tty

# 키보드 입력 매핑
move_bindings = {
    'w': (0.5, 0.0),
    's': (-0.5, 0.0),
    'a': (0.0, 1.0),
    'd': (0.0, -1.0),
    ' ': (0.0, 0.0),
}

def get_key(settings):
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0.1)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, sys.stdin.fileno(), settings)
    return key

class TeleopNode(Node):
    def __init__(self):
        super().__init__('simple_teleop')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info("키보드 제어 노드가 시작되었습니다. (W,A,S,D, Space)")

    def publish_twist(self, linear_x, angular_z):
        msg = Twist()
        msg.linear.x = linear_x
        msg.angular.z = angular_z
        self.publisher_.publish(msg)

def main():
    settings = termios.tcgetattr(sys.stdin)
    rclpy.init()
    node = TeleopNode()

    try:
        while True:
            key = get_key(settings)
            if key in move_bindings.keys():
                lx, az = move_bindings[key]
                node.publish_twist(lx, az)
                print(f"입력: {key} | Linear: {lx}, Angular: {az}")
            elif key == '\x03': # Ctrl+C
                break
    except Exception as e:
        print(e)
    finally:
        node.publish_twist(0.0, 0.0)
        node.destroy_node()
        rclpy.shutdown()
        termios.tcsetattr(sys.stdin, sys.stdin.fileno(), settings)

if __name__ == '__main__':
    main()
