from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
import os

def generate_launch_description():
    world = os.path.expanduser("~/ros2_ws/src/robot_control/world/maze_world.sdf")
    robot = os.path.expanduser("~/ros2_ws/src/robot_control/urdf/simple_robot.urdf")

    with open(robot, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([
        # 1. Gazebo 실행
        ExecuteProcess(cmd=['gz', 'sim', world], output='screen'),

        # 2. 로봇 스폰
        Node(package='ros_gz_sim', executable='create',
             arguments=['-file', robot, '-name', 'simple_robot', '-z', '0.1'], output='screen'),

        # 3. 로봇 상태 발행 (TF)
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             parameters=[{'robot_description': robot_desc}], output='screen'),
        
        # 4. 관절 상태 발행
        Node(package='joint_state_publisher', executable='joint_state_publisher', output='screen'),

        # 5. RViz2
        Node(package='rviz2', executable='rviz2', output='screen'),

        # 6. 브리지 (cmd_vel, scan)
        Node(package='ros_gz_bridge', executable='parameter_bridge',
             arguments=[
                 '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
                 '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan'
             ], output='screen'),

        # 7. ★ 자율 주행 노드 추가 ★ (키보드 대신 이 녀석이 조종함)
        Node(
            package='robot_control',
            executable='obstacle_avoidance',
            output='screen'
        ),
    ])