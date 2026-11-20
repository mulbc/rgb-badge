<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0271: Fixed remaining LED pair supply discovery

Date: 2026-11-20
Status: Accepted for bounded read-only additive route discovery.

Continue from selected22-open source03e74104c51811a1. Independently test
actual PAIR05.4,PAIR07.4,PAIR09.4 against real original main VLED39
conductors, with all483 parts/all19367 source Cu fixed. Use ordinary
0.20 mm B/In4/In3 tracks and at most two supported0.30/0.10 mm adjacent
microvias per route, monotonic B/In4 then In4/In3, source and mutual
hole checks,0.025 mm grid,25 mm conductor/400000 states/1.5 heuristic.
Each search uses x70..88 and respectively y7..17,11..21,15..25 mm.
Each independent full join must preserve every210 original group and
attached source Cu, GND197/USB32, zero orphans, main VLED40 and21
matching native/physical opens. No route is a selected PCB.

If all three succeed, an in-memory combined trial may test all210
original groups/all19367 attached source Cu,19 matching opens/main
VLED42 and all new mutual/source hole clearances. Every new conductor
must be attached; no substitute pad witnesses or source retirements.
No PCB may be written until a separate exact combined prototype ADR.
All trial-package/electrical/current/return/thermal/stack/process/fit and
independent Gate A holds remain; fabrication is prohibited.
