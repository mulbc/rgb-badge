<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0225: Exact front row-zero prototype

Date: 2026-11-20
Status: Accepted for an ignored CAD prototype and validation only.

Starting from the exact 26-open source in ADR0224, move only PAIR01 to F
(76.100,4.300) mm / 270 degrees and R6 to F (76.100,6.900) mm / 90 degrees,
using native top-bottom flips. Retain the exact trial transistor package,
all numbered nets, identities and fields; R6 remains ERJ2RKF1001X. Independent
absolute pad transforms in integer nm are PAIR01 (79850000-y,80050000-x)
and R6 (y+67350000,x-50350000).

Freeze the complete typed copper ledger in
mechanical/review/front-row-zero-prototype-plan.json before writing a PCB.
Retire exactly the 32 private selector items proved by ADR0224, its four
obsolete row-output items, the two original gate straps, and the six R6
supply items from ADR0119. Preserve the R6 shared stem from (58.750,9.713636)
to (58.750,14.050) mm and every original outside junction. Add only the
screened local ordinary 0.20 mm F leads/straps, three supported F/In1
0.30/0.10 mm pad accesses, the screened In1 ground lead and exact 7.913657 mm
maximum selector path. VLED uses the independently witnessed main In1 plane;
no added In1 supply lead, central transition or through via is authorized.

A valid candidate must preserve all 214 source pad groups and all retained
attached source copper, keep zero orphan copper, and have matching native
and physical 23-open counts. Expected main GND/VLED sizes are 197/38. The
complete ROW_SEL_00, ROW_00_A and ROW_GATE_00 groups must remain connected.
Require stable refill/replay, exact inverse restoration and zone equality,
independent part/pad transforms, exact retained raw copper, full hole and
front courtyard checks, fault controls and visual review before adoption.
The original 104 DRC inventory must remain exact after independently mapping
only moved PAIR01 intrinsic pad findings back to its original B pose; no
new external finding may be normalized or waived.

The plan authorizes no canonical replacement, fabrication output, stack or
via-in-pad process approval, substitution, current increase or performance
claim. All electrical, return, thermal, assembly, optical/fit, trial-package,
controlled-stack and independent Gate A holds remain open.

The first complete refill rejects the plane-only supply assumption: native
and physical opens are 24, with the old R6 VLED group split (main size 36).
No candidate is selected. Read-only discover an explicit ordinary 0.20 mm
In1 VLED lead from (75.450,5.225) to the retained main VLED via at
(79.100,7.800), bounded by 6 mm, 0.025 mm eight-neighbour grid,
x=74.500–80.000 / y=4.500–9.000 mm and 100,000 nodes. All current prototype
copper, including the selector route, stays an obstacle. Freeze any successful
refinement separately before rebuilding; retain the failed first evidence.

The explicit In1 lead search exhausts its reachable 182-node component.
Instead read-only screen an F supply extension from R6.1 to an off-pad
supported F/In1 capture, x=76.500–77.400 / y=7.000–8.500 mm at 0.050 mm
steps. Require both straight 0.20 mm F extension and In1 lead to the same
retained main VLED via clear against every existing candidate item, with
full hole audit and ≤6 mm total PAIR01.4-to-main supply conductor length
(including the existing F pull-up supply path). Replace, rather than add to,
the unsuccessful PAIR01.4 capture if an exact successful plan is frozen.
No other candidate item moves or retires; no PCB is written in this screen.

The straight-lead screen rejects all 589 points (259 length, 330 copper).
Some off-pad accesses themselves clear, while only their straight In1 leads
fail. Read-only recheck the same bounded grid for direct contact with an
actual main-VLED In1 filled polygon of the rejected refilled candidate,
using a retained R18.1-connected source witness. Require F extension, via,
full hole rules and ≤6 mm PAIR01.4-to-capture length. Any selected proposal
still requires a fresh complete refill and full original-group preservation;
pre-refill polygon contact alone is insufficient evidence.

The direct-plane subset has no witness in its initial small rectangle.
Extend only this read-only off-pad discovery rectangle to x=74.500–77.400 /
y=5.700–10.500 mm in 0.050 mm steps. Keep both source and candidate fixed,
the actual main-plane witness, copper/hole checks and unchanged ≤6 mm
PAIR01.4-to-capture bound. This expands sampling, not electrical limits.

Read-only test routing the explicit In1 VLED lead before the new selector
lead. In this screen omit only the newly proposed ROW_SEL_00 In1 tracks
from the rejected prototype, retaining its selector capture and every source
item. Use the exact earlier 6 mm / 0.025 mm / 100,000-node VLED search and
bounds. A successful supply path becomes an obstacle for a fresh selector
search under its original 12 mm bounds. This authorizes no source-selector
retirement beyond the already frozen 32 items and no PCB write.
