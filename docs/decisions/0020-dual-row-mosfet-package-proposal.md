<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0020: Proposed complementary MOSFET package for each row stage

- Date: 2026-10-06
- Status: **Proposed for electrical and manufacturing review; no schematic/BOM substitution**
- Applies to: coupon row-stage validation and the eventual 48 × 16 final badge
- Retains: 16 individually selected common-anode rows, hardware-default row blanking, VLED fault inhibition, 1.95 mm pixel pitch and independent Gate A

## Problem and proposed direction

The existing row circuit uses 16 `DMP2066LSN-7` P-channel MOSFETs and 16 `2N7002K-7` N-channel gate sinks. Their project-local courtyards consume **397.6 mm²** outside the projected pack. A [connector-first placement trial](../../mechanical/connector-first-trial-2026-10-06.md) cannot fit four of them plus seven other captured parts, before adding the unfinished power circuit.

Evaluate `DMC1229UFDB-7` (Diodes Incorporated, U-DFN2020-6 Type B) as one **electrically separate N/P pair per row**, retaining the same 1 kΩ P-gate pull-up, 100 kΩ N-gate pull-down, decoder and row-control truth table. The N channel would sink its own P-gate node; the P channel would switch VLED to its row. No transistor connection is internal except each device's own terminals, so schematic pin mapping and external gate wiring still require a fresh source audit. This is a candidate, not approval to edit the canonical row sheet.

The manufacturer's [DMC1229UFDB datasheet](https://www.diodes.com/datasheet/download/DMC1229UFDB.pdf) gives a 2.00 mm nominal body, 0.605 mm maximum body height, ±8 V VGS limits and 12 V drain-source ratings. At 25 °C it specifies N-channel RDS(on) ≤34 mΩ at 2.5 V gate drive, and P-channel RDS(on) ≤81 mΩ at −2.5 V. It lists P-channel steady-state ID −3.0 A at 70 °C **on a 1 × 1 inch, high-coverage 2 oz test board**; that is not a badge-board thermal rating. The exact orderable suffix is `-7` for the stated tape-and-reel option; availability and assembler handling are unverified.

## Quantified screening result

The [driver calculation](../../hardware/coupon/rev-a/driver-capture.md) gives 233.02 mA for one 16-pixel white coupon row at maximum nominal settings. Scaling the same per-pixel setting to 48 pixels gives **699.06 mA per active final-badge row** as a calculation, not a board measurement. With 81 mΩ, `I²R` would be about **39.6 mW while that row is on** at the stated 25 °C resistance condition. It is not a maximum hot-device/assembled-board dissipation bound; pulse edges, LED settings, copper, temperature and simultaneous-row faults require review. A 1 kΩ pull-up from nominal 3.944 V VLED would ask the N channel to sink approximately 3.94 mA while the row is selected; its 3.3 V gate drive lies above the datasheet's 2.5 V RDS(on) test level. Verify actual drain-low voltage, timing and reset behavior rather than inferring them from VGS(th).

The [first-author candidate footprint](../../hardware/coupon/rev-a/dual-row-package-library-audit.md) has a 3 × 3 mm courtyard derived from the manufacturer's suggested Type B lands. Sixteen candidate packages consume **144.0 mm²**, nominally **253.6 mm² less** than the 32 existing courtyards. The [dual-package XY screen](../../mechanical/review/dual-row-package-plan.svg) then gives all currently captured non-row parts, 16 pair boxes, the connector pocket and the BQ24074/TPS63020/two TPS259474/optional INA232 **IC-package minima** nonoverlapping positions. The drawing has no routing gap and excludes power passives/inductors, gauge buffer, hardware display interlock, mounting, RF cable and copper. It does **not** prove full fit.

The 0.605 mm package height cannot be credited automatically beneath the battery: the existing 11 mm section already leaves only 0.25 mm nominal with a 0.55 mm 0402. The pair packages stay outside the pack in this screen. Their manufacturer land pattern now has a first-author transcription, but its pad numbering, stencil and assembly use still need independent review.

## Capture and review conditions

1. Calculate a bounded per-row current including LED-current tolerance, fault/overlap behavior and the chosen VLED rail; check P-channel SOA, hot RDS(on), gate-source/transient margins and copper temperature on the compact board. The 25 °C arithmetic above is only a candidate screen.
2. Audit the current manufacturer bottom-view pin map, pad geometry, pin-one mark, stencil and recommended land pattern into a project-local symbol/footprint. Do not replace 32 schematic instances by reference-number coincidence or treat the trial boxes as lands.
3. Preserve all hardware-default OFF, reset, boot and programming blanking behavior and verify row dead time, turn-off and visible ghosting. The existing 2N7002K uncertainty at 3.3 V does not by itself validate the replacement.
4. Decide whether the 16 × 16 coupon should use the pair package so its measurements validate the final row stage. Record that decision before schematic capture; a coupon with the old stage cannot qualify the new stage by analogy.
5. Run native KiCad ERC/netlist/visual checks, real PCB DRC, assembly/thermal review and independent Gate A before fabrication. No current, charge or enclosure limit changes through this proposal.

This is the highest-leverage component-area option found in the connector-first screen. It is not an accepted design change or a PCB release.
