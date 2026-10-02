#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -eo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/common.bash"
source "$CRAZYSIM_ROOT/config/crazysim_env.bash"
exec timeout --signal=TERM --kill-after=3s 30s "$CRAZYSIM_ROOT/.venv/bin/python" "$CRAZYSIM_ROOT/scripts/verify_baseline.py"
