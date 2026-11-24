<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0136: Select the complete U51–U52 control-cluster routing checkpoint

Date: 2026-11-14
Status: Accepted for CAD continuity only; fabrication prohibited.

Select `led-control-cluster-routing-trial-114mm`, SHA-256
`1d34fd1e29c8f65d22e7626cc0d2f0307be26b8d5255a0f6e16eb0eac46ceb6b`,
as the successor to the immutable 33-open gauge-supply study. Native and
independent physical counts agree at 32 opens. All 221 original live groups
survive; the actual U51.4/U52.1 DISPLAY_CLEAR_3 group is joined.

Implement ADRs 0129/0134/0135 through the frozen complete
[plan](../../mechanical/review/control-cluster-routing-plan.json): exactly two
U52/C71 poses, eleven source retirements and 59 additions. Preserve all other
483-part identities, fields, local pads, poses, all 19,167 retained source
copper items and native via types, rules/profiles and board/net/zone structure.
Only the three recorded U52 necks use the already existing 0.12 mm package
exception, each shorter than 0.750 mm. Other new tracks are 0.20 mm; adjacent
microvias are 0.30/0.10 mm and centre buried vias are 0.50/0.30 mm.

The first directional route cuts APP supply and is rejected. The reverse route
preserves every group. The initial search snapshot and independent replay
have different cached fill geometry; do not claim they are equivalent. Select
only the fully validated replay with the hash above. Two independent source
reconstructions, each with three stable fills, match that selected board
byte for byte. The inverse reconstruction restores all original source items,
poses, all 221 groups, 33 opens, the exact original 104 findings and empty
integer polygon XOR for all nine filled zones. Its cached vertices differ
in serialization; the original source file remains immutable.

Full DRC retains exactly the original 104 finding payloads. Only coordinates
of the eight U52 pad-item occurrences in its four existing intrinsic findings
follow the frozen pose, checked against an independent integer transform.
No description, UUID/pair, actual clearance, severity or ignored-check list
changes. No other finding transformation or waiver is allowed.

Eighteen native/DRC faults, the full 33-command source workflow, canonical
circuit/pin inventory and native old/new layer review pass. The
[implementation record](../development/control-cluster-routing-2026-11-14.md)
and [checkpoint](../../mechanical/review/control-cluster-routing-checkpoint.json)
retain exact evidence references. `tools/check-control-cluster-routing.sh`
reproduces the complete acceptance checks.

This closes one CAD connection. Zero opens, effective capacitance/part approval,
bypass/return/timing/thermal behaviour, HDI/stack/connector/assembly qualification,
the 557 historical unsupported centre microvias and independent Gate A remain
unresolved. The two new centre transitions are mechanical buried vias, not
additional centre microvias. No current limit, rail domain, protection, NTC,
timer, fail-safe USB control or default-off condition changes. No board has
been fabricated or measured by this work; no fabrication release is authorized.
