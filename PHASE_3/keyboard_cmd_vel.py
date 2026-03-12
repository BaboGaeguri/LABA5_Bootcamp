import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class KeyboardCmdVel(Node):

    def __init__(self):
        super().__init__('keyboard_cmd_vel')

        # /cmd_vel 퍼블리셔 생성
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        self.get_logger().info("Keyboard control started")
        self.get_logger().info("W: forward | S: backward | A: left | D: right | space: stop")

        self.run()

    def run(self):
        while rclpy.ok():

            key = input("Enter command (W/S/A/D/space): ")

            msg = Twist()

            if key.lower() == 'w':
                msg.linear.x = 0.5

            elif key.lower() == 's':
                msg.linear.x = -0.5

            elif key.lower() == 'a':
                msg.angular.z = 1.0

            elif key.lower() == 'd':
                msg.angular.z = -1.0

            elif key == ' ':
                msg.linear.x = 0.0
                msg.angular.z = 0.0

            else:
                print("Invalid key")
                continue

            self.publisher.publish(msg)

            self.get_logger().info(
                f'Publishing: linear.x={msg.linear.x}, angular.z={msg.angular.z}'
            )


def main(args=None):

    rclpy.init(args=args)

    node = KeyboardCmdVel()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()