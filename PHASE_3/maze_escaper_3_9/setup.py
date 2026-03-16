from setuptools import find_packages, setup

package_name = 'maze_escaper_3_9'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/urdf', ['urdf/wheeled_robot.urdf']),
        ('share/' + package_name + '/launch', ['launch/maze_escaper.launch.py']),
        ('share/' + package_name + '/worlds', ['worlds/escape_maze.world']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='babogaeguri',
    maintainer_email='psyun0323@gmail.com',
    description='Maze escape robot with LiDAR and camera',
    license='TODO: License declaration',
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'wall_detector = maze_escaper_3_9.wall_detector:main',
            'color_detector = maze_escaper_3_9.color_detector:main',
            'maze_escaper = maze_escaper_3_9.maze_escaper:main',
        ],
    },
)