from setuptools import find_packages, setup

package_name = 'refactoring_3_8'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/full_system.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='babogaeguri',
    maintainer_email='psyun0323@gmail.com',
    description='Phase 3 system visualization and launch file integration',
    license='TODO: License declaration',
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [],
    },
)
