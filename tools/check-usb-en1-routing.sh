#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
repo_root="$(git rev-parse --show-toplevel)"
kicad_python=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3
review_dir="$repo_root/hardware/coupon/rev-a/build/usb-en1-locality"
board="$repo_root/hardware/coupon/rev-a/staging/led-usb-en1-routing-trial-114mm.kicad_pcb"
mkdir -p "$review_dir"
python3 "$repo_root/tools/check-usb-en1-routing-plan.py"
python3 "$repo_root/tools/check-coupon-study-contract.py" --board "$board"
python3 "$repo_root/tools/check-board-pin-map.py"
"$kicad_python" "$repo_root/tools/check-usb-en1-routing.py" --board "$board"
"$kicad_python" "$repo_root/tools/generate-usb-en1-routing.py" --output "$review_dir/validation-replay-a.kicad_pcb"
"$kicad_python" "$repo_root/tools/generate-usb-en1-routing.py" --output "$review_dir/validation-replay-b.kicad_pcb"
cmp "$board" "$review_dir/validation-replay-a.kicad_pcb"
cmp "$board" "$review_dir/validation-replay-b.kicad_pcb"
"$kicad_python" "$repo_root/tools/test-usb-en1-routing-guards.py" --board "$board"
