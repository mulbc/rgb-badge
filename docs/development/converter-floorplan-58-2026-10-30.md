<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Converter floorplan inventory and rigid VLED packing screen

Date: 2026-10-30. Coupon Rev A is unbuilt; these are calculated/native source
observations, not hardware measurements. No firmware change or fabrication
release applies. The accepted source remains commit `6cc2749`, 58 opens,
SHA-256 `3451177253a021d8706ff818696212afabf539a108f15ef9e5d6921e46435acc`.

## Why the next study needs coordinated rework

The [read-only inventory](../../mechanical/review/converter-floorplan-58-inventory-2026-10-30.json)
uses current exact footprints and pad nets. Every stage part except L1/L2 has
at least one direct same-net contact to retained nonzero copper. There are 16
contacted physical pads in the nine-part 3.3 V stage and 37 in the thirteen-part
VLED stage, including repeated exposed-pad lands. Filled-zone and pad-to-pad
contacts are excluded, so these observations do not establish isolation or
permission to move a component. Paste-only apertures are recorded but excluded
from copper-contact queries.

| Stage/function | Straight pad-centre separation to nearest matching IC pad, mm |
|---|---:|
| L1 terminal 1 / 2 to U36 switching pads | 90.880 / 92.889 |
| C40 / C41 input positive to U36 VIN | 63.355 / 63.034 |
| C42 / C43 output positive to U36 VOUT | 20.490 / 82.637 |
| R81 / R82 feedback junction to U36 FB | 50.933 / 47.455 |
| L2 terminal 1 / 2 to U37 switching pads | 78.944 / 78.892 |
| C44 / C45 input positive to nearest U37 SYS pad | 54.889 / 91.933 |
| C46–C49 output positives to nearest U37 VOUT pad | 42.283 / 38.791 / 35.300 / 31.811 |
| C63 VINA bypass positive to nearest U37 SYS pad | 54.603 |
| R85 / R86 feedback junction to U37 FB | 32.184 / 28.767 |

These are centre-distance planning observations, not routed lengths or pad-edge
lower bounds. The nearest SYS pad is not necessarily the correct local VINA
return/feed choice. A completed net on this draft board does not demonstrate
acceptable converter layout. TI TPS631000 Rev C §7.4 and TPS63020 Rev I §10
require nearby passives and short/wide power paths; feedback and ground-return
placement must be designed together. Their previously rendered layout pages
were re-read from the ignored, hash-identified local references.

## Finite packing result

[ADR 0072](../decisions/0072-coordinated-converter-floorplan-feasibility.md)
bounds a rigid-placement experiment. The historical standalone VLED layout
(`8907f5d51f93211c5d67e74254ece1e54f7e37bc4bd41e7e03c4ecb85d956cec`)
supplies poses only. Historical C50 maps to current C63. Current exact source
parts, pad geometry/nets and package IDs are retained, including the corrected
C44/C45 exact Murata lands. The historical front-side arrangement is mirrored
onto the back side. All other footprints and all accepted copper stay fixed.

The [screen](../../tools/screen-vled-cluster-floorplan.py) samples U37 centres
on a 0.5 mm board-wide grid and four 90° rigid rotations. It uses full convex
courtyard polygons, rejects touching courtyards, and checks surviving poses
against native other-net pad/track/via shapes at 0.20 mm clearance and 0.50 mm
copper-to-edge clearance. Filled zones are excluded from that preliminary
screen. All four rigid arrangements have internally clear courtyards.

| Screen outcome | Poses |
|---|---:|
| Sampled | 60,456 |
| Courtyard outside unchanged board | 23,530 |
| Inside, obstructed by fixed courtyards | 33,529 |
| Courtyard clear | 3,397 |
| Clear courtyards but pad/copper/edge obstruction | 3,396 |
| Passing preliminary courtyard and pad screen | **1** |

The sole surviving pose places U37 at (45.5, 17.5) mm, with zero additional
rotation of the mirrored template; exact integer poses are in the
[screen result](../../mechanical/review/vled-rigid-floorplan-58-2026-10-30.json).
This is finite packing evidence, not impossibility evidence for other
arrangements, rotations or positions, nor acceptance of the old local layout.

A separate native all-pairs check bypasses the screen's spatial bins and SAT:
2,769 courtyard comparisons and 211,585 other-net copper comparisons pass.
Eleven unchanged-package footprints match the native mirrored historical pad
positions/sizes exactly. The two corrected CIN lands intentionally differ from
the obsolete shared template lands. The existing convex predicate has its
previous four host guards and 2,000 native oracle comparisons; no change to
that predicate was made. Inventory and complete packing JSON replays are
byte-identical. Accepted source/template bytes remain unchanged.

## Why the surviving pose is rejected as a source replacement

An ignored, unrouted native witness applies only those thirteen poses to the
accepted source. It retains every track/via, all local pad signatures and zone
outlines/settings, then performs three fills. Each fill reports **76 native
opens**, compared with the accepted 58. The separate pad-cluster calculation
reports **73**; the three-edge difference is itself a failure of the existing
native/physical equality gate. There are **53 pad witnesses losing members of
their previous physical group**, including fixed components outside the stage.
The complete witnesses are in the [native experiment report](../../mechanical/review/vled-rigid-floorplan-witness-2026-10-30.json).

The current net changes include SYS 0 → 6 pad-cluster opens, VLED 8 → 14,
each L2 switching net 1 → 2, and feedback midpoint 0 → 1. No route is added.
Vacated copper can also become disconnected from all pads; those cases are why
an open count based only on pad clusters is insufficient.

Full native DRC with the project-local library available reports **118
findings: the same 104 intrinsic clearances, plus six dangling tracks and eight
dangling vias**. The 104 clearance descriptions and involved pad UUIDs match
the accepted baseline; U37's absolute finding positions move with its unchanged
package. This comparison records experiment evidence and does not relax the
canonical unchanged-DRC gate. An initial DRC invocation without a local library
table also produced 199 lookup warnings; the corrected library-backed run is
the reported 118-finding result.

The [exact rework-scope catalog](../../mechanical/review/vled-floorplan-contact-rework-scope-2026-10-30.json)
partitions the five broken prior groups: SYS has 13 physical pads divided into
seven groups; VLED has 34 divided into seven; each two-pad switching group
and the two-pad feedback midpoint divide into two. Their 15 additional
pad-cluster opens explain 58 → 73, while three padless copper opens explain
73 → 76. The catalog identifies all fourteen newly dangling retained copper
items and their original direct pad contacts. It grants no deletion or
replacement permission. Historical normalized physical keys distinguish pad
identities from the actual current Murata pad coordinates in the inventory.

No pose or copper deletion is adopted. The accepted board remains **58 opens /
104 findings**. A useful next implementation is an explicit converter-stage
rework contract: catalog all old contacts and each proposed copper replacement,
reserve short power/ground/feedback paths, and reconnect the stage without
splitting any accepted external group. The thirteen-part rigid template is a
packing seed only. GRM187/GRM219 exact approval/order-code and effective
capacitance evidence, electrical/thermal/EMI/current capacity, fit/assembly/
process qualification and independent Gate A remain open. Fabrication remains
prohibited.

## Reproduce and evidence

Use KiCad Python on `tools/audit-converter-floorplan.py` and
`tools/screen-vled-cluster-floorplan.py`. Both pin the accepted 58-edge board
hash and accept `--source PATH` for an exact archived copy if a later checkpoint
supersedes it. Outputs are restricted to ignored Rev A build storage. Neither
tool writes PCB source. The ignored native witness and all-pairs scripts,
raw reports/logs, current vendor-reference hashes and public tool fingerprints
are indexed in the [validation record](../../mechanical/review/converter-floorplan-58-validation-2026-10-30.json).
