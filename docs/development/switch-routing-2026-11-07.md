<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Application switch routing: 43-open checkpoint

The zero-open goal remains **in progress**. The selected
[switch routing project](../../hardware/coupon/rev-a/staging/led-switch-routing-trial-114mm.kicad_pro)
has **43 native and independently counted physical opens**, with the exact
unchanged **104 intrinsic DRC findings**. It preserves all 232 physical pad
groups and every copper item in the immutable 44-open ADR 0091 parent.
This is an unbuilt Coupon Rev A CAD study, with no powered hardware or firmware
measurement. Fabrication remains prohibited pending qualification and Gate A.

[ADR 0092](../decisions/0092-full-span-plane-join-feasibility.md), the
[exact plan](../../mechanical/review/switch-routing-plan.json),
[manifest](../../mechanical/review/switch-routing-checkpoint.json) and
[native DRC](switch-routing-drc-2026-11-07.json) bind the result. PCB SHA-256:
`b847f59f8a13a63d8db7a3c2ed2e7efc37239edc03c16fe12adc8b5758b4d524`.
The 44-open parent remains byte-identical at its previous path and SHA.

## Selected geometry

SW2.3–R83.1–U36.5 now form one physical APP_ON_SW_DRAFT group. Two
0.50/0.30 mm full-span plated through vias at SW2.3 and R83.1 reach the In4.Cu
route. The exact CK printed contact numbers, source circuit, resistor values,
all component poses and local pads stay unchanged. The manufacturer source
mapping recorded with the 58-open checkpoint is retained. Distinct VLED and
row permission nets remain distinct; no protection/current/default-off setting
or firmware changes.

The ledger adds 254 ordinary 0.20 mm tracks, fifteen 0.30/0.10 mm adjacent
outer microvias and those two full-span vias. No copper retires and no new
central microvia is introduced. CAD trace centre-line lengths, excluding pad,
via and plane travel, are:

| Net | Added trace length |
|---|---:|
| APP_ON_SW_DRAFT | 147.732843 mm |
| +3V3_APP | 14.889949 mm |
| +BAT_PROTECTED_DRAFT | 0.950000 mm |
| VBUS_CONNECTOR | 0.950000 mm |

The long switch route initially cut supply planes after refill. Explicit
bridges on other layers restore every prior group. Those 0.20 mm supply paths
require current-capacity, voltage-drop, return-path and thermal review;
continuity is not ampacity or electrical qualification. The switch route's
noise immunity, via-in-pad fill/cap/wicking, controlled stack and all historical
557 centre microvias also remain unresolved manufacturing/electrical work.

## Validation and rejected trials

- Exact native copper/footprint/field/local-pad/net/pose/profile/outline/zone
  structure, all 232 previous groups, 483 footprints and 2,092 physical pads.
- Three stable fills per generation and two independent byte-identical replays;
  the selected source matches both. Native and physical counts both equal 43.
- Exact 104-finding DRC comparison. Restoring the original three orphan vias
  leaves all live groups identical and adds only their same three warnings.
- Seven isolated faults rejected, including real switch and battery-bridge
  disconnections, full-span retyping/shrinking, narrowing, changed converter
  default and removal of previously accepted IREF copper.
- Source contract passes for 465 common components and 1,718 logical pins.
  All 25 source-only workflow commands pass locally and are recorded in the manifest; these are
  local evidence, not a claim about remote CI.
- Native bottom-copper SVG close-up inspected at the supply bridges. Raw views,
  searches, fills and fault logs remain ignored under `build/switch-routing/`
  and `build/zero-open-routing/`.

Weighted finite searches reached their node bounds on long routes. An
unweighted search found the switch route, and verified supply-plane components
then supported local bridge restoration. A lower count alone was insufficient:
all prior groups and the explicit switch witnesses had to survive refill.

An early experimental bridge builder omitted no-net pads and set via type
after its layer pair. Native DRC rejected its apparent 43-open result. The
accepted ledger includes every-pad/hole clearance screening and correctly
specified adjacent spans; full native DRC and deterministic replay independently
verify the saved result. No rejected full-span microvia or colliding bridge is
selected. Remaining opens are inventoried by net in the manifest.
