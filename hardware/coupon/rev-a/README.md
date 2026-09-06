<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Coupon Rev A

Status: requirements complete, LED pair selected and first-pass core candidates recorded; schematic not started; not safe to fabricate

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

## Release blockers

- Controlled LED datasheets; verified footprints, pad numbering, polarity, tape orientation and optical-bin procurement.
- Exact battery-pack documentation.
- Reviewed resolution of USB default-current, BC1.2 and native-data coexistence in switch-ON and switch-OFF states.
- Completed calculations, schematic and ERC.
- Preliminary placement/routing and DRC/DFM.
- Independent engineer review with every finding resolved or explicitly accepted.

The intended first order is five PCBs with three assembled. That order is not authorized by this README.
