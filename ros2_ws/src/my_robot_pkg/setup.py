from setuptools import setup

package_name = 'my_robot_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='user@todo.todo',
    description='Keyboard cmd_vel publisher',
    license='TODO',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'keyboard_cmd_vel = my_robot_pkg.keyboard_cmd_vel:main',
        ],
    },
)

