from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
import os

def generate_launch_description():
    world = os.path.expanduser("~/ros2_ws/src/robot_control/world/maze_world.sdf")
    robot = os.path.expanduser("~/ros2_ws/src/robot_control/urdf/simple_robot.urdf")
    rviz_config = os.path.expanduser("~/ros2_ws/src/robot_control/rviz/maze.rviz")

    with open(robot, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([
        # 1. Gazebo 실행
        ExecuteProcess(cmd=['gz', 'sim', world], output='screen'),

        # 2. 로봇 스폰 (시작 위치를 미로 좌측 하단 입구로 지정)
        Node(package='ros_gz_sim', executable='create',
             arguments=['-file', robot, '-name', 'simple_robot', '-x', '-2.0', '-y', '-2.0', '-z', '0.1'], output='screen'),

        # 3. 로봇 상태 발행 (use_sim_time 추가!)
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             parameters=[{'robot_description': robot_desc, 'use_sim_time': True}], output='screen'),

# ★ 수정 1: 관절 상태 발행 노드에 robot_description 확실히 추가
        Node(package='joint_state_publisher', executable='joint_state_publisher',
             parameters=[{'robot_description': robot_desc, 'use_sim_time': True}], output='screen'),

        # ★ 수정 2: 브리지에 /clock 토픽 완벽하게 추가!
        Node(package='ros_gz_bridge', executable='parameter_bridge',
             arguments=[
                 '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',   # <- 이거 꼭 추가해야 해!
                 '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
                 '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
                 '/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image'
             ], output='screen'),

        # 5. 브리지 (cmd_vel, scan, camera)
        Node(package='ros_gz_bridge', executable='parameter_bridge',
             arguments=[
                 '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
                 '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
                 '/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image'
             ], output='screen'),

        # 🌟 수정: RViz2 실행 시 저장한 설정 파일(-d)을 불러오도록 변경!
        Node(package='rviz2', executable='rviz2', 
             arguments=['-d', rviz_config],
             parameters=[{'use_sim_time': True}], output='screen'),

          # (기존에 있던 Gazebo, Bridge, RViz 노드들 밑에 아래 내용 추가!)
        
        # 🌟 1. 라이다 프로세서 노드 (거리 센서 전처리)
        Node(
            package='robot_control',
            executable='lidar_processor',
            name='lidar_processor',
            output='screen'
        ),

        # 🌟 2. 비전 노드 (빨간색, 초록색 색상 인식)
        Node(
            package='robot_control',
            executable='color_detector',
            name='color_detector',
            output='screen'
        ),

        # 🌟 3. 최종 두뇌 노드 (동적 시야각 + 왼손 법칙 상태 머신)
        Node(
            package='robot_control',
            executable='maze_solver',
            name='maze_solver',
            output='screen'
        ),

        # 🌟 4. 수동 조종기 노드 (키보드 입력을 위해 ⭐️새 터미널 창 띄우기⭐️)
        Node(
            package='robot_control',
            executable='keyboard_cmd_vel',
            name='keyboard_cmd_vel',
            output='screen',
            prefix='gnome-terminal --'  # 우분투 기본 터미널을 새 창으로 엽니다!
        ),
    ])