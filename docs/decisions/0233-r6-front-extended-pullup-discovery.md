<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0233: Extended front pull-up restoration study

Date: 2026-11-20
Status: Accepted for bounded read-only CAD discovery only.

Use the unchanged selected 25-open source. All earlier local R6/copper
replacement studies are unselected. Keep the original COL_06_B route and
every other source net intact; do not carry any prospective color retirement
into this independent study.

Screen only the previously qualified R6 front pose (76.100,6.900) mm /
90 degrees and its 1.175 mm ordinary F gate lead to actual PAIR01.5. R6
remains ERJ2RKF1001X with the exact source pad nets/identity. Prospectively
replace only the exact six R6 supply items from ADR0119, retaining its
mandatory shortened In2 shared stem and every outside source junction.

The earlier 8 mm inner-layer and 12 mm front-only pull-up searches were
bounded placement studies, not a demonstrated maximum electrical length.
Independently discover a completely F 0.20 mm resistor pull-up supply lead
from R6.1 (76.100,7.400) to actual retained main VLED R11.1
(79.350,9.100) mm, with ≤24 mm conductor, x=75.400–85.000 /
y=7.000–25.000 mm, 0.025 mm eight-neighbour steps and ≤100,000 nodes.
The expanded geometry explicitly permits going around existing address and
gate-trace endpoints. Every source trace/pad stays an obstacle, with unchanged
0.200 mm native clearance and 0.500 mm copper-edge requirements.

This is a resistor pull-up lead, with unchanged 1 kΩ value and unchanged
supply/current/protection/default-off limits. It does not connect PAIR01.4
or authorize any row-current supply path. No timing/capacitance/EMI/thermal
or hardware qualification is inferred from CAD length; those remain open
before fabrication. The previous PAIR01 high-side ≤6 mm study limit is
unchanged. No new via, unsupported centre or through transition is authorized.

Write no PCB. A complete clear path needs its own exact frozen plan, all 213
original groups/retained attached Cu, matching 24-open counts, exact104,
replay/inverse/nine-zone equality, faults and visual checks before selection.
Trial-package, electrical/return/thermal, stack/process, assembly/optical/fit
and independent Gate A/fabrication holds remain open.
