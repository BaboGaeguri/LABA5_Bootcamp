"""
NUC: /game/score 수신 (Int32)
Orin에서 보낸 점수를 받아 터미널에 출력한다.
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class NucSubscriber(Node):
    def __init__(self):
        super().__init__('nuc_sub')
        self.sub = self.create_subscription(
            Int32, '/game/score', self.callback, 10)
        self.get_logger().info('NUC subscriber ready — /game/score 대기 중...')

    def callback(self, msg: Int32):
        self.get_logger().info(f'[NUC] 점수 수신: {msg.data}')


def main():
    rclpy.init()
    node = NucSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
