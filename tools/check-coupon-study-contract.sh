#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
repo_root="$(git rev-parse --show-toplevel)"
review_dir="$repo_root/hardware/coupon/rev-a/build/reconciliation-review"
mkdir -p "$review_dir"
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli sch export netlist --format kicadxml \
  --output "$review_dir/coupon.xml" "$repo_root/hardware/coupon/rev-a/rgb-badge-coupon.kicad_sch"
python3 "$repo_root/tools/check-coupon-study-contract.py" --netlist "$review_dir/coupon.xml" \
  --report "$review_dir/report.json"
python3 -m unittest discover -s "$repo_root/tools/tests" -p test_coupon_study_contract.py -v
