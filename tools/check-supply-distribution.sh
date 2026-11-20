#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Full native acceptance of one supply-distribution study stage.
set -euo pipefail
rail="${1:-vled}"
if [[ $# -gt 1 ]]; then
  echo 'Usage: tools/check-supply-distribution.sh [app|usb|vled]' >&2
  exit 2
fi
case "$rail" in app|usb|vled) ;; *) echo "Unknown supply stage: $rail" >&2; exit 2 ;; esac
repo_root="$(git rev-parse --show-toplevel)"
kicad_python=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3
kicad_cli=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
review_dir="$repo_root/hardware/coupon/rev-a/build/$rail-distribution-review"
mkdir -p "$review_dir"
"$kicad_cli" pcb drc --format json --output "$review_dir/drc.json" \
  "$repo_root/hardware/coupon/rev-a/staging/led-$rail-distribution-trial-114mm.kicad_pcb"
"$kicad_python" "$repo_root/tools/check-supply-distribution-trial.py" --rail "$rail" \
  --drc "$review_dir/drc.json" --report "$review_dir/check.json"
"$kicad_python" "$repo_root/tools/check-coupon-led-placement.py" \
  "$repo_root/hardware/coupon/rev-a/staging/led-$rail-distribution-trial-114mm.kicad_pcb"
