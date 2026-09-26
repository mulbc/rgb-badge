<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# USB opening and last LED column: preliminary geometry screen

2026-09-26. Calculation for a **hypothetical final 48 × 16 badge** with a centred, all-QBLP1515A-RGB2A LED grid on the project's preliminary 106 × 32.5 mm PCB. No final PCB outline, placement, router clearance rule or enclosure CAD has been made. The 16 × 16 mixed-LED coupon has its own geometry and must not inherit this result without recalculation.

## Inputs and nominal calculation

Coordinates below start at the top-left corner of the hypothetical PCB; X increases along its 106 mm length and Y across its 32.5 mm width. Assume `USB4505-03-0-A` exits through the middle of the right short edge, with its **straight** cutout sides at Y = 16.25 ± 4.62 mm. Its audited layout guide places the board edge at local Y = 6.75 mm and the rear of the straight cutout at local Y = 0.55 mm; therefore the inward cutout reach is `6.75 - 0.55 = 6.20 mm` and its nominal inner boundary is PCB X = `106 - 6.20 = 99.80 mm`. The undimensioned curved corner reliefs are excluded from this calculation.

For 48 columns at 1.95 mm pitch, centred grid origin X is `(106 - 47×1.95)/2 = 7.175 mm`; the last column's centre is X = **98.825 mm**. For 16 rows the centred origin Y is `(32.5 - 15×1.95)/2 = 1.625 mm`. The exact QT footprint has pad centres at X = ±0.70, Y = ±0.40 mm and pads measuring 0.60 × 0.40 mm. The resulting horizontal copper half-extent is 1.00 mm at 0° or 0.60 mm at 90°. [ADR 0008](../docs/decisions/0008-qblp1515-checkerboard-placement.md) specifies 0° when zero-based `(row + column)` is even, otherwise 90°.

| LED position in last column | Y centre (mm) | Rotation | Rightmost copper X (mm) | Nominal gap to straight cutout (mm) |
|---|---:|---:|---:|---:|
| Row 7, column 47 | 15.275 | 0° | 99.825 | **−0.025** |
| Row 8, column 47 | 17.225 | 90° | 99.425 | **+0.375** |

Both rows lie within the nominal 9.24 mm opening. **Row 7 copper intrudes 0.025 mm into the straight cutout guide** for these assumptions. This is a draft placement conflict, not a physical measurement; moving the grid, choosing the PCB length and qualifying the real cutout reliefs can change it. In particular, the row-7 nominal pad-to-edge clearance becomes 0.25 mm if the array is shifted left by **at least 0.275 mm**, with no additional manufacturing tolerance included. If the grid stays centred, increasing the board length to **106.55 mm** adds 0.275 mm at the right edge and gives the same *nominal* 0.25 mm clearance, assuming the connector keeps its relative edge position. Neither example is an approved clearance rule or an instruction to modify the board.

This centreline calculation excludes LED body/courtyard, connector shell and staking, solder mask, fabrication/placement tolerances, board-edge milling, strain relief, case walls and display registration. The actual footprint's 0° courtyard extends 1.10 mm horizontally from centre, so its right edge would be X = **99.925 mm** in row 7 under the same assumptions. The maximum case length is 110 mm; a longer PCB must still fit the USB plug and case rather than treating the 4 mm difference as free space.

## Connector stack-up conflict

The [original GCT USB4505 drawing, revision A2](https://gct.co/files/drawings/usb4505.pdf), independently checked against the owner-supplied PDF with SHA-256 `b1ea604d8e579ee60bf3db78fc55a300bc107cb3bdb3ac3e6c881955898b52ad`, calls out **0.80 mm recommended PCB thickness** in its recommended layout. The [project-local connector audit](../hardware/coupon/rev-a/usb-connector-audit.md) and exact candidate footprint also say 0.80 mm. The historical [project plan](../docs/project-plan.md) instead models 1.0 mm FR-4. The connector's description of a 1.0 mm *offset* is not a 1.0 mm board-thickness specification. The 0.80 mm section in the [envelope screen](envelope-screen-2026-09-26.md) is a trial stack, not a frozen board stack-up.

Do not use the plan's 1.0 mm thickness to order a coupon or model a USB opening with the 0.80 mm connector land pattern without an explicit mechanical/assembly review. Confirm connector fit, acceptable finished-board thickness tolerance and supplier availability with the fabricator/assembler; then update PCB stack-up, layer design, mass and case section consistently. Do not infer missing corner-relief radii from the drawing.

## Before layout freeze

1. Obtain GCT dimensioned cutout geometry or CAD for the undimensioned corner reliefs and confirm acceptable board thickness and slot process with the assembler.
2. In a preliminary KiCad PCB, place the exact USB footprint and LED grid, choose a board edge and run board-edge/copper DRC with the selected fabricator's tolerances. Review LED body, courtyard and assembly access with the USB shell.
3. Export a board STEP and check the connector, plug, diffuser, button/switch, rear battery and RF antenna within the 110 × 35 × 11 mm case limit. Require independent Gate A review before fabrication.

The calculated overlap is a reason to revise the *layout proposal*; no LED pitch, approved candidate footprint or schematic has been changed here.
