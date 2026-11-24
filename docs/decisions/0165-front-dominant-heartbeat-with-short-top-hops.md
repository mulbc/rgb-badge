<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0165: Front-dominant heartbeat with bounded top-layer hops

Date: 2026-11-15
Status: Accepted for ignored additive feasibility; no successor selected.

ADR 0164's access prototype preserves all 217 groups and all original copper.
Its F-only search exhausts 419,806 sampled nodes without a join; its F/In1
search reaches 1,200,001 nodes. Neither result establishes global impossibility
or permits selection. The selected 29-open source remains unchanged.

Keep exactly that nine-item access cohort and every immutable source part,
pose, net, rule/profile, item/type and safety boundary. Permit a further
front-dominant DISPLAY_HEARTBEAT search on F/In1/In2 only. In1 is transit-only:
no new horizontal signal track on In1. Planar tracks remain ordinary 0.20 mm
on F or In2; all new route transitions are supported outer adjacent
0.30/0.10 mm microvias, with same-hole aligned stacks allowed only under the
existing exact adjacent/same-net policy. No new centre microvia or additional
mechanical/full-span capture is introduced by this search.

Bound all newly added In2 track length, including the fixed 0.500 mm access
lead, to 24 mm total and each added In2 segment to 4 mm. Keep the 120 mm total
signal and 1,200,000-node bounds. Use F cost 1, transit-only In1 cost None and
In2 cost 25, with weighted heuristics up to 20; these are exploration costs,
not optimality claims or clearance changes. Record exact costs/layers and
independently check output lengths before any adoption. The F/In1-only
alternative may also use a larger heuristic weight under its original bounds.

Honor the exact unchanged 0.500 mm source copper-edge minimum plus each
conductor/pad radius, actual foreign/no-net/mechanical copper, source/mutual
holes and every filled-input group. Require complete heartbeat continuity,
matching native/physical reduction below 29, all original 217 groups/items,
exact original 104 findings under the existing two transforms and the full
contact/hole/replay/inverse/orphan/fault/source/visual gates before selection.
Unused access findings, power/ground splits, excessive In2 usage or extra
findings reject the result. No deeper planar signal track or unlisted width
exception. All electrical/current/protection/NTC/timer/default-off, part,
return/timing/thermal/HDI/stack/process/fit and independent Gate A holds remain;
zero opens is unfinished and fabrication prohibited.
