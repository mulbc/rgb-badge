<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Connector-first rear layout trial

The [to-scale rear plan](review/connector-first-plan.svg) and [position record](review/fit-trial.json) come from the native coupon KiCad netlist and project-local captured footprint courtyards. Regenerate them with `python3 tools/screen-final-fit-trial.py`. This is an **unrouted geometric trial**, not a PCB, a qualified battery installation or a complete final-badge circuit.

The trial reserves an **illustrative 8 × 8 mm pocket** next to the left end of a centred, separately supported LP503055 pack. The pocket represents a candidate two-circuit Molex PicoBlade right-angle connector and an initial mated-area allowance; it is **not** a transcribed land pattern, full wire bend or strain-relief envelope. The switch remains on the top edge but moves to the right. The row decoder moves below the USB connector. The MCU, three driver bodies, USB connector, battery body and 77 conditional under-pack 0402 positions keep their previous trial envelopes. The 32 row FETs are then repacked bottom-up, followed by the remaining captured parts with zero extra gap beyond their courtyards.

| Geometry result | Count |
|---|---:|
| Row FETs given nonoverlapping XY positions | 28 of 32 |
| Other captured coupon parts given first-fit XY positions | 32 |
| Captured coupon parts still unplaced | 11: `Q1`–`Q4`, `U11`, `U17`, `U23`–`U25`, `U29`, `U34` |
| Conditional 0402 XY positions under the pack | 77 |

All drawn trial rectangles are nonoverlapping, but several share courtyard edges and have **no added routing or assembly gap**. Pin orientation, signal paths, decoder-to-row distance, converter locality, RF, heat and copper area have not been checked. This alternative therefore does not solve the placement problem: it trades the earlier eight unplaced captured parts for eleven after reserving a connector pocket. Charger, LED converter, input protection, connector land pattern, their support passives, mounting and cable path remain absent.

A useful area check reinforces the concern without proving an impossible layout. The 106 × 32.5 mm board has 1,737 mm² outside the LP503055's centred 56 × 30.5 mm projected body. The currently drawn and still-unplaced captured courtyards, the 64 mm² illustrative connector pocket, and only the five proposed power-IC package minima leave roughly **120 mm²** of nominal outside-pack area. That remainder must also accommodate power passives/inductors, interlock and gauge support, mounting, isolation, copper and routing; the current screen does not allocate them. Some passives may sit beneath the pack only if the separate vertical, thermal and locality qualification succeeds.

**Disposition:** keep the 106 × 32.5 mm board and 110 × 35 × 11 mm case as trial targets for now. A full-board PCB is premature because the complete power netlist, exact terminated pack and audited connector footprint are unavailable. The largest currently captured outside-pack area is the 32-device row-switch bank (about 398 mm² of courtyards). Any attempt to reduce it is a material electrical change requiring a reviewed current/thermal/default-off circuit and ADR before capture. In parallel, a shorter protected pack could free board area, but it must still meet the full-white current and runtime requirements; the existing 900 mAh LP452845 listing is not a qualified replacement. The first physical milestone remains the 16 × 16 coupon and its independently reviewed power design.

A [follow-on package screen](dual-row-package-screen-2026-10-06.md) tests the most promising row-stage area reduction under a proposed ADR. It does not change this connector-first result or implement a new circuit.

Manufacturer sources: [LP503055 protected-pack drawing](https://www.lipolbattery.com/LiPo-Battery-Datahseet/LiPo_Battery_LP503055_3.7V_950mAh.pdf), [Molex PicoBlade connector data](https://www.content.molex.com/dxresources/e24c/e24ca95a-11dc-46d6-be7b-592110a37b66.pdf), [Molex right-angle header drawing](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/532/53261/532610471_sd.pdf).
