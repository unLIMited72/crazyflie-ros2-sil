#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -eo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/common.bash"
source /etc/os-release
[[ "$ID" == ubuntu && "$VERSION_ID" == 22.04 ]] || fail '지원 환경: Ubuntu 22.04.x'
clean_ros
for cmd in git python3 pip3 colcon rosdep cmake gcc g++ make pkg-config; do
    command -v "$cmd" >/dev/null || fail "$cmd 없음. docs/INSTALL.md의 사전 시스템 준비가 필요합니다."
done
python3 -c 'import sys, venv; assert sys.version_info[:2] == (3,10)' || fail 'Python 3.10 / python3-venv가 필요합니다.'
"$CRAZYSIM_ROOT/scripts/setup_sources.sh"
"$CRAZYSIM_ROOT/scripts/setup_python.sh"
"$CRAZYSIM_ROOT/scripts/setup_firmware.sh"
"$CRAZYSIM_ROOT/scripts/setup_ros_dependencies.sh"
"$CRAZYSIM_ROOT/scripts/build_ros2.sh"
"$CRAZYSIM_ROOT/scripts/verify_environment.sh"
echo '[PASS] bootstrap 완료. 다음 명령으로 실행하십시오.'
printf 'source %q\n' "$CRAZYSIM_ROOT/config/crazysim_env.bash"
echo 'use_crazysim_ros'
echo 'ros2 launch crazysim_bringup single_cf.launch.py'
