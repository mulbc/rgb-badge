<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0229: Reversed R6 in the vacated R11 pose

Date: 2026-11-20
Status: Accepted for bounded read-only geometry discovery only.

Use the immutable selected 25-open source. ADR0227/0228 do not produce an
accepted R6 route. Test only exact R6 ERJ2RKF1001X on B at (72.750,4.250) mm /
0 degrees. This explicit reversal puts its VLED pad at (72.250,4.250) and
ROW_GATE_00 pad at (73.250,4.250), both inside the vacated old R11 corridor.
No other part moves or net/identity/package changes. Include the exact six
prospective supply retirements and mandatory stem remainder from ADR0119.

First check actual B courtyards/pads and supported 0.30/0.10 mm B/In4
accesses at both new pads against every source and mutual Cu/hole. Any
via-in-pad, assembly and controlled-stack qualification remains open.
If both pass, independently discover a pull-up supply lead on In4/In3 from
(72.250,4.250) to the actual retained main VLED In4/B via at
(70.250,8.750), uuid 966a8409-91f4-54bf-96fd-3b4c932b2e9c. Use 0.025 mm
planar steps, 0.050 mm supported In3/In4 access grid, x=69.000–74.000 /
y=3.750–9.500 mm, ≤100,000 nodes, ≤8 mm conductor and ≤4 added transitions.
Use the same 0.5 mm transition search penalty, source/mutual Cu/hole checks
and bounded-heuristic interpretation as ADR0228. Include the proposed gate
capture as a foreign-net obstacle. No centre/through transition or row-power
connection is authorized; PAIR01.4 remains open.

Write no PCB. The gate still needs a separate supported route to the front
PAIR01 group and a complete frozen prototype before any reduction can be
claimed. Preserve all 213 original groups/retained attached Cu and the exact
source rules/current/protection/default-off. Electrical/return/thermal,
trial-package, process/stack, optical/fit and Gate A/fabrication holds remain.
