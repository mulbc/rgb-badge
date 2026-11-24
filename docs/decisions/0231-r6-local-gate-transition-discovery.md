<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0231: R6 local supported gate transition discovery

Date: 2026-11-20
Status: Accepted for bounded read-only geometry discovery only.

Use the exact selected 25-open source and ADR0230's R6 B (75.750,3.750) /
0-degree pose. Its first combined route is rejected: the direct In3 power
lead and gate transition collide with retained row/color copper and a legacy
hole. Keep those exact negative results; write no PCB.

Independently screen gate B lead from R6.2 (76.250,3.750) to (76.650,4.550),
aligned supported B/In4 and In3/In4 accesses there, and the previously clear
aligned supported In1/In2 plus F/In1 accesses at actual PAIR01 gate body
(76.600,4.300). Discover a mechanical buried In2/In3 0.50/0.30 mm centre on
a 0.050 mm grid over x=74.500–78.000 / y=2.500–5.500 mm. Each candidate
must clear source/mutual Cu and full source/new drill rules. Require ordinary
0.20 mm direct In3 lead to the lower capture and direct In2 lead to the top
capture, with total gate conductor ≤12 mm. No source Cu may be omitted
except the exact six R6 supply items (remote from this gate screen); include
all actually proposed new gate objects in mutual screening. Retain all part
courtyards/pads and capture identities. No centre/micro coincident drilling
or new through via is permitted.

Separately screen supported B/In4 plus In3/In4 pull-up accesses at
(75.250,4.250), with the 0.50 mm B lead from R6.1, but do not assume supply
restoration. The full supply remains a separate prerequisite before any
prototype/selection or open-count reduction can be claimed. All original
213 groups and attached Cu, electrical/timing/return/thermal, current/default-off,
trial-package, assembly/fit, process/controlled-stack and Gate A holds persist.

The 4,331-point centre screen yields ten source/mutual-Cu/drill-clear gate
centres, rejecting 4,291 for Cu and 30 for holes. Every fixed gate item and
R6 pad/courtyard clears. The separate proposed power In3/In4 access at
(75.250,4.250) is blocked by COL_06_B and is rejected; keep only its clear
B/In4 root and B lead in the next screen.

Read-only fix one gate centre at (77.100,4.350) with its exact two direct
leads and all four supported gate microvias. Include that complete gate as
foreign-net obstacles for a two-layer In4/In3 power search from the retained
power root (75.250,4.250). Targets are actual original main VLED In3 via
(78.850,6.800) or In4 via (70.250,8.750). Use x=70.000–79.500 /
y=3.750–9.500 mm, 0.025 mm planar steps, 0.050 mm access grid, ≤100,000
nodes, ≤4 added supported In3/In4 transitions, and ≤8 mm combined B plus
inner conductor. Use the established 0.5 mm search penalty and exact native
source/mutual Cu/hole checks. All fixed gate and new power holes must pass
together. No unsupported centre or through via, new source omission, row-power
connection or PCB write is authorized. A complete path still requires a frozen
prototype and every full successor gate before any selection.

With that fixed gate, the power heuristic ends after 2,516 nodes and 662
transition positions, none clear. The gate occupies the old usable In3/In4
crossing. Read-only test relocating only the proposed lower gate capture
(B/In4 + In3/In4) over x=76.800–78.000 / y=4.200–5.200 mm at 0.050 mm
steps. Keep gate centre (77.100,4.350), top captures and direct In2 lead fixed;
use a direct B lead from R6.2 and direct In3 lead to the gate centre.

Reserve the old (76.650,4.550) In3/In4 crossing for VLED, with B lead
R6.1→(75.250,4.250), supported B/In4 access there and ordinary In4 via
(76.650,4.250) to that crossing. The proposed rejected In3/In4 power access
at (75.250,4.250) is omitted. Do not add the blocked direct In3 power lead.
All fixed/proposed gate and power items must clear source/mutual Cu/holes,
with no source omissions beyond the same exact six R6 supply items. This
remains read-only; power restoration and every full successor gate are still
prerequisites before writing/selecting a candidate PCB.
