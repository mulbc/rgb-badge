<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0010: Charge while OFF only from a qualified source

- Status: Accepted for Coupon Rev A schematic capture; thermal and Gate A review pending
- Date: 2026-09-14
- Extends: [ADR 0009](0009-usb-input-current-closure.md)

## Decision

Switch OFF is not permission to draw charging current from every powered USB connector. Coupon Rev A shall charge while OFF only after hardware identifies either a BC1.2 charging source or a USB Type-C source advertising 1.5 A or 3 A. An ordinary Standard Downstream Port (SDP), an attached source advertising only Type-C default current, and an unclassified source remain in charger standby while the switch is OFF.

When the switch is ON, native ESP32-S3 USB may enumerate through a data switch. An SDP remains in standby before configuration, may use the charger's 500 mA mode only while the USB device stack grants configured operation, and returns to standby on reset, detach or USB suspend. This firmware grant cannot select the resistor-programmed high-current mode. A valid Type-C 1.5 A / 3 A advertisement or positive charging-port classification selects the bounded high-current mode without ESP32 firmware.

Use this provisional component topology for the next library and schematic increment:

- `BQ24074RGTR`, a standalone linear PowerPath charger with hardware-selected standby, 100 mA, 500 mA and external-ILIM modes;
- `BQ24392RSER`, a VBUS-powered BC1.2 detector and USB 2.0 data switch;
- the already audited `TUSB320LAIRWBR`, fixed as a UFP in GPIO mode, for attach and Type-C current-advertisement detection;
- `TS3USB31ERSER`, powered from the switched 3.3 V application rail, as a second USB 2.0 isolation switch between BQ24392 and the ESP32-S3;
- VBUS-powered fail-safe logic whose passive state drives BQ24074 `EN2=1, EN1=1` (standby).

The 100 mA charger mode is retained as a testable capability but is not a normal product state: the battery-powered ESP32 can enumerate without taking startup power from VBUS. The selected external input limit is nominally about 0.90 A using 1.78 kΩ at `ILIM`, with a calculated 0.834–0.976 A range from TI's factor limits and a 1% resistor. A provisional 1.13 kΩ `ISET` resistor gives 0.698–0.872 A fast-charge current. That charge setting is prohibited until the exact terminated pack explicitly permits at least 0.872 A throughout the allowed temperature range.

## Required state table

| Switch/source state | USB data | BQ24074 mode | Permission source |
|---|---|---|---|
| No VBUS | Off | Input asleep | None |
| OFF + SDP, Type-C default-only, or unclassified source | Off | Standby (`EN2=1, EN1=1`) | None |
| OFF + BC1.2 CDP/DCP or supported dedicated charger | Off | External ILIM (`EN2=1, EN1=0`) | `BQ24392RSER` hardware |
| OFF + Type-C 1.5 A / 3 A | Off | External ILIM (`EN2=1, EN1=0`) | `TUSB320LAIRWBR` hardware |
| ON + SDP, before configuration or during suspend | Connected for enumeration when classified SDP | Standby | None |
| ON + configured, unsuspended SDP | Connected | USB500 (`EN2=0, EN1=1`) | Validated USB-device-stack grant |
| ON + CDP | Connected | External ILIM | `BQ24392RSER` hardware |
| ON + DCP/dedicated charger | Off | External ILIM | `BQ24392RSER` hardware |
| ON + Type-C 1.5 A / 3 A | As allowed by D+/D− classification | External ILIM | `TUSB320LAIRWBR` hardware |

Type-C 1.5 A / 3 A current advertisement remains usable during USB suspend under the Type-C current rules; the suspend-to-standby requirement above applies to the default-current SDP route. Any loss or reduction of the CC advertisement removes the hardware high-current permission.

## Why this topology

This choice makes reset and switch-OFF behavior conservative without adding a second always-on USB enumerator. The BQ24074 limits total current entering its `IN` pin, including its system output and battery charge current, and exposes the four required modes directly. Its specified no-input battery sleep current is 6.5 µA maximum at the listed condition, leaving materially more of the 50 µA OFF budget than LTC4088. BQ24392 can distinguish SDP, CDP and DCP.

BQ24392 `GOOD_BAT` must be high while VBUS is valid: holding it low to isolate data starts the detector's 30-minute nominal / 45-minute maximum Dead Battery Provision timer and can withdraw CDP charge permission before the target charge completes. The separately switched `TS3USB31ERSER` therefore provides the product's OFF-state data isolation. It is powered only by `+3V3_APP`, supports partial-power-down isolation, and defaults disconnected whenever the application rail is off.

The BQ24074 is linear, so it replaces the earlier switching-charger thermal advantage with a real coupon risk. At 5 V, 0.8 A charge current and a 3.0 V cell, a first-order no-system-load estimate is approximately 1.6 W. TI specifies thermal regulation at 125°C and recommends that nominal operation not rely on it. Copper spreading, enclosure temperature and charge time must therefore be measured; the charge current may be reduced if the coupon enters thermal regulation or makes the case unacceptably hot.

## Fail-safe implementation rules

- Pull both BQ24074 mode inputs high from the VBUS-only logic rail so reset, incomplete detection and lost firmware permission select standby. Do not rely on the charger's internal pull-downs, which would select 100 mA.
- Hardware high-current permission has priority over the SDP firmware grant. Simultaneous assertions must not create an unintended mode.
- Hold BQ24392 `GOOD_BAT` high from the VBUS domain so the Dead Battery Provision timer cannot end a long OFF-state CDP charge. Use the switched-rail TS3USB31E—not `GOOD_BAT`—to isolate native USB while OFF.
- The TS3USB31E shall be powered only by `+3V3_APP`; route the detector-facing pair to its `D+/D-` pins covered by the published zero-VCC `Ioff` condition, route the ESP32 pair to `HSD+/HSD-`, and tie active-low `OE` low. Its partial-power-down isolation must prevent an attached port from back-powering an OFF ESP32.
- The 500 mA request defaults inactive on ESP reset and is asserted only by the validated USB device layer after configuration; suspend, detach and reset clear it.
- No application command may synthesize BC1.2 or Type-C high-current permission.
- The complete VBUS budget includes detector/LDO/logic/status loads as well as the charger input.

## Verification and remaining blockers

`check-power-design.py` freezes the selected resistor arithmetic and state table. Its strict closure gate shall continue to fail until the exact BQ24074/BQ24392/TS3USB31E libraries, priority logic and complete power sheet are captured and pass native KiCad checks. Gate A must then review source classification, Type-C advertisement changes, both data switches, suspend handling, no-battery/depleted-battery startup, NTC/timer settings, input transients, thermal performance and the exact pack rating.

This ADR authorizes design capture, not procurement or fabrication.

## Sources

- [TI BQ2407x datasheet](https://www.ti.com/lit/ds/symlink/bq24074.pdf), SLUS810N, EN1/EN2 table, input/charge-current factors, quiescent current, PowerPath, NTC, timer and thermal sections.
- [TI BQ24392 datasheet](https://www.ti.com/lit/ds/symlink/bq24392.pdf), SLIS146G, BC1.2 detection table, GPIO meanings, data-switch behavior and application limits.
- [TI TUSB320LAI datasheet](https://www.ti.com/lit/ds/symlink/tusb320lai.pdf), SLLSEQ8D, UFP GPIO current-mode truth table and dead-battery behavior.
- [TI TS3USB31E datasheet](https://www.ti.com/lit/ds/symlink/ts3usb31e.pdf), single-enable USB 2.0 switch and partial-power-down isolation.
- [USB-IF USB Type-C Cable and Connector Specification Release 2.5](https://usb.org/document-library/usb-type-cr-cable-and-connector-specification-release-25), current advertisement and USB suspend interaction.
