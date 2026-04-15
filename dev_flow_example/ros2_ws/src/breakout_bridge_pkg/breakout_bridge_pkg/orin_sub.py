"""
Orin: /game/status 수신 (String)
NUC의 응답 상태를 수신한다.
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class OrinSubscriber(Node):
    def __init__(self):
        super().__init__('orin_sub')
        self.sub = self.create_subscription(
            String, '/game/status', self.callback, 10)
        self.get_logger().info('Orin subscriber ready — /game/status 대기 중...')

    def callback(self, msg: String):
        self.get_logger().info(f'[Orin] NUC status 수신: {msg.data}')


def main():
    rclpy.init()
    node = OrinSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
