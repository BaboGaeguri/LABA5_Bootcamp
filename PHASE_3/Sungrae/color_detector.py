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
        
        # 1. 카메라 이미지 구독
        self.subscription = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 10)
            
        # 2. 색상 판단 결과 발행 (RED, GREEN, NONE)
        self.publisher = self.create_publisher(String, '/color_hint', 10)
        
        self.bridge = CvBridge()
        self.get_logger().info('👁️ 색상 인식 비전 노드 가동 완료!')

    def image_callback(self, msg):
        # 1. ROS 이미지를 OpenCV 이미지로 변환
        cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        
        # 2. 색상 영역을 찾기 쉽도록 BGR을 HSV 색상 공간으로 변환
        hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

        # 3. 빨간색 영역 정의 (빨간색은 HSV에서 양끝에 걸쳐 있어서 두 범위를 합쳐야 함)
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([179, 255, 255])
        
        mask_red1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
        mask_red = mask_red1 + mask_red2 # 빨간색 마스크 합치기

        # 4. 초록색 영역 정의
        lower_green = np.array([40, 100, 100])
        upper_green = np.array([80, 255, 255])
        mask_green = cv2.inRange(hsv_image, lower_green, upper_green)

        # 5. 화면에서 해당 색상의 픽셀 개수 세기
        red_pixels = cv2.countNonZero(mask_red)
        green_pixels = cv2.countNonZero(mask_green)

        # 6. 표지판 감지 판단 (픽셀 수가 5000개 이상이면 가까이 있다고 판단)
        threshold = 10000
        hint_msg = String()
        
        if red_pixels > threshold and red_pixels > green_pixels:
            hint_msg.data = "RED"
            self.get_logger().info(f'🛑 막다른 길 감지! (RED: {red_pixels} px)')
        elif green_pixels > threshold and green_pixels > red_pixels:
            hint_msg.data = "GREEN"
            self.get_logger().info(f'✅ 올바른 길 감지! (GREEN: {green_pixels} px)')
        else:
            hint_msg.data = "NONE"

        self.publisher.publish(hint_msg)
        
        # (선택 사항) 로봇의 시야를 직접 보기 위한 디버깅 창
        # cv2.imshow("Robot View", cv_image)
        # cv2.imshow("Red Mask", mask_red)
        # cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = ColorDetector()
    rclpy.spin(node)
    node.destroy_node()
    cv2.destroyAllWindows()
    rclpy.shutdown()

if __name__ == '__main__':
    main()