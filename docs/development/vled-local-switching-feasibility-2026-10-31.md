<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Local U37/L2 switching-node feasibility

Date: 2026-10-31. Coupon Rev A is unbuilt. These are calculated source-geometry
and native CAD checks, not power, thermal, EMI or hardware measurements. No
firmware, current, voltage, protection or display-enable setting is changed.
No pose or copper transaction is selected for the accepted PCB.

[ADR 0074](../decisions/0074-local-vled-switching-node-feasibility.md) tests the
actual switching connections at ADR 0072's clear packing seed. Both variants
place exact TPS63020DSJT U37 at (45.50, 17.50) mm, 0°, and exact
DFE252012P-1R5M=P2 L2 at (49.55, 17.50) mm, −90°, on B.Cu. The pair variant
moves only these two footprints; the stage variant moves all thirteen previously
recorded footprints. Each variant independently checks actual fixed/moved
courtyards and external native pad/copper clearance at 0.20 mm.

## Positive local routing result

Both switching nets can be drawn directly on B.Cu. Each uses three 0.20 mm
segments totalling **3.215685425 mm, calculated**; no switching-node via is added.
The two paths are mutually clear at 0.20 mm, clear every other-net native pad/
track/via, and join the exact three-pad physical groups:

- U37.8 / U37.9 / L2.1, TPS63020's L1 switching node.
- U37.6 / U37.7 / L2.2, TPS63020's L2 switching node.

Both totals are within the unchanged 5 mm exploratory bound. This establishes
local geometry feasibility at this sampled pose. Ordinary 0.20 mm width is a
geometry probe and is not approval of switching-current capacity, loop
inductance, EMI or finished copper. The inductor's distinct temperature-rise
and inductance-drop ratings remain separate qualifications.

TI TPS63020 Rev I page 4 and §10 were re-read, including the rendered pin table.
Control/logic ground is pin 2. Grounded PS/SYNC pin 13 is a mode input and must
not replace the control-ground return in a layout argument. Source pin maps,
local pad geometry and all original component metadata remain unchanged.
The supplied 2021 catalogue still does not qualify the shared converter
capacitor lands/order codes. This experiment adopts no capacitor change.

## Why neither variant is canonical

| Native result | Pair only | Thirteen-part stage |
|---|---:|---:|
| Added switching tracks / vias | 6 / 0 | 6 / 0 |
| Native opens after each of three fills | 63 | 72 |
| Separate physical-pad-cluster opens | 61 | 69 |
| Earlier groups losing members | 2 | 3 |
| Full native DRC findings | 110 | 118 |
| Existing intrinsic clearances | 104 | 104 |
| New dangling tracks / vias | 3 / 3 | 6 / 8 |

The pair case loses members only from the old SYS and VLED groups. All other
prior physical groups survive, including ground. The stage case also splits
the feedback midpoint. Old switching stubs remain at the previous IC location;
retaining every source item leaves padless copper, explaining the differences
between native and physical-pad counts. Neither count satisfies the canonical
58-edge acceptance gate.

Full DRC retains all 104 intrinsic clearance descriptions and involved pad
UUIDs; U37's absolute finding positions move with its unchanged footprint.
There are no additional clearance findings. The new dangling findings from
vacated copper are real failures of the unchanged full gate. This research
comparison does not authorize moving/normalizing arbitrary DRC findings or
suppressing warnings.

The accepted board remains **58 native/physical opens / 104 findings**, SHA-256
`3451177253a021d8706ff818696212afabf539a108f15ef9e5d6921e46435acc`.
Moving the pair is a smaller reconnection problem than moving the entire stage,
but neither the local join nor a lower aggregate score would approve a power
stage with incomplete supplies or unqualified passives/returns.

The next useful feasibility transaction is additive restoration of the pair's
old SYS/VLED groups, followed by an exact policy for copper made obsolete by
the IC move. No old track or via may be silently discarded. Power-path sizing,
capacitor/feedback locality and return topology still need engineering review;
L1/U36 remains unresolved. Full independent pose/contact/DRC/replay/fault/source
and original-orphan evidence must precede any source selection. Electrical,
process/assembly/fit qualification and independent Gate A precede fabrication.

## Reproduce and evidence

Run KiCad Python on `tools/probe-vled-local-switching.py --scope pair --output
hardware/coupon/rev-a/build/vled-switching-2026-10-31/pair/trial.kicad_pcb`, or
use `--scope stage` and a separate ignored output directory. The tool pins the
58-edge source and exact packing seed, preserves every source copper item and
zone definition, and writes only ignored geometry-probe artifacts. Optional
`--source PATH` permits an exact archived source with its paired profile/rules.

An independent native inventory verifies exactly six additions, all old copper,
exact three-pad switching groups, stable three-fill counts/losses and unchanged
profile/rules. New track UUIDs and sorted copper output make both PCB replays
byte-identical. Three real CLI fault cases reject archive-source overwrite,
output outside ignored build storage and the wrong source hash; source bytes
remain unchanged. These safeguards do not make the experimental board releasable.

[Pair probe](../../mechanical/review/vled-local-switching-pair-2026-10-31.json),
[stage probe](../../mechanical/review/vled-local-switching-stage-2026-10-31.json),
[pair full DRC](vled-local-switching-pair-drc-2026-10-31.json),
[stage full DRC](vled-local-switching-stage-drc-2026-10-31.json) and
[validation fingerprints](../../mechanical/review/vled-local-switching-validation-2026-10-31.json)
record exact poses, segments, counts and local evidence. Vendor PDFs, rejected
PCB/profile outputs and raw review artifacts remain uncommitted.
