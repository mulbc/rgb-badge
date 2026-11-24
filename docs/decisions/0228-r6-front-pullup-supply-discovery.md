<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0228: R6 front pull-up supply discovery

Date: 2026-11-20
Status: Accepted for bounded read-only routing discovery only.

Use the exact selected 25-open source and preserve all 213 original groups.
ADR0227's R6 B proposal fails: no direct supply contact, a 1,200-node bounded
B supply search exhausts, and its centre transition is blocked. Retain that
negative evidence; do not select a PCB from it.

Independently test moving only R6 ERJ2RKF1001X to F (76.100,6.900) mm /
90 degrees, using its native top-bottom flip. Keep PAIR01's existing trial
front pose and all other parts fixed. Retire prospectively only ADR0119's
exact six R6 supply items and include the mandatory shortened shared In2 stem.
R6.2 reaches existing PAIR01.5 with the previously screened 1.175 mm ordinary
F gate lead. PAIR01.4 remains its original isolated power pad; no row-current
supply conductor or closure is proposed.

Screen a 0.20 mm F pull-up supply lead R6.1 (76.100,7.400) to supported
0.30/0.10 mm F/In1 access (77.200,7.400). Discover ordinary 0.20 mm In1
restoration to actual retained main VLED via (79.100,7.800), within
x=76.900–81.000 / y=6.000–10.000 mm, 0.025 mm eight-neighbour steps and
at most 100,000 nodes. Bound the complete R6 pull-up supply conductor to
8 mm, including its 1.100 mm F segment. This is a separate resistor pull-up
lead; ADR0225's 6 mm PAIR01 high-side/row-current supply limit still applies
to any future PAIR01.4 closure. No current-limit or row-power capacity claim
is made, and electrical/timing/thermal qualification remains open.

Require actual F courtyards/pads, all source/new Cu and full-board hole rules.
All new Cu must restore original groups; no new central or through transition
is authorized. Write no PCB. Any successful path needs a frozen prototype
plan, independent part/pad transform and all full successor gates before
selection. Existing power/default-off/protection, via/process, trial package,
controlled-stack, return/fit and independent Gate A/fabrication holds remain.

The bounded In1 supply search exhausts 769 reachable nodes without a route.
Instead read-only discover a completely F supply lead from the same R6.1 to
actual retained main VLED F via at (78.800,10.650) mm. Use x=75.400–80.300 /
y=7.000–14.500 mm, 0.025 mm eight-neighbour steps, ≤100,000 nodes and a
separate ≤12 mm pull-up conductor bound. This explicitly studies going around
the existing ROW_A2 F route end, retaining every address/gate/source wire;
no new via or source omission is permitted. The 12 mm is a CAD pull-up study
bound, with no row-current/PAIR01.4 connection, no changed current limit and
no electrical/timing/return/assembly/fabrication approval. Do not select any
route until a frozen full prototype preserves all groups and exact104.

The F-only graph exhausts 13,674 nodes without a ≤12 mm restoration in its
fixed bounds. Read-only inventory actual R18.1-connected VLED Cu on In2
within 8 mm of (77.200,7.400), and screen an aligned supported F/In1 plus
In1/In2 0.30/0.10 mm pair at that same proposed off-pad capture. Retain all
source and existing candidate-group copper and full hole rules. This inventory
and two-access screen writes no PCB and authorizes no centre/through via.

The In2 inventory establishes nearby main VLED copper, including via
39d4d099-d79a-5165-a9ec-4ef886262bed at (78.800,9.650) and wire
c793938e-bbd0-5ef0-9f5a-77924ee5c4ca near (78.850,6.950). The proposed
(77.200,7.400) second access is blocked by COL_13_B/COL_11_G. Read-only sample
aligned supported F/In1 + In1/In2 captures at x=75.000–77.400 /
y=7.000–9.500 mm in 0.050 mm steps. Require both via shapes and a direct
0.20 mm F lead from R6.1 clear, full-board holes (including aligned-stack
policy), and ≤8 mm combined F plus future In2 conductor. Record exact clear
captures before any In2 route search; no PCB or new source omission.

The exact 2,499-point capture screen yields 31 copper/hole-clear aligned
access pairs and rejects 2,468 for copper. Read-only multi-source search on
In2 from those 31 exact captures to either retained main-VLED wire endpoint
(78.850,6.950) or retained In1/In2 via (78.800,9.650) mm. Use 0.025 mm
eight-neighbour steps, x=74.500–81.000 / y=6.500–10.500 mm, at most
100,000 nodes and ≤8 mm combined original F extension plus In2 conductor.
Retain every source item and require merged-segment native collision checks.
Write no PCB; full prototype/inverse/DRC/group gates remain prerequisites.

The two-target In2 multi-source graph exhausts 489 nodes without a route.
One further read-only two-layer search may start with the already screened
F/In1 capture (77.200,7.400), and switch only between In1 and In2 through
supported 0.30/0.10 mm accesses. Use 0.025 mm planar steps, access candidates
only on the 0.050 mm lattice, x=75.000–81.000 / y=6.500–10.500 mm,
≤100,000 expanded nodes, ≤8 mm total F plus inner conductor and ≤6 added
In1/In2 transitions. Targets are the two existing In2 interfaces above or
the retained main In1 via at (79.100,7.800). Each access must clear both Cu
layers and every original/root/new hole; an aligned F/In1-to-In1/In2 root
pair is allowed only by the existing supported-stack policy. Prefer fewer
transitions using a 0.5 mm search penalty per transition; this penalty is
not conductor length or a physical measurement. Preserve all source Cu.
Any search failure is only a bounded heuristic result, not a proof that no
multi-layer route exists. Write no PCB; a successful path still needs every
full successor gate and unresolved process qualification.

The fixed-root two-layer heuristic ends after 1,260 nodes, checking 308
transition positions (11 clear), without a route. One final bounded variant
may seed the same two-layer search from every F/In1-only access that passes
the existing 2,499-point capture grid and actual F lead/hole checks. Keep
exactly the same two-layer ROI, 8 mm conductor, 6-transition, 100,000-node
and source-retention bounds. Each search state carries its actual root,
whose supported F/In1 access must also satisfy every new drill pairing.
Final native mutual-hole checks remain mandatory if any route is found.
