<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0081: Full-stage obsolete copper cleanup feasibility

Date: 2026-11-01
Status: Ignored bounded simulation only; no canonical retirement.

The ADR 0079/0080 restored-stage replay preserves all 246 accepted and 257
stage-input groups at 55 native / 52 physical opens, with exactly 104 intrinsic
clearances plus fourteen old dangling findings. Its deterministic PCB SHA-256 is
`7604b4807de28c1058afdb2c297df2053690fd83f0861517f813318fb92ca2f7`.
Read-only contact inventory ties each initial dangling item to a vacated stage
pad; native net names, rather than cross-board numeric net codes, identify those
contacts. Both frozen-215 source and previously accepted copper are involved.

Permit a private iterative native dangling-copper simulation only on that
exact restored input. Every removal must be newly reported as dangling by full
native DRC, occur exactly once in the accepted 58-edge copper inventory and be
wholly within one of these fixed rectangles (mm):

- x 2.50–5.75, y 28.75–31.95: former C45 supply access.
- x 35.50–42.00, y 0.50–6.50: former C44/C63 supply access.
- x 53.00–64.50, y 0.50–2.00: former output-capacitor accesses.
- x 57.50–64.25, y 8.50–12.00: former feedback-midpoint accesses.
- x 91.50–96.00, y 0.50–5.00: former U37/switching accesses.

Only +SYS_APP_IN_DRAFT, VLED, VLED_FB_TOP_MID and the two L2 switching nets are
eligible. Record exact signatures, UUIDs, direct same-net pad/copper/filled-zone
contacts and frozen-215 versus accepted-addition origin before each removal.
Stop/report any item outside scope, duplicate signature, new item, non-dangling
item or different net. Use at most ten full-DRC/refill rounds and one hundred
removals; do not expand a boundary automatically. This is discovery of an exact
obsolete cohort, not a general deletion rule.

Preserve every current physical pad group (including all new joins), all 246
accepted and 257 stage-input groups, all remaining source and newly added
copper, all 483 poses/parts/local pads/fields, zones, structure, profiles/rules
and settings. Reject a split or any geometric finding beyond the unchanged
104 intrinsic clearances; old dangling findings may peel into newly dangling
old items under the same strict scope. A long shared-bus leaf outside a window
requires separate exact contact proof and a documented extension before removal.

Canonical source retirement/adoption still requires an independently enforced
exact multiset catalog, frozen-presence/origin and contact proof, native/physical/
full-DRC/pose checks, stable replay/fills, fault/source/original-orphan evidence
and all existing electrical/part/return/process/assembly/fit and Gate A holds.
No current, protection, EN/interlock, firmware, footprint or fabrication change
is selected. No new source-orphan exception follows from this experiment.

## Exact leaf continuation

The bounded simulation stops after 49 removals at 52 native/physical opens and
104 intrinsic clearances plus three out-of-window dangling F.Cu SYS tracks.
Read-only current contacts show each touches only its retained shared bus;
frozen 58-edge contacts additionally include its own now-retired F/In1 via.
All three are accepted additions absent from the frozen 215-edge source.
Permit private removal of exactly these 0.20 mm F.Cu SYS signatures from round-7
SHA-256 `682fd1dbc0ce93bea6524ef1223d037655fe82bee1c92952703839dc9426bdbb`:

- (37.55,1.00) → (37.55,31.80) mm; retain the (5.30,31.80) → (40.00,31.80) bus.
- (92.25,3.65) → (92.25,31.80) mm; retain the (84.00,31.80) → (104.55,31.80) bus.
- (94.25,0.85) → (94.25,31.80) mm; retain that same right bus.

Verify the frozen/current exact contact sets before removal and preserve all
other items, current/accepted/stage groups, geometry and settings. Refill and
check full native DRC and physical/native counts. This exact exception does not
expand the five windows or authorize canonical retirement. Record the complete
52-item cleanup cohort separately from the two ADR 0078 UART retirements.

## Recorded result

The [native evidence](../development/vled-cleaned-stage-feasibility-2026-11-01.md)
records 49 local removals, a boundary stop and three exact leaf removals at
52 native/physical opens / 104 intrinsic clearances. All current/new and 246
earlier groups survive. Two cleaned replays/three fills, independent native
geometry/pin checks, fourteen rejection cases and original-orphan restoration
pass. The complete 52-item private cleanup is not a canonical retirement policy;
source adoption and all standing qualification/Gate A holds remain open.
