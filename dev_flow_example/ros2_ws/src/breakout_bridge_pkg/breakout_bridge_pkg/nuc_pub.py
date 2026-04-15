"""
NUC → Orin: /game/status 발행 (String)
점수 수신 확인 응답을 Orin에 보낸다.
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class NucPublisher(Node):
    def __init__(self):
        super().__init__('nuc_pub')
        self.pub = self.create_publisher(String, '/game/status', 10)

    def publish_status(self, status: str):
        msg = String()
        msg.data = status
        self.pub.publish(msg)
        self.get_logger().info(f'[NUC] status 발행: {status}')


def main():
    rclpy.init()
    node = NucPublisher()
    node.publish_status('received')
    rclpy.spin_once(node, timeout_sec=1.0)
    node.destroy_node()
    rclpy.shutdown()
