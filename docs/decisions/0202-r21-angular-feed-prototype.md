<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0202: R21 angular feed prototype

Date: 2026-11-16
Status: Accepted for ignored complete-circuit feasibility only.

ADR0201 finds exact-pad-preserving R21 alternatives at 15 and 165 degrees,
but no pad-centred supported capture. Freeze its 15-degree pose at
(66.267037,5.879410) mm, with original gate pad 2 fixed at (66.750,5.750).
The separate 165-degree alternative at (67.232963,5.879410) mm may be
tested under the same bounds, retaining the same fixed gate-pad centre.
Keep R11 at its original selected pose and all other parts/copper/rules fixed.
No source retirement or initial addition. All part/field/local-pad identities
and independently calculated rounded global pad transforms must match.

Permit one ignored exact-pose prototype and the same bounded supported VLED
feed search as ADR0200 from actual R21.1 to the retained main supply group:
0.050 mm native eight-neighbour graph, ≤1,000,000 nodes, ≤12 mm new ordinary
0.20 mm feed, ≤4 mm In2 copper, supported outer microvias and mechanical
centre transitions only. Preserve every original/current group and contact
through native refills, source edge/hole/clearance rules and exact104.

Matching reduced native/physical count and every source/replay/inverse/contact/
hole/fault/visual gate precede selection. Clear geometry without a complete
join is rejected. No current/resistance, electrical/part/process/stack/fit/
Gate A or fabrication hold changes.
