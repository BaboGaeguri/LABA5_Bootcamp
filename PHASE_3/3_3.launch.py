from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node

import os


def generate_launch_description():

    world = os.path.expanduser(
        "~/ros2_ws/src/robot_control/world/simple_world.sdf"
    )

    robot = os.path.expanduser(
        "~/ros2_ws/src/robot_control/urdf/simple_robot.urdf"
    )

    return LaunchDescription([

        # Gazebo world 실행
        ExecuteProcess(
            cmd=['gz', 'sim', world],
            output='screen'
        ),

        # 로봇 spawn
        ExecuteProcess(
            cmd=['gz', 'sim', '-v', '4', '--spawn-file', robot],
            output='screen'
        ),

        # ROS2 → Gazebo bridge
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=[
                '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist'
            ],
            output='screen'
        ),

        # 키보드 제어
        Node(
            package='robot_control',
            executable='keyboard_cmd_vel',
            output='screen'
        ),

    ])