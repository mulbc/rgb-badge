<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0214: Local R11 ground bridge discovery

Date: 2026-11-19
Status: Accepted for read-only native discovery only.

All nine ADR0213 refilled poses split the original main GND group into
194 pads plus isolated PAIR07.1 and PAIR08.1. All retained source copper
remains attached, but these two plane-only contacts are lost. Reject all
nine as successors; preserve the qualified 27-open source unchanged.

On only the exact ADR0212 middle-pose ignored prototype, discover ordinary
0.20 mm B ground restoration to individually witnessed main-GND filled
polygons. Sample 0.050 mm centres within 2.5 mm of each actual isolated pad;
require exact new-track endcap overlap with a polygon physically touched by
retained copper in the actual main group. Screen straight and orthogonal
one-elbow leads, then bounded eight-neighbour 0.050 mm native-screened
polylines within the same window, each at most 3 mm, against all foreign/no-net source copper
and both new supply/gate leads. Allow no new via, source retirement, part
move, smaller feature, or inferred connection to an unwitnessed zone object.

Write no PCB. Discovery alone cannot qualify a return path. A subsequent
exact complete prototype needs frozen bridge geometry plus all original
groups/contact/copper, matching 26 native/physical opens, exact104 and all
source/serialized/replay/inverse/hole/orphan/fault/visual gates before selection.
No electrical/return/thermal/bypass/stack/process/fit/Gate A or fabrication
qualification is inferred or relaxed, and no current/safety boundary changes.
