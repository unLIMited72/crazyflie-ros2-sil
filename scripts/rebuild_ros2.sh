#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -eo pipefail
# build/install/log를 삭제하지 않고 증분 재빌드합니다.
exec "$(dirname -- "${BASH_SOURCE[0]}")/build_ros2.sh" "$@"
