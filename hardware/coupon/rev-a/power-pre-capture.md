<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Coupon Rev A power/input pre-capture record

Status: historical arithmetic recorded and core IC libraries reviewed; direct input-current proposal rejected by [ADR 0009](../../../docs/decisions/0009-usb-input-current-closure.md). Power/input capture is on hold pending a complete topology; not approved for fabrication.

## Purpose

This record narrows the final schematic increment without hiding the two safety decisions that still need Gate A review: USB source classification with native USB data, and the selected pack's charge/NTC limits. The automated calculation is `python3 tools/check-power-design.py`. It is a design calculation, not a simulation or measurement.

## Frozen functional partitions

| Partition | Exact candidate | Power state | Draft boundary |
|---|---|---|---|
| Charger and NVDC path | `BQ25616JRTWT` | Always connected to protected cell; autonomous on USB | `D+`/`D-` topology and exact TS network remain open |
| Type-C sink detector | `TUSB320LAIRWBR` | Powered from USB-only 3.3 V | Fixed UFP/GPIO mode; Type-C advertisement does not prove USB enumeration |
| USB-only rail | `TLV75533PDBVR` | On only while VBUS is present | Must meet the TUSB320LAI 25 ms VDD-ramp condition |
| Application rail | `TPS631000DRLR` | Latching-switch controlled | 3.3 V; converter MODE starts in PFM |
| LED rail | `TPS63020DSJT` | Switch plus hardware display interlock | Nominal 3.944 V; must stay off through boot/reset/programming |
| Fuel gauge | `MAX17048G+T10` | Always connected to cell | Must enter hibernate with the application off |
| Current monitor | `INA232AIDDFR` | Powered only from application 3.3 V | Monitored common mode may remain present while IC is off |

## Calculated settings

The charger uses TI's `I = K/R` relationships. With an 806 ohm, 1% `ICHG` resistor, the draft charge-current range is 0.785–0.896 A. This is prohibited unless the exact protected, terminated pack permits at least 0.90 A across the complete allowed temperature range. A lower-rated pack forces a larger resistor.

The previously proposed unknown-adapter `ILIM` network produces these calculated values:

| Hardware state | Resistance | Calculated range |
|---|---:|---:|
| Passive branch | 1.00 kohm, 1% | 0.454–0.505 A |
| Higher Type-C advertisement | 1.00 kohm in parallel with 665 ohm, both 1% | 1.138–1.265 A |

These historical numbers are not approval of the circuit. The 1 kohm nominal setting is 478 mA using TI's typical KILIM, below its documented 500 mA minimum programmable setting; the proposed network also lacks the USB-host low-current and suspend states. See the [input assessment](usb-input-assessment.md). The BQ25616J datasheet says `ILIM` controls an input classified as unknown; its own BC1.2 `D+`/`D-` detection otherwise selects the limit. The TUSB320LAI reports the Type-C `Rp` advertisement, but its default-current output does not distinguish an unenumerated USB host from every other default-current source. Gate A must therefore choose and verify one complete topology, including A-to-C and C-to-C, switch ON/OFF, SDP/CDP/DCP, attach/detach, and native ESP32 USB enumeration. The schematic must not label the current path “fail-safe” until that review is complete.

For the converters, the current draft starts from manufacturer application values:

| Rail | Feedback divider | Nominal result | Initial filter parts |
|---|---|---:|---|
| `+3V3_APP` | 511 kohm / 91 kohm | 3.308 V | `DFE252012P-1R0M=P2`, 22 uF input, 47 uF output |
| `VLED` | 1.24 Mohm / 180 kohm | 3.944 V | 1.5 uH, 2 x 10 uF input, 4 x 22 uF output, 100 nF VINA |

The 3.3 V values follow TI's August 2026 TPS631000 Rev. C application table. The VLED divider applies the TPS63020 500 mV feedback equation; the 1.5 uH and capacitor counts start from its manufacturer guidance. DC-bias derating, output tolerance, inductor saturation, transient response, EMI, heat and physical height remain calculation/layout tasks before Gate A.

## OFF-current budget

The BQ25616J battery-current maximum is 15 uA in the stated standby condition. The MAX17048 hibernate maximum is 5 uA with its reset comparator disabled. Those two controlled IC limits consume 20 uA of the 50 uA requirement, leaving only 30 uA for the pack protector, switch leakage, disabled converters, dividers and PCB leakage. This is a worst-case component-budget calculation, not a claim that the board meets PWR-003.

## Hardware defaults required in capture

- Charger `CE` is asserted without MCU assistance only after the selected USB topology establishes a permitted state.
- Charger `OTG` is held low and can never float.
- The latching switch disables both application converters without carrying display current.
- `VLED` requires the physical switch ON and a separate hardware-qualified display request; an unpowered or resetting ESP32 cannot enable it.
- TPS63020 shutdown disconnects its output from the input; row pull-ups reference the switched VLED output.
- MAX17048 `QSTRT` is held low unless a reviewed reset path is added.
- Test pads expose VBUS, BAT+, SYS, `+3V3_APP`, VLED, charger status, Type-C outputs and both grounds before a cell is connected.

## Stop conditions

Do not order a battery, power PCB or production components from this record. Stop capture and revise the architecture if the reviewed USB topology cannot bound input current in every required state, if the selected pack cannot accept the calculated charge maximum, if the OFF-current worst case exceeds 50 uA, or if converter/layout calculations cannot meet temperature and thickness limits.
