<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# C32 ground escape and local colour restoration feasibility

Reviewed 2026-10-31; experiments began 2026-10-30. Coupon Rev A is unbuilt.
These are native source-geometry observations and calculated lengths, not hardware
measurements. Firmware and all electrical settings are unchanged. No new source
track retirement, narrow route, pose or fabrication output is selected.

The accepted input is the 58-edge PCB at `fc54584`, SHA-256
`3451177253a021d8706ff818696212afabf539a108f15ef9e5d6921e46435acc`.
Its ground groups have 193, two, one and one physical pads: the main group,
U38.3/U52.3, C32.2 and PAIR01.1. VLED still has eight open edges.
[ADR 0073](../decisions/0073-c32-staggered-ground-escape-feasibility.md)
bounds the ignored C32 work; no broader deletion exception follows.

The corrected exact C32 footprint remains fixed. An eight-direction 0.025 mm
native search reaches 7,797 B.Cu cells without a legal adjacent via. A
co-located complete ground stack has multiple obstructions. Screening only the
first B/In4 transition exposes fourteen sites obstructed solely by the original
COL_03_B In4 track and twelve solely by original COL_04_R. This changes the
next experiment: a staggered path can move on an inner layer before descending
again, instead of requiring all vias at one XY position.

Removing just COL_03_B reaches 285 In4 cells; removing just COL_04_R reaches
325. Neither reaches main ground. The second-layer audit identifies original
COL_01_G on In3 as the sole obstruction at 31 sampled sites in the red-track
vacancy. Exact signatures and source-derived original-layer interfaces remain
part of the future replacement requirement. TI TLC59581 Rev A pages 4–5 were
rendered/re-read; U1 output pins 12/19/20 and their constant-current roles stay
unchanged. The PDF is local only, hash-indexed with the evidence.

## A partial ground route does not pass the transaction gate

Temporarily removing COL_04_R and COL_01_G lets a full-width ground route reach
the existing main group. Its aggregate track length calculates to
**7.614823228 mm**, using four adjacent microvias. Native and separate pad-cluster
counts both become **59**, compared with accepted 58. An independent saved-board
inventory confirms the main ground group grows **193 → 194** and includes C32.
It also proves exactly **two original colour groups are split**. Every other
source copper item, pose, local pad signature and zone outline/setting survives.
See the [partial-board audit](../../mechanical/review/c32-ground-partial-audit-2026-10-31.json).

This is rejected. The preliminary route starts at a C32 pad corner; subsequent
prefix trials place its full-width end cap 0.10 mm inside both adjacent land
edges. Neither version becomes canonical. There is no claim that the long
return or its local bypass behavior is electrically qualified.

## Restoration screens

Native colour A* screens retain 0.20 mm tracks, adjacent 0.30/0.10 mm microvias,
original-layer endpoint/direct contacts, each source segment's x range ±1 mm,
y excursion ±1 mm and aggregate track length at most original plus 2 mm.
They try adjacent inner layers first, then all six copper layers. Screen shape
comparisons use the existing 10 nm numerical tolerance; final unchanged 0.20 mm
DRC remains mandatory and is never waived.

The first two greedy restoration orders fail with the complete ground route
present. Further experiments retain only the initial ground escape, restoring
colour first so that the long return can be routed afterward:

| Prefix restoration class | Site/order cases | Complete transaction |
|---|---:|---:|
| Two removed colour tracks; four selected via sites | 8 | 0 |
| Three scoped colour tracks; selected sites/orders | 16 | 0 |
| Three tracks; second via offset along In4 | 27 | 0 |

Some individual colour paths exist, including simple reinstatement of an
original blue segment. No case restores every colour around the ground escape.
The staggered cases use first-via sites from the reachable C32 region and a
second In4/In3 via at x = 83.65, 83.85 or 84.05 mm, y = 10.30 mm, with the
intervening full-width In4 conductor. All 51 listed case logs terminate without
script assertions; none reaches a complete transaction's refill/DRC gate.

The [finite-screen record](../../mechanical/review/c32-ground-feasibility-2026-10-31.json)
indexes exact rejected case logs, partial paths, local raw scripts/boards and
source/vendor fingerprints. The raw experiments remain under ignored build
storage. These are bounded greedy/grid results, not proof that a different
joint route topology, placement, between-grid path or separately scoped rework
is impossible. Do not infer global impossibility or retire extra copper from
these failures.

The accepted source remains **58 native/physical opens / 104 intrinsic findings**,
with all source bytes intact. A future change still needs the exact independent
replacement/contact policy, every old external group restored, lower counts,
full unchanged DRC, stable fills/replay, fault/source checks and original-orphan
restoration. Converter locality and the remaining ground/VLED joins remain open.
Return/current/timing/EMI, electrical/process/assembly/fit qualification and
independent Gate A precede fabrication.
