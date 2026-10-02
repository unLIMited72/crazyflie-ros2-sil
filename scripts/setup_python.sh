#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -eo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/common.bash"
clean_ros
python3 -c 'import sys, venv; assert sys.version_info[:2] == (3,10)' || fail 'Python 3.10과 python3-venv가 필요합니다.'
if [[ ! -e "$CRAZYSIM_ROOT/.venv" ]]; then
    python3 -m venv --system-site-packages "$CRAZYSIM_ROOT/.venv" || fail 'venv 생성 실패. docs/INSTALL.md의 python3-venv 설치를 확인하십시오.'
fi
source "$CRAZYSIM_ROOT/.venv/bin/activate"
python -c 'import sys; assert sys.version_info[:2] == (3,10)'
python -m pip install -r "$CRAZYSIM_ROOT/requirements/build-tools.txt"
python -m pip install -r "$CRAZYSIM_ROOT/requirements/requirements-lock.txt"
# cflib만 설치합니다. fpv 구버전을 설치하면 UDP 지원 버전을 덮어쓰게 됩니다.
SETUPTOOLS_SCM_PRETEND_VERSION_FOR_CFLIB=0.1.33.post1.dev9+g3c1cb0d02 \
python -m pip install --no-build-isolation --no-deps -e "$CRAZYSIM_ROOT/crazyflie-lib-python"
python -c 'import mujoco, numpy, cflib, tomli, scipy, transforms3d; print("[PASS] Python runtime import")'
