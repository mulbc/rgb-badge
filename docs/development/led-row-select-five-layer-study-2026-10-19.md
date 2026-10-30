<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Complete decoder-to-row-pair selects on the six-layer coupon study

The [saved candidate board](../../hardware/coupon/rev-a/staging/led-row-select-five-layer-trial-114mm.kicad_pcb) connects **all sixteen 74HC4514 U2 decoder outputs to their matching candidate onsemi row-pair select pads**. It retains all 48 complete colour-driver/LED cathode channels, sixteen complete row-output/LED anode channels and sixteen local three-land gate ties from the [preceding study](led-row-gate-tie-study-2026-10-19.md). Full-board open edges fall from 566 to **550**. These are native KiCad connected-item results, not hardware tests.

The [deterministic generator](../../tools/generate-row-select-five-layer-trial.py) searches 0.05 mm cells across B.Cu and the four inner layers, with 0.20 mm traces, 0.20 mm clearance plus search margin, and provisional 0.30/0.10 mm adjacent-layer microvias. It reserves the board-edge envelope and all relevant pad copper, including plated through-hole and netless projected-driver pads. Routing the lower-left bottleneck selects first allows all sixteen paths. The derivative has 483 footprints and 9,553 tracks/vias. These paths still need trace simplification and manufacture/process review.

The [independent saved-board check](../../tools/check-row-select-five-layer-trial.py) verifies every decoder-to-pair pad cluster, all colour channels, anode rows and gate ties, the [manifest](../../mechanical/review/row-select-five-layer-trial.json) board hash, and exact native DRC equivalence to the original 104 intrinsic fine-pitch footprint-clearance findings. The separate LED-placement check passes all 256 placements, orientations and exact pad nets. The native DRC report has **104 findings**, no added shorts, track clearances or board-edge errors. Two full generations produced byte-identical boards with SHA-256 `7ac1b6c7544adb37bd03ea8f39e2fcaee659b5085e4c876bad24ae591a6e5859`.

This remains a mixed-source, unbuilt candidate layout. The onsemi row pair is not selected in the canonical schematic/BOM; two projected final-driver footprints are netless; the provisional HDI process and pre-existing pad gaps are unqualified. Each select pulldown resistor end, each gate pullup resistor end, pair VLED/GND and other power/control copper still need routing. Current/return, thermal, switching, RF, enclosure and process reviews remain; independent Gate A is mandatory before fabrication.

From the repository root on the current Mac:

```sh
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/generate-row-select-five-layer-trial.py
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb drc --format json --output /private/tmp/rgb-row-select-five-layer-drc.json hardware/coupon/rev-a/staging/led-row-select-five-layer-trial-114mm.kicad_pcb
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/check-row-select-five-layer-trial.py --drc /private/tmp/rgb-row-select-five-layer-drc.json
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/check-coupon-led-placement.py hardware/coupon/rev-a/staging/led-row-select-five-layer-trial-114mm.kicad_pcb
```
