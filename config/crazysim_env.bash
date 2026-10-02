# SPDX-License-Identifier: Apache-2.0
# Bash에서 source 하십시오. 이 파일 위치로 clone 경로를 자동 결정합니다.
export CRAZYSIM_ROOT="${CRAZYSIM_ROOT:-$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)}"
export ROS_DOMAIN_ID="${ROS_DOMAIN_ID:-25}"
export RMW_IMPLEMENTATION="${RMW_IMPLEMENTATION:-rmw_fastrtps_cpp}"
export PYTHONNOUSERSITE=1
export ROS_LOG_DIR="$CRAZYSIM_ROOT/log/ros"
if [[ ! -f /opt/ros/humble/setup.bash ]]; then
    echo '[FAIL] ROS2 Humble 없음: /opt/ros/humble/setup.bash' >&2
    return 1
fi
source /opt/ros/humble/setup.bash
# 기존 같은 이름의 alias를 해제하여 함수를 확실히 등록합니다.
unalias use_crazysim use_crazyswarm use_crazysim_ros 2>/dev/null || true
function use_crazysim {
    [[ -f "$CRAZYSIM_ROOT/.venv/bin/activate" ]] || { echo '[FAIL] .venv 없음. bootstrap을 실행하십시오.'; return 1; }
    source "$CRAZYSIM_ROOT/.venv/bin/activate"
}
function use_crazyswarm {
    [[ -f "$CRAZYSIM_ROOT/crazyswarm2_ws/install/local_setup.bash" ]] || { echo '[FAIL] ROS2 build가 필요합니다.'; return 1; }
    source "$CRAZYSIM_ROOT/crazyswarm2_ws/install/local_setup.bash"
}
function use_crazysim_ros {
    use_crazysim && use_crazyswarm
}
use_crazysim_ros
