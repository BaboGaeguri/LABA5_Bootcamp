import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray, String
from geometry_msgs.msg import Twist


class MazeEscaper(Node):
    def __init__(self):
        super().__init__('maze_escaper')

        self.dist_sub = self.create_subscription(
            Float32MultiArray, '/wall_distances', self.dist_callback, 10)
        self.hint_sub = self.create_subscription(
            String, '/color_hint', self.hint_callback, 10)
        self.mode_sub = self.create_subscription(
            String, '/mode', self.mode_callback, 10)

        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.color_hint = 'none'
        self.mode = 'auto'

        self.wall_follow_dist = 0.4   # 왼쪽 벽 목표 거리
        self.front_threshold  = 0.35  # 우회전 시작 거리
        self.back_threshold   = 0.20  # 후진 시작 거리

        # 회전 지속 카운터: 전방이 열릴 때까지 회전을 강제로 유지
        self.turn_count = 0

    def hint_callback(self, msg):
        self.color_hint = msg.data

    def mode_callback(self, msg):
        self.mode = msg.data
        self.get_logger().info(f'모드 전환: {self.mode}')

    def dist_callback(self, msg):
        if self.mode == 'manual':
            return

        front, left, right = msg.data[0], msg.data[1], msg.data[2]
        twist = Twist()

        # ── 1. 후진 (최우선 안전 로직) ──
        if front < self.back_threshold:
            twist.linear.x  = -0.5
            twist.angular.z = -1.0 if right > left else 1.0
            self.turn_count = 0
            self.get_logger().info(f'후진 | 전: {front:.2f}m 좌: {left:.2f}m 우: {right:.2f}m')

        # ── 2. 빨간 표지판: 막다른 길 → 반대 벽을 찾아가도록 좌회전 ──
        elif self.color_hint == 'red':
            twist.linear.x  = 0.0
            twist.angular.z = 1.5
            self.turn_count = 8   # 충분히 돌고 나서 전진
            self.get_logger().info('빨간 표지판 → 우회전 회피')

        # ── 3. 전방 막힘 OR 회전 중 ──
        elif front < self.front_threshold or self.turn_count > 0:
            twist.linear.x  = 0.0
            twist.angular.z = -1.5

            if front > self.front_threshold + 0.15:
                self.turn_count = max(0, self.turn_count - 1)
            else:
                self.turn_count = 8

            self.get_logger().info(f'우회전 중 | 전: {front:.2f}m count: {self.turn_count}')

        # ── 4. 초록 표지판: 올바른 경로 → 직진 유지 ──
        elif self.color_hint == 'green':
            twist.linear.x  = 0.5
            twist.angular.z = 0.0
            self.turn_count = 0
            self.get_logger().info(f'초록 표지판 → 직진 | 전: {front:.2f}m')

        # ── 5. 왼손 법칙 ──
        elif left > self.wall_follow_dist + 0.2:
            twist.linear.x  = 0.5
            twist.angular.z = 0.6
            self.turn_count = 0
            self.get_logger().info(f'왼쪽 열림 → 좌조향 | 좌: {left:.2f}m')

        elif left < self.wall_follow_dist - 0.1:
            twist.linear.x  = 0.5
            twist.angular.z = -0.6
            self.turn_count = 0
            self.get_logger().info(f'왼쪽 근접 → 우조향 | 좌: {left:.2f}m')

        else:
            twist.linear.x  = 0.5
            twist.angular.z = 0.0
            self.turn_count = 0
            self.get_logger().info(f'직진 | 전: {front:.2f}m 좌: {left:.2f}m')

        self.cmd_pub.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    node = MazeEscaper()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()