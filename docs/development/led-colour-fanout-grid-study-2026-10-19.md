<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Complete colour-driver fanout on the accepted-pitch coupon study

## Source result

The [saved six-layer KiCad study](../../hardware/coupon/rev-a/staging/led-colour-fanout-grid-trial-114mm.kicad_pcb) connects **all 48 TLC59581 U1 colour outputs to all 16 LED cathodes in their respective columns**. All sixteen existing candidate row-pair outputs still reach their complete anode rows. This is native copper connectivity, not a powered-board measurement.

It retains all **483 footprints**, their placements, exact LED pad shapes and the ADR 0034 coupon pitch. The [previous row-bank board](led-row-bank-study-2026-10-16.md) had six colour-driver joins and 640 full open edges; this derivative has **598 full open edges**. The remaining edges belong to the unfinished board. KiCad CLI's 499-item unconnected list is capped and is not the full count.

The [KiCad 10.0.6 DRC report](led-colour-fanout-grid-drc-2026-10-19.json) contains **exactly the same 104 intrinsic footprint-clearance findings** as the earlier row-bank study: 96 in the sixteen candidate row pairs and eight in U48/U52. There are no added shorts, track clearances, hole or other geometric findings. The existing findings remain unresolved process constraints; this is not a clean fabrication DRC result.

## Method and checks

The [generator](../../tools/generate-colour-fanout-grid-trial.py) copies the previous row-bank board, removes its six tentative colour-driver fanouts, and preserves the original matrix copper and row routes. It searches the four inner layers with a 0.05 mm grid, 0.20 mm tracks and 0.20 mm clearance plus a 0.012 mm search margin. Each colour can join its existing matrix trunk along its length. Reserving driver-pad via sites across the inner layers lets different pins escape on different layers. Routing `COL_06_G` and `COL_10_B` first avoids trapped driver exits from the earlier ordering.

Layer changes retain the provisional **0.30 mm diameter / 0.10 mm drill adjacent-layer microvia** geometry. Driver pads can use stacks through several inner layers. The output contains **6,624 track/via objects**, including **1,366 vias**; these totals include the earlier matrix copper. No current limit, exact part, symbol pin map or footprint pad is changed.

The [saved-board checker](../../tools/check-colour-fanout-trial.py) uses KiCad's native connected-item clusters. It independently checks the controlled [TLC59581 pin map](../../hardware/coupon/rev-a/driver-capture.md), the exact expected driver/LED pad set for every colour, all sixteen complete row clusters, the board hash, and the DRC finding descriptions/coordinates against the original 104-finding baseline. The separate LED-placement check also passes all 256 LEDs.

The [manifest](../../mechanical/review/colour-fanout-grid-trial.json) records source hashes, search settings, per-channel native LED counts and the output hash. Two complete runs produced byte-identical boards with SHA-256 `39ab69bd7b5be40f557984ab47ceaf241e1a0e7adb7eed5f46442d42d08d936d`. The full `tools/check-kicad.sh` source check also passes with zero configured canonical ERC violations; the separate onsemi candidate retains only its 18 expected standalone boundary findings.

## Reproduction

From the repository root on the current Mac:

```sh
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/generate-colour-fanout-grid-trial.py
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb drc --format json --output /private/tmp/rgb-colour-fanout-drc.json hardware/coupon/rev-a/staging/led-colour-fanout-grid-trial-114mm.kicad_pcb
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/check-colour-fanout-trial.py --drc /private/tmp/rgb-colour-fanout-drc.json
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/check-coupon-led-placement.py hardware/coupon/rev-a/staging/led-colour-fanout-grid-trial-114mm.kicad_pcb
```

## Remaining work

This remains a **mixed-source routing study**. The onsemi `NTLJD3119CTBG` row-pair candidate is not selected in the canonical schematic/BOM, and two projected final-driver footprints remain netless geometry. The accepted coupon pitch does not qualify a final 1.95 mm 1515 display.

Row select/gate/VLED/GND, driver supply/control, USB/charger/converter and other control routing remain open. The separate power study's copper has not been transferred. Ground/return paths, switching loops, current capacity, timing, RF, battery/enclosure heights, solder-mask/paste rules, stacked/via-in-pad HDI capability and cost still need review. Independent Gate A precedes fabrication. No hardware has been built or measured.
