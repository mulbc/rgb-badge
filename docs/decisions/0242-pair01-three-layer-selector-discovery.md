<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0242: PAIR01 three-layer selector discovery

Date: 2026-11-20
Status: Accepted for bounded read-only selector routing discovery.

Use the exact ADR0239 source, package pose, 62 obsolete-leaf retirements and
its qualified fixed power, row and gate geometry. ADR0241's exact below-bus
point is rejected for source COL_06_B/ROW_01_A Cu and a through-hole conflict;
its proposed ground U path is also blocked by retained ROW_01_A. Keep those
negative results. Retain ADR0239's original short direct F ground lead to
(82.600,5.250); no ground U route is carried into this independent study.

Remove only all proposed selector access/lead objects, keeping every other
fixed proposed object and original retained source Cu. Discover selector
restoration from the actual new F pad centre (80.925,5.200) to the same
witnessed retained R22/U2 driver-side Cu on F/In1/In2. Permit only supported
0.30/0.10 mm F/In1 or In1/In2 transitions at 0.050 mm lattice points, at
most six transitions. No preselected selector capture may bypass source/new
Cu or hole rules. All original 62-item retirement/contact obligations remain.

Use x=75.000–85.500 / y=4.000–12.000 mm, 0.025 mm planar eight-neighbour
steps, ≤100,000 expanded nodes and ≤12 mm complete selector conductor.
A 0.5 mm transition search penalty is separate from physical length. Use
native source/mutual Cu and all source/new drill checks, including exact
supported adjacent alignment only when allowed by the unchanged policy.
Simplified segments and actual retained driver contact must recheck before
a path is accepted. A failure is only bounded discovery, not impossibility.

Write no PCB. No source color/row Cu may retire or change; no new centre or
through via is allowed. Row/high-side paths retain ≤6 mm bounds, all 212
original groups and retained attached Cu must survive, and the full frozen
prototype/replay/inverse/exact104/fault/visual gates remain prerequisites for
23 opens. Current/protection/default-off, timing/return/thermal, trial package,
fit/process/controlled-stack and independent Gate A/fabrication holds persist.
