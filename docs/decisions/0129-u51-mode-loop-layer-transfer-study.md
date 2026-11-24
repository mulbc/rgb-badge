<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0129: Bounded U51 MODE_BOOT_N loop transfer

Date: 2026-11-14
Status: Accepted for ignored feasibility only; no successor selected.

The selected source remains the immutable 33-open board
`14f0c49582063bab84ea685a8cec798011eb4cd66389b085a3a47777180a13ce`.
ADR 0128's 441 poses yield seven geometrically clear poses, but none yields
an ordinary-width local path to a supported capture. A native contact
inventory identifies the retained MODE_BOOT_N B.Cu loop enclosing U51.4.

Permit replacing only these three exact 0.20 mm B.Cu tracks on an ignored copy:

- `9b8a2e6e-3dae-53ca-8d32-998c02d25f88`: (96.8,0.899999)–(96.8,1.9) mm.
- `603b5899-dfa0-5fcc-a29d-866c989fe914`: (96.8,1.9)–(97.05,2.15) mm.
- `2f82fdbb-eae9-5498-a755-08b12a55a5df`: (97.05,2.15)–(103.25,2.15) mm.

Retain their complete original external contacts, including the interior
branch `75433db9-88f5-507c-8474-3d11561bd47f`, not merely the two outer ends.
Freeze the native contact catalog before implementation. Keep U51 and every
other part at its original pose, with exact identities, local lands, fields,
net assignments, rules, profiles and board/zone outlines unchanged. Retain every
other original copper item/via type and every accepted addition outside this
explicit cohort. MODE_BOOT_N's logic/default-off function must not change.

Test ordinary 0.20 mm B/In4 replacement copper within
x=95.8..104.0, y=0.35..3.1 mm, with supported 0.30/0.10 mm B/In4 microvias only.
Screen all actual copper/holes, source interfaces, native board edges and
filled-component preservation. Do not add a centre microvia, narrow a route,
change a current limit or bridge distinct nets. Preserve the complete original
MODE_BOOT_N terminal group and all other original groups before continuation.
Temporary cut/restoration snapshots remain ignored and are never successors.

A completed successor must also establish the actual U51.4–U52.1 connection,
retain all 221 source groups, match native/physical opens below 33, retain
exact original 104 findings and pass complete frozen-ledger/replay/fault/source
and visual checks. All electrical/stack/process/fit/Gate A holds remain; this
study authorizes no fabrication or powered-operation claim.

After removing only the three recorded tracks, an exact supported B/In4 capture
may be added at U51.4's unchanged (97.325,1.750) mm position, provided it clears
all copper/holes and preserves every current group. Reserve that actual output
capture during MODE_BOOT_N restoration so its replacement cannot close the
escape again. This unfinished capture is not a selected join; its dangling
finding must disappear in the completed U51.4–U52.1 successor.

The first generic restoration regains all terminal groups but adds two dangling
findings at the original branch and right-side ends. It also chooses an outer
source lead reaching y=3.299999 mm, outside this study's bounds. That trial is
rejected. Before continuation, replace its new outer lead with a direct B.Cu
branch from original (103.25,2.15) mm to the new MODE_BOOT_N capture at
(102.649999,2.7) mm. Restore the interior branch through a direct B.Cu segment
from original (96.925,2.025) mm to the new capture at (96.6,1.3) mm. Both remain
ordinary 0.20 mm tracks within the original bounds. Require native clearance,
all source contacts/groups and exact DRC; this records no acceptance waiver.
