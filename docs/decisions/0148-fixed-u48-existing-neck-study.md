<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0148: Fixed U48 existing-rule neck study

Date: 2026-11-14
Status: Accepted for read-only native capture discovery; no successor selected.

Continue from the immutable 30-open selected source. Recheck fixed U48.2
DISPLAY_HEARTBEAT and U48.4 HEARTBEAT_FALL_CLK under the unchanged existing
U48 package/net 0.12 mm B.Cu neck rule. Keep SN74LVC1G04DSFR, all six local
lands/nets, position/side/orientation and every source copper item unchanged.
TI SCES214AF / October 2025, page 3, confirms DSF pin 2 A, 3 GND, 4 Y,
6 VCC and 1/5 NC; the manufacturer pin table has been rechecked visually.
No source pin map, no-connect or manufacturer land pattern changes.

Read-only screen 0.025 mm eight-neighbour native B.Cu paths of at most 0.750 mm
actual total neck length, with each segment intersecting the actual U48 courtyard
under the existing rule. Check actual foreign/no-net/mechanical copper, all
board/cutout edges and supported 0.30/0.10 mm B/In4 captures. Where clear,
screen an exact aligned In3/In4 transition at that point. Use ADR 0147's
native-fixture-verified disjoint supported-span model while keeping the prior
0.25 mm overlapping/mechanical/through-hole checks and exact aligned-stack
handling. All subsequent routing must use ordinary 0.20 mm copper.

This screen writes no PCB. Before an implemented prototype, freeze exact
successful path/capture geometry and its full source-preservation scope in a
follow-up paragraph. Every one of the source's 218 groups, every other source
item/part/net/rule/profile and complete successor finding/replay/inverse/orphan/
native-fault/source/visual checks remain required. An unfinished capture is not
a terminal join. No current/rail/protection/NTC/timer/fail-safe/default-off change,
new width exception or fabrication/qualification authority is introduced.
All existing part/electrical/timing/return/thermal/HDI/stack/process/fit and
independent Gate A holds remain; zero opens is unfinished.

The read-only eight-neighbour screen expands 21 points from U48.2 and 108 from
U48.4 and finds no clear supported capture within the stated 0.750 mm neck
bound. No PCB, placement, width exception or rule is changed. This finite
result does not establish that a coordinated relocation is impossible.
