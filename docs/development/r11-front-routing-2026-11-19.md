<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Front-side R11 supply join: 27 to 26 opens

The selected unbuilt CAD source is
`hardware/coupon/rev-a/staging/led-r11-front-routing-trial-114mm.kicad_pcb`.
It has **26 native and independently counted physical open connections**,
all 215 preceding physical pad groups preserved and the exact original
104 design-rule finding payloads. All 196 main ground pads remain connected.
The zero-open goal remains unfinished. Fabrication is prohibited.

The [exact plan](../../mechanical/review/r11-front-routing-plan.json),
[checkpoint](../../mechanical/review/r11-front-routing-checkpoint.json) and
[continuation evidence](../../mechanical/review/r11-placement-continuation.json)
record the frozen change and ignored raw evidence hashes. ADR0217 selects
this successor; ADRs0210–0216 record the preceding bounded discoveries and
rejected bottom-side alternatives. The 27-open R21 parent remains immutable
at SHA-256 `e7748bee49f33b3b5c021c9215d441a047718b284e3a1ee27975e3832ddfb5d2`.
The new source is SHA-256
`fb862c0a548599b7acf328ad8bb5006ce5f78d8b98ceec12bb4af9ace21f1d0f`.

Exact Panasonic ERJ2RKF1001X R11 moves from B (72.750,4.250) mm / 180 degrees
to F (78.850,9.100) mm / 180 degrees using a native top-bottom side flip.
Its original part/field/pad identities and pad-number/net mapping survive.
Mirrored local package geometry and an independent integer absolute-pad
transform are checked. Every other component placement remains exact.
The existing Panasonic source/package review still applies; there is no part
substitution or resistor value change. Front placement requires separate
assembly/enclosure/optical-access review before fabrication qualification.

R11.1 at (79.350,9.100) mm directly touches a retained main VLED F wire;
main supply grows from 36 to 37 pads. No new supply trace or via is needed.
The original 25-item private gate prefix is retired, including five obsolete
vias and one historical unsupported centre microvia. Its complete native
outside contact cluster is frozen. One ordinary 0.20 mm F lead connects
R11.2 at (78.350,9.100) mm to the retained F gate endpoint at
(78.300,10.800) mm, touching all four overlapping retained stair wires.
Its calculated length is 1.700735135 mm. All four original gate pads remain
one group. Every one of the 19,356 retained source copper items stays exact
and attached; all 19,357 resulting tracks/vias attach to live pad groups.
There is no orphan copper.

Validation passes:

- Matching 26 native/physical opens, 214 physical groups across 188 nets,
  all 215 preceding groups and their retained attached copper preserved.
- Exact identities/fields/local package geometry for 483 parts, independent
  global-pad transform, complete raw serialized copper ledger before native
  import, actual main supply and all original outside gate contacts.
- Unchanged profiles/net/zone/setup definitions and exact original104 full
  finding payloads; no additional clearance, dangling or other finding.
- Two independent byte-identical replays, each with three stable fills.
- Byte-identical inverse to the original 27-open source across three fills,
  all original 215 groups restored and empty integer XOR for all nine zones.
- Twenty-eight injected fault rejections, including wrong-side placement and
  three independently established native terminal disconnections, plus eight
  shared hole-policy controls.
- All 39 source workflow commands and native front/bottom visual review of
  the new site, retained ground plane and vacated original site.

Run `tools/check-r11-front-routing.sh` to reproduce the complete source,
native, replay, inverse and fault workflow. Raw reports/renders remain ignored
under `hardware/coupon/rev-a/build/r11-front-routing/`. No vendor PDF,
rendered vendor page or unsigned manufacturing output is committed.

The preceding bottom-side alternative is explicitly rejected. Nine otherwise
clear short-lead poses each split the old ground group into 194 pads plus
isolated PAIR07.1 and PAIR08.1, yielding 28 opens. Native subset controls show
the obsolete gate retirement alone preserves ground, while the new B resistor
and leads cut its narrow plane paths. B ground restoration searches exhaust;
six supported PAIR08 gateways remain incomplete and PAIR07 has none within
the bound. None of those 65-item retirements, bottom-side poses or ground
repair proposals is present in the selected source. A separate fine-phase
R11 supply gateway screen samples 22,701 captures, all blocked on B/In4;
that finite miss is not a general impossibility claim.

No USB/battery/LED/regulator current limit, NTC/protection/timer/default-off
function or firmware behavior changes. Electrical/return/thermal/bypass,
part/assembly/fit and controlled stack/process qualification remain open.
The remaining 556 historical unsupported centre microvias stay held; removing
one does not qualify the other transitions or the proposed fabricator stack.
Independent Gate A review still precedes fabrication; a source merge is not
a fabrication release.
