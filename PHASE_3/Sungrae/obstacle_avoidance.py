import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ObstacleAvoidance(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance')
        # /scan 구독
        self.subscription = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        # /cmd_vel 발행
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info('장애물 회피 노드가 시작되었습니다!')

    def scan_callback(self, msg):
        # 전방/좌/우 거리 샘플링 (슬라이싱 사용)
        # 180번이 정면이므로 170~190번의 평균 혹은 최솟값을 확인
        front_dist = min(msg.ranges[170:190])
        left_dist = min(msg.ranges[260:280])
        right_dist = min(msg.ranges[80:100])

        twist = Twist()

        if front_dist > 0.7:  # 앞에 장애물이 0.8m 이상 떨어져 있으면
            twist.linear.x = 0.7
            twist.angular.z = 0.0
            self.get_logger().info(f'전방 깨끗! 직진 중 (거리: {front_dist:.2f})')
        else:  # 장애물 발견!
            twist.linear.x = 0.0
            if left_dist > right_dist:
                twist.angular.z = 0.7  # 왼쪽이 더 넓으면 왼쪽으로 회전
                self.get_logger().info('장애물! 왼쪽으로 회전')
            else:
                twist.angular.z = -0.7 # 오른쪽이 더 넓으면 오른쪽으로 회전
                self.get_logger().info('장애물! 오른쪽으로 회전')

        self.publisher.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidance()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()