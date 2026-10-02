#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -eo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/common.bash"
errors=0
if ! "$CRAZYSIM_ROOT/scripts/setup_sources.sh" --check; then errors=$((errors + 1)); fi
check() {
    local label="$1"; shift
    if "$@" >/dev/null 2>&1; then pass "$label"; else echo "[FAIL] $label"; errors=$((errors + 1)); fi
}
source /etc/os-release
check "Ubuntu 22.04.x ($PRETTY_NAME)" test "$ID:$VERSION_ID" = ubuntu:22.04
check 'ROS2 Humble 존재' test -f /opt/ros/humble/setup.bash
check 'venv 존재' test -x "$CRAZYSIM_ROOT/.venv/bin/python"
for cmd in colcon rosdep; do check "$cmd 존재" command -v "$cmd"; done
if [[ -x "$CRAZYSIM_ROOT/.venv/bin/python" && -f /opt/ros/humble/setup.bash ]]; then
    clean_ros
    source "$CRAZYSIM_ROOT/.venv/bin/activate"
    check 'Python 3.10' python -c 'import sys; assert sys.version_info[:2] == (3, 10)'
    for mod in mujoco numpy cflib tomli scipy transforms3d rclpy; do
        check "$mod import" python -c "import $mod"
    done
    if [[ -f "$CRAZYSIM_ROOT/crazyswarm2_ws/install/local_setup.bash" ]]; then
        source "$CRAZYSIM_ROOT/crazyswarm2_ws/install/local_setup.bash"
        for pkg in crazysim_bringup aideck_ros2_bridge crazyflie; do
            prefix="$(ros2 pkg prefix "$pkg" 2>/dev/null || true)"
            check "$pkg export prefix" test "$prefix" = "$CRAZYSIM_ROOT/crazyswarm2_ws/install/$pkg"
        done
        check '카메라 node 및 ROS message import' python -c 'from aideck_ros2_bridge.aideck_camera_node import AIDeckCameraNode; from crazyflie_interfaces.msg import Status'
        check 'cflib가 export source를 사용' python -c 'import cflib, os; from pathlib import Path; assert Path(cflib.__file__).resolve().is_relative_to(Path(os.environ["CRAZYSIM_ROOT"])/"crazyflie-lib-python")'
    else
        echo '[FAIL] ROS2 install 없음'; errors=$((errors + 1))
    fi
fi
check 'firmware SITL binary' test -x "$CRAZYSIM_ROOT/crazyflie-firmware/sitl_make/build/cf2"
[[ -n "${DISPLAY:-}" ]] || echo '[WARN] DISPLAY 없음. GUI MuJoCo launch는 그래픽 세션에서 확인하십시오.'
[[ "$errors" == 0 ]]
