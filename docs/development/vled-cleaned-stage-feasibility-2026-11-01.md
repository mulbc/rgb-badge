<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Exact cleanup of the restored full VLED stage

Date: 2026-11-01. **Unselected CAD experiment, not a built/qualified converter
or a canonical routing increment.** [ADR 0081](../decisions/0081-full-stage-obsolete-copper-cleanup-feasibility.md)
bounds discovery and exact removal of newly dangling old copper. The accepted
source remains **58 native/physical opens / 104 intrinsic findings**, SHA-256
`3451177253a021d8706ff818696212afabf539a108f15ef9e5d6921e46435acc`.

## Result

The ignored full-stage candidate now has **52 native / 52 physical-pad opens
and exactly the original 104 intrinsic clearances**, with no dangling findings.
It retains all **246 accepted source groups** and the new switching, input/VINA,
output-capacitor, feedback, EN pull-down and C47 return joins. All thirteen
converter poses stay fixed; all other poses, all 483 identities/local pads/fields,
zone definitions, outline, stack, nets, profiles/rules and electrical settings
remain unchanged. No new source-checker exception or canonical selection is made.

Two exact cleaned replays and all three filled PCB files are byte-identical,
SHA-256 `7c5196b19decc3a4fbaf5724a24aae479a0fdb9c2679706f3cc5f86253992e11`.
Both earlier local and restored phases reproduce their original PCB bytes.

## Bounded discovery, then three exact leaves

The input is the [restored-stage result](vled-restored-stage-feasibility-2026-11-01.md)
at 55 native / 52 physical opens and 118 findings. Its fourteen dangling items
come from vacated stage pads. Frozen/current contact inventories use native net
**names** across separately loaded boards; numeric net codes are board-local.

Eight inspected states remove **49 items** in the five fixed ADR windows and
stop at three long F.Cu SYS leaves outside the permitted rectangles. Every
state retains all earlier and current pad groups and the exact 104 intrinsic
clearance identities. Only newly DRC-dangling, unique retained 58-edge signatures
on the five named nets are eligible. No source duplicate, new route, other net
or out-of-window item is removed implicitly.

Read-only exact contact inventories show that each remaining leaf now touches
only a shared SYS bus. Its frozen contact set additionally contains its own
now-retired F/In1 via. All three are accepted additions absent from the frozen
215-edge source. The documented leaf extension precedes removal of exactly:

| F.Cu SYS track, 0.20 mm | Retained bus at y = 31.80 mm |
| --- | --- |
| (37.55,1.00) → (37.55,31.80) mm | x = 5.30–40.00 mm |
| (92.25,3.65) → (92.25,31.80) mm | x = 84.00–104.55 mm |
| (94.25,0.85) → (94.25,31.80) mm | x = 84.00–104.55 mm |

Both buses and every other copper item survive. The complete **52-item cleanup
cohort comprises 17 tracks and 35 adjacent vias**: sixteen items from the frozen
215-edge source and thirty-six previously accepted additions. The exact ledger
records every signature, UUID, origin, removal round, direct same-net pad/copper
contacts and filled-zone contacts. This is separate from the **two UART
retirements** and the **three original retired orphan vias**.

Relative to the full-stage input, the final exact replay adds the same 95 items
as the restored stage and retires 54 items (52 cleanup plus two UART). Relative
to the accepted 58-edge board it adds 101 items, including the six local switching
tracks, and retires those same 54 items. Final copper count is **18,385**.
No new route, width or current-limit change is included in this cleanup.

## Independent audit and negative evidence

The [exact plan](../../mechanical/review/vled-cleaned-stage-plan-2026-11-01.json)
contains the cleanup multiset, complete contact ledger, boundary stops, leaf
proof and all added geometry. The [validation record](../../mechanical/review/vled-cleaned-stage-validation-2026-11-01.json)
includes independent native counts, all 246 retained groups, exact cardinality
and geometry of all 483 footprints, named converter pin-group witnesses,
structure/profiles, stable fills/replays and original-orphan restoration.

The [full native DRC](vled-cleaned-stage-drc-2026-11-01.json) matches all 104
canonical intrinsic finding descriptions, severity and pad identities. Only
unchanged intra-U37 pad positions translate to the exact recorded seed pose;
all other coordinates, exclusions and severity settings remain exact. This
normalization is confined to the ignored-probe auditor; the canonical checker
is unchanged and grants no new placement/retirement permission.

Nine replay rejection cases cover all three phases' input-overwrite, out-of-build
output and wrong-input guards. Five native negative fixtures reject a missing
C47 return via, restored original VLED copper, unapproved U36 move, altered U37
pad and duplicate footprint. The restored-via fixture is round-trip checked to
ensure it contains the intended original VLED signature before audit.

Restoring the three original +3V3_APP orphan microvias adds **only their three
known dangling-via findings**, giving 104 intrinsic + 3 dangling findings.
Exact restored signatures, all 246 old groups and 52 native/physical opens are
verified. This proof does not create a general orphan or source-retirement rule.

```sh
KPY=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3
"$KPY" tools/probe-vled-local-switching.py --scope stage --output hardware/coupon/rev-a/build/vled-cleaned-replay/input/trial.kicad_pcb
"$KPY" tools/replay-vled-local-stage.py --phase cleaned --source hardware/coupon/rev-a/build/vled-cleaned-replay/input/trial.kicad_pcb --output hardware/coupon/rev-a/build/vled-cleaned-replay/cleaned/trial.kicad_pcb
"$KPY" tools/check-vled-cleaned-stage-probe.py --board hardware/coupon/rev-a/build/vled-cleaned-replay/cleaned/trial.kicad_pcb
```

## Remaining holds

Canonical generator/plan/source-retention/pose policy, full source/fault/checkpoint
and source-only checks must precede any source adoption. The 50-edge target and
L1/U36 locality remain open. Suitable power widths/loops, control/PGND and quiet
feedback returns, exact capacitor lands/order codes/effective capacitance,
electrical/thermal/EMI/process/assembly/fit qualification and independent Gate A
also remain open. The earlier geometric bounds are not current-capacity or
converter-stability approval. No current, protection, hardware interlock,
firmware or fabrication restriction changes. Vendor PDFs and raw PCBs remain
ignored local evidence.
