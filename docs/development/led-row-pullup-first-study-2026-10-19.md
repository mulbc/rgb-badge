<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Gate-pullup-first routing comparison

This [separate six-layer candidate board](../../hardware/coupon/rev-a/staging/led-row-pullup-first-trial-114mm.kicad_pcb) branches from the [local row-gate study](led-row-gate-tie-study-2026-10-19.md) **before** decoder-select routing. It connects **all sixteen 1 kΩ gate pullup resistor pads to their respective row-pair gate nets**. It retains the 48 complete colour channels, sixteen anode rows and all local gate ties. Full-board open edges fall from 566 to **550**. Its decoder-to-pair select routes are still open; it is a comparison to the [select/pulldown-first board](led-row-pulldown-study-2026-10-19.md), not a combined result.

The [deterministic generator](../../tools/generate-row-pullup-first-trial.py) searches B.Cu and all four inner layers with 0.05 mm cells, 0.20 mm traces, 0.20 mm clearance plus search margin, and provisional 0.30/0.10 mm adjacent-layer microvias. Routing rows 0–5, then 15, then 6–14 avoids trapping the last gate net. The [saved-board checker](../../tools/check-row-pullup-first-trial.py) verifies all sixteen resistor-to-gate pad clusters, expected open decoder selects, all 48 colour channels and sixteen anode rows, the [manifest](../../mechanical/review/row-pullup-first-trial.json) hash, and exact equivalence to the original 104 intrinsic native DRC footprint-clearance findings. The separate LED-placement check passes all 256 LEDs. Native DRC reports **104 findings**, with no added short, clearance or board-edge error. The board SHA-256 is `81deb3647c3ed148e87986d645f2233f9bc2a7e7641d3b409db815c4a9e4d6b2`.

**Routing interaction:** Adding all sixteen pullups first with the present placements and path choices traps several decoder-select exits. Conversely, the select/pulldown-first derivative joins all sixteen selects and fifteen pulldowns but makes several gate-pullup paths unreachable with the same search. One moved gate resistor, R13, could be connected first while all sixteen selects still routed around it, proving that local placement and route order can change the outcome. A combined route requires coordinated resistor placement/path reservations or selective rip-up and reroute. Neither branch proves a complete row bank. The row-pair candidate is not selected in the canonical schematic/BOM, and the pre-existing fine-pitch pad gaps, HDI process, power/ground, current/return and independent Gate A reviews remain open. No hardware has been built or measured.

From the repository root on the current Mac:

```sh
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/generate-row-pullup-first-trial.py
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb drc --format json --output /private/tmp/rgb-row-pullup-first-drc.json hardware/coupon/rev-a/staging/led-row-pullup-first-trial-114mm.kicad_pcb
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/check-row-pullup-first-trial.py --drc /private/tmp/rgb-row-pullup-first-drc.json
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/check-coupon-led-placement.py hardware/coupon/rev-a/staging/led-row-pullup-first-trial-114mm.kicad_pcb
```
