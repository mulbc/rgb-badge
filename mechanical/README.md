<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Mechanical design

The enclosure will be parameterized in CadQuery and released as source plus reviewed STEP/STL exports. It must enforce the finished envelope, protect the pouch cell, reserve the RF zone and support a replaceable development diffuser.

Do not freeze the 900 mAh cell or final enclosure until a complete PCB STEP assembly proves the thickness stack without pouch compression.

The [2026-09-26 envelope screen](envelope-screen-2026-09-26.md) quantifies display width and a trial 11 mm thickness stack. It flags conflicting manufacturer length figures for the 900 mAh *bare* cell. Under [ADR 0019](../docs/decisions/0019-board-mounted-battery-temperature-sensing.md), a protected two-wire pack with a battery-facing PCB NTC is now allowed for testing; no final pack or physical fit is selected.

The [USB/LED edge screen](usb-led-edge-screen-2026-09-26.md) finds a nominal 0.025 mm copper intrusion into the USB cutout guide with the centred final LED grid and 106 mm board, and flags the connector's 0.80 mm board recommendation against the historical 1.0 mm plan. Actual placement and stack-up remain to be qualified.

The [preliminary front/rear placement study](preliminary-placement-screen-2026-09-26.md) additionally checks exact LED/USB courtyards. A centred grid conflicts with the USB courtyard; an illustrative 1.775 mm left shift avoids *bounding-box* intersections but does not establish manufacturability. The trial rear placement omits many components and the final battery.

The [2026-10-06 board/battery fit trial](fit-trial-2026-10-06.md) adds a grouped rear footprint plan and an 11 mm section with a separate LP503055 pack that still needs support above the board. All 32 row switches and 77 conditional under-pack 0402 candidates have nonoverlapping XY trial positions, but eight then-captured coupon parts remained unplaced. The [current inventory comparison](current-fit-inventory-delta-2026-10-11.md) finds 56 more rear-side parts in the now 466-item coupon schematic, for 64 references without even a historical XY trial position. A 0.55 mm 0402 height example leaves only 0.25 mm nominal case margin before assembly tolerances. No present-day complete PCB, physical mount or DRC has been validated.

The [fresh LP452845 XY screen](current-lp452845-xy-screen-2026-10-11.md) uses all current captured courtyards and the exact J2 land. Greedy placement leaves 16–18 boxes unplaced with the canonical 32 row FETs, while a *geometric-only* substitution of 16 proposed dual packages leaves none unplaced **before** reserving the interlock. A 7 × 12 mm trial interlock reservation makes the latter leave one or two packages unplaced. This supports an electrical audit of the dual package and a real layout study, not a fit or routing approval.

An additional board-width screen finds that lengthening the trial PCB from 106 to 108 mm clears the one remaining area-first courtyard miss with the dual package and a 7 × 12 mm interlock reservation. The 110 mm outer-case target leaves only 1 mm nominal at each end for a centered 108 mm PCB, so this is a layout direction to verify against the real enclosure and USB opening, not an accepted dimension change.

The [battery-connector screen](battery-connector-screen-2026-10-06.md) compares JST GH/PH and Molex PicoBlade families for the LP503055's bare AWG 28 wires. An illustrative PH mated pocket has no free position in the original grouped plan, even before small-part packing. No pack termination or polarity has been selected.

The [connector-first follow-on](connector-first-trial-2026-10-06.md) adds a compact Molex PicoBlade candidate and moves the switch, decoder and row FETs around its illustrative 8 × 8 mm pocket. It leaves 11 captured parts unplaced before the missing power hardware. The added connector is a geometric reservation, not a qualified footprint or selected pack termination.

The [dual-row package screen](dual-row-package-screen-2026-10-06.md) evaluates one complementary N/P MOSFET package per row under [proposed ADR 0020](../docs/decisions/0020-dual-row-mosfet-package-proposal.md). Its current XY trial accommodates the retained non-row captured parts, four power-IC package minima and the staged VLED passives; ADR 0021 removes the on-board battery-current monitor. Other support circuits, routing, copper and assembly clearances remain. It is not a complete PCB fit or an approved row-circuit change.

The [110 mm grouped-power XY screen](paired-charger-110mm-screen-2026-10-14.md) is a separate, unselected candidate with sixteen paired-row courtyard boxes and local E0/E1/BQ support reservations. One packing order places every candidate rear box; routing, battery height, connector cutout and row-part approval remain open.

[ADR 0033](../docs/decisions/0033-badge-length-relaxation-proposal.md) now proposes studying a 114 mm PCB in an approximately 118 mm case: the grouped-power first-fit screen can then keep all nine interlock bypass boxes near their ICs with zero unplaced boxes in one ordering. MEC-001's 110 mm outer-case limit is unchanged pending actual PCB and enclosure checks.
