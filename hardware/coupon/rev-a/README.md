<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Coupon Rev A

Status: matrix, driver and row-library native reviews passed; row-stage capture plus independent Gate A verification pending; not safe to fabricate

## Purpose

Validate the production electrical architecture and compare 1010 versus 1515 RGB LEDs before scaling to the 48 × 16 badge.

## Required contents

- 16 × 16 pixels at 1.95 mm pitch: columns 0–7 use Everlight `EAST10105RGBA0`; columns 8–15 use QT Brightek `QBLP1515A-RGB2A`.
- ESP32-S3-WROOM-1U-N16R8 and external antenna.
- One TLC59581 and all sixteen level-shifted row stages.
- Production USB-C, ESD, Type-C detection and standalone charger circuits.
- Production 3.3 V/VLED converters, fuel gauge, battery-current monitor, NTC interfaces and controls.
- Native USB diagnostics and hidden factory programming/test pads.

The exact draft candidates and open circuit risks are tracked in the [Coupon Rev A sourcing record](../../../docs/sourcing/coupon-rev-a-core-candidates.md). A candidate in that record is not an approved purchase or fabrication BOM line.

## Open and validate

Follow the [macOS KiCad setup and round-trip check](../../../docs/development/kicad-macos.md). The canonical project entry point is `rgb-badge-coupon.kicad_pro`. Run `../../../tools/check-kicad.sh` from this directory, or `./tools/check-kicad.sh` from the repository root.

The root now links four matrix sheets, each containing 64 LEDs, plus the driver sheet. Together they capture all 256 LEDs and their row/colour-column connections. The [matrix capture record](matrix-capture.md) defines the reference/net contract, completed source checks, native KiCad validation and drawing review. The [driver capture record](driver-capture.md) covers U1, its current reference, decoupling, provisional E-variant footprint and draft supply assumptions. TP1 resolves the earlier isolated `LED_SOUT` warning. The `8e95eb0` native run passed ERC, all 1,094 physical pin assignments and six-page visual review. The [row library audit](row-library-audit.md) controls the exact decoder, two MOSFETs and 1 kΩ pull-up, including the low-voltage-drive and hardware-default-off limitations; its [native rendering review](../../../docs/development/row-library-review-0c71860.md) passed at `0c71860`. Row stages, controller and power source are not captured yet; no PCB exists.

The two project-local LED symbols and footprints completed the first-author [LED audit](footprints/led-audit.md) and rendering review. Independent verification remains pending. The earlier macOS blank-sheet ERC result does not validate this new circuit.

## Release blockers

- Controlled LED datasheets; verified footprints, pad numbering, polarity, tape orientation and optical-bin procurement.
- Confirm supplied TLC59581 E/G package variant, current-limit accuracy/derating and remaining driver layout/thermal checks.
- Exact battery-pack documentation.
- Reviewed resolution of USB default-current, BC1.2 and native-data coexistence in switch-ON and switch-OFF states.
- Completed calculations, schematic and ERC.
- Preliminary placement/routing and DRC/DFM.
- Independent engineer review with every finding resolved or explicitly accepted.

The intended first order is five PCBs with three assembled. That order is not authorized by this README.
