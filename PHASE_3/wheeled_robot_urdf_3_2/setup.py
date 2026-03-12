from setuptools import setup
import os
from glob import glob

package_name = 'wheeled_robot_urdf_3_2'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # URDF 파일 포함
        (os.path.join('share', package_name, 'urdf'),
            glob('urdf/*.urdf')),
        # Launch 파일 포함
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.py')),
        # RViz 설정 포함
        (os.path.join('share', package_name, 'rviz'),
            glob('rviz/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    description='2-wheeled robot with caster URDF',
    license='Apache-2.0',
    entry_points={},
)
