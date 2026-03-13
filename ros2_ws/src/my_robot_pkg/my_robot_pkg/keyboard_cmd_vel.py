import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class KeyboardCmdVel(Node):

```
def __init__(self):
    super().__init__('keyboard_cmd_vel')
    
    # /cmd_vel 토픽으로 메시지를 보내는 publisher 생성
    self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

    self.get_logger().info("Keyboard control node started")

def run(self):

    while True:

        key = input("W/A/S/D or SPACE : ").lower()

        msg = Twist()

        if key == 'w':
            msg.linear.x = 0.5
            msg.angular.z = 0.0

        elif key == 's':
            msg.linear.x = -0.5
            msg.angular.z = 0.0

        elif key == 'a':
            msg.linear.x = 0.0
            msg.angular.z = 1.0

        elif key == 'd':
            msg.linear.x = 0.0
            msg.angular.z = -1.0

        elif key == ' ':
            msg.linear.x = 0.0
            msg.angular.z = 0.0

        else:
            print("Unknown key")

        self.publisher.publish(msg)
        print(f"Published → linear.x: {msg.linear.x}, angular.z: {msg.angular.z}")
```

def main(args=None):

```
rclpy.init(args=args)

node = KeyboardCmdVel()

try:
    node.run()
except KeyboardInterrupt:
    pass

node.destroy_node()
rclpy.shutdown()
```

if **name** == '**main**':
main()
