<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0295: Wider supported row corridor

Date: 2026-11-24
Status: Accepted for bounded RAM-only continuity discovery.

Existing narrow row studies remain rejected or exhausted. Permit a wider
x72..90/y7..22 mm corridor,0.025 mm/100000 states/18 mm new ordinary
0.20 mm conductor, from actual new ROW04 Cu/PADs to actual retained16-pad
ROW04 Cu/PADs, on either exact three-part front-cell pose. The wider
boundary includes real retained source ports formerly outside the ROI.

Use F routing, at most one aligned supported F/In1 plus In1/In2
0.30/0.10 mm pair, then In2 routing, and optionally one supported
0.50/0.30 mm mechanically drilled In2/In3 buried transition and In3
routing. No In1 trace is needed; both actual outer captures are required.
All source/new Cu and full source/mutual0.25 mm drill policy apply, including
no unsupported-source or mechanical aligned-stack exception. No new
centre microvia, through hole, extra source retirement or current change.

Require native ROW18/VLED40/GND197/gate4 and209 original groups with only
selector pending,19256 retained attached source Cu/no orphans/21 opens.
After adding the respective proved real selector route, require all210
original groups and20 matching opens before separately frozen PCB
qualification. No partial source selection or PCB write. The longer
calculated lead does not establish row timing/current/return performance;
original DRC/replay/inverse/fault/visual/electrical/stack/Gate A holds remain.
Fabrication is prohibited.

## Search-budget continuation, same date

Both0.025 mm searches reach the100000-node bound without a join or
completed candidate. Permit a second0.050 mm/300000-node pass in the
same exact corridor/18 mm conductor/transition/source/preservation bounds.
This broadens computation only; no new physical allowance or acceptance
waiver. Frontier distances are geometric diagnostics, not continuity proof.

Both coarse graphs exhaust49156/55920 states without joins. Permit a
300000-node fine0.025 mm pass in the same physical bounds, to resolve
narrow corridors the coarse lattice may miss. No global no-path claim
is inferred from either discretization.
