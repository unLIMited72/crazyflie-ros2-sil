#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -eo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/common.bash"
clean_ros
source "$CRAZYSIM_ROOT/.venv/bin/activate"
firmware="$CRAZYSIM_ROOT/crazyflie-firmware"
cmake -S "$firmware/sitl_make" -B "$firmware/sitl_make/build"
# all은 Gazebo plugin까지 빌드합니다. 이 baseline에는 cf2 target만 필요합니다.
cmake --build "$firmware/sitl_make/build" --target cf2 -j "${CRAZYSIM_BUILD_JOBS:-2}"
[[ -x "$firmware/sitl_make/build/cf2" ]] || fail 'firmware cf2 생성 실패'
pass 'firmware SITL 빌드 완료'
