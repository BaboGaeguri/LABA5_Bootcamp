import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray, String
from geometry_msgs.msg import Twist

class MazeSolver(Node):
    def __init__(self):
        super().__init__('maze_solver')
        
        self.create_subscription(Float32MultiArray, '/wall_distances', self.lidar_callback, 10)
        self.create_subscription(String, '/color_hint', self.color_callback, 10)
        self.create_subscription(String, '/mode', self.mode_callback, 10)
        
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # 🌟 이제 4개의 센서값을 받음
        self.front_narrow = 10.0
        self.front_wide = 10.0
        self.left_d = 10.0
        self.right_d = 10.0
        self.current_color = "NONE"
        
        self.mode = "AUTO"
        self.avoid_direction = 0.0  
        
        self.timer = self.create_timer(0.1, self.control_loop)
        self.get_logger().info('🧠 미로 탈출 V9 (동적 시야각 + 상태 머신 복귀!) 가동!')

    def lidar_callback(self, msg):
        # 4개의 데이터 언패킹
        self.front_narrow, self.front_wide, self.left_d, self.right_d = msg.data

    def color_callback(self, msg):
        self.current_color = msg.data

    def mode_callback(self, msg):
        self.mode = msg.data

    def control_loop(self):
        if self.mode == "MANUAL":
            return

        twist = Twist()
        turn_start_dist = 0.5 
        turn_stop_dist = 0.6   

        # ==========================================================
        # 🌟 STEP 1: 회전 종료 조건 (넓은 시야 확인!)
        # ==========================================================
        if self.avoid_direction != 0.0:
            # 회전 중일 때는 '넓은 시야(front_wide)'가 뻥 뚫려야만 탈출 인정!
            if self.front_wide > turn_stop_dist and self.current_color != "RED":
                self.avoid_direction = 0.0  
                self.get_logger().info('💨 넓은 시야 확보! 코너 완벽 탈출!')

        # ==========================================================
        # 🌟 STEP 2: 새로운 위험 감지 (좁은 시야 확인!)
        # ==========================================================
        if self.avoid_direction == 0.0:
            if self.current_color == "RED":
                if self.left_d > self.right_d:
                    self.avoid_direction = 0.7
                else:
                    self.avoid_direction = -0.7
                    
            # 평상시 직진할 때는 '좁은 시야(front_narrow)'만 보고 판단!
            elif self.front_narrow < turn_start_dist:
                if self.left_d > self.right_d:
                    self.avoid_direction = 0.7
                    self.get_logger().info('🧱 좁은 시야에 벽 감지! [좌회전] 시작!')
                else:
                    self.avoid_direction = -0.7
                    self.get_logger().info('🧱 좁은 시야에 벽 감지! [우회전] 시작!')

        # ==========================================================
        # 🌟 STEP 3: 주행 명령 실행
        # ==========================================================
        if self.avoid_direction != 0.0:
            twist.linear.x = 0.0
            twist.angular.z = self.avoid_direction
        else:
            if self.current_color == "GREEN":
                twist.linear.x = 0.5   # 초록색 돌진!
                twist.angular.z = 0.0
            else:
                # 오리지널 왼손 법칙 (왼쪽에 공간이 생기면 다시 벽을 찾으러 파고듦)
                if self.left_d > turn_start_dist + 0.3: 
                    twist.linear.x = 0.2
                    twist.angular.z = 0.8
                else:
                    twist.linear.x = 0.4   # 일반 직진
                    twist.angular.z = 0.0

        self.cmd_pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = MazeSolver()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()