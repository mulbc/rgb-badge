<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# RGB Badge

An open-source, full-colour wearable LED badge inspired by the FOSSASIA Badge Magic form factor.

The project is currently in **pre-schematic development**. Requirements and the system architecture are agreed, but no PCB in this repository has yet been electrically reviewed, fabricated or tested. Do not treat any current design material as production-ready.

## Product target

| Property | Target |
|---|---:|
| Display | 48 × 16 individually controlled RGB pixels |
| Pixel pitch | 1.95 mm |
| Finished envelope | ≤110 × 35 × 11 mm |
| Finished weight | ≤75 g target; 100 g absolute maximum |
| Reference runtime | Approximately 6 h at the defined mixed-content workload and fixed indoor brightness |
| Charging/data | USB-C, 5 V, A-to-C and C-to-C; native USB data |
| Wireless | BLE enabled only in programming mode |
| Controller | ESP32-S3-WROOM-1U-N16R8 |
| Manufacturing | Turnkey PCBA; no hand assembly of SMT parts |

Six hours is not a maximum-brightness guarantee. The initial model predicts about 6.3 hours with a 900 mAh cell for the reference workload and about 1.1 hours for continuous maximum full-screen white. Coupon measurements will replace those estimates.

## Development strategy

The first physical board is a production-intent 16 × 16 coupon. It compares 1010 and 1515 common-anode RGB LEDs while exercising the intended controller, matrix driver, USB-C, charger, battery gauge, power converters, antenna and controls. The full 48 × 16 badge will not be ordered until the coupon passes its electrical, optical, thermal, runtime and RF acceptance tests.

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
