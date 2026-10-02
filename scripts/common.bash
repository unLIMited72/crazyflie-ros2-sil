#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# 공통 경로 및 외부 workspace 오염 방지
CRAZYSIM_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
export CRAZYSIM_ROOT
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
export PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_CACHE_DIR="$CRAZYSIM_ROOT/cache/pip"
export ROS_LOG_DIR="$CRAZYSIM_ROOT/log/ros"
fail() { printf '[FAIL] %s\n' "$*" >&2; exit 1; }
pass() { printf '[PASS] %s\n' "$*"; }
clean_ros() {
    unset AMENT_PREFIX_PATH CMAKE_PREFIX_PATH COLCON_PREFIX_PATH PYTHONPATH
    unset ROS_PACKAGE_PATH ROS_DISTRO ROS_VERSION ROS_PYTHON_VERSION
    unset VIRTUAL_ENV LD_LIBRARY_PATH
    export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
    [[ -f /opt/ros/humble/setup.bash ]] || fail "ROS2 Humble을 찾을 수 없습니다. 먼저 설치하십시오. Expected: /opt/ros/humble/setup.bash"
    source /opt/ros/humble/setup.bash
}
