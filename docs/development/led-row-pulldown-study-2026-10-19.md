<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Candidate row-select pulldown routing

The [saved six-layer candidate board](../../hardware/coupon/rev-a/staging/led-row-pulldown-trial-114mm.kicad_pcb) connects **fifteen of sixteen** 100 kΩ select pulldown resistor pads to their complete decoder-to-row-pair select nets. `R24` pad 1 on `ROW_SEL_02` remains open; all sixteen resistor ground pads also remain to be routed. It retains 48 complete colour channels, sixteen complete anode rows, sixteen local row-gate ties and all sixteen decoder-to-pair select channels from the [preceding study](led-row-select-five-layer-study-2026-10-19.md). Native KiCad full-board open edges fall from 550 to **535**. These are layout connectivity results, not powered-board measurements.

The [generator](../../tools/generate-row-pulldown-trial.py) searches B.Cu and the four inner layers with 0.05 mm cells, 0.20 mm traces, 0.20 mm clearance plus search margin, and provisional 0.30/0.10 mm adjacent-layer microvias. It joins resistor pads to existing same-net copper. Routing the resistor bank in reverse order leaves only R24 open; routing R24 early instead blocks R25. Both are independently routable on the untouched board, so the remaining conflict is local route/placement coordination, not evidence that the net is impossible.

The [saved-board checker](../../tools/check-row-pulldown-trial.py) verifies all expected LED, row-output, gate, select and resistor pad clusters, the [manifest](../../mechanical/review/row-pulldown-trial.json) board hash, and exact equivalence to the original 104 intrinsic native DRC footprint-clearance findings. The separate placement check verifies all 256 LEDs. Native DRC reports **104 findings** with no added shorts, clearance or board-edge errors. The board SHA-256 is `6fc5022bce254c82ea8e02b0c038d700f635081bb6a84fd142e8e5499b2bf9ac`.

This is an unbuilt mixed-source candidate layout. The onsemi row pair is not selected in the canonical schematic/BOM; two projected final-driver footprints remain netless; provisional HDI and pre-existing fine-pitch gaps are unqualified. Next, resolve R24 locally, connect the sixteen gate pullups and pair VLED/GND, then route other power/control copper and review current/return, switching, RF, enclosure and process constraints. Independent Gate A is required before fabrication.

From the repository root on the current Mac:

```sh
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/generate-row-pulldown-trial.py
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb drc --format json --output /private/tmp/rgb-row-pulldown-drc.json hardware/coupon/rev-a/staging/led-row-pulldown-trial-114mm.kicad_pcb
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/check-row-pulldown-trial.py --drc /private/tmp/rgb-row-pulldown-drc.json
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/check-coupon-led-placement.py hardware/coupon/rev-a/staging/led-row-pulldown-trial-114mm.kicad_pcb
```
