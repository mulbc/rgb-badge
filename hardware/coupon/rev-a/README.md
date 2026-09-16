<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Coupon Rev A

Status: matrix, driver, row-stage and controller staged electrical reviews passed; power-library copper/stencil/heading corrections passed native review at `3638b1d`. The row-page readability repair passed [native review at `91ef697`](../../../docs/development/layout-review-91ef697.md), and the USB4505 candidate library passed [native rendering review at `bf1627c`](../../../docs/development/usb-connector-review-bf1627c.md). Remaining power capture and independent Gate A verification are pending; not safe to fabricate. See the [finding record](../../../docs/development/power-library-review-c84f8ce.md).

## Purpose

Validate the production electrical architecture and compare 1010 versus 1515 RGB LEDs before scaling to the 48 × 16 badge.

The provisional direct input-current network is rejected by [ADR 0009](../../../docs/decisions/0009-usb-input-current-closure.md). [ADR 0010](../../../docs/decisions/0010-source-qualified-off-charging.md) selects BQ24074/BQ24392/TUSB320/TS3USB31E for the next power capture, with standby as the fail-safe state, OFF charging limited to hardware-qualified sources and a switched-rail second data switch for hard-OFF isolation. The [assessment](usb-input-assessment.md) records its state table and missing proof. Exact replacement libraries pass host audits and [native rendering review at c054cb4](../../../docs/development/power-replacement-review-c054cb4.md); [ADR 0011](../../../docs/decisions/0011-usb-total-current-headroom.md) now reserves configured-SDP auxiliary headroom using low external ILIM and a hardware-only resistor boost. Its static GPIO permission checks pass; physical logic, power capture and thermal validation are still pending.

## Required contents

Follow-on circuit checkpoint: the [staged permission capture](permission-capture.md) adds two canonical sheets, 61 PCB items and 176 pins for Schmitt conditioning and the physical gate implementation of ADR 0011. Complete source now has ten pages and 417 items / 1,536 pins. All external detector/supervisor/application inputs and charger/ILIM outputs remain explicit test boundaries. Native ERC/XML/render review is pending for this combined library-and-circuit increment.

The [permission-library audit](permission-library-audit.md) adds five exact LVC gates, a TPS3808G01DBVR supervisor candidate and a DBV6 footprint for the upcoming hardware permission circuit. Source checks cover 32 added pins and package geometry; native rendering and circuit qualification remain pending. It also records the DBV5 body/courtyard drawing correction. No new component is connected yet. Batch native review with the next circuit checkpoint rather than requesting another library-only owner run.

- 16 × 16 pixels at 1.95 mm pitch: columns 0–7 use Everlight `EAST10105RGBA0`; columns 8–15 use QT Brightek `QBLP1515A-RGB2A`.
- ESP32-S3-WROOM-1U-N16R8 and external antenna.
- One TLC59581 and all sixteen level-shifted row stages.
- Production USB-C, ESD, Type-C detection and standalone charger circuits.
- Production 3.3 V/VLED converters, fuel gauge, battery-current monitor, NTC interfaces and controls.
- Native USB diagnostics and hidden factory programming/test pads.

The exact draft candidates and open circuit risks are tracked in the [Coupon Rev A sourcing record](../../../docs/sourcing/coupon-rev-a-core-candidates.md). A candidate in that record is not an approved purchase or fabrication BOM line.

## Open and validate

Follow the [macOS KiCad setup and round-trip check](../../../docs/development/kicad-macos.md). The canonical project entry point is `rgb-badge-coupon.kicad_pro`. Run `../../../tools/check-kicad.sh` from this directory, or `./tools/check-kicad.sh` from the repository root.

The root now links four matrix sheets, the TLC59581 driver, the [sixteen-row selector sheet](row-capture.md) and the [ESP32-S3 controller sheet](controller-capture.md). The matrix/driver native run at `8e95eb0` passed all 1,094 then-captured physical pins and six-page visual review. The [row library audit](row-library-audit.md) and [native rendering review](../../../docs/development/row-library-review-0c71860.md) control the decoder/MOSFET libraries. The row source includes U2, C2, all 32 MOSFETs and 37 resistors; the native run at `eb4129b` passed zero-violation ERC, all 335 PCB items / 1,290 physical pins and seven-page visual review. The [review record](../../../docs/development/row-capture-review-eb4129b.md) preserves that evidence. Controller source adds U3, reset/mode networks, native USB/UART boundaries and eleven hidden test pads; the [native controller review](../../../docs/development/controller-review-d56e1aa.md) passed the exact temporary USB-boundary warning pair, all 356 PCB items / 1,360 logical pins, footprint renders and eight-page visual review. The [power-library audit](power-library-audit.md) adds machine-checked exact symbols and manufacturer land patterns for the charger, both switched converters, USB-only LDO/inverter, Type-C detector, fuel/current monitors and USB ESD array; corrected native rendering passed at `3638b1d`. The recovered [USB4505 candidate-library audit](usb-connector-audit.md) controls the separate connector symbol and draft footprint; host and [owner-generated native rendering checks](../../../docs/development/usb-connector-review-bf1627c.md) pass, while cutout reliefs and mechanical/process qualification remain pending. USB-C input, charging, gauging and switched power sources are not captured; #FLG01–#FLG03 remain explicit draft supply assumptions; no PCB exists.

The two project-local LED symbols and footprints completed the first-author [LED audit](footprints/led-audit.md) and rendering review. Independent verification remains pending. The earlier macOS blank-sheet ERC result does not validate this new circuit.

## Release blockers

- Controlled LED datasheets; verified footprints, pad numbering, polarity, tape orientation and optical-bin procurement.
- Confirm supplied TLC59581 E/G package variant, current-limit accuracy/derating and remaining driver layout/thermal checks.
- Exact battery-pack documentation.
- Audited BQ24074/BQ24392/TS3USB31E libraries and reviewed priority/level logic for USB default-current, BC1.2, Type-C advertisement and native-data coexistence in switch-ON and switch-OFF states.
- Completed calculations, schematic and ERC.
- Preliminary placement/routing and DRC/DFM.
- Independent engineer review with every finding resolved or explicitly accepted.

The intended first order is five PCBs with three assembled. That order is not authorized by this README.
