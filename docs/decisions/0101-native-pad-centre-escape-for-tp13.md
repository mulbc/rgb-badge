<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0101: Exact pad-centre escape and local TP13 inner lead

Date: 2026-11-07
Status: Selected as a validated 37-open CAD successor; fabrication prohibited.

The existing U55.7 VLED_ENABLE_CANDIDATE land permits the ordinary
0.30/0.10 mm B.Cu/In4.Cu microvia at its exact (26.250,20.875) mm centre.
Its half-grid Y coordinate is significant at the neighbouring pin clearances;
do not silently round the capture to the 0.05 mm routing grid.

Study this exact source capture and an adjacent B.Cu/In4.Cu capture inside
TP13's unchanged 1.0 mm land, with an ordinary 0.20 mm In4.Cu connection.
TP13 may move within the ADR 0098 locality region while retaining all exact
fields, numbered net, circular copper/mask/paste, B.Cu and orientation.
The complete added B.Cu/In4.Cu trace length remains at most 5 mm, excluding
via travel. This explicitly extends ADR 0098's B.Cu-only lead experiment;
no other part moves, and no source copper is retired or altered.

Require prior TP13 isolation/no-copper-contact proof, all existing copper and
live pad groups, an actual U55.7–TP13.1 join, exact unchanged 104 native
findings, stable replay/fills, source contracts, isolated faults and visual
review before selection. A partial seed or dangling via is never selected or
counted as a join. No narrowing, skipped span or central via is authorized.

SN74LVC2G08DCUR, all source/sink nets, window/current thresholds, hardware
permission/defaults, cell/charger protection and firmware remain unchanged.
Via-in-pad assembly/process, probe access/loading, signal/return, controlled
stack, fit and independent Gate A remain unqualified; fabrication is held.

Select TP13 at (23.250,23.300) mm with the exact source capture and two
0.30/0.10 mm B.Cu/In4.Cu microvias. One 0.20 mm In4.Cu track calculates to
3.857541315 mm. All 226 preceding groups and 223 additions survive with no
additional retirement. Native/physical 37 opens, exact unchanged 104 findings,
identical replay/fills, all 27 source commands, 30 fault guards and separate
native layer views pass. See the
[implementation record](../development/native-tp13-escape-2026-11-07.md).
