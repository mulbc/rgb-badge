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
python3 "$repo_root/tools/check-coupon-study-contract.py" --legacy-rse-study --board "$board"
"$kicad_cli" pcb drc --format json --output "$review_dir/drc.json" "$board"
"$kicad_python" "$repo_root/tools/generate-routing-orphan-witness.py" --output "$review_dir/restored-orphan-vias.kicad_pcb"
"$kicad_cli" pcb drc --format json --output "$review_dir/restored-orphan-vias.json" "$review_dir/restored-orphan-vias.kicad_pcb"
"$kicad_python" "$repo_root/tools/check-routing-progress-trial.py" \
  --drc "$review_dir/drc.json" --report "$review_dir/check.json" \
  --restored-via-board "$review_dir/restored-orphan-vias.kicad_pcb" \
  --restored-via-drc "$review_dir/restored-orphan-vias.json"
"$kicad_python" "$repo_root/tools/check-coupon-led-placement.py" "$board"
"$kicad_python" "$repo_root/tools/test-routing-progress-guards.py" -v

# ADR 0085: verify the selected child in addition to its immutable parent.
python3 "$repo_root/tools/check-converter-checkpoint-plan.py"
python3 "$repo_root/tools/check-coupon-study-contract.py" --legacy-rse-study --board "$repo_root/hardware/coupon/rev-a/staging/led-converter-routing-trial-114mm.kicad_pcb"
"$kicad_python" "$repo_root/tools/check-converter-checkpoint.py" --check-orphans
"$kicad_python" "$repo_root/tools/test-converter-checkpoint-guards.py"

# ADR 0090: validate the selected complete-stage routing-study successor.
python3 "$repo_root/tools/check-u36-stage-plan.py"
python3 "$repo_root/tools/check-coupon-study-contract.py" --legacy-rse-study --board "$repo_root/hardware/coupon/rev-a/staging/led-u36-stage-routing-trial-114mm.kicad_pcb"
"$kicad_python" "$repo_root/tools/check-u36-stage-checkpoint.py" --check-orphans
"$kicad_python" "$repo_root/tools/test-u36-stage-checkpoint-guards.py"

# ADR 0091: validate the ongoing zero-open-goal successor and cap geometry.
python3 "$repo_root/tools/check-routing-closure-plan.py"
python3 "$repo_root/tools/check-coupon-study-contract.py" --legacy-rse-study --board "$repo_root/hardware/coupon/rev-a/staging/led-routing-closure-trial-114mm.kicad_pcb"
"$kicad_python" "$repo_root/tools/check-routing-closure.py" --check-orphans
"$kicad_python" "$repo_root/tools/test-routing-closure-guards.py"
"$kicad_python" "$repo_root/tools/test-route-cap-contact.py"
"$kicad_python" "$repo_root/tools/test-native-zone-targets.py"

# ADR 0092: preserve the immutable 44-open source and check the switch successor.
python3 "$repo_root/tools/check-switch-routing-plan.py"
python3 "$repo_root/tools/check-coupon-study-contract.py" --legacy-rse-study --board "$repo_root/hardware/coupon/rev-a/staging/led-switch-routing-trial-114mm.kicad_pcb"
"$kicad_python" "$repo_root/tools/check-switch-routing.py" --check-orphans
"$kicad_python" "$repo_root/tools/test-switch-routing-guards.py"

# ADR 0091 continuation from the immutable switch checkpoint.
python3 "$repo_root/tools/check-remaining-routing-plan.py"
python3 "$repo_root/tools/check-coupon-study-contract.py" --legacy-rse-study --board "$repo_root/hardware/coupon/rev-a/staging/led-remaining-routing-trial-114mm.kicad_pcb"
"$kicad_python" "$repo_root/tools/check-remaining-routing.py" --check-orphans
"$kicad_python" "$repo_root/tools/test-remaining-routing-guards.py"

# Native retained-copper endpoint regression (no temporary source pads).
"$kicad_python" "$repo_root/tools/test-native-copper-endpoint.py"

# ADR 0117: old routing checkpoints retain superseded RSE wiring. The corrected
# successor must pass current canonical pins and functional terminal retention.
python3 "$repo_root/tools/check-rse-pin-migration-plan.py"
"$repo_root/tools/check-rse-pin-migration.sh"

# ADR 0121: retain the corrected RSE parent and validate the 34-open child.
"$repo_root/tools/check-usb-en1-routing.sh"
