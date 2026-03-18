import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import sys
import select
import termios
import tty

msg = """
🕹️ Maze Explorer Robot Controller 🕹️
-----------------------------------
Movement (Only works in MANUAL mode):
   w
a  s  d
   x

w/x : Forward / Backward
a/d : Turn Left / Turn Right
s   : Force Brake (Stop)

🔄 Mode Switch (Very Important!):
m : MANUAL Mode (User control)
t : AUTO Mode (Autonomous maze escape)

Press CTRL-C to quit
"""

class KeyboardCmdVel(Node):
    def __init__(self):
        super().__init__('keyboard_cmd_vel')
        
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.mode_pub = self.create_publisher(String, '/mode', 10)
        
        self.mode = "AUTO" 
        self.settings = termios.tcgetattr(sys.stdin)
        
        self.create_timer(0.5, self.publish_mode)
        
        print(msg)

    def publish_mode(self):
        mode_msg = String()
        mode_msg.data = self.mode
        self.mode_pub.publish(mode_msg)

    def get_key(self):
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key

    def run(self):
        twist = Twist()
        try:
            while rclpy.ok():
                key = self.get_key()
                
                if key:
                    # 1. Mode Switch
                    if key == 'm':
                        self.mode = "MANUAL"
                        print("\n🚨 [MODE CHANGED] Current Mode: MANUAL (User Control)")
                        twist.linear.x = 0.0
                        twist.angular.z = 0.0
                        self.cmd_pub.publish(twist)
                        
                    elif key == 't':
                        self.mode = "AUTO"
                        print("\n🤖 [MODE CHANGED] Current Mode: AUTO (Autonomous Escape)")
                        
                    # 2. Manual Control (Only works in MANUAL mode)
                    elif self.mode == "MANUAL":
                        if key == 'w':
                            twist.linear.x = 0.5
                            twist.angular.z = 0.0
                        elif key == 'x':
                            twist.linear.x = -0.5
                            twist.angular.z = 0.0
                        elif key == 'a':
                            twist.linear.x = 0.0
                            twist.angular.z = 1.0
                        elif key == 'd':
                            twist.linear.x = 0.0
                            twist.angular.z = -1.0
                        elif key == 's':
                            twist.linear.x = 0.0
                            twist.angular.z = 0.0
                        else:
                            if (key == '\x03'): # CTRL-C
                                break
                            
                        self.cmd_pub.publish(twist)

                rclpy.spin_once(self, timeout_sec=0)
                
        except Exception as e:
            print(e)
        finally:
            twist = Twist()
            self.cmd_pub.publish(twist)
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)

def main(args=None):
    rclpy.init(args=args)
    node = KeyboardCmdVel()
    node.run()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()