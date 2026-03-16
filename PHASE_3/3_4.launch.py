from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
import os


def generate_launch_description():

    world = os.path.expanduser(
        "~/ros2_ws/src/robot_control/world/maze_world.sdf"
    )

    robot = os.path.expanduser(
        "~/ros2_ws/src/robot_control/urdf/simple_robot.urdf"
    )

    return LaunchDescription([

        # Gazebo 실행
        ExecuteProcess(
            cmd=['gz', 'sim', world],
            output='screen'
        ),

        # 로봇 spawn
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-file', robot,
                '-name', 'simple_robot',
                '-z', '0.1'
            ],
            output='screen'
        ),

        # bridge
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=[
                '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist'
            ],
            output='screen'
        ),

        # keyboard teleop
        ExecuteProcess(
            cmd=['python3', '/home/hohoho897/ros2_ws/install/robot_control/lib/robot_control/keyboard_cmd_vel'],
            output='screen'
        )
    ])