import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32MultiArray

class LidarProcessor(Node):
    def __init__(self):
        super().__init__('lidar_processor')
        self.subscription = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.publisher = self.create_publisher(Float32MultiArray, '/wall_distances', 10)
        self.get_logger().info('📡 라이다 프로세서 V2 (거리 실시간 모니터링) 가동!')

    def scan_callback(self, msg):
        def get_min_dist(slice_arr):
            valid_dists = [x for x in slice_arr if 0.1 < x < 10.0]
            return min(valid_dists) if valid_dists else 10.0

        # 🌟 4방향 거리 계산
        front_narrow = get_min_dist(msg.ranges[178:182])
        front_wide = get_min_dist(msg.ranges[165:195])
        left_dist = get_min_dist(msg.ranges[260:280])
        right_dist = get_min_dist(msg.ranges[80:100])

        # 🌟 터미널에 보기 좋게 출력 (소수점 2자리까지만)
        self.get_logger().info(
            f'📏 좁은전방: {front_narrow:.2f}m | 넓은전방: {front_wide:.2f}m | 좌: {left_dist:.2f}m | 우: {right_dist:.2f}m'
        )

        # 🌟 두뇌로 데이터 전송
        dist_msg = Float32MultiArray()
        dist_msg.data = [float(front_narrow), float(front_wide), float(left_dist), float(right_dist)]
        self.publisher.publish(dist_msg)

def main(args=None):
    rclpy.init(args=args)
    node = LidarProcessor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()