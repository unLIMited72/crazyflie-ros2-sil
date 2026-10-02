#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -eo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/common.bash"
clean_ros
# 시스템 /etc/ros 및 기존 ~/.ros를 변경하지 않고 이 clone 전용 데이터베이스 사용.
export ROS_HOME="$CRAZYSIM_ROOT/cache/ros_home"
export ROSDEP_SOURCE_PATH="$CRAZYSIM_ROOT/cache/rosdep/sources.list.d"
export XDG_CACHE_HOME="$CRAZYSIM_ROOT/cache/xdg"
mkdir -p "$ROSDEP_SOURCE_PATH"
if [[ ! -f "$ROSDEP_SOURCE_PATH/20-crazysim.list" ]]; then
    cat > "$ROSDEP_SOURCE_PATH/20-crazysim.list" <<'LIST'
yaml https://raw.githubusercontent.com/ros/rosdistro/master/rosdep/base.yaml
yaml https://raw.githubusercontent.com/ros/rosdistro/master/rosdep/python.yaml
yaml https://raw.githubusercontent.com/ros/rosdistro/master/rosdep/ruby.yaml
LIST
fi
if [[ ! -f "$ROS_HOME/rosdep/sources.cache/index" ]]; then
    rosdep update --rosdistro humble
fi
if rosdep check --from-paths "$CRAZYSIM_ROOT/crazyswarm2_ws/src" --ignore-src --rosdistro humble; then
    pass 'ROS dependency 이미 설치됨'
elif [[ "${CRAZYSIM_INSTALL_SYSTEM_DEPS:-0}" == 1 ]]; then
    rosdep install --from-paths "$CRAZYSIM_ROOT/crazyswarm2_ws/src" --ignore-src -r -y --rosdistro humble
else
    echo '[FAIL] ROS 시스템 dependency가 누락됐습니다.'
    echo '설치를 허용하려면 CRAZYSIM_INSTALL_SYSTEM_DEPS=1 ./scripts/bootstrap.sh 로 재실행하십시오.'
    echo 'rosdep이 요청하는 sudo/APT 설치는 사용자 PC에서만 실행됩니다.'
    exit 1
fi
