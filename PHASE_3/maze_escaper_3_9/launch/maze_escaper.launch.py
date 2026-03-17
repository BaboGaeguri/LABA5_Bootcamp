import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    pkg_path = get_package_share_directory('maze_escaper_3_9')

    urdf_file = os.path.join(pkg_path, 'urdf', 'wheeled_robot.urdf')
    world_file = os.path.join(pkg_path, 'worlds', 'escape_maze.world')

    robot_description = ParameterValue(
        Command(['cat ', urdf_file]),
        value_type=str
    )

    return LaunchDescription([

        # 1. Gazebo + escape_maze.world
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

        # 3. 로봇 소환 (미로 입구 x=-3, y=-3)
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=[
                '-topic', 'robot_description',
                '-entity', 'wheeled_robot',
                '-x', '-8.75', '-y', '11.0', '-z', '0.1'
            ],
            output='screen'
        ),

        # 4. 벽 감지 노드
        Node(
            package='maze_escaper_3_9',
            executable='wall_detector',
            output='screen'
        ),

        # 5. 색상 감지 노드
        Node(
            package='maze_escaper_3_9',
            executable='color_detector',
            output='screen'
        ),

        # 6. 미로 탈출 노드
        Node(
            package='maze_escaper_3_9',
            executable='maze_escaper',
            output='screen'
            
        ),
        # 7. teleop (새 터미널 창으로 실행)
        ExecuteProcess(
            cmd=['xterm', '-e', 'ros2 run teleop_twist_keyboard teleop_twist_keyboard'],
            output='screen'
        ),
    ])