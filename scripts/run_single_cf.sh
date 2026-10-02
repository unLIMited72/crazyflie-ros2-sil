#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -eo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/common.bash"
source "$CRAZYSIM_ROOT/config/crazysim_env.bash"
cd "$CRAZYSIM_ROOT"
if [[ $# -gt 0 && "$1" != *:=* ]]; then
    scene="$1"; shift
    if [[ "$scene" != /* ]]; then
        scene="$CRAZYSIM_ROOT/crazyflie-firmware/tools/crazyflie-simulation/simulator_files/mujoco/$scene"
    fi
    [[ -f "$scene" ]] || fail "scene 없음: $scene"
    set -- "scene:=$scene" "$@"
fi
exec ros2 launch crazysim_bringup single_cf.launch.py "$@"
