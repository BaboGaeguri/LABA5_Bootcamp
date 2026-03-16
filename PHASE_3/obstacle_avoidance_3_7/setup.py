from setuptools import find_packages, setup

package_name = 'obstacle_avoidance_3_7'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/urdf', ['urdf/wheeled_robot.urdf']),
        ('share/' + package_name + '/launch', ['launch/gazebo.launch.py']),
        ('share/' + package_name + '/worlds', ['worlds/maze.world']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='babogaeguri',
    maintainer_email='psyun0323@gmail.com',
    description='LiDAR-based obstacle avoidance',
    license='TODO: License declaration',
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'obstacle_avoidance = obstacle_avoidance_3_7.obstacle_avoidance:main',
        ],
    },
)