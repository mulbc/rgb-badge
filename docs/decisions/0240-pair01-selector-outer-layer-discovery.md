<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0240: PAIR01 selector outer-layer discovery

Date: 2026-11-20
Status: Accepted for bounded read-only selector restoration discovery.

Use ADR0239's exact source, pose, 62-item prospective retirement and all fixed
new geometry. Its In1 selector search ends after 10,483 nodes without reaching
the chosen port. Keep that negative result; no PCB is written or selected.
All fixed row, gate, power, ground and three F/In1 accesses clear.

Independently discover the selector on In1/In2, beginning at the proposed
F/In1 selector access (81.350,5.150). Permit only supported 0.30/0.10 mm
In1/In2 transitions, at 0.050 mm lattice points, at most four additional
transitions. Require each actual source and new drill pairing; an aligned
adjacent root pair is allowed only under the unchanged supported-stack policy.
No new centre or through transition is authorized.

Before routing, remove only the frozen 62 prospective items in memory and
identify the actual retained driver-side ROW_SEL_00 component anchored by
R22. Its retained original Cu (not a label or any new proposed Cu) supplies
all valid In1/In2 route goals. The moving PAIR01 pad may not be counted as a
driver witness. Preserve every original retained source interface/group in
any final prototype.

Use x=75.000–83.000 / y=4.900–11.500 mm, 0.025 mm planar eight-neighbour
steps, ≤100,000 nodes and ≤12 mm combined F plus inner selector conductor.
Use a 0.5 mm transition search penalty separate from actual length, and
native merged-segment/source/mutual Cu and full source/new-hole checks.
Include every other fixed proposed object as an obstacle. A failure is only
a bounded heuristic outcome. Write no PCB; a complete path still needs a
frozen prototype and all full successor gates before 23 opens can be claimed.
Current/default-off/protection, row-power/return/thermal/timing, trial-package,
fit/process/controlled-stack and independent Gate A/fabrication holds persist.
