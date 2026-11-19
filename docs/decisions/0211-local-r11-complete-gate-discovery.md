<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0211: Local R11 complete gate discovery

Date: 2026-11-19
Status: Accepted for read-only native discovery only.

ADR0210 finds no clear B/In4 capture in 22,701 fine-phase samples on the
qualified 27-open source. Preserve that source and its exact rules. Inspect
the full ROW_GATE_05 copper/contact graph before considering a different
R11 supply-anchored placement near PAIR06. The source contains 67 gate
copper items, including two local PAIR06 bridges. Discover an exact private
replacement cohort only if its sole outside interfaces are the original
R11.2 and the three PAIR06 gate pads, with no zone/other-net interface.

Read-only screen exact Panasonic ERJ2RKF1001X R11 cardinal poses within
x=76–83 / y=10–18 mm at 0.050 mm centres. Keep all other parts/source
copper fixed during this first screen, except omit original R11 pads from
collision indexing. Require exact local pads, unchanged courtyards and edge
clearance, an actual direct contact to retained main VLED B copper and an
ordinary 0.20 mm B gate path of at most 3 mm to retained PAIR06 gate copper.
After the direct-contact screen, separately permit a supply neck of at most
3 mm to an exact retained main VLED B endpoint, mutually checked against
the full gate lead and both moved pads.
A private-cohort alternative may omit only its graph-proven exact items
in a separately recorded second screen; it cannot alter neighboring nets.
No PCB is written and no original copper is yet authorized for retirement.

A complete ignored prototype requires a separate frozen cohort/pose/route
record. Retain all 215 original physical groups, prove attached retained
copper and complete gate/supply contacts, matching reduced native/physical
opens and exact104, then all source/serialized/replay/inverse/hole/orphan/
fault/visual gates before selection. No part substitution, current/value,
protection/default-off, rule, electrical/thermal/bypass/stack/process/fit,
Gate A or fabrication hold changes are authorized.
