<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0248: R9 staggered lower access discovery

Date: 2026-11-20
Status: Accepted for bounded read-only lower-access discovery.

The ADR0247 B-only graph exhausts10,171 nodes without reaching any of the15
aligned lower pairs. This is a bounded result, not a global impossibility.
Keep every source copper item, package and electrical setting unchanged.

Study a staggered lower topology independently: first discover an ordinary
0.20 mm B lead from actual PAIR04 gate pads to only a supported0.30/0.10
B/In4 access. Do not require an In3/In4 microvia at that same coordinate.
A later In4 lead to a separately clear In3/In4 transition would require its
own source/mutual Cu, hole and full-route verification. No mechanical or
upper capture may be inferred from this lower partial path.

Use x=75.000–85.000 /y=6.000–13.000 mm,0.025 mm eight-neighbour B
steps, candidate B/In4 points at0.050 mm,≤100,000 expanded nodes and
≤12 mm B conductor. Use native exact source/pad and merged-segment Cu
checks, and full source/new0.25 mm drill policy for each accepted candidate.
Only exact supported adjacent same-net alignment retains its existing
exception; no new centre or through via is allowed in this stage.

Write no PCB, retire no source item and move no part. Any complete22-open
successor still requires frozen exact original leaves, all211 previous groups
and retained attached Cu, exact104, stable replay/inverse/fault/visual gates.
Current/default-off/protection, timing/return/thermal, trial part, process/
controlled-stack, fit and independent Gate A/fabrication holds persist.
