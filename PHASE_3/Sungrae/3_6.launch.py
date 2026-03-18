from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
import os

def generate_launch_description():
    # 1. 미로 맵으로 경로 수정 완료!
    world = os.path.expanduser("~/ros2_ws/src/robot_control/world/maze_world.sdf")
    robot = os.path.expanduser("~/ros2_ws/src/robot_control/urdf/simple_robot.urdf")

    # URDF 파일 읽기
    with open(robot, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([

        ExecuteProcess(
            cmd=['gz', 'sim', world],
            output='screen'
        ),

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

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_desc}],
            output='screen'
        ),

        # 바퀴 등 움직이는 관절의 기본 각도 상태를 발행해 주는 노드
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            output='screen'
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            output='screen'
        ),

        # 2. 브리지에 /scan 완벽 추가!
        # 브리지 설정 수정
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=[
                '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
                '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
                # 카메라 브리지 추가 (GZ -> ROS 방향)
                '/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image'
            ],
            output='screen'
        ),

        # 키보드 터미널 자동 실행
        ExecuteProcess(
            cmd=['gnome-terminal', '--', 'ros2', 'run', 'robot_control', 'keyboard_cmd_vel'],
            output='screen'
        ),
    ])