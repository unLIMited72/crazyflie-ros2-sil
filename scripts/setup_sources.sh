#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -eo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/common.bash"
exec python3 "$CRAZYSIM_ROOT/scripts/manage_sources.py" "$@"
