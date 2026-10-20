<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Partial combined row-control routing

The [saved six-layer study](../../hardware/coupon/rev-a/staging/led-row-combined-partial-trial-114mm.kicad_pcb) builds on the complete select-pulldown board and connects **seven gate pullup resistor pads** on that same board. It retains all 48 colour channels, sixteen anode rows, sixteen local gate ties, sixteen decoder-to-pair selects and sixteen select pulldown signal pads. The seven combined gate routes are rows **1, 8, 9, 10, 11, 12 and 15**. Native open edges fall from 534 to **527**.

The [generator](../../tools/generate-row-combined-partial-trial.py) searches B.Cu and four inner layers on a 0.05 mm grid with provisional 0.20 mm traces and 0.30/0.10 mm adjacent-layer microvias. Nine gate routes remain blocked or exceed the current one-million-node search limit: rows 0, 2–7, 13 and 14. The [saved-board check](../../tools/check-row-combined-partial-trial.py) verifies every colour/row/gate/select/pulldown cluster, checks precisely which gate pullups joined, and compares native DRC against the original 104 intrinsic footprint-clearance findings. All 256 LED placements pass separately. The [manifest](../../mechanical/review/row-combined-partial-trial.json) records source and board hashes. Native DRC reports **104 findings**, with no new short or clearance finding.

This is the first saved board with both complete decoder-select/pulldown signals and some gate pullups, but it is **not a complete row bank**. The other nine gate pullups, all sixteen select-pulldown ground pads, pair VLED/GND, and other power/control routes remain open. The separate [In2 ground-zone study](led-in2-ground-plane-study-2026-10-20.md) branches from the same source, so its copper is not present here. Candidate onsemi row pairs are absent from the canonical schematic/BOM. HDI, current returns, RF, enclosure and independent Gate A remain unqualified; no hardware has been built or measured.

From the repository root on the current Mac:

```sh
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/generate-row-combined-partial-trial.py
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb drc --format json --output /private/tmp/rgb-row-combined-partial-drc.json hardware/coupon/rev-a/staging/led-row-combined-partial-trial-114mm.kicad_pcb
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/check-row-combined-partial-trial.py --drc /private/tmp/rgb-row-combined-partial-drc.json
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/check-coupon-led-placement.py hardware/coupon/rev-a/staging/led-row-combined-partial-trial-114mm.kicad_pcb
```
