<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0033: Provisional longer badge envelope

- Date: 2026-10-14
- Status: Accepted as the working PCB/case envelope on 2026-10-14; physical fit unverified
- Scope: Final 48 × 16 badge mechanics, not the coupon fabrication release

## Context

The original limit was a 110 × 35 × 11 mm complete case (MEC-001). The grouped-power, paired-row placement screen needs a 110 × 32.5 mm *PCB* for a zero-miss first-fit result. A PCB as long as the original outer case has no demonstrated end-wall or connector allowance. In a stricter screen that keeps each of nine interlock bypass capacitors within a 3 mm courtyard-edge gap of its IC, the 110 mm arrangement still leaves three component boxes without positions in the priority ordering. This is a geometric screen, not a circuit placement, electrical-distance requirement or PCB routing result.

## Decision

Use a **114 × 32.5 mm PCB** and **118 × 35 × 11 mm maximum outer case** as the working final-badge targets. The owner accepted the additional 4 mm of PCB length on 2026-10-14. Keep LED pitch, pack selection, electrical current limits, battery clearance, case thickness and weight requirements unchanged. The added PCB length is at the USB/component end; the battery and sensor reservation stay fixed. A centered 114 mm PCB in a nominal 118 mm case leaves only 2 mm per end before wall, connector opening and tolerances. These are design targets, not a fitted enclosure claim.

In the reproducible first-fit sensitivity, the 114 mm priority run places every currently counted box while keeping all nine interlock bypass boxes within the trial 3 mm gap. At 112 mm, the same run leaves C70 unplaced; at 110 mm it leaves U33, U49 and C68. These results depend on the particular greedy order and reserved boxes. They do not prove 114 mm is a minimum possible length or that the board can be routed.

The historical [USB/last-LED calculation](../../mechanical/usb-led-edge-screen-2026-09-26.md) also improves under the same centred-grid and straight-cutout assumptions: the nominal row-7 copper gap changes from −0.025 mm at a 106 mm PCB to +3.975 mm at 114 mm. Actual connector reliefs, LED courtyards and case opening still require CAD/PCB checks.

## Conditions before layout freeze

The [native footprint-only board](../../docs/development/paired-charger-114mm-placement-study-2026-10-14.md) checks actual pad and edge geometry but has no routes. Complete the grouped power, interlock and display-driver connections, then check USB cutout and mating access, RF antenna, battery insulation and wire exit, 0.80 mm connector board-thickness guidance, and an enclosure section with walls, diffuser and assembly tolerances. Revisit the length target if those checks fail; do not tighten battery clearance or electrical limits to preserve it. Independent Gate A still precedes fabrication.

Evidence: [grouped-power placement screen](../../mechanical/paired-charger-110mm-screen-2026-10-14.md) and its [machine-readable sensitivity](../../mechanical/review/paired-charger-110mm-xy.json).
