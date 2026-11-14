<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Routing continuation from the 30-open checkpoint

The selected ADR 0142 source remains byte-identical at SHA-256
`90db778d8e44b2c71ab5e1f5d8a1c586ee71c25d46892b1406c4792ac7720abd`:
30 native/physical opens, 218 live groups and the original 104 findings. This
record covers unselected CAD studies under ADRs 0143–0148. No hardware
measurement, manufacturing qualification or fabrication release is claimed.

The [evidence manifest](../../mechanical/review/routing-continuation-30-open-study.json)
records exact ignored raw report hashes. Vendor documents, renderings and
experimental boards remain local and ignored. The four unrelated owner probe
files are untouched.

The exact retained off-grid transition inventory selects no eligible capture.
The fine 0.025 mm ROW_GATE_02 search exhausts both bounded sampled components.
Two distinct complete R8 screens each examine 7,344 poses: the first requires
membership in the PAIR03 gate component and the second allows a supported
layer transfer within 3 mm. Neither finds a clear complete pose. These finite
screens do not establish global infeasibility.

The exact anchored R8 flip and one selector-segment retirement in ADR 0145
create a real ROW_GATE_02 join, but split the original ROW_SEL_15 group by
losing R37.1. The prototype retains only 217 of 218 original groups, has two
additional dangling boundary findings and still has 30 native/physical opens.
It is rejected as a successor. Three stable fills do not repair that loss.
The original-hole restoration attempt exhausts the R37 side and reaches the
300,001-node bound on the other side. The qualified-span retry exhausts
1,229 points from R37 and reaches its 600,001-node bound from PAIR16; it also
adds no copper. Neither result is counted as progress.

The read-only R37 anchored-ground rotation screen evaluates 72 five-degree
orientations. Only the original pose clears; it has no supported capture.
Fresh footprint state per angle is required: repeated incremental rotation
introduced approximately two-nanometre coordinate rounding and was discarded
before the independently checked integer-transform result was recorded.

Nine isolated six-layer KiCad 10.0.6 fixtures use byte-identical source rules
and project settings. Disjoint supported drill spans do not produce native
hole-clearance findings, while mechanical-through/microvia and shared-layer
mechanical-buried/microvia controls do. Same-net overlapping microvia controls
also lack a native hole finding: this does not qualify fabrication spacing.
ADR 0147 therefore retains the prior conservative check for overlapping spans
and permits only a bounded supported-disjoint-span prefilter extension in
ignored searches. No native minimum, rule, legacy via type or production tool
changes. Any future successful candidate needs an independent actual close-pair
hole audit and native policy faults in addition to all ordinary successor gates.

The qualified-span direct-source control batch makes no join. Fixed U48's
existing 0.12 mm neck-rule screen uses actual eight-neighbour Euclidean lengths
up to 0.750 mm, actual courtyard intersection and native foreign copper/hole
checks: 21 points expand from pin 2 and 108 from pin 4, with no clear capture.
No extra width exception is introduced. Complete supply/return and coordinated
inverter-locality studies are separately scoped in ADRs 0149/0150; unfinished
runs are not evidence of a successful successor.

All current, protection, NTC, timer, fail-safe and default-off boundaries remain.
Electrical/part/timing/return/thermal/HDI/stack/process/fit qualification, the
557 historical centre microvias and independent Gate A remain unresolved.
The zero-open objective is unfinished and fabrication remains prohibited.
