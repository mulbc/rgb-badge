<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0085: Checked converter routing checkpoint above the frozen 58-edge parent

Date: 2026-11-05
Status: Validated intermediate 52-edge replay; ADR 0088 selects the cumulative 50-edge child.

Continue ADRs 0074–0081/0083 using the corrected ADR 0084 parent PCB SHA-256
817241b48eee1ae6ccc6ff0a99bf89d6c373bde6b45cba687a71e2309115f3d4.
Preserve that PCB, its plan, generator and acceptance checker as the validated
58-edge parent. A separate deterministic child checkpoint makes its exceptional
converter rework explicit without weakening historical copper-retention rules.
Select the child as the current routing study only after all checks pass.

Apply exactly the thirteen poses in the pinned earlier VLED packing seed,
54 enumerated retirements (16 frozen-215 originals and 38 accepted additions),
the 101 previously audited additions and ADR 0083's exact 0.475 mm C49 lead.
Use canonical corrected footprints throughout; no library alias or pad change.
Pin the prior catalog/seed fingerprints, derive the exact combined ledger and
reject any missing/duplicate/extra retirement, addition, pose or field change.
No general cleanup, placement or source-retirement permission is granted.

Require all 246 parent UUID pad groups, all new named converter joins, 52 native
and physical opens, exact full 104 intrinsic findings (only unchanged U37
intra-package coordinates may translate to the checked pose), three stable
fills, byte-identical replay, exact original/accepted origins, profile/structure/
rule retention, schematic contract, visual review and meaningful rejection
cases. Restore the original three waived orphan vias and require only their
same three dangling findings with every selected group retained. The exact
54-item rework is separate from that unchanged orphan waiver.

Keep the new PCB/project/rules project-local and source-controlled. Extend
source-only CI and the routing acceptance entry point to validate the selected
child as well as the unchanged parent. Keep historical probes pinned to their
original inputs; never relabel their results as current source validation.

These are CAD routing acceptance conditions, not current-capacity, power-loop,
thermal, effective-capacitance, feedback-noise, HDI/assembly, RF or fit approval.
Keep every exact MPN/value/current/protection/enable setting and firmware fixed.
L1/U36 locality, further ground/VLED work and independent Gate A remain open.
No fabrication release is authorized.
