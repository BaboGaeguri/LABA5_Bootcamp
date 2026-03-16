import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    pkg_path = get_package_share_directory('LiDAR_3_5')

    urdf_file = os.path.join(pkg_path, 'urdf', 'wheeled_robot.urdf')
    world_file = os.path.join(pkg_path, 'worlds', 'maze.world')

    robot_description = ParameterValue(
        Command(['cat ', urdf_file]),
        value_type=str
    )

    return LaunchDescription([

        # 1. maze.world 로드하여 Gazebo 실행
        ExecuteProcess(
            cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so', world_file],
            output='screen'
        ),

        # 2. robot_state_publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
            output='screen'
        ),

        # 3. 로봇 소환 (출발점 x=-2, y=-2)
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=[
                '-topic', 'robot_description',
                '-entity', 'wheeled_robot',
                '-x', '-2', '-y', '-2', '-z', '0.1'
            ],
            output='screen'
        ),

    ])