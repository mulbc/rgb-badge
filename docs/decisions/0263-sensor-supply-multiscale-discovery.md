<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0263: Sensor supply multiscale discovery

Date: 2026-11-20
Status: Accepted for bounded read-only complete-join discovery.

ADR0262 stops at100,000 nodes with3,612 global capture candidates, all
Cu-blocked. It does not establish a global routing impossibility. Keep the
same exact frozen source-preserving sensor gateway, source and physical rules.

Use0.005 mm B steps only inside x=56.000–57.800 /y=14.400–15.800 mm,
and global0.025 mm B/In4 steps elsewhere. Global B points may also take
native-clear coarse edges inside the fine region. Connect a fine boundary
point to nearby global coarse points only by explicit ordinary0.20 mm
native-screened physical segments; count their lengths. Do not snap or
invent an electrical contact. Keep every actual source, point/edge/merged
segment and source/new hole check, one additional supported power B/In4
access at most, original ROI and12 mm physical conductor bound. Allow
≤300,000 expanded nodes and the same1.5 discovery heuristic weight.

Every candidate still requires an in-memory refill with all211 original
groups/retained Cu, no orphans, main GND197/VLED38/USB33 and22 matching
opens. Roll back and prove base23 restoration after any failed join. Write
no PCB; a separate full frozen prototype and all source/DRC104/replay/
inverse/fault/visual gates precede adoption. No physical dimension, current,
threshold, bypass/thermal/return/protection/default-off, process/stack/fit/
independent Gate A or fabrication hold changes.
