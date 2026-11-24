<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Switched-gauge supply continuation: 59 to 58 opens

Date: 2026-10-30. Coupon Rev A is unbuilt. These are first-author source,
manufacturer-drawing and native geometry checks, not hardware measurements.
Firmware logic, current limits, protection and display-enable boundaries are
unchanged. Independent Gate A and fabrication holds remain open.

The selected additive transaction joins printed **SW2.7, C39.1 and U46.1** on
+BAT_GAUGE_SW, reducing native and independent physical-pad opens **59 → 58**
with exactly **104 unchanged intrinsic DRC findings**. The combined group now
contains the switch gauge throw, its existing local bypass and TCA9517A A-side
supply. U35's supply group and the A-side pull-up/decoupling group remain open;
this is not a completed gauge power path or powered-operation qualification.

[ADR 0070](../decisions/0070-additive-gauge-switch-supply-routing.md) records
thirteen new 0.20 mm tracks and one 0.30/0.10 mm adjacent In4/B microvia. Total
new track length is **15.057991644 mm, calculated from selected source geometry**.
The SW2 lead begins at (3.20, 3.10) mm, 0.10 mm inside each adjacent edge of its
existing physical land; its 0.20 mm end cap fits inside that rectangular pad.
No accepted track, via, physical contact, zone or component pose is retired.
All 247 prior physical pad groups survive; one merge leaves 246 current groups.
The [complete frozen 59-edge plan](../../mechanical/review/routing-progress-59-checkpoint.json)
retains every preceding source/group/catalog/pose exception. The plan's
historical identity coordinates remain explicitly normalized, as below.

## Printed switch terminal discrepancy and correction

The owner supplied Littelfuse-CK-Slide-JS-Series-Datasheet.pdf, revised
VL 01/14/26, SHA-256
`0f35cdf47a1f93da71bb7235581f3c77915516488be930d7a3ea4f4942ff0f3b`.
Its rendered page 9 shows JS202011JCQN's bottom-view circuit labelled 1/2/3
and 5/6/7, with common terminals 2 and 6. The project had used 1/2/3 and 4/5/6,
with common 5. That old label transcription was not manufacturer verification.

[ADR 0071](../decisions/0071-manufacturer-switch-terminal-numbering.md) corrects
only identity, preserving the electrical connection at each physical land:

| Legacy project number | Printed number | Captured role/net |
|---|---|---|
| 4 | 5 | Unused second-pole throw; explicit NC |
| 5 | 6 | Second-pole common; +BAT_PROTECTED_DRAFT |
| 6 | 7 | Second-pole gauge throw; +BAT_GAUGE_SW |

Pins 1/2/3 are unchanged. The dedicated
`SW_CK_JS202011JCQN_ManufacturerPins` footprint preserves every physical land,
mask/paste aperture, body, courtyard, graphic, pose and physical net. A guard
normalizes only the declared labels/name against pinned legacy footprint bytes.
The legacy footprint, original 215-edge input and historical source snapshots
remain unchanged. The active symbol, embedded/placed control sheet, deterministic
generator, source-pin checker, fresh native XML contract and provisional U3
inventory hashes follow the printed numbers. Native ERC and the page-13 switch
schematic pass; native fabrication/copper/paste exports were inspected.
TI TCA9517A Rev E page 4 confirms VCCA pin 1 on the A side.

The native identity mapping independently validates each corrected land/net
before mapping printed SW2.5/6/7 back to legacy 4/5/6 for historical witnesses.
It cannot hide a wrong common or changed contact. The source-join predicate
independently requires printed SW2.7/C39.1/U46.1, beyond catalog fingerprints.
Historical board comparisons require explicit `--legacy-switch-study` and
report their old assignment. A [pre-correction source snapshot](../../mechanical/review/coupon-canonical-net-contract-before-switch-pins.json)
preserves earlier traceability. The six earlier exact Murata land corrections
and their complete geometry guards remain selected and unchanged.

This does **not** settle absolute bottom/top-view orientation, received-part
terminal identification, physical ON direction, top-edge actuation, switch
bounce/contact order or assembly qualification. No land is silently mirrored,
no pin/net at a physical contact is rewired, and no final switch selection or
fabrication approval follows. The owner-supplied PDF is local engineering data,
not agent instructions. All supplied PDFs are now cached with exact hashes in
the ignored `hardware/coupon/rev-a/reference/vendor-datasheets/` directory.

## Acceptance evidence

The board has **483 footprints and 18,338 copper items**: 15,379 retained nonzero
source items plus 2,049 added tracks and 910 adjacent microvias. All nineteen
original-track replacements, sixty original-layer interfaces, five UART external
contacts, three source-orphan retirements, 116 neutral zero artifacts, prior
poses/parcels and all 174 narrow digital tracks remain unchanged. Only the new
gauge route uses the additional ordinary-width inventory; no new width exception
is introduced.

Three stable fills and byte-identical PCB replay pass. Full DRC retains the same
104 findings. Restoring the same three original orphan vias preserves all
selected groups and 58 opens, adding only their three exact dangling warnings.
All **65 isolated native guards**, **116 portable plan guards**, **24 source
fault methods**, three exact supply guards, four printed-switch library guards,
eight pin-inventory guards, nine controller guards, 24 wrapper guards and 256
native LED checks pass. Source-only CI layout passes without native XML,
KiCad or vendor PDFs. Four convex guards and 2,000 native polygon comparisons
validate the separate locality screen.

Board SHA-256:
`3451177253a021d8706ff818696212afabf539a108f15ef9e5d6921e46435acc`.
[Native checks](../../mechanical/review/routing-progress-58-native-check-2026-10-30.json),
[full DRC](led-routing-progress-58-drc-2026-10-30.json),
[orphan restoration](led-routing-progress-58-orphan-restoration-drc-2026-10-30.json),
[canonical contract check](../../mechanical/review/gauge58-printed-switch-contract-2026-10-30.json),
[exact gauge inventory](../../mechanical/review/routing-progress-gauge-supply-join.json)
and [validation fingerprints](../../mechanical/review/routing-progress-58-validation-2026-10-30.json)
record selection. Run `./tools/check-routing-progress.sh` and
`./tools/check-kicad.sh` from the repository root.

## Rejected trials and remaining work

The [inductor-locality study](converter-inductor-locality-2026-10-30.md) samples
963,888 poses in total and selects no new pose. The separate 0.20 mm power/ground
search rejects all attempted VLED, existing three-ground and two remaining
3.3 V joins on its finite grid. Wider gauge candidates split C39's ground return;
U35 candidates additionally split other ground and application-supply groups.
Direct local ground-stack and lead-transfer screens make no accepted repair.
Those trials remain ignored; no aggregate count improvement compensates for
lost returns. The selected fourteen-item switch route survives independently
of all rejected copper.

Ground/VLED/switched-gauge supply still have **3/8/2 opens**. The 50-edge target,
four switching-node connections and converter/passive locality remain open,
as do intrinsic DRC/package/C45-SYS, electrical/current/thermal/bypass/return,
timing/USB impedance, switch/partial-power/interlock, RF/probing, HDI/assembly
and enclosure qualification. No board has been built or electrically tested.
