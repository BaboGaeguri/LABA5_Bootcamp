import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2
import numpy as np


class ColorDetector(Node):
    def __init__(self):
        super().__init__('color_detector')
        self.bridge = CvBridge()
        self.image_sub = self.create_subscription(
            Image, '/camera_sensor/image_raw', self.image_callback, 10)
        self.hint_pub = self.create_publisher(String, '/color_hint', 10)

    def image_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        h = cv_image.shape[0]
        # 바닥(하단 40%) 제거 - 바닥 색이 초록 HSV 범위에 걸리는 오탐 방지
        cv_image = cv_image[:int(h * 0.6), :]

        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

        lower_green = np.array([40, 80, 80])
        upper_green = np.array([80, 255, 255])

        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 100, 100])
        upper_red2 = np.array([180, 255, 255])

        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        mask_red = cv2.inRange(hsv, lower_red1, upper_red1) + \
                   cv2.inRange(hsv, lower_red2, upper_red2)

        green_pixels = cv2.countNonZero(mask_green)
        red_pixels   = cv2.countNonZero(mask_red)

        hint = String()
        if green_pixels > 30000:    
            hint.data = 'green'
        elif red_pixels > 30000:
            hint.data = 'red'
        else:
            hint.data = 'none'

        self.hint_pub.publish(hint)

        if hint.data != 'none':
            self.get_logger().info(f'색상 감지: {hint.data}  (녹:{green_pixels} 적:{red_pixels})')

def main(args=None):
    rclpy.init(args=args)
    node = ColorDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()