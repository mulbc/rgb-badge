<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0161: Read-only private USB bridge replacement screen

Date: 2026-11-15
Status: Accepted for read-only complete-bridge feasibility only.

The source remains ADR 0153's immutable selected 29-open board. Diagnostic
component analysis identifies a private +3V3_USB bridge consisting only of
old In2/In3 microvias `2d23bdcc-84c4-5006-bbe7-a2365567c1a8` at
(76.151904,30.849096) mm and `387fd145-92e5-58b6-ad44-f0d221c07505` at
(76.951904,30.049096) mm, plus their 0.20 mm In2 segment
`8a099688-0c59-590b-8ee0-2a7e6042b185`. Complete native contact discovery
shows no external pad or track: the only external interfaces are original
In3 source-zone `52361cb6-e447-5a7a-8fab-433f1b57c9c9` polygons 0 and 1.
The signal candidate severs both zone contacts and strands that three-item
branch. Original source contact evidence is retained; no retirement occurs yet.

Screen a complete replacement in memory with only those three items omitted
from obstacle/hole checks. Keep every other source item, part/pose/net/field,
profile/rule and all safety boundaries fixed. Test two 0.50/0.30 mm In2/In3
mechanical buried captures on a 0.050 mm grid within x=74.5–78.5 mm,
y=28.5–31.75 mm. Each must make a robust native annular-area contact with its
respective original connected In3 plane component; record 16 sample points
at radius 0.200 mm, requiring at least four consecutive points in that source
component as a geometric screen, not current-capacity qualification.

Test actual foreign/no-net/mechanical copper on In2/In3, all retained holes
under ADR 0147's bounded supported-span model, mutual capture spacing and
board edges. Seek ordinary 0.20 mm direct/single-corner In2 replacement paths
no longer than 6 mm; check every candidate item mutually. Record finite misses
and successful exact cohorts with original plane/source-copper witnesses.
Do not add/retype any other historical via or use a new centre microvia.

Write no PCB. Before implementation freeze the exact successful capture/path,
complete source contact catalog and independent original interface restoration
scope in a later record. All 217 source groups, every retained item/type, exact
original 104 findings under existing pose transforms, native/physical count,
replay/inverse/orphan/contact/hole/fault/source/visual gates remain mandatory.
A same-count bridge prototype alone does not close an open connection or the
zero-open goal. All 557 existing centre-via and electrical/part/process/stack/
fit/Gate A holds remain until independently disposed of. No current/voltage,
protection/NTC/timer/fail-safe/default-off or fabrication boundary changes.
