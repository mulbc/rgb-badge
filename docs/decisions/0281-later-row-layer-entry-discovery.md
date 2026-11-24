<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0281: Later layer entry for the front row output

Date: 2026-11-24
Status: Accepted for bounded RAM-only row restoration discovery.

ADR0280 finds38 native-clear hop vertices but none form a pair within
its1..3 mm window. Clear vertices before the supply cut are near the
first proposed row microvia; later vertices lie more than4 mm along the
path. Do not add a repeated/closely spaced same-span hole.

Keep the exact ADR0279 cell/cohort. Replace only the unselected proposed
row path. Search F only in x76..85/y10..16 mm,0.025 mm/100000 states,
against all actual source and cell copper. Goals are either a real
original ROW04 F conductor or one of the native-clear later path vertices
after the rejected path's maximum-y In1 section. For a later vertex,
use one supported0.30/0.10 mm F/In1 microvia and the exact existing
proposed In1 suffix from that vertex to the actual original ROW04 port.
These new routing vertices are not circuit witnesses; the entire suffix
and actual source contact must be present before counting a join.

Require all source/new Cu and holes, at most12 mm total row conductor
including package strap, and refill at21 matching opens with full18-pad
row, GND197/VLED40/gate4, every original group except explicitly pending
selector, all19256 retained attached source Cu and no orphans. This is
still unselected; only final20 opens/all210 prior groups may advance.
No source item beyond the111 retires, no new centre/through via, no PCB
write. Full qualification/electrical/return/trial-package/process/stack/
fit/independent Gate A boundaries remain; fabrication is prohibited.
