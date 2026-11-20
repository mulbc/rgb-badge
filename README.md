<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

**2026-11-20 selected — 22 opens:** The [additive PAIR03 supply join](docs/development/pair03-supply-routing-2026-11-20.md) preserves all 211 previous groups and all 19,349 existing copper items, with GND197/VLED39/USB32. Matching native/physical counts, exact original 104 findings, stable independent replays, byte-exact inverse/nine zone XORs, 32 fault rejections, eight hole controls, 43 source checks and native visual review pass. Use `led-pair03-supply-routing-trial-114mm`. Zero opens and all qualification/Gate A holds remain unfinished; fabrication is prohibited.

**2026-11-20 selected — 23 opens:** The [PAIR01 supply continuation](docs/development/pair01-supply-routing-2026-11-20.md) joins PAIR01.4 to main VLED38, preserving all 212 prior groups, main GND197 and retained attached copper. Native and physical counts match at23 with exact original104. Replays, byte-exact inverse/all nine zone XORs, 43 fault/hole/courtyard controls, 42 source checks and native visual review pass. Use `led-pair01-supply-routing-trial-114mm`. Zero opens and all qualification/Gate A holds remain unfinished; fabrication is prohibited.

**2026-11-20 selected — 24 opens:** The [R6 direct bottom continuation](docs/development/r6-direct-bottom-routing-2026-11-20.md) preserves all 213 prior groups, all 197 main ground pads, all 37 main VLED pads and attached retained copper. Native and physical counts match at 24 with exact original104. Replays, byte-exact inverse/all nine zone XORs, 43 fault/hole/courtyard controls, 41 source checks and native visual review pass. Use `led-r6-direct-bottom-trial-114mm`. Zero opens and all qualification/Gate A holds remain unfinished; fabrication is prohibited.

**2026-11-19 selected — 27 opens:** The [minimal R21 supply join](docs/development/r21-routing-2026-11-19.md) preserves all 216 prior groups and attached source copper, with 27 matching native/physical opens and exact original104. Exact replays/inverse, serialized-source guards, 28 fault rejections, eight hole controls, 38 source checks and native visual review pass. Use `led-r21-routing-trial-114mm`; the zero-open goal and all qualification/Gate A holds remain unfinished. Fabrication is prohibited.

**2026-11-15 selected — 29 opens:** The [inverter clock join](docs/development/inverter-routing-2026-11-15.md) localizes exact U48/C67 and joins U48.4–U49.7. All 218 prior groups survive. Native/physical 29 opens, exact original 104 findings under independent U48/prior U52 transforms, two byte-identical replays, byte-identical inverse reconstruction, 18 fault guards, eight hole-policy controls, 36 source checks and visual review pass. Use `led-inverter-routing-trial-114mm`. Zero opens and all electrical/part/process/fit/stack/Gate A holds remain; fabrication is prohibited.

**2026-11-14 selected — 30 opens:** The [complete enable join](docs/development/enable-routing-2026-11-14.md) closes the five-terminal DISPLAY_ENABLE group with one exact C71 shift and two private-leaf replacements. All 219 prior groups survive. Native/physical 30 opens, exact original 104 findings under the unchanged prior pose transform, stable independent replays, inverse-source proof, 18 fault guards, 35 source checks and native visual review pass. Use `led-enable-routing-trial-114mm`. Zero opens and all electrical/part/process/fit/stack/Gate A holds remain; fabrication is prohibited.

**2026-11-14 selected — 31 opens:** The [clear-output join](docs/development/clear-output-routing-2026-11-14.md) connects U52.4 to U49.2/R108.1 through ordinary-width copper. All 220 prior groups and 19,226 source copper items survive. Native/physical 31 opens, exact original 104 finding payloads under the existing frozen pose transform, independent stable replays, byte-identical source restoration, eleven native faults, 34 source checks and native visual review pass. Use `led-ordinary-routing-trial-114mm`. Zero opens and electrical/part/process/fit/stack/Gate A acceptance remain unresolved; fabrication is prohibited.

**2026-11-14 selected — 32 opens:** The [complete control cluster](docs/development/control-cluster-routing-2026-11-14.md) joins U51.4–U52.1 with exact U52/C71 placement and bounded loop/row replacements. All 221 original groups survive, with 32 native/physical opens, the original 104 finding payloads under the exact U52 pose transform, stable byte-identical replays, inverse-source proof, 18 fault guards, 33 source checks and native visual review. Use `led-control-cluster-routing-trial-114mm`. Zero opens, electrical/part/process/fit/stack qualification and independent Gate A remain open; fabrication is prohibited.

**2026-11-12 selected — 33 opens:** The [gauge-supply join](docs/development/gauge-supply-routing-2026-11-12.md) adds exact ordinary-width copper, preserving every prior group and source item. Native/physical 33 opens, exact unchanged 104 findings, stable byte-identical replays, eleven native faults, 32 source checks and visual review pass. Use `led-gauge-routing-trial-114mm`. U35 supply, zero opens and electrical/process/fit/stack/Gate A acceptance remain open; fabrication is prohibited.


**2026-11-12 selected — 34 opens:** The [USB EN1 join](docs/development/usb-en1-routing-2026-11-12.md) localizes exact R70/TP31 and joins U23.4, preserving every prior group and all other copper with no new vias. Exact unchanged 104 findings, stable independent replays, 12 native faults, 31 source checks and visual review pass. Use `led-usb-en1-routing-trial-114mm`; the corrected RSE parent stays immutable. Zero opens and electrical/process/fit/stack/Gate A acceptance remain open; fabrication is prohibited.

**2026-11-12 corrected routing source — 35 opens:** The [RSE pin correction](docs/development/rse-pin-correction-2026-11-12.md) fixes U49/U50 physical pin assignments, restores all 223 prior functional groups and preserves all previous accepted additions. Exact unchanged 104 findings, independent stable replays, native/source/fault and visual checks pass. Continue from `led-rse-corrected-routing-trial-114mm`; preceding boards retain the historical wrong map. Zero opens, electrical/process/fit/stack qualification and independent Gate A remain open; fabrication is prohibited.


**2026-11-07 switch routing selected — 43 opens:** The [validated successor](docs/development/switch-routing-2026-11-07.md) joins SW2.3–R83.1–U36.5, retains all 232 immutable 44-open parent groups and every prior copper item, and passes exact unchanged 104-finding DRC, stable replay/fills, source/orphan/fault and visual checks. The zero-open goal remains in progress. Added supply bridges, controlled stack, 557 historical centre microvias, electrical/process/fit qualification and independent Gate A remain open; fabrication is prohibited.

**2026-11-09 remaining routing selected — 36 opens:** The [validated successor](docs/development/remaining-routing-2026-11-07.md) shifts exact C32 upward by 0.250 mm, retaining its supply contact and joining its ground island through one filled B.Cu component. No copper is added or retired by this step. All 225 preceding groups and 226 additions, plus all 231 immutable parent groups, survive. Exact unchanged 104-finding DRC, stable replay/fills, 36 fault guards, 27 source checks and native visual review pass. The zero-open goal, electrical/thermal/stack/process/fit qualification, 557 historical centre vias and independent Gate A remain open; fabrication is prohibited.
# RGB Badge

An open-source, full-colour wearable LED badge inspired by the FOSSASIA Badge Magic form factor.

The project is currently in **draft schematic development**. Several coupon circuits are captured, including a provisional charger core, but the complete power circuit and PCB are unfinished. No board in this repository has been independently reviewed, fabricated or tested. Do not treat current design material as production-ready.

The current [30-open CAD study](docs/development/enable-routing-2026-11-14.md) retains 104 inventoried intrinsic findings. Circuit completion, electrical/process/fit/stack qualification and independent Gate A review remain open.

## Product target

| Property | Target |
|---|---:|
| Display | 48 × 16 individually controlled RGB pixels |
| Pixel pitch | 1.95 mm |
| Finished envelope | ≤118 × 35 × 11 mm working limit; 114 × 32.5 mm PCB target |
| Finished weight | ≤75 g target; 100 g absolute maximum |
| Reference runtime | Approximately 6 h at the defined mixed-content workload and fixed indoor brightness |
| Charging/data | USB-C, 5 V, A-to-C and C-to-C; native USB data |
| Wireless | BLE enabled only in programming mode |
| Controller | ESP32-S3-WROOM-1U-N16R8 |
| Manufacturing | Turnkey PCBA; no hand assembly of SMT parts |

Six hours is not a maximum-brightness guarantee. The initial model predicts about 6.3 hours with a 900 mAh cell for the reference workload and about 1.1 hours for continuous maximum full-screen white. Coupon measurements will replace those estimates.

## Development strategy

The first physical board is a production-intent 16 × 16 coupon. It compares Everlight `EAST10105RGBA0` 1010 and QT Brightek `QBLP1515A-RGB2A` 1515 common-anode RGB LEDs while exercising the intended controller, matrix driver, USB-C, charger, battery gauge, power converters, antenna and controls. The full 48 × 16 badge will not be ordered until the coupon passes its electrical, optical, thermal, runtime and RF acceptance tests.

For coupon routing, [ADR 0034](docs/decisions/0034-uniform-qt-coupon-pitch-proposal.md) sets the 1515 half to 2.2 mm horizontal / 1.95 mm vertical pitch and uniform orientation; the 1010 half stays at 1.95 mm in both axes. The final badge still targets no more than 1.95 mm in either axis, so coupon optical comparisons must account for the different spacing.

Start with:

1. [Project context](CONTEXT.md)
2. [Requirements](docs/requirements.md)
3. [Full project plan](docs/project-plan.md)
4. [Accepted decisions](docs/decisions/README.md)
5. [Coupon core component candidates](docs/sourcing/coupon-rev-a-core-candidates.md)
6. [Contributor and agent rules](AGENTS.md)

## Repository layout

| Path | Contents |
|---|---|
| `docs/` | Requirements, decisions, project plan, bring-up and test evidence |
| `hardware/` | Editable KiCad projects and project-local libraries |
| `firmware/` | ESP-IDF firmware and host-side tests |
| `mechanical/` | Parametric enclosure source and reviewed exports |
| `manufacturing/` | Immutable, revisioned fabrication and assembly releases |
| `tools/` | Asset compiler, validation and release tooling |

## Safety and verification

This project contains a rechargeable lithium-polymer cell and switching power electronics. A completed coupon schematic and preliminary PCB layout must be reviewed by an experienced hardware engineer before fabrication. Battery charge limits may only be changed after checking the exact terminated-pack specification. Test results must always identify the board revision and must never be inferred or fabricated.

## Attribution

The project uses the [FOSSASIA Badge Magic hardware](https://github.com/fossasia/badgemagic-hardware) as an attributed reference. It is a new design rather than a copy of that PCB. See [NOTICE](NOTICE).

## Licensing

- Hardware design files, mechanical design files, manufacturing files and hardware documentation: [CERN-OHL-S-2.0](LICENSES/CERN-OHL-S-2.0.txt).
- Firmware, scripts and software tooling: [Apache-2.0](LICENSES/Apache-2.0.txt).
- Third-party files retain their original licences and must be recorded before inclusion.
