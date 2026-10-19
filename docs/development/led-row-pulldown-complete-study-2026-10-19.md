<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Complete select-pulldown routing on the candidate matrix

The [saved six-layer candidate board](../../hardware/coupon/rev-a/staging/led-row-pulldown-complete-trial-114mm.kicad_pcb) connects **all sixteen 100 kΩ select pulldown resistor pads** to the already complete U2 decoder-to-row-pair select nets. It retains 48 complete colour channels, sixteen complete anode rows and sixteen local gate ties. Native KiCad full-board open edges fall from 535 to **534**. This is copper connectivity, not powered-board evidence.

The [generator](../../tools/generate-row-pulldown-complete-trial.py) branches from the [fifteen-pulldown study](led-row-pulldown-study-2026-10-19.md), moves `R24` from its earlier remote site to **(69.5, 13.5) mm** on B.Cu, and routes its `ROW_SEL_02` pad to existing same-net copper. The other fifteen select-pulldown connections remain unchanged. A footprint/copper scan found this position clear; native DRC confirms no new placement, short, trace-clearance or board-edge findings. The route uses the same provisional 0.20 mm trace and adjacent-layer 0.30/0.10 mm microvia search settings as the earlier study.

The [independent saved-board check](../../tools/check-row-pulldown-complete-trial.py) verifies every colour, anode-row, gate-tie, decoder-select and select-pulldown cluster, the R24 position, the [manifest](../../mechanical/review/row-pulldown-complete-trial.json) hash and exact equivalence to the original 104 intrinsic fine-pitch footprint-clearance findings. The separate LED-placement check passes all 256 LEDs. Native DRC reports **104 findings** and no additions. The board SHA-256 is `330909098cacf16d71eb44a9361d863c145190b8ade2352576f730de68dbfe6f`.

All sixteen pulldown **ground** pads remain unrouted. The [separate gate-pullup-first comparison](led-row-pullup-first-study-2026-10-19.md) connects all sixteen gate resistors but leaves decoder selects open. These are different boards; their connection counts cannot be added. Coordinated gate/selection placement and routing, pair VLED/GND, other power/control copper, current/return review, HDI/mask process qualification, enclosure and independent Gate A remain. The onsemi row pair is still a candidate absent from the canonical schematic/BOM. No hardware has been built or measured.

From the repository root on the current Mac:

```sh
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/generate-row-pulldown-complete-trial.py
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb drc --format json --output /private/tmp/rgb-row-pulldown-complete-drc.json hardware/coupon/rev-a/staging/led-row-pulldown-complete-trial-114mm.kicad_pcb
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/check-row-pulldown-complete-trial.py --drc /private/tmp/rgb-row-pulldown-complete-drc.json
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/check-coupon-led-placement.py hardware/coupon/rev-a/staging/led-row-pulldown-complete-trial-114mm.kicad_pcb
```
