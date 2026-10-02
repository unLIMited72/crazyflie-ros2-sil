#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

"""
AI Deck image packet decoder.

This module is responsible only for:

1. Parsing the AI Deck image header.
2. Validating image metadata.
3. Converting raw image bytes into a NumPy grayscale image.

It does not handle:
- TCP / CPX communication
- ROS 2
- Crazyflie commands
"""

from dataclasses import dataclass
import struct

import numpy as np


@dataclass(frozen=True)
class AIDeckImageHeader:
    """
    Metadata contained in the AI Deck image header.

    Header format:
        <BHHBBI

    Fields:
        magic   : Packet identifier. Expected value is 0xBC.
        width   : Image width in pixels.
        height  : Image height in pixels.
        depth   : Pixel depth information supplied by the stream.
        format  : Image format information supplied by the stream.
        size    : Number of image payload bytes.
    """

    magic: int
    width: int
    height: int
    depth: int
    format: int
    size: int


class AIDeckImageDecoder:
    """
    Decoder for AI Deck image headers and grayscale image payloads.
    """

    MAGIC = 0xBC

    HEADER_FORMAT = "<BHHBBI"
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

    # Current CrazySim / AI Deck FPV stream configuration
    DEFAULT_WIDTH = 324
    DEFAULT_HEIGHT = 244

    def parse_header(self, data: bytes) -> AIDeckImageHeader:
        """
        Parse the AI Deck image header.

        Args:
            data:
                Bytes containing at least the complete image header.

        Returns:
            Parsed AIDeckImageHeader.

        Raises:
            ValueError:
                If the input is too short or the magic byte is invalid.
        """

        if len(data) < self.HEADER_SIZE:
            raise ValueError(
                f"Image header is too short: "
                f"received {len(data)} bytes, "
                f"expected at least {self.HEADER_SIZE}"
            )

        magic, width, height, depth, image_format, size = struct.unpack(
            self.HEADER_FORMAT,
            data[:self.HEADER_SIZE],
        )

        if magic != self.MAGIC:
            raise ValueError(
                f"Invalid AI Deck image magic: "
                f"0x{magic:02X}, expected 0x{self.MAGIC:02X}"
            )

        if width <= 0 or height <= 0:
            raise ValueError(
                f"Invalid image dimensions: {width}x{height}"
            )

        if size <= 0:
            raise ValueError(
                f"Invalid image payload size: {size}"
            )

        return AIDeckImageHeader(
            magic=magic,
            width=width,
            height=height,
            depth=depth,
            format=image_format,
            size=size,
        )

    def decode_frame(
        self,
        image_bytes: bytes,
        header: AIDeckImageHeader,
    ) -> np.ndarray:
        """
        Decode a complete grayscale image payload.

        Args:
            image_bytes:
                Raw image payload received after the header.

            header:
                Previously parsed AI Deck image header.

        Returns:
            NumPy array with shape:

                (height, width)

            and dtype:

                uint8

        Raises:
            ValueError:
                If the payload size does not match the header or if the
                number of pixels is inconsistent with width x height.
        """

        if len(image_bytes) < header.size:
            raise ValueError(
                f"Incomplete image payload: "
                f"received {len(image_bytes)} bytes, "
                f"expected {header.size}"
            )

        # Ignore any bytes after the image payload.
        payload = image_bytes[:header.size]

        frame = np.frombuffer(
            payload,
            dtype=np.uint8,
        )

        expected_pixels = header.width * header.height

        if frame.size != expected_pixels:
            raise ValueError(
                f"Image payload does not match dimensions: "
                f"{frame.size} pixels received, "
                f"but {header.width}x{header.height} "
                f"requires {expected_pixels} pixels"
            )

        frame = frame.reshape(
            (header.height, header.width)
        )

        return frame

    def decode(
        self,
        header_bytes: bytes,
        image_bytes: bytes,
    ) -> tuple[AIDeckImageHeader, np.ndarray]:
        """
        Convenience method that parses the header and decodes the frame.

        Returns:
            (header, frame)
        """

        header = self.parse_header(header_bytes)

        frame = self.decode_frame(
            image_bytes,
            header,
        )

        return header, frame
