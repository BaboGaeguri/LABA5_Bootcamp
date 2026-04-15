"""
Orin → NUC: /game/score 발행 (Int32)
게임 종료 시 최종 점수를 NUC에 전송한다.
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class OrinPublisher(Node):
    def __init__(self):
        super().__init__('orin_pub')
        self.pub = self.create_publisher(Int32, '/game/score', 10)
        self.get_logger().info('Orin publisher ready')

    def publish_score(self, score: int):
        msg = Int32()
        msg.data = score
        self.pub.publish(msg)
        self.get_logger().info(f'[Orin] score 발행: {score}')


def main():
    rclpy.init()
    node = OrinPublisher()
    # 테스트용: 점수 240 발행
    node.publish_score(240)
    rclpy.spin_once(node, timeout_sec=1.0)
    node.destroy_node()
    rclpy.shutdown()
