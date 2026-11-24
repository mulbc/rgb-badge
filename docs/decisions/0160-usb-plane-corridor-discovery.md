<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0160: Read-only USB plane continuity corridor discovery

Date: 2026-11-15
Status: Accepted for read-only native geometry discovery only.

The selected 29-open source remains immutable. The bounded reverse heartbeat
path repeatedly separates the original main +3V3_USB group and leaves two old
In2/In3 microvias dangling. The correct-profile rejected input from ADR 0156
is diagnostic evidence only; no item from it is adopted.

On the immutable selected source, inspect original +3V3_USB In3 filled-plane
components actually connected to U31.12. Classify their original copper contacts
by native component in the diagnostic rejected input. Read-only find short
ordinary 0.20 mm track corridors connecting contacts that the rejected input
separates. Include the original via witnesses at (76.151904,30.849096) and
(76.951904,30.049096) mm if they share eligible original fill. Preserve every
source via type, including legacy centre microvias; do not add/retype any hole.

Candidate track polygons must lie wholly within an original individual filled
source-plane polygon, using conservative outside polygonization and exact
integer subtraction, and pass actual native foreign/no-net/mechanical copper
clearance. Endpoints must physically contact recorded original copper witnesses.
Sample centre paths at 0.025 mm, retain exact non-grid endpoints, record all
bounds and misses, and limit each corridor to 10 mm and a later cohort to
20 mm total. Use original-plane geometry only, not a plane name or the cut
candidate's fill. This is a finite discovery, not global feasibility proof.

Write no PCB. Freeze any successful exact contact/zone/path cohort before
implementation. Its purpose would be to make already-present plane continuity
explicit so later signal routing treats it as a real obstacle; it does not
raise supply current, qualify conductor capacity or alter native rules.
All 217 selected-source groups, source copper/parts/nets/poses and complete
native/physical/finding/hole/contact/replay/inverse/orphan/fault/source/visual
gates remain required. No electrical/protection/default-off or fabrication
boundary changes; zero opens and every qualification/Gate A hold remain open.

The first strict fill-only screen finds no eligible cross-component endpoint
pair: original pads/vias/thermal contacts are not wholly represented by the
fill polygon alone. Extend the read-only containment model only by unioning
that individual original filled polygon with original same-net In3 native
copper outlines that directly touch it. Polygonize those original outlines
conservatively inward, and the proposed track outlines outward, at 0.001 mm
error; require exact empty subtraction against that original union. Preserve
and explicitly report all original drill inventory and native types. This is
native copper-outline geometry, not a drilled-volume/fabrication assessment.
No copper from the rejected candidate or a disconnected original net/group
may enter the containment union. All previous bounds and no-write/full-gate
restrictions remain. Record source fill and original-contact witnesses for
each tested union and the reason for the initial finite miss.

The original-contact union exposes the expected three diagnostic components,
but no cross-component pair lies within the first 8 mm endpoint filter. This
is a bound miss, not a geometric impossibility. Extend read-only discovery
to endpoint separations up to 30 mm, each corridor at most 40 mm and a future
cohort at most 80 mm total, while keeping every track wholly within the
original native copper union. Retain the 100,000-node search bound, exact
containment/foreign-copper checks and no-PCB restriction. This does not alter
the heartbeat signal's independent 120 mm bound or any electrical limit.
Record minimum cross-component witness separations in each original unit.
