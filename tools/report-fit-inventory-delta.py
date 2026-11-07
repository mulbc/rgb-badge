#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Compare a current native KiCad XML export with the historical fit trial.

This counts references only. It does not establish footprint clearance or fit.
"""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
TRIAL = ROOT / "mechanical/review/fit-trial.json"


def report(xml_path: Path) -> dict:
    trial = json.loads(TRIAL.read_text(encoding="utf-8"))
    rear = trial["rear_trial"]
    old_placed = {p["ref"] for category in ("anchors", "under_pack_0402_candidates",
                                               "other_unrouted_first_fit") for p in rear[category]}
    # Three driver boxes in the old study are projections of a single U1.
    old_placed.difference_update({"U1-1", "U1-2", "U1-3"})
    old_placed.add("U1")
    old_unplaced = set(rear["unplaced_captured_refs"])
    components = {}
    for comp in ET.parse(xml_path).getroot().findall("./components/comp"):
        ref = comp.get("ref")
        if ref is None or ref.startswith("#FLG"):
            continue
        if ref in components:
            raise ValueError(f"Duplicate KiCad component {ref}")
        footprint = comp.findtext("footprint")
        if not footprint:
            raise ValueError(f"No footprint for {ref}")
        components[ref] = {"ref": ref, "value": comp.findtext("value"), "footprint": footprint}
    front = {ref for ref in components if re.fullmatch(r"D\d+", ref)}
    historical_coupon_leds = trial["captured_footprint_count"] - len(old_placed | old_unplaced)
    if len(front) != historical_coupon_leds:
        raise ValueError("Current coupon LED count differs from the historical trial")
    current_rear = set(components) - front
    missing_historical = (old_placed | old_unplaced) - current_rear
    if missing_historical:
        raise ValueError(f"Historical refs missing from current export: {sorted(missing_historical)}")
    added = current_rear - old_placed - old_unplaced
    footprints = Counter(components[ref]["footprint"] for ref in added)
    return {
        "SPDX-License-Identifier": "CERN-OHL-S-2.0",
        "status": "INVENTORY_DELTA_ONLY_NO_CURRENT_PLACEMENT_OR_FIT_APPROVAL",
        "historical_trial": str(TRIAL.relative_to(ROOT)),
        "current_native_xml_sha256": hashlib.sha256(xml_path.read_bytes()).hexdigest(),
        "board_mm": trial["board_mm"],
        "current_total_pcb_items": len(components),
        "front_led_count": len(front),
        "current_rear_items": len(current_rear),
        "historical_rear_items": len(old_placed | old_unplaced),
        "historical_rear_refs_with_xy_trial": len(old_placed),
        "historical_unplaced_refs": sorted(old_unplaced),
        "additional_current_rear_refs_without_xy_trial": len(added),
        "current_rear_refs_without_xy_trial": sorted(old_unplaced | added),
        "additional_parts": [components[ref] for ref in sorted(added)],
        "additional_footprint_counts": dict(sorted(footprints.items())),
        "limitations": [
            "Historical XY trial uses LP503055, while LP452845 is the current design target",
            "Historical driver projections are not KiCad PCB placements",
            "Hardware display interlock and final PCB routing are absent",
            "A current part inventory does not prove that any component fits",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("native_xml", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = report(args.native_xml)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"{result['current_total_pcb_items']} current items; "
          f"{len(result['current_rear_refs_without_xy_trial'])} rear refs without a historical XY trial "
          f"({result['additional_current_rear_refs_without_xy_trial']} added since trial)")


if __name__ == "__main__":
    main()
