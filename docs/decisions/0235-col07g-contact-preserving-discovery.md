<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0235: Contact-preserving COL_07_G discovery

Date: 2026-11-20
Status: Accepted for bounded read-only geometry/contact discovery only.

Use the exact selected 25-open source. ADR0234's fixed geometry passes all
courtyards/pads and new drill checks, but original COL_07_G In2 track
73a74c95-a110-5f1a-b5ec-43a975fd645c blocks the proposed gate centre and its
In2 lead. That complete 0.20 mm track runs (78.050,3.750)→(73.900,3.750).
All other fixed geometry clears once only this additional track is omitted.
Catalogue every original outside pad/Cu/zone contact before any replacement.
Retain all original terminal groups and attached outside copper.

Read-only discover an ordinary 0.20 mm In2 replacement between its exact
original endpoints, keeping all other source Cu and all ADR0234 fixed
R6/gate/power-root/COL_06_B-detour objects as obstacles. Use x=73.400–78.500 /
y=2.500–5.800 mm, 0.025 mm eight-neighbour steps, ≤100,000 expanded nodes
and ≤10 mm conductor. No source omission beyond this one track, the exact
fifteen COL_06_B tracks and exact six R6 supply items is allowed. Retain the
mandatory R6 stem remainder. Source vias/pads/nets/widths remain unchanged;
no new color via, centre or through transition is permitted.

This does not authorize a PCB write or imply full R6 supply restoration.
Require exact fixed/source/mutual Cu and all source/new holes, preserved
outside contacts, all 213 original groups, complete supply restoration,
matching reduction, exact104 and every full successor gate before selection.
Current/default-off/protection and all electrical/timing/return/thermal,
trial-package, process/stack/fit and independent Gate A/fabrication holds persist.

The exact COL_07_G search finds a 4.688478 mm replacement after 3,593 nodes,
with merged segments natively rechecked. Fix that path and all ADR0234
objects for the next independent supply search. All prospective source
retirements remain exactly 22 items (15 color stair segments, one COL_07_G
wire, six R6 supply items); no PCB is written.

Read-only search on In3/In4 from the fixed power capture (76.650,4.550),
initializing both layers through its actual supported access pair. Targets
must be original R18.1-connected VLED Cu endpoints on those two layers,
inside x=75.000–81.500 / y=4.100–9.000 mm. Use 0.025 mm planar steps,
0.050 mm supported In3/In4 access grid, ≤100,000 nodes and ≤4 additional
transitions. Combined original B lead plus inner conductor remains ≤8 mm.
Use exact native source/mutual Cu and source/new holes, the established
0.5 mm transition penalty, and bounded-heuristic interpretation. Include the
whole fixed gate/color geometry as obstacles; no new core or through via
is authorized in this search. Full restoration and all successor checks are
still required before a prototype, selection or reduced count is claimed.
