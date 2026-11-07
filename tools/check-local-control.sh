#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Full acceptance of the latest combined routing geometry study.
set -euo pipefail
repo_root="$(git rev-parse --show-toplevel)"
kicad_python=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3
kicad_cli=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
review_dir="$repo_root/hardware/coupon/rev-a/build/local-control-review"
mkdir -p "$review_dir"
"$kicad_cli" pcb drc --format json --output "$review_dir/drc.json" \
  "$repo_root/hardware/coupon/rev-a/staging/led-local-control-trial-114mm.kicad_pcb"
"$kicad_python" "$repo_root/tools/check-local-control-trial.py" \
  --drc "$review_dir/drc.json" --report "$review_dir/check.json"
"$kicad_python" "$repo_root/tools/check-coupon-led-placement.py" \
  "$repo_root/hardware/coupon/rev-a/staging/led-local-control-trial-114mm.kicad_pcb"
