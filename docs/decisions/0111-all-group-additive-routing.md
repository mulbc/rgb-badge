<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0111: Additive bridges between any disconnected same-net groups

Date: 2026-11-10
Status: Accepted for ignored exploration; no successor selected.

The existing search targets only the largest connected pad group on a net.
This omits shorter joins between two other disconnected groups. Explore
ordinary additive bridges to every other actual same-net group, starting
from the unchanged 36-open board. No part, pose, source copper, profile,
zone, width, clearance or safety/current setting changes are permitted.

Use the existing ADR 0091 ordinary 0.20 mm track and adjacent-via policy;
no new unsupported central microvia is permitted. Capture native endpoints
in actual retained pads/copper, not arbitrary zone anchors. After refill,
require the source group to join an originally different target group and
all preceding groups and exact original copper/net identities to survive.
An aggregate count reduction alone is insufficient.

Ignored candidates are not selected until exact unchanged 104-finding DRC,
independent physical counts, exact ledger/replay, source/fault checks and
visual review pass. Partial VLED group joins do not establish connection to
the regulator or electrical functionality. Qualification and independent
Gate A still precede fabrication; the zero-open objective remains open.

Outcome: the opt-in `--all-group-targets` extension and explicit source-pad
reference selection are implemented. The default largest-group mode remains.
A native regression with an unreachable largest group proves that the new
mode joins two other groups (2→1 opens) while the default stays at 2, with
all old groups retained. Portable group-change/deduplication checks also pass.
The real-board exploratory three-net search selects no join and retains
36 opens. This is a search-tool improvement, not a board successor.

Also permit an ignored eight-neighbour grid variant to check whether the
four-direction grid misses diagonal ordinary-width corridors. Every diagonal
edge must pass exact native swept-shape clearance even when both endpoints
pass the coarse mask. Use Euclidean step length and a zero heuristic
(Dijkstra), retaining bounded search, all source/group guards and unchanged
physical geometry. This variant is not enabled in the production tool by
this record; only complete successor gates can select resulting copper.

The eight-neighbour ignored variant also selects no join across VLED, GND,
+BAT_GAUGE_SW and DISPLAY_CLEAR_OK. It adds no copper and remains at 36 opens;
several searches hit the explicit 150,000-node bound. No global routing
impossibility or diagonal production-mode validation is inferred.
