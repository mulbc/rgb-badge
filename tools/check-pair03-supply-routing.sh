#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
repo_root="$(git rev-parse --show-toplevel)"
kicad_python=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3
review_dir="$repo_root/hardware/coupon/rev-a/build/pair03-supply-routing"
board="$repo_root/hardware/coupon/rev-a/staging/led-pair03-supply-routing-trial-114mm.kicad_pcb"
mkdir -p "$review_dir"
python3 "$repo_root/tools/check-pair03-supply-plan.py"
python3 "$repo_root/tools/check-coupon-study-contract.py" --board "$board"
python3 "$repo_root/tools/check-board-pin-map.py"
"$kicad_python" "$repo_root/tools/check-pair03-supply-routing.py" --board "$board"
"$kicad_python" "$repo_root/tools/generate-pair03-supply-routing.py" --output "$review_dir/replay-a.kicad_pcb"
"$kicad_python" "$repo_root/tools/generate-pair03-supply-routing.py" --output "$review_dir/replay-b.kicad_pcb"
cmp "$board" "$review_dir/replay-a.kicad_pcb"
cmp "$board" "$review_dir/replay-b.kicad_pcb"
"$kicad_python" "$repo_root/tools/test-pair03-supply-guards.py" --board "$board"
