<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0234: Separate R6 gate and supply lower captures

Date: 2026-11-20
Status: Accepted for exact read-only combined geometry discovery only.

Use the immutable selected 25-open source. ADR0232 proves the exact fifteen
COL_06_B items form a private connected path with preserved source interfaces;
sixteen sampled three-wire replacements clear. Fix its Y=3.050 mm replacement
for this independent screen. Do not infer a complete supply route from it.
ADR0233's extended front-only route still fails its bounded search and writes
no PCB (14,878 nodes); it is not selected.

Explicitly orient R6 B at (75.750,3.750) mm / 180 degrees. Its exact 1 kΩ
ERJ2RKF1001X supply pad is now (76.250,3.750), gate pad (75.250,3.750).
No other part moves or net/package/field changes. Omit only the exact fifteen
COL_06_B tracks and exact six R6 supply items, retaining the mandatory In2
shared-stem remainder from ADR0119. Use the three ordinary 0.20 mm color
replacement wires through (74.400,3.050) and (75.750,3.050), keeping both
original endpoints. Preserve all original groups and attached retained Cu.

Power: ordinary B lead to supported aligned B/In4 + In3/In4 captures at
(76.650,4.550). This only establishes a supply root, not restoration. Gate:
ordinary B lead to supported aligned B/In4 + In3/In4 captures at
(75.250,4.250), ordinary In3 to mechanical buried In2/In3 0.50/0.30 centre
(75.150,3.650), then ordinary In2 through (76.600,3.650) to aligned supported
In1/In2 + F/In1 captures at actual PAIR01 gate body (76.600,4.300).
All ordinary conductors are 0.20 mm and supported microvias 0.30/0.10 mm.
Screen actual B courtyards/pads, all mutual/source Cu and all drill pairs.
No co-located mechanical/micro drill stack or new through via is allowed.

If fixed geometry clears, independently route the pull-up supply on In3/In4
from (76.650,4.550) to actual retained main-VLED Cu only, including every new
fixed gate/color object as an obstacle. The whole pull-up conductor remains
≤8 mm and gate ≤12 mm; PAIR01.4 remains open. A separate frozen plan and all
full successor gates are mandatory before any PCB is written or selected.
No changed current/protection/default-off, row-current or hardware-performance
claim is authorized. All timing/return/thermal, trial package, fit/process/stack
and independent Gate A/fabrication holds remain open.
