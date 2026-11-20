<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0147: Native drill-span clearance semantics study

Date: 2026-11-14
Status: Accepted for isolated native fixtures only; no routing policy or source change.

The selected source remains ADR 0142's immutable 30-open board. R37's rejected
capture includes existing COL_12_R microvia `4646eaa0-52e6-56ff-b61a-15fd00e1dad5`
at (67.475,7.075) mm on F/In1, while the proposed capture is on In4/B. These
actual layer spans do not overlap. The current exploratory search nevertheless
applies its two-dimensional 0.25 mm hole-spacing check to every hole on every
layer. Its conservatism may exclude native-valid captures.

Before changing any search assumption, create ignored minimal six-layer native
fixtures using the selected source's unchanged project/rule profile. Compare
opposite outer microvias, overlapping/shared-layer microvias, exact aligned
adjacent stacks and through-hole interactions. Include unsafe overlapping and
safe separated controls. Keep native minimum hole clearance at 0.25 mm,
microvias at 0.30/0.10 mm and through vias at 0.50/0.30 mm. Record complete
native results and exact inputs. Fixture dangling items are diagnostic artifacts,
not accepted project findings or manufactured objects.

Do not alter the selected PCB, its profile/rules, part/pose/copper/net inventory,
existing drill types, current limits, protections or default-off circuits.
This decision authorizes no new capture in a routing candidate. A later exact
scope and native evidence must justify any search-model extension; complete
source-group/full-finding/replay/orphan/fault/source/visual gates remain required.
Native CAD acceptance does not qualify fabrication spacing or the controlled
HDI stack. The 557 historical centre microvias, all electrical/process/fit/Gate A
holds, fabrication prohibition and unfinished zero-open goal remain unchanged.

The six native fixtures preserve the exact source profile/rule hashes. Native
DRC reports no hole violation for opposite F/In1 and In4/B microvias at 0.20 mm
centre spacing. The mechanical-through/microvia control does report
`hole_to_hole`; separated controls and the aligned adjacent stack do not.
Same-net microvia controls also produce no hole finding, so native silence
alone must not be interpreted as fabrication qualification or justify dropping
the existing conservative checks for overlapping microvia spans.

Permit an ignored ROW_GATE_02 additive search directly from the selected
30-open source with only this narrowly bounded search-model extension: skip the
two-dimensional drill comparison between two 0.30/0.10 mm microvias only when
both actual spans are supported outer adjacent pairs (F/In1, In1/In2,
In3/In4, In4/B) and their copper-layer sets are disjoint. Preserve the prior
0.25 mm checks for all overlapping spans, every mechanical/through/NPTH hole
and all other cases; keep the existing exact aligned-stack exception. Continue
checking foreign copper on every actual layer. Do not change any native rule,
profile, part/pose/source copper/net or current/safety boundary. New tracks
remain 0.20 mm; centre transitions remain mechanical 0.50/0.30 mm buried vias.

Record every skipped close pair and its actual native layer spans in an
independent completed-candidate hole audit. An accepted successor still needs
all 218 original groups, actual native/physical reduction below 30, the exact
original 104 findings, a complete additive ledger, stable independent replay,
source-removal/orphan proof, native source and hole-policy faults, source checks
and visual review. No fabrication-spacing or controlled-stack qualification is
inferred from these CAD fixtures. All independent Gate A and fabrication holds
remain unchanged; no prototype is selected by this search permission.

Three additional native fixtures show no hole violation between the supported
In2/In3 0.50/0.30 mm mechanical buried via and either opposite outer microvia
span at 0.20 mm centre spacing. The shared-In2 buried/microvia control does
report `hole_to_hole`, confirming that the same unchanged rule is active for
physically overlapping layer spans. Nine complete native fixture reports are
retained; this is CAD evidence, not fabrication qualification.

Extend the same ignored ROW_GATE_02 search permission only to disjoint pairs
whose declared types/sizes are either supported outer 0.30/0.10 mm microvias
or the supported In2/In3 0.50/0.30 mm mechanical buried via. Compute actual
closed copper-layer spans before skipping a two-dimensional comparison. Keep
the full prior 0.25 mm check for overlapping spans, unsupported legacy types,
all through/NPTH holes and every other case. Preserve foreign-copper tests,
exact aligned-stack handling, profiles/rules, parts/source items and all full
successor requirements. Record actual close disjoint pairs independently.
No native rule or manufacturing clearance is relaxed or certified.

The qualified-span ROW_GATE_02 search exhausts both sampled components and
selects no join. Extend only the same ignored additive search method to the
remaining nets already inventoried in ADR 0143: DISPLAY_CLEAR_OK, ESP_EN,
HEARTBEAT_SEEN, CHARGER_EN2, CHARGER_TS, LED_GCLK, LED_LAT, LED_SCLK,
ROW_GATE_00/03/04/06/07, DISPLAY_HEARTBEAT and HEARTBEAT_FALL_CLK. Start directly
from the selected immutable 30-open board. Keep every part/pose/source copper,
all 218 groups, every profile/native rule and safety boundary fixed. All new
tracks remain 0.20 mm; no local-width exception or new centre microvia.
Temporary cut-selector/R8/R37 experiments are not inputs to this search.
No lower count is selected without complete native/finding/hole/source/replay/
inverse/orphan/fault/visual checks and the unchanged fabrication/qualification holds.

The direct selected-source control batch adds no copper and retains the exact
selected bytes. Permit the same qualified-span method on ADR 0145's exact
ignored selector-cut/R8 prototype (SHA-256
`6cf68a2a7303fdeac7d169a0a7e6de2a0f05307bfececfc887075ec193dc8bcc`)
only to restore ROW_SEL_15. Preserve that decision's exact single retirement,
R8 anchored pose and bounded gate copper, every retained item/external branch,
and its 120 mm selector-length ceiling. The temporary prototype lacks one
original group and has two declared dangling boundary findings; no lower count
is accepted unless all 218 selected-source groups, every boundary contact and
the exact original 104 findings are restored. The per-search input-group guard
is necessary but insufficient: independently compare against the immutable
30-open selected board before considering any successor. All other qualified
span restrictions and full successor requirements above remain in force.
