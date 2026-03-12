import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import tty
import termios

class TeleopKeyboard(Node):
    def __init__(self):
        super().__init__('teleop_keyboard')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info('WASD로 조종, 스페이스바로 정지, q로 종료')

    def get_key(self):
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return key

    def run(self):
        msg = Twist()
        while rclpy.ok():
            key = self.get_key()
            msg.linear.x = 0.0
            msg.angular.z = 0.0

            if key == 'w':
                msg.linear.x = 0.5
                self.get_logger().info('전진')
            elif key == 's':
                msg.linear.x = -0.5
                self.get_logger().info('후진')
            elif key == 'a':
                msg.angular.z = 1.0
                self.get_logger().info('좌회전')
            elif key == 'd':
                msg.angular.z = -1.0
                self.get_logger().info('우회전')
            elif key == ' ':
                self.get_logger().info('정지')
            elif key == 'q':
                break

            self.publisher.publish(msg)

def main():
    rclpy.init()
    node = TeleopKeyboard()
    try:
        node.run()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()