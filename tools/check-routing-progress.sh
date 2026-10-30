#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
repo_root="$(git rev-parse --show-toplevel)"
kicad_python=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3
kicad_cli=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
review_dir="$repo_root/hardware/coupon/rev-a/build/routing-progress-review"
board="$repo_root/hardware/coupon/rev-a/staging/led-routing-progress-trial-114mm.kicad_pcb"
mkdir -p "$review_dir"
python3 "$repo_root/tools/check-routing-progress-plan.py"
python3 "$repo_root/tools/check-coupon-study-contract.py" --board "$board"
"$kicad_cli" pcb drc --format json --output "$review_dir/drc.json" "$board"
"$kicad_python" "$repo_root/tools/generate-routing-orphan-witness.py" --output "$review_dir/restored-orphan-vias.kicad_pcb"
"$kicad_cli" pcb drc --format json --output "$review_dir/restored-orphan-vias.json" "$review_dir/restored-orphan-vias.kicad_pcb"
"$kicad_python" "$repo_root/tools/check-routing-progress-trial.py" \
  --drc "$review_dir/drc.json" --report "$review_dir/check.json" \
  --restored-via-board "$review_dir/restored-orphan-vias.kicad_pcb" \
  --restored-via-drc "$review_dir/restored-orphan-vias.json"
"$kicad_python" "$repo_root/tools/check-coupon-led-placement.py" "$board"
"$kicad_python" "$repo_root/tools/test-routing-progress-guards.py" -v
