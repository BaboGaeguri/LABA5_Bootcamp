from setuptools import setup

package_name = 'breakout_bridge_pkg'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'orin_pub = breakout_bridge_pkg.orin_pub:main',
            'orin_sub = breakout_bridge_pkg.orin_sub:main',
            'nuc_pub  = breakout_bridge_pkg.nuc_pub:main',
            'nuc_sub  = breakout_bridge_pkg.nuc_sub:main',
        ],
    },
)
