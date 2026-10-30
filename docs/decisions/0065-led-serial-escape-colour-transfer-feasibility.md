<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0065: Exact LED serial escape colour-transfer feasibility

Date: 2026-10-29; continuation 2026-10-30
Status: Ignored feasibility only; no additional original retirement selected.

The 60-edge board leaves LED_SOUT open at U1.42. A native obstruction screen
finds that short B.Cu escapes toward x = 82.20–81.10 mm, y = 1.75 mm meet
exactly one original In4 obstruction: COL_10_B, from (84.40, 1.60) to
(61.70, 1.60) mm, width 0.20 mm. Other accepted copper remains fixed.

Permit ignored rework of only that exact original signature. Keep both original
In4 endpoints and every direct source-layer contact. Transfer at most 2 mm of
its interval through an adjacent-layer dogleg (B.Cu or In3), with at most 1 mm
vertical displacement and aggregate replacement at most original plus 2 mm.
Preserve every 60-edge addition/group/pose/zone and every other original item.
Keep colour width/clearance at 0.20 mm and adjacent microvias at 0.30/0.10 mm.

LED_SOUT may be investigated under the existing ADR 0047 exact digital-net
feasibility scope, with 0.12 mm tracks, 0.20 mm clearance and its unchanged
120 mm aggregate bound. It carries U1 serial data from TLC59581RTQT pin 42;
COL_10_B is a constant-current LED sink output. Rechecked
[TI TLC59581/82 Rev. A](https://www.ti.com/lit/ds/symlink/tlc59581.pdf).
No part, pin map, current, protection/enable setting or package change is allowed.
This trial does not qualify serial timing/returns, output current, thermal behavior
or the manufacturing process.

Adoption requires exact source/replacement/interface and narrow-digital catalogs,
frozen 60-edge preservation, independent lower native/physical counts, unchanged
full 104 findings, stable fills/replay, source/fault checks and unchanged original-
orphan restoration. No original deletion, new narrow inventory or fabrication
exception is selected merely by authorizing this ignored screen. Independent
Gate A remains required before fabrication.

## Local three-dimensional follow-up, 2026-10-30

The two-layer symmetric/asymmetric screens make no accepted escape. Native
inspection identifies U1.43 and its retained +3V3_APP B.Cu descent as an extra
barrier to the colour detour. Keep that supply copper fixed. An ignored follow-up
may transfer only the interval x = 81.10–84.30 mm (3.20 mm) of the same original
COL_10_B signature, using a local full-width multilayer path and adjacent
microvias. Bound its local search region to x = 80.60–84.40, y = 0.65–3.00 mm
and aggregate replacement length to the unchanged original-plus-2-mm bound.
This revises only the earlier two-millimetre interval planning screen; it changes
no clearance, width, current or source-retention rule. Every retained original
In4 contact and every 60-edge group/copper item other than the one enumerated
original must survive. No canonical adoption is selected before the complete gate.
