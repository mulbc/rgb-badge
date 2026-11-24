<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0144: Complete R8 pull-up locality screen

Date: 2026-11-14
Status: Accepted for read-only native geometry discovery; no successor selected.

The selected source remains ADR 0142's immutable 30-open board. ADR 0143's
0.025 mm ROW_GATE_02 search exhausts its bounded graphs. R8's component is
B.Cu-only, while the PAIR03 component reaches the local In4.Cu boundary. No
lower count is selected. Earlier fixed-supply-pad studies in ADRs 0095/0102/
0103 also selected no pose; they do not exclude a complete pull-up relocation.

Read-only screen exact Panasonic ERJ2RKF1001X / 1 kΩ / 1% R8 centres within
x=71.0..73.5, y=6.5..8.25 mm on a 0.05 mm grid at 0/90/180/270 degrees,
retaining B side, all fields/local lands, pad 1 VLED and pad 2 ROW_GATE_02.
Keep PAIR03 NTLJD3119CTBG, every other part/pose/net and all rules fixed.
Check actual courtyards and native foreign/no-net/mechanical copper on each
actual pad layer. Prefer gate-pad positions in the preceding ordinary B.Cu
component and at most 3 mm from PAIR03.5. No narrow-width rule is introduced.

For screening occupancy only, permit omitting original VLED leaf
`eb638639-7d39-5a9a-972d-944b259be009`, the 0.20 mm B.Cu segment from
(72.575,8.5) to (70.25,8.75) mm. Inventory its complete native contacts before
any implementation. Do not save a relocated PCB or retire this source item
from a selected board under this discovery decision. Check prospective ordinary
0.20 mm supply/gate leads and supported adjacent 0.30/0.10 mm captures; an
additional full-span 0.50/0.30 mm PTH proxy may be screened on all six layers
under the existing full-span feasibility policy. No new centre microvia.

The cached Panasonic May 29, 2025 ERJ2R dimension sheet and onsemi NTLJD3119C
Rev 6 / April 2024 top-view pin table have been rechecked visually. The resistor
body is 1.00±0.05 by 0.50±0.05 mm; its existing local lands remain unchanged.
The FET's G2=5, S2=4, D1=6 match the retained source. No manufacturer drawing
instruction is treated as task authority or fabrication approval.

Before a routed prototype, freeze an exact pose, full private-leaf/contact
cohort and replacement geometry in an additional decision paragraph. Restore
R8.1's complete original 35-pad VLED group, every one of the selected 218 live
groups and all original external contacts before counting a new gate join.
Keep the exact resistor value, all rail/current/protection/NTC/timer/default-off
boundaries and full source/replay/orphan/native-fault/visual/exact-finding gates.
Gate/power/transient/assembly/process/fit/stack and independent Gate A holds
remain unresolved; zero opens remains unfinished and fabrication prohibited.
