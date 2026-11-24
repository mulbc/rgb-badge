<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0219: Row-zero colour bridge discovery

Date: 2026-11-19
Status: Accepted for read-only native discovery only.

ADR0218 finds no row-zero capture through the freed old R11 corridor. The
whole three-pad gate group's bounded B graph has 870 nodes. At 171 otherwise
B-clear nodes, the sole lower-access obstruction is exact COL_09_R wire
`88aa7fc4-2e84-5bb4-847e-f3ce1119f29a`, ordinary 0.20 mm In4 from
(60.900,3.250) to (78.600,3.250) mm. Native contact audit proves its only
interfaces are original supported In3/In4 vias
`2e107139-e58d-57b0-82af-12b01fac6688` and
`2998cfc2-9f71-5e9c-bcd4-f36219e2185f`; there is no pad, intermediate
branch or zone contact. Retain both original vias and every other source item.

Read-only omit only that exact wire, check supported row-zero B/In4 plus
aligned In3/In4 access at actual reachable B nodes under ADR0218 bounds,
including all source/mutual copper and full-board hole checks. Prefer a
capture directly touching existing PAIR01 gate body copper; an off-pad
capture must include its actual ordinary B lead. Then discover an ordinary
0.20 mm In3 replacement between the two unchanged colour via centres,
mutually clearing the gate access, within x=60.250–79.250 / y=0.750–5.000 mm,
0.050 mm eight-neighbour steps and at most 24 mm total. No new colour via,
source interface removal, unsupported centre/through via, smaller feature,
part move or current/function change is allowed.

If the whole-wire In3 graph fails, separately screen a local In3 hop around
fixed gate access (74.825,3.250) mm. Retain original In4 source-end portions
with exact ordinary replacement fragments to two new supported In3/In4
captures on y=3.250 mm, x=73.750–76.250 mm at 0.050 mm centres. Use a
mutually clear In3 straight/orthogonal detour of at most 4.5 mm within that
x window and y=2.250–4.250 mm. Check all four new supported vias together
against each other and the full source hole policy. Retire no other source
item; preserve both original far interfaces and the same one-wire cohort.

Write no PCB. A gateway/colour path is incomplete until a separately frozen
full original-group restoration and gate join pass matching reduced counts,
exact104 and all source/contact/serialized/replay/inverse/hole/orphan/fault/
visual gates. No source successor, electrical/return/assembly/fit/stack/
process/Gate A or fabrication qualification is selected or relaxed.
