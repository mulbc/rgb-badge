<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Dual-converter placement and routing goal closure

Date: 2026-11-05. Coupon Rev A is unbuilt. This closes the recorded local
converter feasibility/routing-study goal, not the entire board or fabrication
release. Firmware behavior, current limits, protection and enable settings do
not change. All evidence here is native CAD/source validation, not bench data
or independent Gate A review.

The selected current routing study is
[`led-converter-routing-trial-114mm.kicad_pcb`](../../hardware/coupon/rev-a/staging/led-converter-routing-trial-114mm.kicad_pcb),
SHA-256 `5e07fb866cc059de670e34102045d9dfd88c88f101355fcdbb27253c0ae26e43`.
It has **50 native/physical opens** and exactly **104 unchanged intrinsic
clearance findings**. It preserves all **246 physical pad groups** from the
immutable corrected 58-edge parent. No component or package is substituted.

## Local converter result

| Exact parts / numbered node | Calculated B.Cu switching path |
| --- | ---: |
| TPS631000DRLR U36.3 → DFE252012P-1R0M=P2 L1.1 | 2.452998 mm |
| U36.2 → L1.2 | 2.238170 mm |
| TPS63020DSJT U37.8/9 → DFE252012P-1R5M=P2 L2.1 | 3.215685 mm |
| U37.6/7 → L2.2 | 3.215685 mm |

All switching paths use ordinary 0.20 mm B.Cu tracks, no switching-node vias,
and stay within the unchanged 5 mm study bound. Native numbered-pin witnesses
check all four nodes separately from aggregate counts. Width here is a geometric
study parameter, not a qualified power-current rating.

U36 moves to (108.75,12.50) mm, 180°, and L1 to (111.65,12.75) mm, 90°,
on B.Cu. The earlier regional rectangle excluded this position. The broader
[whole-coupon finite screen](../../mechanical/review/u36-l1-global-review-2026-11-05.json)
samples 2,541,840 cardinal/grid templates and finds 28,514 clear short-node
templates. The nearest retained template displaces U36 by 8.980013 mm. A clear
template alone is not acceptance: its first filled probe loses the two old SYS/
output connections, exactly offsetting its two new local switching joins.

The bounded restoration reconnects U36.4 to its former SYS group and U36.1 to
its former application-3.3-V group. Added restoration-track lengths calculate
to 6.374988 and 2.520919 mm, each below 25 mm. Every prior/current group survives
refill. The resulting count reaches 50; no lost old group is hidden by that
aggregate result.

U37/L2 and eleven associated passives adopt the previously audited thirteen-part
VLED packing seed. Their local input/output/feedback/enable/ground joins and
global supply connections are enforced by named pad witnesses, including every
physical U37 exposed-ground land. The former 52-edge VLED result remains
reproducible with `--stage vled52`; its exact frozen plan is
[`converter-vled-52-checkpoint.json`](../../mechanical/review/converter-vled-52-checkpoint.json).

## Exact copper and interface policy

[ADRs 0085](../decisions/0085-selected-converter-routing-checkpoint.md),
[0086](../decisions/0086-global-u36-l1-pair-feasibility.md),
[0087](../decisions/0087-u36-pair-restoration-feasibility.md) and
[0088](../decisions/0088-dual-converter-routing-selection.md) precede their
implementation. The cumulative frozen ledger permits exactly 15 poses,
65 retirements (20 frozen-215 originals and 45 accepted additions), and
134 additions. All other copper, canonical pad geometry/nets/fields, poses,
zones, stack, profiles and rules remain fixed. The 58-edge parent, its plan,
generator and retention gate are unchanged.

The U36 cleanup first stops at its configured boundary. A long old SYS F.Cu
branch is now used partway along its length by the new supply route. It is
**trimmed, not deleted**: retain (103.865,13.037450) → (103.865,31.800000) mm
and its bottom shared bus, preserving the new endpoint and side track/via
interfaces. The 18.762550 mm retained tail occupies only old copper. It is
distinct from the 6.374988 mm additive SYS restoration path; the full inventory
and lengths record both, without resetting the search bound or concealing a
branch retirement.

The selected ledger, contact/origin records, named routes and search metadata
are in the [plan](../../mechanical/review/converter-routing-checkpoint-plan.json).
The [portable selector](../../mechanical/review/converter-routing-checkpoint.json)
pins the selected board, plan, profile/rules and tools. An isolated
[policy](../../tools/converter_checkpoint.py),
[generator](../../tools/generate-converter-checkpoint.py) and
[native checker](../../tools/check-converter-checkpoint.py) enforce the child
without weakening the earlier parent gate. Persistent pad UUID groups avoid
dependence on corrected-coordinate identity normalization.

Three fills and a second independent generation produce identical selected
PCB bytes. The intermediate 52-edge replay also retains its exact original
SHA-256 `db9643801c165fb25c8078816b5cb0a4223c4ddaffa516aae1775392b3a65ded`.
Native copper/body/courtyard windows for both converter pairs were visually
reviewed; schematic reconciliation retains the same 465 shared components and
1,718 logical pins. Full DRC retains exactly the original intrinsic findings.
Restoring the original three waived orphan vias preserves every selected group
and 50 opens, adding only their same three exact dangling-via warnings (107
findings total). The 65-item rework does not create a new orphan waiver.

Eight isolated native faults reject a missing application switching lead,
missing C49 contact lead, restored retired via, wrong IC pose, oversized
capacitor pad, extra copper retirement, wrong numbered inductor net and false
origin ledger. The complete acceptance entry point runs both the unchanged
parent and selected child gates. Source-only CI checks the selected child in
addition to the parent. Detailed counts and fingerprints are in the
[validation manifest](../../mechanical/review/dual-converter-validation-2026-11-05.json).

## Remaining ground/VLED continuation and limits

The final native group inventory provides the next routing frontier: ground has
one 193-pad main group, an isolated U38.3/U52.3 pair, C32.2 and PAIR01.1.
VLED has one 35-pad main group and seven isolated PAIR03.4/R21.1/PAIR05.4/
PAIR09.4/R11.1/PAIR07.4/PAIR01.4 pads. The inventory is recorded with exact
locations/UUID-derived grouping in the validation evidence; no extra join is
claimed. Existing ground/VLED groups all survive the selected converter work.

The local feasibility goal and the separate 50-edge planning target are met.
**Fifty opens remain**, as do the 104 intrinsic findings. Application bypass/
feedback locality, ordinary-width power-path current/thermal qualification,
remaining control/ground connections, exact orderable capacitor suffixes,
combined electrical derating, USB/RF/enclosure/HDI/stencil/assembly and independent
Gate A remain open. None is waived by routing counts or this goal closure.
Fabrication is prohibited.

Raw ignored evidence is under
`hardware/coupon/rev-a/build/converter-checkpoint-2026-11-05/` and
`hardware/coupon/rev-a/build/converter-checkpoint-review/`. Reproduce with
`./tools/check-routing-progress.sh`; generate the current or intermediate child
into a fresh ignored build path with KiCad Python and
`tools/generate-converter-checkpoint.py --output PATH [--stage vled52]`.
Vendor PDFs, native review renders and local build/manufacturing output remain
outside Git.
