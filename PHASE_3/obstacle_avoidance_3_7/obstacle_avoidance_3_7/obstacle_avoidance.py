import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class ObstacleAvoidance(Node):

    def __init__(self):
        super().__init__('obstacle_avoidance')

        # /scan 구독
        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

        # /cmd_vel 발행
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # 장애물 판단 거리 (미터)
        self.threshold = 0.5

        self.get_logger().info('Obstacle avoidance node started!')

    def scan_callback(self, msg):
        ranges = msg.ranges
        total = len(ranges)

        # 전방 (0도): 인덱스 180 기준 ±30도
        front = ranges[150:211]

        # 좌측 (+90도): 인덱스 270 기준
        left = ranges[240:301]

        # 우측 (-90도): 인덱스 60 기준
        right = ranges[60:121]

        def min_range(arr):
            valid = [r for r in arr if r != float('inf') and r > 0.0]
            return min(valid) if valid else float('inf')

        front_min = min_range(front)
        left_min  = min_range(left)
        right_min = min_range(right)

        twist = Twist()

        if front_min > self.threshold:
            # 전방 충분 → 직진
            twist.linear.x = 0.2
            twist.angular.z = 0.0
            self.get_logger().info(f'직진 | 전방: {front_min:.2f}m')
        elif front_min < 0.3:
            # 너무 가까움 → 후진
            twist.linear.x = -0.2
            twist.angular.z = 0.0
            self.get_logger().info(f'후진 | 전방: {front_min:.2f}m')
        else:
            # 장애물 감지 → 제자리 회전
            twist.linear.x = 0.0
            if left_min >= right_min:
                twist.angular.z = 1.0
                self.get_logger().info(f'좌회전 | 좌: {left_min:.2f}m 우: {right_min:.2f}m')
            else:
                twist.angular.z = -1.0
                self.get_logger().info(f'우회전 | 좌: {left_min:.2f}m 우: {right_min:.2f}m')

        self.cmd_pub.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidance()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()