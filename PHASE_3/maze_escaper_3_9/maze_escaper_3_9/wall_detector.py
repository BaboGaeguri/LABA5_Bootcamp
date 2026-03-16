import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32MultiArray


class WallDetector(Node):
    def __init__(self):
        super().__init__('wall_detector')
        self.scan_sub = self.create_subscription(
            LaserScan, '/scan', self.scan_callback, 10)
        self.dist_pub = self.create_publisher(
            Float32MultiArray, '/wall_distances', 10)

    def scan_callback(self, msg):
        ranges = msg.ranges

        # angle_min=-π 기준: index 180=전방, index 270=좌측, index 90=우측
        front = ranges[150:211]
        left  = ranges[240:301]
        right = ranges[60:121]

        def min_range(arr):
            valid = [r for r in arr if r != float('inf') and r > 0.0]
            return min(valid) if valid else float('inf')

        front_min = min_range(front)
        left_min  = min_range(left)
        right_min = min_range(right)

        out = Float32MultiArray()
        out.data = [front_min, left_min, right_min]
        self.dist_pub.publish(out)

        self.get_logger().info(
            f'전방: {front_min:.2f}m  좌: {left_min:.2f}m  우: {right_min:.2f}m')


def main(args=None):
    rclpy.init(args=args)
    node = WallDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()