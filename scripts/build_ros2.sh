#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -eo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/common.bash"
clean_ros
export ROS_HOME="$CRAZYSIM_ROOT/cache/ros_home"
export ROSDEP_SOURCE_PATH="$CRAZYSIM_ROOT/cache/rosdep/sources.list.d"
export XDG_CACHE_HOME="$CRAZYSIM_ROOT/cache/xdg"
source "$CRAZYSIM_ROOT/.venv/bin/activate"
cd "$CRAZYSIM_ROOT/crazyswarm2_ws"
if [[ $# -gt 1 || ( $# -eq 1 && "$1" != --skip-rosdep-check ) ]]; then
    fail '사용법: build_ros2.sh [--skip-rosdep-check]'
fi
if [[ "${1:-}" == --skip-rosdep-check ]]; then
    echo '[WARN] 명시적으로 rosdep 사전 검사 생략. 이미 의존성이 설치된 격리 QA 용도입니다.'
elif ! rosdep check --from-paths src --ignore-src --rosdistro humble; then
    echo '[FAIL] ROS dependency가 없거나 rosdep 데이터베이스가 준비되지 않았습니다.'
    echo '새 PC에서 docs/INSTALL.md의 rosdep 초기화/설치 절차를 실행하십시오.'
    exit 1
fi
python -m colcon build --symlink-install --parallel-workers "${CRAZYSIM_BUILD_JOBS:-2}" \
    --cmake-args -DCMAKE_BUILD_TYPE=Release "-DPython3_EXECUTABLE=$CRAZYSIM_ROOT/.venv/bin/python" \
    "-DPYTHON_EXECUTABLE=$CRAZYSIM_ROOT/.venv/bin/python" \
    -DBUILD_PYTHON_BINDINGS=OFF -DBUILD_CPP_EXAMPLES=OFF
source install/local_setup.bash
for pkg in crazysim_bringup aideck_ros2_bridge crazyflie crazyflie_interfaces; do
    prefix="$(ros2 pkg prefix "$pkg")"
    [[ "$prefix" == "$CRAZYSIM_ROOT/crazyswarm2_ws/install/"* ]] || fail "$pkg 가 다른 workspace에서 검색됨: $prefix"
    pass "$pkg: $prefix"
done
