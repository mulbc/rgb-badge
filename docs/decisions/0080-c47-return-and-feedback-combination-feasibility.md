<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0080: Exact C47 return and feedback combination feasibility

Date: 2026-11-01
Status: Ignored additive native simulation only; no source adoption.

ADR 0079's first search restores SYS and the inner VLED output cluster but
rejects outer-bank joins because C47.2 loses ground after fill. The rejected
state is not accepted by lowering the retention requirement. Its retained
forward parent has 57 native opens, SHA-256
`5f68623ecc034eee32ec981e62e383d8febee3573a085b198e79797a8519da62`.

A finer ADR 0077 feedback search on the prior exact full-stage replay finds an
ordinary-width B.Cu path of calculated 4.564213562 mm from U37.3 to R86.1,
using eight tracks. It preserves every current group and the full 118-finding
inventory. A read-only native-shape comparison finds no foreign-net collision
between those exact eight tracks and the retained global parent. Permit their
private combination only with exact inventory, three fills, all current-group
retention and full native DRC; retain both policies' lengths and fixed geometry.
Do not generalize this into a feedback-routing or source-retirement exception.

Investigate a short C47.2 ground connection to the existing In2 ground plane,
solely to preserve its return when a later outer VLED join is attempted. Keep
all poses, source parts/pads, all current copper, zones, source/profile/rules,
current/protection/enable and firmware fixed. Permit at most one three-via
adjacent B/In4/In3/In2 stack, diameter/drill 0.30/0.10 mm, within ±1 mm of
C47.2's fixed (48.60,20.35) mm centre. An optional ordinary 0.20 mm B.Cu lead
from that pad must total at most 2 mm, with unchanged 0.20 mm foreign clearance.
Use a finite 0.05 mm position screen; no other ground, net, via, pose or removal
is unlocked. Require actual filled In2 ground contact, no collateral split and
all previous physical pad groups after every fill. Reject an obstructed or
isolating candidate; source group requirements never weaken.

Only after a complete return passes native/full-DRC checks may ADR 0079's
bounded outer VLED restoration repeat in a private descendant. Preserve the
exact feedback and return additions, every other item/group and all previous
bounds. Record ground and supply lengths separately and the combined total
relative to the fixed full-stage seed; do not reset the global 25 mm/net bound
on continuation. A ground-cluster connection is not electrical/EMI or assembly
qualification. The three stacked microvias remain process-unqualified.

No source retirement, canonical move, power/part/return qualification or
fabrication release is selected. All standing exact-component, replay/fault/
source/original-orphan and independent Gate A requirements remain open.

## Recorded result

The [native study](../development/vled-restored-stage-feasibility-2026-11-01.md)
records complete restoration of all 246 accepted groups and retention of all
257 stage-input groups at 55 native / 52 physical opens. The feedback path,
short C47 return and outer VLED join retain the exact 118 input-stage findings.
Deterministic replays/stable fills, independent audit, replay rejection and
original-orphan checks pass. Old dangling power copper and source adoption
remain outside the selected scope; canonical source stays at 58 opens.
