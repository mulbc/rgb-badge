#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
repo_root="$(git rev-parse --show-toplevel)"
kicad_python=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3
review_dir="$repo_root/hardware/coupon/rev-a/build/gauge-supply-routing"
board="$repo_root/hardware/coupon/rev-a/staging/led-gauge-routing-trial-114mm.kicad_pcb"
mkdir -p "$review_dir"
python3 "$repo_root/tools/check-gauge-supply-routing-plan.py"
python3 "$repo_root/tools/check-coupon-study-contract.py" --board "$board"
python3 "$repo_root/tools/check-board-pin-map.py"
"$kicad_python" "$repo_root/tools/check-gauge-supply-routing.py" --board "$board"
"$kicad_python" "$repo_root/tools/generate-gauge-supply-routing.py" --output "$review_dir/replay-a.kicad_pcb"
"$kicad_python" "$repo_root/tools/generate-gauge-supply-routing.py" --output "$review_dir/replay-b.kicad_pcb"
cmp "$board" "$review_dir/replay-a.kicad_pcb"
cmp "$board" "$review_dir/replay-b.kicad_pcb"
"$kicad_python" "$repo_root/tools/test-gauge-supply-routing-guards.py" --board "$board"
