<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0086: Whole-coupon U36/L1 short-node feasibility

Date: 2026-11-05
Status: Ignored finite search only; adoption needs complete restoration proof.

The corrected converter-child trial has SHA-256
db9643801c165fb25c8078816b5cb0a4223c4ddaffa516aae1775392b3a65ded.
Earlier fixed-U36 and regional pair screens find no candidate. Broaden only
the two-part geometric screen to the whole coupon, leaving every other part,
pad, copper item, zone, rule and electrical setting fixed. This does not grant
retirement or relocation of nearby hardware permission logic.

Use U36 centres x = 1.5…112.5 mm, y = 1.5…31.0 mm on a 0.25 mm grid,
four cardinal rotations, and the same exact numbered-pin coil templates as
ADR 0082: outward distance 2.65/2.90/3.15/3.40 mm, tangential offset
-0.25/0/+0.25 mm. Keep 0.20 mm foreign clearance and 0.50 mm copper-edge
clearance. Test two ordinary-width B.Cu switching paths, each at most 5 mm,
with an initial 0.60 mm outward lead. Preserve exact TPS631000DRLR and
DFE252012P-1R0M=P2 pins/packages; U36.7 is its power-ground return.

Record the complete finite outcome and blockers, retaining at most twenty
best clear templates. Any positive template must be exported separately and
filled, with full DRC and every prior pad-group loss reported. No positive
packing template is a selected circuit: SYS/output/EN/FB/ground and every
old/current group must be restored under a separately bounded additive policy
before adoption. A zero result proves only this finite template set, not global
physical impossibility. Power/bypass/return/feedback/thermal/process and Gate A
qualification remain open; fabrication remains prohibited.

## Result

The [complete finite review](../../mechanical/review/u36-l1-global-review-2026-11-05.json)
records 2,541,840 templates and 28,514 clear short-node templates. The nearest
retained pair is filled and restored under ADR 0087, then selected only through
ADR 0088's complete 50-edge source gate. This is a positive finite feasibility
result, not an optimal-placement or electrical qualification claim.
