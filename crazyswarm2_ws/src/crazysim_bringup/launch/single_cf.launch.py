# SPDX-License-Identifier: Apache-2.0
import os

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    IncludeLaunchDescription,
    TimerAction,
)
from launch.launch_description_sources import (
    PythonLaunchDescriptionSource,
)
from launch.substitutions import (
    LaunchConfiguration,
)
from launch_ros.actions import Node
from ament_index_python.packages import (
    get_package_share_directory,
)


def generate_launch_description():

    # ------------------------------------------------------
    # Paths
    # ------------------------------------------------------

    home = os.path.expanduser('~')

    crazysim_root = os.environ.get(
        'CRAZYSIM_ROOT', os.path.join(home, 'CrazySim')
    )

    firmware_root = os.path.join(
        crazysim_root,
        'crazyflie-firmware'
    )

    sitl_script = os.path.join(
        firmware_root,
        'tools',
        'crazyflie-simulation',
        'simulator_files',
        'mujoco',
        'launch',
        'sitl_camera.sh'
    )

    crazyflie_share = (
        get_package_share_directory(
            'crazyflie'
        )
    )

    crazyflie_launch = os.path.join(
        crazyflie_share,
        'launch',
        'launch.py'
    )

    # ------------------------------------------------------
    # Launch arguments
    # ------------------------------------------------------

    model = LaunchConfiguration('model')
    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')
    scene = LaunchConfiguration('scene')

    model_arg = DeclareLaunchArgument(
        'model',
        default_value='cf2x_P250',
        description='CrazySim drone model'
    )

    x_arg = DeclareLaunchArgument(
        'x',
        default_value='0',
        description='Initial X position'
    )

    y_arg = DeclareLaunchArgument(
        'y',
        default_value='0',
        description='Initial Y position'
    )

    scene_arg = DeclareLaunchArgument(
        'scene',
        default_value=os.path.join(
            firmware_root,
            'tools',
            'crazyflie-simulation',
            'simulator_files',
            'mujoco',
            'scene.xml'
        ),
        description='MuJoCo scene XML file'
    )

    # ------------------------------------------------------
    # CrazySim + MuJoCo + Firmware SITL
    # ------------------------------------------------------

    crazysim = ExecuteProcess(
        cmd=[
            'bash',
            sitl_script,
            '-m',
            model,
            '-x',
            x,
            '-y',
            y,
            '-s',
            scene,
            '--flowdeck',
        ],
        cwd=firmware_root,
        output='screen',
    )

    # ------------------------------------------------------
    # Crazyswarm2
    #
    # CrazySim이 UDP port와 firmware를 먼저 준비할 시간을
    # 조금 확보한 뒤 Crazyswarm2를 실행한다.
    # ------------------------------------------------------

    crazyswarm2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            crazyflie_launch
        ),
        launch_arguments={
            'backend': 'cflib',
            'gui': 'false',
            'mocap': 'false',
            'teleop': 'false',
        }.items(),
    )

    delayed_crazyswarm2 = TimerAction(
        period=7.0,
        actions=[
            crazyswarm2
        ]
    )

    aideck_camera_node = Node(
        package='aideck_ros2_bridge',
        executable='aideck_camera_node',
        name='aideck_camera_node',
        output='screen',
        parameters=[{
            'host': '127.0.0.1',
            'port': 5050,
            'topic': '/cf231/camera/image_raw',
            'frame_id': 'cf231_camera',
        }],
    )

    delayed_aideck_camera = TimerAction(
        period=4.0,
        actions=[
            aideck_camera_node
        ]
    )


    # ------------------------------------------------------
    # Launch description
    # ------------------------------------------------------

    return LaunchDescription([
        model_arg,
        x_arg,
        y_arg,
        scene_arg,

        crazysim,
        delayed_aideck_camera,
        delayed_crazyswarm2,
    ])
