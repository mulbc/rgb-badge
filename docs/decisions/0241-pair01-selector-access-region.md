<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0241: PAIR01 selector access below the color bus

Date: 2026-11-20
Status: Accepted for bounded read-only geometry/restoration discovery.

Use ADR0239's immutable source, exact F package pose, 62 prospective obsolete
leaf retirements, row/power/gate paths and all source-contact obligations.
ADR0240's two-layer heuristic ends after 16,896 nodes and 2,994 transition
positions (1,122 clear), without restoration. No PCB is written or selected.

Move only the proposed selector access below the retained In1 COL_06_B bus
at y=6.050. To avoid crossing the proposed ground lead on F, independently
screen a new F ground U path from PAIR01.1 (80.925,5.850), via
(80.925,7.200), (82.600,7.200) to the same actual main ground F port
(82.600,5.250), 4.975 mm. This preserves the original ground net/function;
no row-return/current capacity or timing qualification is claimed.

First screen exact selector F/In1 access (81.550,6.550), reached from actual
PAIR01.2 (80.925,5.200) via (81.550,5.200). Require all source/mutual Cu and
source/new holes with the fixed ROW/GATE accesses unchanged. If this exact
point fails, a separately recorded finite sample may vary only selector
X=81.375–82.150 / Y=6.500–6.750 mm, at 0.025 mm steps, with the same two-
segment F template. Do not relax the hole floor or omit any source color Cu.

A clear access may use the already bounded In1/In2 selector search of ADR0240,
now starting at its actual access position and counting its complete F lead
within the unchanged ≤12 mm selector conductor. All retained driver-side Cu
witnesses, source/mutual and full-hole checks remain mandatory. Row/high-side
≤6 mm bounds and every other part/pose/limit remain unchanged. No new centre
or through via is authorized. Write no PCB; only a complete frozen prototype
with every full successor gate may establish a 23-open checkpoint. All current/
protection/default-off, electrical/return/thermal/timing, trial package, assembly/
fit, process/controlled-stack and independent Gate A/fabrication holds persist.
