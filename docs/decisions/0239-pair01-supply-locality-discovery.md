<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0239: PAIR01 supply locality discovery

Date: 2026-11-20
Status: Accepted for exact read-only coordinated placement/route discovery.

Use only the selected 24-open source from ADR0238. Its exact pad-centre
F/In1 VLED access clears, but In1/In2 is blocked by original COL_08_G and
there is no witnessed main-plane contact. No access or PCB is selected.

Independently move only the existing trial PAIR01 package on F to
(80.000,5.200) mm / 180 degrees. Do not flip, substitute or change any field,
numbered net, local package geometry or other part. Independent absolute pad
transform from the current F pose is x'=84.300-y / y'=x-70.900 mm.

Catalogue and prospectively retire exactly the 61 added Cu items frozen in
the accepted PAIR01 front-ground plan plus the one R6-plan F/In1 gate access
at (76.600,4.300). These obsolete package leaves comprise old row strap/lead,
gate F straps, ground access/lead and selector access/path, plus the old gate
F access. No other source Cu or original row/selector interface may retire.
Native source contacts must prove the remaining ground/row/selector/gate
ports and all retained attached Cu survive; keep source groups as full gates.

Screen three new ordinary F package straps (one ROW_00_A, two ROW_GATE_00).
Screen a 0.20 mm F VLED path from new PAIR01.4 (79.075,4.550) via
(78.400,4.550), (78.400,7.800) to actual main VLED F port (79.100,7.800),
4.625 mm. Screen ordinary F GND from new PAIR01.1 (80.925,5.850) to retained
main GND F port (82.600,5.250). Both actual main-port memberships must be
witnessed from source, not inferred from labels.

Screen supported 0.30/0.10 F/In1 accesses at new ROW body (80.000,4.700),
selector PAIR01.2 (80.925,5.200), and gate PAIR01.5 (79.075,5.200).
Screen ordinary In1 ROW from its new body access to original retained row
F/In1 port (74.700,2.599999), ≤6 mm; gate to retained In1/In2 gate access
(76.600,4.300), ≤12 mm; selector to retained actual ROW_SEL_00 In1 via
(77.750,9.650), ≤12 mm. First catalogue exact source/mutual blockers. All
new Cu/holes and actual F courtyards/pads must clear before routing refinement.
No new centre, through or power via is authorized beyond the three specified
F/In1 accesses. Write no PCB; a complete path requires a separate frozen plan
and every full successor gate before selection.

A successful complete successor would preserve all 212 previous groups,
GND197 and all 37 prior main-VLED pads, grow main VLED to38 and have 23
matching native/physical opens. Gate00 four-pad, selector three-pad and row
output eighteen-pad groups must remain intact; zero orphan Cu is required.
Row/high-side conductor study bounds remain ≤6 mm on each side. No current,
protection/default-off or firmware limit changes. All row-power/return/thermal,
timing, trial-package, assembly/optical/fit, via/process/controlled-stack and
independent Gate A/fabrication holds remain open; this is unbuilt CAD discovery.

The exact first pose clears courtyards, all fixed conductors and source main
port witnesses; the direct selector lead is blocked. The proposed gate
small-pad capture is too close to a retained unsupported centre hole at
(78.950,5.050), so reject it. Independently move only that proposed F/In1
gate capture to the existing new gate body centre (80.000,5.700), and use
a direct In1 lead from there to the same retained gate port. Keep all other
poses/paths/source omissions unchanged. Report hole results for each proposed
capture separately. Own-package pad-pad intrinsic pairs are excluded only
from this preliminary pad collision screen; full exact104 DRC normalization
remains mandatory and cannot waive any new via/track external finding.

The body-centre gate access clears holes but is too close to original In1
COL_06_B at y=6.050. The selector pad-centre access also violates the unchanged
hole floor against an unsupported centre at (80.700,5.250). Refine only these
proposed accesses: gate F/In1 at (80.000,5.550), inside its unchanged gate
body pad, and selector F/In1 off-pad at (81.350,5.150), connected by an ordinary
F lead from PAIR01.2. Use the gate's actual new access as its In1 lead start
and selector's off-pad access as its start. Keep all other poses, retirements,
paths and bounds unchanged. Full native source/mutual Cu, three individual
and combined drill audits remain mandatory; no source hole is waived.

The refined pose clears all fixed tracks, pads/courtyards and all three new
accesses/holes; only the straight selector In1 lead is obstructed. Discover
its replacement from (81.350,5.150) to retained selector via (77.750,9.650)
with 0.025 mm eight-neighbour steps, x=76.500–83.000 / y=4.900–10.500 mm,
at most 100,000 nodes and ≤12 mm combined F plus In1 selector conductor.
Include every other fixed proposed item and source Cu as an obstacle; omit
only the rejected prospective straight selector wire. Require native merged-
segment checks. This writes no PCB and does not select a reduced count.
