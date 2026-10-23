<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Local row-gate copper on the complete colour study

The [saved six-layer candidate board](../../hardware/coupon/rev-a/staging/led-row-gate-tie-trial-114mm.kicad_pcb) retains all 48 complete colour channels and all sixteen complete anode rows from the [colour study](led-colour-fanout-grid-study-2026-10-19.md). It connects the numbered onsemi candidate's pin 5 to both pin-6 lands for each of the sixteen row pairs with two short B.Cu tracks. Native KiCad connected-item checks find all three gate lands together in every pair. Full-board open edges decrease from **598 to 566**; the resistor ends of these gate nets are still open.

The [generator](../../tools/generate-row-gate-tie-trial.py) and [independent saved-board check](../../tools/check-row-gate-tie-trial.py) use the exact `NTLJD3119CTBG_TRIAL_ONLY` candidate pad net map. The [manifest](../../mechanical/review/row-gate-tie-trial.json) records the source and output hashes. The derivative has 483 footprints and 6,656 tracks/vias, adding 32 B.Cu segments to the prior study. The checker also verifies every colour-driver/LED cathode cluster, every row-output/LED anode cluster, all 256 unchanged LED placements through the separate placement check, and native DRC equivalence to the 104 original intrinsic fine-pitch footprint-clearance findings. No new geometric DRC finding appeared.

This is a candidate layout study, **not** a selected row-package or fabrication PCB. The numbered onsemi pair remains absent from the canonical schematic/BOM, and its fine-pitch intrinsic gaps still exceed the current board clearance rule. The remaining 566 open edges include all sixteen row-select connections to U2 and their pulldowns, each gate pullup, pair VLED/GND, and the unfinished board-wide power/control routes. A quick inner-layer row-select path search did not prove the whole row bank routable; those routes need coordinated B.Cu and inner-layer escape planning. Power-current, return, thermal, HDI process, enclosure and independent Gate A checks remain open. No hardware has been built or measured.

Reproduce on the current Mac from the repository root:

```sh
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/generate-row-gate-tie-trial.py
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb drc --format json --output /private/tmp/rgb-row-gate-tie-drc.json hardware/coupon/rev-a/staging/led-row-gate-tie-trial-114mm.kicad_pcb
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/check-row-gate-tie-trial.py --drc /private/tmp/rgb-row-gate-tie-drc.json
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/check-coupon-led-placement.py hardware/coupon/rev-a/staging/led-row-gate-tie-trial-114mm.kicad_pcb
```
