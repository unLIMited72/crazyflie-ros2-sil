#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

"""
Camera-only CPX transport for the AI Deck ROS 2 bridge.

Responsibilities:
- Connect to the CrazySim CPX TCP server.
- Receive CPX packets.
- Ignore non-camera CPX functions.
- Reassemble one complete AI Deck image message.

This module does NOT:
- control the Crazyflie
- send CRTP commands
- use cflib Crazyflie()
- publish ROS 2 messages
"""

from dataclasses import dataclass
import socket
import struct
from typing import Optional


@dataclass(frozen=True)
class CPXPacket:
    """
    One decoded CPX packet.
    """

    source: int
    destination: int
    function: int
    last: bool
    data: bytes


class CPXCameraTransport:
    """
    Receive AI Deck camera data from a CPX TCP server.
    """

    # CPX target IDs
    CPX_T_HOST = 3
    CPX_T_GAP8 = 4

    # CPX function ID for application data
    CPX_F_APP = 5

    # CPX wire header:
    #
    # uint16 length
    # uint8  routing
    # uint8  function
    #
    CPX_WIRE_HEADER_SIZE = 4
    CPX_INTERNAL_HEADER_SIZE = 2

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 5050,
        timeout: float = 2.0,
    ) -> None:

        self.host = host
        self.port = port
        self.timeout = timeout

        self._sock: Optional[socket.socket] = None

    def connect(self) -> None:
        """
        Connect to the CrazySim CPX TCP server.
        """

        if self._sock is not None:
            return

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )

        sock.settimeout(self.timeout)

        sock.connect(
            (self.host, self.port)
        )

        sock.setsockopt(
            socket.IPPROTO_TCP,
            socket.TCP_NODELAY,
            1,
        )

        self._sock = sock

    def close(self) -> None:
        """
        Close the TCP connection.
        """

        if self._sock is None:
            return

        try:
            self._sock.close()
        finally:
            self._sock = None

    def _recv_exact(self, size: int) -> bytes:
        """
        Receive exactly 'size' bytes from TCP.

        TCP does not guarantee that one recv() call returns
        all requested bytes, so we keep reading until enough
        data has arrived.
        """

        if self._sock is None:
            raise ConnectionError(
                "CPX transport is not connected"
            )

        buffer = bytearray()

        while len(buffer) < size:

            chunk = self._sock.recv(
                size - len(buffer)
            )

            if not chunk:
                raise ConnectionError(
                    "CPX server disconnected"
                )

            buffer.extend(chunk)

        return bytes(buffer)

    def receive_packet(self) -> CPXPacket:
        """
        Receive and decode one CPX packet.
        """

        header = self._recv_exact(
            self.CPX_WIRE_HEADER_SIZE
        )

        length, route, function_byte = struct.unpack(
            "<HBB",
            header,
        )

        if length < self.CPX_INTERNAL_HEADER_SIZE:
            raise ValueError(
                f"Invalid CPX packet length: {length}"
            )

        data_length = (
            length - self.CPX_INTERNAL_HEADER_SIZE
        )

        destination = route & 0x07
        source = (route >> 3) & 0x07
        last = bool(route & 0x40)

        function = function_byte & 0x3F

        if data_length > 0:
            data = self._recv_exact(
                data_length
            )
        else:
            data = b""

        return CPXPacket(
            source=source,
            destination=destination,
            function=function,
            last=last,
            data=data,
        )

    def receive_camera_message(
        self,
    ) -> tuple[bytes, bytes]:
        """
        Receive one complete AI Deck camera message.

        The CrazySim CPX bridge sends:

            CPX APP packet
                ↓
            11-byte image header
                ↓
            multiple CPX APP packets
                ↓
            image pixel payload

        Returns:
            (image_header_bytes, image_payload_bytes)
        """

        # --------------------------------------------------
        # Find the beginning of an image
        # --------------------------------------------------

        while True:

            packet = self.receive_packet()

            if (
                packet.function == self.CPX_F_APP
                and packet.source == self.CPX_T_GAP8
                and packet.destination == self.CPX_T_HOST
            ):
                break

        image_header = packet.data

        # Header packet must NOT be the last packet.
        if packet.last:
            raise ValueError(
                "Unexpected end of CPX image message "
                "at header packet"
            )

        # --------------------------------------------------
        # Receive image payload packets
        # --------------------------------------------------

        payload = bytearray()

        while True:

            packet = self.receive_packet()

            # Ignore non-camera packets if any appear.
            if packet.function != self.CPX_F_APP:
                continue

            if packet.source != self.CPX_T_GAP8:
                continue

            if packet.destination != self.CPX_T_HOST:
                continue

            payload.extend(
                packet.data
            )

            if packet.last:
                break

        return (
            image_header,
            bytes(payload),
        )

    def __enter__(self):
        """
        Allow:

            with CPXCameraTransport(...) as transport:
                ...
        """

        self.connect()
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        self.close()
