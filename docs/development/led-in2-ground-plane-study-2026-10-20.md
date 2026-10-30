<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Provisional In2 ground-copper screen

The [saved six-layer study](../../hardware/coupon/rev-a/staging/led-in2-ground-plane-trial-114mm.kicad_pcb) adds one In2.Cu GND zone to the [complete select-pulldown routing study](led-row-pulldown-complete-study-2026-10-19.md). Three adjacent-layer 0.30/0.10 mm trial microvias join the zone to `R25` pad 2 at (34.25, 7.25) mm. KiCad fills one connected polygon of **2921.998 mm²** after removing isolated islands. The filled copper is a geometry result, not a qualified ground return or current-capacity result.

The [generator](../../tools/generate-in2-ground-plane-trial.py) and [saved-board check](../../tools/check-in2-ground-plane-trial.py) preserve all 11,481 source tracks/vias, add only those three GND microvias and the zone, verify the anchor and compare native DRC findings with the original baseline. The [manifest](../../mechanical/review/in2-ground-plane-trial.json) records source and output hashes. Native DRC reports the same **104 intrinsic footprint-clearance findings**, no new violation. Full open edges remain **534**: the other select-pulldown ground pads and the rest of the power/ground network are still open.

A separate unsaved probe put stacked vias directly on all sixteen select-pulldown ground pads. It reduced the native open count to 522 but raised DRC findings to 165, including **42 shorts** and 19 extra clearance findings. Many candidate vias intersect existing colour copper on inner layers. This probe is rejected; ground connections require routed escapes or a revised layer allocation, with DRC on each completed derivative.

A second unsaved probe used a **single B.Cu–In4.Cu via per pulldown pad** and poured GND on In4.Cu. On the complete-pulldown board it produced 118 DRC findings: the original 104 plus nine shorts, three clearance findings and two dangling vias. On the later combined row-control board, four selected non-shorting vias gave the original 104 findings but only reduced open edges from 527 to 525 and left **two separate copper polygons**. This is not a unified ground network, so the In4 variants were also rejected. The probes show that changing the plane layer alone does not resolve the local return routing.

This zone has not been shaped around the antenna, converter switching loops, thermal paths or return-current needs. The 0.30/0.10 mm stacked-via process and mask/paste treatment remain unapproved. The mixed-source row-pair board is not schematic-synchronized fabrication source. No hardware has been built or measured; independent Gate A remains required before fabrication.

From the repository root on the current Mac:

```sh
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/generate-in2-ground-plane-trial.py
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb drc --format json --output /private/tmp/rgb-in2-ground-plane-drc.json hardware/coupon/rev-a/staging/led-in2-ground-plane-trial-114mm.kicad_pcb
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/check-in2-ground-plane-trial.py --drc /private/tmp/rgb-in2-ground-plane-drc.json
```
