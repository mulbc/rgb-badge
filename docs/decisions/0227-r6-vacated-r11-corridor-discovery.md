<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0227: R6 discovery through the vacated R11 corridor

Date: 2026-11-20
Status: Accepted for bounded read-only geometry and contact discovery only.

Use only the selected 25-open PAIR01 ground source, SHA-256
ec0bf7fc842f3dd4f9210e7667925cffc388d3d82906e44c5bde4e10f428ee88.
Read ADR0119's exact R6 supply cohort/shared-stem requirements and the current
selected README. R6 remains Panasonic ERJ2RKF1001X, with all pin identities,
numbered nets and package geometry unchanged. No other part moves.

Screen R6 B at (72.750,4.250) mm / 180 degrees, the vacated original R11 pose.
Prospectively omit only the six exact R6 supply items frozen in ADR0119;
include their required shortened In2 stem from (58.750,9.713636) to
(58.750,14.050) mm. Require direct native contact between proposed R6.1 and
original main VLED copper, without assuming that the old R11 pose still has
such contact. Actual B courtyards, pads, source/mutual Cu and hole rules apply.

Discover a gate route through the vacated old R11 corridor, without copying
any unsupported old centre microvia. First screen B/In4 access at
(72.150,4.250), ordinary In4 to (76.200,4.250), In3/In4 access there,
ordinary In3 to a 0.50/0.30 mm mechanical buried In2/In3 transition at
(76.650,4.550), ordinary In2 to supported In1/In2 access at (77.100,4.850),
and ordinary In1 to supported F/In1 access at PAIR01 gate body centre
(76.600,4.300) mm. Include the short B lead from R6.2 (72.250,4.250).
All ordinary conductors are 0.20 mm and total new gate lead is bounded by
12 mm; the bound is a CAD study limit, with electrical/timing qualification
remaining open. Audit every new drill against all source and new holes.
No new through via, co-located mechanical/micro drill stack, rule relaxation,
other source omission or PCB write is authorized. A successful screen needs
its own frozen complete prototype plan and full successor checks before use.

The source's all 213 groups/retained attached copper must remain intact in
any eventual candidate. VLED and all power/protection/default-off limits,
trial PAIR qualification, return/thermal/fit/process/controlled-stack and
independent Gate A/fabrication holds remain unchanged.

The exact first screen is rejected: the vacated R11 supply pad has no contact
with original main VLED, and the proposed centre/lower transition collides
with retained COL_06_B/COL_08_G copper and a historical centre hole. Do not
claim that an old occupied pose implies a usable supply connection.
Read-only catalogue actual main VLED B pads/copper within 6 mm of R6's
proposed supply pad, preserving all the same omissions and geometry. This
inventory authorizes no new wire, larger search or PCB.

The actual nearest B main-supply witness is R8.1 at (72.575,8.500) mm,
4.303270 mm from proposed R6.1, on original wire
eb638639-7d39-5a9a-972d-944b259be009. Read-only discover a 0.20 mm B supply
lead from (73.250,4.250) to that exact port, ≤6 mm, in x=71.000–74.500 /
y=3.750–9.000 mm using 0.025 mm eight-neighbour steps and ≤100,000 nodes.
Only the exact six R6 supply items may be prospectively omitted; include
the unchanged ghost R6 pads and required shared-stem remainder. Omit all
rejected proposed gate-routing items from this independent supply screen.
Retain every other source item and write no PCB. No increased current or
assembly/electrical/return/thermal qualification is inferred from geometry.
