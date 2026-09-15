<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Coupon Rev A power/input pre-capture record

Status: direct input-current proposal rejected by [ADR 0009](../../../docs/decisions/0009-usb-input-current-closure.md); source-qualified BQ24074/BQ24392/TUSB320/TS3USB31E topology selected by [ADR 0010](../../../docs/decisions/0010-source-qualified-off-charging.md). Replacement libraries pass host audits and [native rendering review at c054cb4](../../../docs/development/power-replacement-review-c054cb4.md); power capture is pending; not approved for fabrication.

## Purpose

This record narrows the next schematic increment without hiding the remaining safety proof: USB source classification/native data, fail-safe priority logic, linear thermal behavior and the selected pack's charge/NTC limits. The automated calculation is `python3 tools/check-power-design.py`. It is a design calculation, not a simulation or measurement.

## Frozen functional partitions

| Partition | Exact candidate | Power state | Draft boundary |
|---|---|---|---|
| Charger and PowerPath | `BQ24074RGTR` | Always connected to protected cell; standby unless source permission exists | Native library review, TS/timer/termination network and thermal layout remain open |
| BC1.2 detector/data switch | `BQ24392RSER` | Powered directly from VBUS; `GOOD_BAT` high whenever VBUS is valid | Native library review and GPIO translation remain open |
| Application USB isolator | `TS3USB31ERSER` | Powered only from switched `+3V3_APP`; detector side on `D+/D-`, ESP32 side on `HSD+/HSD-`, active-low `OE` tied low | Native library review and high-speed routing remain open; `Ioff` isolates the connector-facing `D+/D-` pins when unpowered |
| Type-C sink detector | `TUSB320LAIRWBR` | Powered from USB-only 3.3 V | Fixed UFP/GPIO mode; 1.5 A/3 A is an independent hardware grant |
| USB-only rail | `TLV75533PDBVR` | On only while VBUS is present | Must meet the TUSB320LAI 25 ms VDD-ramp condition |
| Permission logic and ILIM boost switch | Exact parts pending | VBUS-only; passive output is BQ24074 standby, boost off | Hardware alone selects the parallel ILIM branch under ADR 0011 |
| Application rail | `TPS631000DRLR` | Latching-switch controlled | 3.3 V; converter MODE starts in PFM |
| LED rail | `TPS63020DSJT` | Switch plus hardware display interlock | Nominal 3.944 V; must stay off through boot/reset/programming |
| Fuel gauge | `MAX17048G+T10` | Always connected to cell | Must enter hibernate with the application off |
| Current monitor | `INA232AIDDFR` | Powered only from application 3.3 V | Monitored common mode may remain present while IC is off |

## Calculated settings

The selected charger uses TI's `I = K/R` relationships. With a 1.13 kohm, 1% `ISET` resistor, the draft charge-current range is 0.698–0.872 A. This is prohibited unless the exact protected, terminated pack permits at least 0.872 A across the complete allowed temperature range. A lower-rated pack forces a larger resistor.

[ADR 0011](../../../docs/decisions/0011-usb-total-current-headroom.md) replaces USB500 with a 3.65 kohm, 1% base ILIM resistor and a hardware-only switched parallel 3.48 kohm, 1% branch. The ideal-switch settings are:

| Hardware state | BQ24074 mode | Calculated range |
|---|---:|---:|
| Passive/reset/unqualified | Standby | No charger input path |
| Configured, unsuspended SDP | Low external ILIM | 0.361–0.476 A |
| BC1.2 charging source or Type-C 1.5 A/3 A | Boosted external ILIM | 0.834–0.975 A |

These are capture targets, not approval of an uncaptured circuit. See the [input assessment](usb-input-assessment.md) and ADRs 0010/0011 for the complete state table. The low setting reserves 20 mA for configured-state auxiliaries plus 2 mA for programming-network effects; these allocations require proof and do not establish suspend compliance. Both BQ24074 mode pins must have external pull-ups to the VBUS-only rail so loss of permission selects standby; its internal pull-downs would select USB100. BQ24392 `GOOD_BAT` must stay high while VBUS is valid because holding it low starts a finite Dead Battery Provision timer. The application-powered TS3USB31E supplies the permanent OFF-state isolation instead. Gate A must verify A-to-C and C-to-C, switch ON/OFF, SDP/CDP/DCP, attach/detach, advertisement changes, native enumeration and suspend. The exact priority/level-shift circuit must be audited before the schematic can be called fail-safe.

The selected charger is linear. At 5 V input, 0.8 A charge current and a 3.0 V cell, a first-order no-system-load dissipation estimate is approximately 1.6 W. This is not a thermal result. Layout analysis and a depleted-to-full coupon charge log must show whether the 125°C regulation loop engages and whether enclosure temperature is acceptable.

For the converters, the current draft starts from manufacturer application values:

| Rail | Feedback divider | Nominal result | Initial filter parts |
|---|---|---:|---|
| `+3V3_APP` | 511 kohm / 91 kohm | 3.308 V | `DFE252012P-1R0M=P2`, 22 uF input, 47 uF output |
| `VLED` | 1.24 Mohm / 180 kohm | 3.944 V | 1.5 uH, 2 x 10 uF input, 4 x 22 uF output, 100 nF VINA |

The 3.3 V values follow TI's August 2026 TPS631000 Rev. C application table. The VLED divider applies the TPS63020 500 mV feedback equation; the 1.5 uH and capacitor counts start from its manufacturer guidance. DC-bias derating, output tolerance, inductor saturation, transient response, EMI, heat and physical height remain calculation/layout tasks before Gate A.

## OFF-current budget

The BQ24074 no-input BAT-pin sleep-current maximum is 6.5 uA at the stated 85°C condition. The MAX17048 hibernate maximum is 5 uA with its reset comparator disabled. Those two controlled IC limits consume 11.5 uA of the 50 uA requirement, leaving 38.5 uA for the pack protector, switch leakage, disabled converters, dividers and PCB leakage. This is a component-budget calculation, not a claim that the board meets PWR-003 across all temperatures.

## Hardware defaults required in capture

- BQ24074 `EN2=1, EN1=1` is the externally pulled passive/reset state. Its `CE` remains low; the mode inputs, not MCU control of `CE`, enforce source permission.
- Hardware high-current permission selects `EN2=1, EN1=0`; an SDP grant can select only `EN2=0, EN1=1` and defaults inactive.
- BQ24392 `GOOD_BAT` is high whenever VBUS is valid so its 30-minute nominal / 45-minute maximum Dead Battery Provision timer cannot terminate a long OFF-state CDP charge.
- TS3USB31E is powered only by `+3V3_APP`; its connector/detector-facing pair uses the `D+/D-` pins covered by the published `Ioff` condition, its ESP32 pair uses `HSD+/HSD-`, and active-low `OE` is tied low. With the slide switch OFF, loss of VCC provides the data disconnect and prevents back-powering.
- The latching switch disables both application converters without carrying display current.
- `VLED` requires the physical switch ON and a separate hardware-qualified display request; an unpowered or resetting ESP32 cannot enable it.
- TPS63020 shutdown disconnects its output from the input; row pull-ups reference the switched VLED output.
- MAX17048 `QSTRT` is held low unless a reviewed reset path is added.
- Test pads expose VBUS, BAT+, SYS, `+3V3_APP`, VLED, charger status, Type-C outputs and both grounds before a cell is connected.

## Stop conditions

Do not order a battery or power PCB from this record. Stop capture and revise the architecture if the priority logic cannot default safely, if the selected pack cannot accept the calculated charge maximum, if the OFF-current worst case exceeds 50 uA, or if the BQ24074/converter layout cannot meet temperature and thickness limits.
