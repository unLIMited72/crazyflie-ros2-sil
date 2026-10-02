# SPDX-License-Identifier: Apache-2.0
from setuptools import find_packages, setup

package_name = 'aideck_ros2_bridge'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml', '../../../LICENSE']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='lab',
    maintainer_email='LimCraft7260@gmail.com',
    description='AI Deck CPX camera to ROS2 Image bridge',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'aideck_camera_node = aideck_ros2_bridge.aideck_camera_node:main'
        ],
    },
)
