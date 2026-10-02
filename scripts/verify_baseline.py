#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""실행 중인 SIL을 읽기 전용 구독으로 검증합니다. command는 보내지 않습니다."""
import time
import rclpy
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image

def main():
    rclpy.init()
    node = rclpy.create_node("crazysim_baseline_verifier")
    images = []
    def receive(msg):
        images.append((time.monotonic(), msg.width, msg.height, msg.encoding, msg.step, len(msg.data)))
    subscription = node.create_subscription(Image, "/cf231/camera/image_raw", receive, qos_profile_sensor_data)
    deadline = time.monotonic() + 15
    nodes, topics = set(), set()
    try:
        while time.monotonic() < deadline:
            rclpy.spin_once(node, timeout_sec=0.2)
            nodes = {("/" if ns == "/" else ns + "/") + name for name, ns in node.get_node_names_and_namespaces()}
            topics = {name for name, _ in node.get_topic_names_and_types()}
        failed = False
        for name in ["/crazyflie_server", "/aideck_camera_node"]:
            ok = name in nodes
            print(f"[{'PASS' if ok else 'FAIL'}] node {name}")
            failed |= not ok
        for name in ["/cf231/pose", "/cf231/status", "/cf231/tof", "/cf231/flow", "/cf231/camera/image_raw"]:
            ok = name in topics
            print(f"[{'PASS' if ok else 'FAIL'}] topic {name}")
            failed |= not ok
        ok = bool(images) and all(x[1:] == (324, 244, "mono8", 324, 79056) for x in images)
        print(f"[{'PASS' if ok else 'FAIL'}] camera 수신/324x244/mono8/79056 bytes: {len(images)} frames")
        failed |= not ok
        if len(images) > 1:
            hz = (len(images) - 1) / (images[-1][0] - images[0][0])
            print(f"[{'PASS' if 12 <= hz <= 24 else 'WARN'}] camera {hz:.2f} Hz (기준 약 18 Hz, PC/GPU에 따라 변동)")
        if failed:
            print("[FAIL] docs/TROUBLESHOOTING.md: ROS domain, RMW, launch, TCP/UDP 연결을 확인하십시오.")
        return int(failed)
    finally:
        node.destroy_subscription(subscription)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    raise SystemExit(main())
