<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Fixed-contact resistor routing study

The selected board remains **28 native and independently counted physical
opens**, with its original 216 groups and exact104 acceptance record unchanged.
No successor is selected. These are CAD geometry/routing experiments on an
unbuilt board; the zero-open goal and all fabrication holds remain unresolved.

ADRs 0199–0202 freeze the exact parts, poses and bounded experiments. The
[machine-readable evidence](../../mechanical/review/fixed-contact-resistor-continuation.json)
records source/evidence hashes, independent audits and complete search
outcomes. Raw boards, native reports and generators remain in the ignored
`hardware/coupon/rev-a/build/row2-routing/` directory.

R71 ERJ2RKF8873X and R21/R11 ERJ2RKF1001X each have an isolated supply pad
1 and a connected pad 2. Twelve cardinal rotations about their fixed pad-2
centres yield five clear poses: three original controls and two alternatives.
R21 at (66.250,5.750) mm / 0 degrees and R11 at (72.250,3.750) mm /
270 degrees retain every original direct gate contact, but neither supply
pad joins main VLED. R71 has no clear alternative. All source copper remains.

A separate 48-pose, 15-degree screen of R21/R11 finds six clear exact-local-pad
poses. Its additional R21 alternatives are 15 and 165 degrees, both about the
same fixed gate pad (66.750,5.750) mm. Eight sampled poses reject native
local-pad identity drift; every sample starts from a fresh original footprint
copy. None of the clear poses has a clear pad-centred supported B/In4 capture.
This does not exclude a capture elsewhere or a different routing topology.

Three complete prepared prototypes retain all 216 original groups, all 483
part identities/fields/local pads, independently calculated global pad
positions, all 19,381 source copper items and via types, immutable board
structure, profiles/rules and the exact original 104 finding payloads. Each
has 28 matching native/physical opens and three stable fill hashes. The
prepared states do not establish a new supply join.

| Supported full-board VLED feed search | Expanded nodes | Result |
| --- | ---: | --- |
| Fixed-pad R21 / 0 degrees | 1,500 | Finite graph exhausted; no join |
| Fixed-pad R11 / 270 degrees | 7,530 | Finite graph exhausted; no join |
| R21 / 15 degrees; original R11 retained | 1,493 | Finite graph exhausted; no join |
| R21 / 165 degrees; original R11 retained | 264 | Finite graph exhausted; no join |

All four output boards are byte-identical to their prepared inputs, adding
no copper. Their 0.050 mm native eight-neighbour graphs retain the original
0.20 mm ordinary width/clearance/edge rules, supported outer microvias and
mechanical centre transitions, full-board hole policy, 12 mm feed and 4 mm
inner-plane limits. These bounded misses prove no global impossibility.

Inverse checks for all three prepared prototypes restore the selected source
byte for byte across three refills each. For non-cardinal poses, restoring
only the angle leaves native rectangle-to-polygon primitive conversion;
the inverse instead restores the complete original footprint and its original
field identifiers. No output is selected merely because its inverse passes.

Evidence hashes, selected source SHA, unchanged-output identities and whitespace
checks pass. The preceding study commit passes all 37 source workflow commands
and both hosted Host software runs. This continuation changes only records;
source PCB/profile bytes and current/resistance/protection/default-off,
electrical/part/thermal/bypass/stack/process/fit/Gate A holds remain unchanged.
Fabrication remains prohibited. Further routing work needs a different
contact-preserving escape or coordinated bus replacement; repeating these
unchanged finite graphs provides no new evidence.
