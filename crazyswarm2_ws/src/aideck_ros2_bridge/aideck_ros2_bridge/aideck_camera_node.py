#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

"""
ROS 2 bridge for the Crazyflie AI Deck camera.

Data flow:

CrazySim Camera
    ↓
CPX TCP server
    ↓
CPXCameraTransport
    ↓
AIDeckImageDecoder
    ↓
sensor_msgs/Image
    ↓
/cf231/camera/image_raw
"""

import threading
import time

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image

from aideck_ros2_bridge.cpx_transport import CPXCameraTransport
from aideck_ros2_bridge.image_decoder import AIDeckImageDecoder


class AIDeckCameraNode(Node):
    """
    Receive AI Deck camera frames over CPX and publish them as ROS 2 images.
    """

    def __init__(self) -> None:
        super().__init__('aideck_camera_node')

        # --------------------------------------------------
        # ROS 2 parameters
        # --------------------------------------------------

        self.declare_parameter(
            'host',
            '127.0.0.1'
        )

        self.declare_parameter(
            'port',
            5050
        )

        self.declare_parameter(
            'topic',
            '/cf231/camera/image_raw'
        )

        self.declare_parameter(
            'frame_id',
            'cf231_camera'
        )

        self.host = (
            self.get_parameter('host')
            .get_parameter_value()
            .string_value
        )

        self.port = (
            self.get_parameter('port')
            .get_parameter_value()
            .integer_value
        )

        self.topic = (
            self.get_parameter('topic')
            .get_parameter_value()
            .string_value
        )

        self.frame_id = (
            self.get_parameter('frame_id')
            .get_parameter_value()
            .string_value
        )

        # --------------------------------------------------
        # ROS 2 image publisher
        # --------------------------------------------------

        self.image_pub = self.create_publisher(
            Image,
            self.topic,
            qos_profile_sensor_data,
        )

        # --------------------------------------------------
        # Camera transport and decoder
        # --------------------------------------------------

        self.transport = CPXCameraTransport(
            host=self.host,
            port=self.port,
        )

        self.decoder = AIDeckImageDecoder()

        # Used when shutting the node down
        self.stop_event = threading.Event()

        # --------------------------------------------------
        # Start camera receiver in another thread
        # --------------------------------------------------

        self.receiver_thread = threading.Thread(
            target=self._receiver_loop,
            daemon=True,
        )

        self.receiver_thread.start()

        self.get_logger().info(
            f'AI Deck camera bridge started'
        )

        self.get_logger().info(
            f'CPX camera: {self.host}:{self.port}'
        )

        self.get_logger().info(
            f'ROS 2 topic: {self.topic}'
        )

    # ------------------------------------------------------
    # Camera receiving loop
    # ------------------------------------------------------

    def _receiver_loop(self) -> None:
        """
        Continuously receive camera frames from the CPX TCP server.
        """

        while (
            rclpy.ok()
            and not self.stop_event.is_set()
        ):

            try:
                self.get_logger().info(
                    f'Connecting to CPX camera server '
                    f'{self.host}:{self.port}...'
                )

                self.transport.connect()

                self.get_logger().info(
                    'Connected to CPX camera server'
                )

                # ------------------------------------------
                # Receive frames continuously
                # ------------------------------------------

                while (
                    rclpy.ok()
                    and not self.stop_event.is_set()
                ):

                    header_bytes, image_bytes = (
                        self.transport.receive_camera_message()
                    )

                    try:
                        header, frame = self.decoder.decode(
                            header_bytes,
                            image_bytes,
                        )

                    except ValueError as exc:
                        self.get_logger().warning(
                            f'Invalid camera frame: {exc}'
                        )
                        continue

                    self._publish_frame(
                        frame=frame,
                        width=header.width,
                        height=header.height,
                    )

            except (
                ConnectionError,
                OSError,
            ) as exc:

                if self.stop_event.is_set():
                    break

                self.get_logger().warning(
                    f'CPX camera connection lost: {exc}'
                )

                self.transport.close()

                self.get_logger().info(
                    'Retrying connection in 1 second...'
                )

                time.sleep(1.0)

    # ------------------------------------------------------
    # Convert NumPy frame → ROS 2 Image
    # ------------------------------------------------------

    def _publish_frame(
        self,
        frame,
        width: int,
        height: int,
    ) -> None:
        """
        Publish one grayscale frame as sensor_msgs/Image.
        """

        msg = Image()

        # ROS timestamp
        msg.header.stamp = (
            self.get_clock()
            .now()
            .to_msg()
        )

        msg.header.frame_id = self.frame_id

        # Image dimensions
        msg.height = height
        msg.width = width

        # HM01B0 / CrazySim grayscale image
        msg.encoding = 'mono8'

        # Little endian
        msg.is_bigendian = 0

        # Number of bytes in one image row
        msg.step = width

        # NumPy image → raw byte array
        msg.data = frame.tobytes()

        # Publish
        self.image_pub.publish(msg)

    # ------------------------------------------------------
    # Shutdown
    # ------------------------------------------------------

    def shutdown(self) -> None:

        self.stop_event.set()

        self.transport.close()


def main(args=None) -> None:

    rclpy.init(args=args)

    node = AIDeckCameraNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.shutdown()
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
