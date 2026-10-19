<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Row-select routing on the six-layer coupon study

The [saved candidate board](../../hardware/coupon/rev-a/staging/led-row-select-two-layer-trial-114mm.kicad_pcb) connects **fourteen of sixteen** 74HC4514 U2 decoder outputs to their matching candidate onsemi row-pair select pads. `ROW_SEL_02` and `ROW_SEL_03` remain open. It retains all 48 complete colour-driver/LED cathode channels, sixteen complete row-output/LED anode channels and sixteen local three-land gate ties from the [previous study](led-row-gate-tie-study-2026-10-19.md). Full-board open edges fall from 566 to **552**. These are native KiCad connected-item results, not hardware tests.

The [generator](../../tools/generate-row-select-two-layer-trial.py) searches 0.05 mm cells on B.Cu and In4.Cu with 0.20 mm traces, 0.20 mm clearance plus margin, and provisional 0.30/0.10 mm adjacent-layer microvias. It reserves the board-edge envelope and all B.Cu/In4.Cu pad copper, including plated through-hole pads and netless projected-driver pads. The chosen route order leaves the two lower-bank selects open; other orders trap different selects. This is evidence that most of the decoder channel fits, **not** an optimized or complete bank escape. The fourteen routes use a substantial number of narrow segments and require cleanup before manufacturing review.

The [independent saved-board check](../../tools/check-row-select-two-layer-trial.py) verifies each decoder-to-pair pad cluster, every colour channel, anode row and gate tie, the [manifest](../../mechanical/review/row-select-two-layer-trial.json) hash and route status, and exact native DRC equivalence to the original 104 intrinsic fine-pitch footprint-clearance findings. The separate LED-placement check passes all 256 placements, orientations and exact pad nets. The native DRC report has **104 findings**, no added shorts, track clearances or board-edge errors.

This is still a mixed-source, unbuilt candidate layout. The onsemi row pair is not selected in the canonical schematic/BOM; the two final projected-driver footprints are netless; the provisional HDI process and pre-existing pad gaps are not qualified. All sixteen row-select pulldown resistor ends, sixteen gate pullup resistor ends, pair VLED/GND and other power/control copper still need routing. The remaining two selects need another escape layer or a placement change, followed by DRC and current/return/process review. Independent Gate A remains mandatory before fabrication.

From the repository root on the current Mac:

```sh
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/generate-row-select-two-layer-trial.py
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb drc --format json --output /private/tmp/rgb-row-select-two-layer-drc.json hardware/coupon/rev-a/staging/led-row-select-two-layer-trial-114mm.kicad_pcb
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/check-row-select-two-layer-trial.py --drc /private/tmp/rgb-row-select-two-layer-drc.json
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/check-coupon-led-placement.py hardware/coupon/rev-a/staging/led-row-select-two-layer-trial-114mm.kicad_pcb
```
