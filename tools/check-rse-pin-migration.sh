#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
repo_root="$(git rev-parse --show-toplevel)"
kicad_python=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3
kicad_cli=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
review_dir="$repo_root/hardware/coupon/rev-a/build/rse-pin-correction"
board="$repo_root/hardware/coupon/rev-a/staging/led-rse-corrected-routing-trial-114mm.kicad_pcb"
mkdir -p "$review_dir"
python3 "$repo_root/tools/check-rse-pin-migration-plan.py"
python3 "$repo_root/tools/check-coupon-study-contract.py" --board "$board"
"$kicad_cli" pcb drc --format json --output "$review_dir/current-drc.json" "$board"
"$kicad_python" "$repo_root/tools/audit-rse-pin-migration.py" --board "$board" \
  --report "$review_dir/current-audit.json" --require-complete --drc "$review_dir/current-drc.json"
"$kicad_python" "$repo_root/tools/generate-rse-pin-migration.py" --output "$review_dir/validation-replay-a.kicad_pcb"
"$kicad_python" "$repo_root/tools/generate-rse-pin-migration.py" --output "$review_dir/validation-replay-b.kicad_pcb"
cmp "$board" "$review_dir/validation-replay-a.kicad_pcb"
cmp "$board" "$review_dir/validation-replay-b.kicad_pcb"
"$kicad_python" "$repo_root/tools/test-rse-pin-migration-guards.py" --board "$board"
