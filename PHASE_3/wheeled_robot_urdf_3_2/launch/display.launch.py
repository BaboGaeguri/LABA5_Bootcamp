"""
launch/display.launch.py
========================
robot_state_publisher + joint_state_publisher_gui + RViz를
한 번에 실행하는 ROS2 launch 파일
"""

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    # URDF 파일 경로 설정
    urdf_file = os.path.join(
        get_package_share_directory('wheeled_robot_urdf_3_2'),
        'urdf',
        'wheeled_robot.urdf'
    )

    # RViz 설정 파일 경로
    rviz_config = os.path.join(
        get_package_share_directory('wheeled_robot_urdf_3_2'),
        'rviz',
        'robot_view.rviz'
    )

    # robot_description 파라미터 = URDF 파일 내용
    robot_description = ParameterValue(
        Command(['cat ', urdf_file]),
        value_type=str
    )

    return LaunchDescription([

        # ── 1. robot_state_publisher ──────────────────────────────
        # URDF를 파싱하여 TF 트리를 퍼블리시
        # /robot_description 토픽으로 URDF 내용 전달
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{
                'robot_description': robot_description,
                'use_sim_time': False
            }],
            output='screen'
        ),

        # ── 2. joint_state_publisher_gui ─────────────────────────
        # 슬라이더 GUI로 joint 값 조작
        # → left_wheel_joint, right_wheel_joint 슬라이더 생성
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            output='screen'
        ),

        # ── 3. RViz2 ─────────────────────────────────────────────
        # 3D 시각화 도구
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config],
            output='screen'
        ),

    ])
