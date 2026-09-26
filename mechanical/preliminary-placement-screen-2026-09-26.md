<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Preliminary front/rear placement screen

2026-09-26. [Review drawing](review/placement.svg) and [machine-readable result](review/placement.json). Generate both from the canonical, project-local footprints with:

```sh
python3 tools/screen-preliminary-placement.py --output mechanical/review
```

This is a **two-dimensional bounding-box calculation**, not a KiCad PCB, completed component placement, DRC, manufacturer-approved board outline or cell fit. It screens the hypothetical **final 48 × 16 board**, not the 16 × 16 mixed-LED coupon. Preliminary dimensions are 106 × 32.5 mm, with a 1.95 mm pitch. To see spatial feasibility independently of coupon power choices, the drawing uses 48 columns of the QT Brightek QBLP1515A-RGB2A candidate; Gate B has not selected the final LED. All LED courtyards follow [ADR 0008](../docs/decisions/0008-qblp1515-checkerboard-placement.md). The USB4505 footprint's drawing guides determine the connector's position. Its corner reliefs are not dimensioned; the opening in the drawing is a straight-sided **guide only**.

## Results

| Check | Calculated outcome | Practical reading |
|---|---:|---|
| Centred final grid against USB4505 F.CrtYd | **8 LED courtyard overlaps**; worst horizontal intrusion 1.525 mm | The previous 0.025 mm copper/cutout overlap is only part of the placement problem. Courtyard is an assembly reservation, not necessarily a solid shell outline. |
| Trial array shift left 1.775 mm | Zero LED/USB **courtyard box** overlaps; nearest horizontal gap 0.25 mm | Illustrative layout adjustment only; this does not establish a safe LED-to-shell gap, body clearance or manufacturing rule. |
| Trial leftmost LED courtyard | X = 4.3 mm on a 106 mm board | The grid remains inside this draft board rectangle; actual optical registration and wall alignment are unverified. |
| Rear large-component rectangles | Module at (14.5, 16.25) mm; three TLC59581 footprint centres at X = 83.0 mm, Y = 5.0/16.25/27.5 mm; 700 mAh coupon pack **50.5 × 31.0 mm** centred (drawing's 30.5 mm width plus 0.5 mm) | The selected bounding rectangles stay on the board and do not overlap one another in XY. The closest pack-to-driver courtyard gap is **0.30 mm**, without routing, a connector, swelling, insulation, standoffs or height checks. |

The manufacturer drawing's straight USB opening reaches 6.20 mm into the right edge; the project USB footprint's front courtyard reaches **7.60 mm inward**. Moving only 0.275 mm left to create nominal 0.25 mm pad-to-*cutout* clearance, as calculated in the [earlier edge screen](usb-led-edge-screen-2026-09-26.md), still intersects the USB courtyard. This updated screen protects against solving the wrong clearance.

The rear battery rectangle is the **protected GlobTek BL0750F5030481S1PCTC 700 mAh coupon-only candidate** from the [pack screen](../docs/sourcing/pack-screen-2026-09-25.md). [GlobTek Rev D page 4](https://www.globtek.com/pdf/manual-datasheets/BL0750F5030481S1PCTC.pdf) specifies 50.5 × 30.5 (+0.5) × 5.3 (+0.3) mm: this rectangle includes the documented **maximum width** of 31.0 mm, but wire exit/connector position, pouch swelling, mounting and insulating clearance remain outside it. It is **not an approved final battery**: the full-badge reference runtime model is about 4.9 h and the estimated maximum-white draw exceeds its documented continuous-discharge rating. An actual final pack may have very different dimensions.

The rear boxes represent only the MCU, three LED drivers and nominal pouch, **not** the decoder, sixteen row switches, charger, protection, converters, magnet/screw zones, antenna and feedline, USB shell, test pads or all of their routing. The near-zero spare margin at the driver/pack boundary shows why no complete fit should be inferred from four nonoverlapping rectangles. The actual 11 mm section must keep the cell isolated from circuitry, as required by SAF-002. Moving LEDs on the front does not make room for rear components.

## Next layout work

1. Source the missing dimensioned GCT cutout reliefs and agree on the 0.80 mm connector-compatible board thickness and process with the assembler.
2. After the unfinished power schematic is captured, generate the *entire* real netlist/footprint set and make a preliminary KiCad board with actual front/rear footprints. Place the real pack drawing with wire exit, protection and clearance, and reserve the antenna/switch/button/case zones.
3. Run native board DRC, power and signal routing feasibility, exact-parts PCBA review and STEP assembly checks. Resolve the affected last-column LED rows nearest USB with real mating geometry; require independent Gate A engineering review before fabrication.

**No PCB or cell was ordered.** The drawing is suitable for discussing envelope risks only.
