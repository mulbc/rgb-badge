<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# MAX17048 fuel-gauge capture contract

Status: source-based circuit requirements and calculations, 2026-09-26, amended by the owner's [ADR 0015](../../../docs/decisions/0015-switch-fuel-gauge-with-application.md) choice. A [staged gauge sheet](switch-gauge-boundary.md) now places the gauge, bypass and pull-ups using a **flagged assumed switched-BAT source**. The latching switch and physical battery connection remain uncaptured; no PCB or bench result exists. The source is the [MAX17048/MAX17049 Rev. 7 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX17048-MAX17049.pdf), especially the pin table, electrical specifications, HIBRT/VRESET sections and I²C timing table. The existing [exact-MPN library audit](power-library-audit.md) controls the gauge symbol and footprint.

## Capture connections

| `MAX17048G+T10` TDFN pin | Net / treatment | Basis and limitation |
|---|---|---|
| 1 CTG; 4 GND; exposed pad 9 | GND | Manufacturer pin table. |
| 2 CELL; 3 VDD | Protected battery positive through an isolated pole of the latching switch | CELL is internally unconnected for this one-cell part; the manufacturer still directs it to battery positive. VDD senses protected-cell voltage only while ON. In OFF both pins disconnect from the cell. Verify the exact pack, switch pole, connector and contact topology before naming this net. |
| 3 VDD | 0.1 µF ceramic bypass to GND at the device | Manufacturer pin table; the existing audited `GRM155R71C104KA88D` is a candidate, subject to its rated bias/temperature behavior at cell voltage. |
| 5 ALRT | Unconnected with explicit KiCad no-connect marker | Firmware can poll SOC/status while ON. If a wake interrupt becomes a requirement, reassess the OFF domain and pull-up supply. |
| 6 QSTRT | GND | No hardware quick-start requested. |
| 7 SCL; 8 SDA | Existing `SYS_I2C_SCL` / `SYS_I2C_SDA` respectively | Shared with the ESP32 and application-only INA232. Place exactly one 2.2 kΩ pull-up on each bus line to **switched `+3V3_APP`**, after checking the entire bus. No always-on battery pull-ups. |

The controller already exports both labels and TP11/TP12. While ON, pulled-up I²C voltage must stay within all devices' specified limits. While OFF, the application supply, both I²C pull-ups and gauge supply all turn off; **check for sneak paths/back-powering through the ESP32, INA232, gauge and switch transitions on the actual circuit**. No still-powered net may leak into the isolated gauge feed.

## Pull-up sizing: do not reuse the convenient 10 kΩ

The manufacturer's I²C table specifies a **300 ns maximum rise time** for SDA and SCL (regardless of whether the clock is run at 100 or 400 kHz), and lists **60 pF gauge input capacitance per bus line**. For a simple open-drain RC rise, 30%–70% rise time is approximately `0.8473 × Rpullup × Cbus`. This is a first-order calculation, not a bus waveform measurement; the 60 pF entry itself has no stated production maximum.

| Candidate resistance | Calculated rise with gauge's 60 pF alone | Maximum *total* modeled capacitance at 300 ns | Assessment |
|---|---:|---:|---|
| 10 kΩ (existing audited `ERJ-2RKF1002X`) | 508 ns | 35 pF | Fails the device's stated limit even before other pins/traces. Do not copy it for this bus. |
| 4.7 kΩ (new exact MPN needed) | 239 ns | 75 pF | Only 15 pF nominal allowance for ESP32, INA232, PCB and test points; insufficient evidence to freeze. |
| 2.2 kΩ ([Panasonic `ERJ-2RKF2201X`](https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ2RKF2201X)) | 112 ns | 161 pF | Selected draft 0402 pull-up, 1%, ±100 ppm/K, using the project's audited ERJ2 land pattern. At 3.3 V its simple current into a LOW output is 1.5 mA per line, beneath the gauge's 4 mA low-output test condition. Actual LOW voltage and bus rise still require review. |

Use 100 kHz for initial firmware bring-up, but do **not** treat a slower clock as a waiver of the manufacturer's rise-time specification. Espressif lists 2 pF **typical** for the module GPIO, TI lists 3 pF INA232 digital input capacitance, and Analog Devices lists 60 pF for the gauge: 65 pF before PCB/test pads. At a conservative illustrative 2.2 kΩ × 1.023 resistance including initial tolerance and a 130 °C × 100 ppm/K excursion, modeled rise time with those listed capacitances is about 124 ns. This is **not a worst-case capacitance proof** because the published gauge and MCU entries lack production maximums. Keep the total line capacitance below the calculated ~157 pF at that resistance, and verify SCL/SDA rise times and LOW levels on the assembled coupon. No extra bus switch or level shifter is selected unless OFF isolation fails. Sources: [Panasonic ERJ series](https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf), [Espressif module](https://documentation.espressif.com/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf), [INA232](https://www.ti.com/lit/ds/symlink/ina232.pdf).

## Superseded always-on current calculation

The gauge draws **up to 40 µA in active mode**. The quoted **5 µA maximum in hibernate** applies when `VRESET.Dis = 1`; with the comparator enabled the datasheet shows 4 µA **typical**, but no hibernate maximum in that row. These figures explain the rejected always-on budget; they do not apply to a successfully isolated OFF gauge.

| USB-absent OFF state | Charger no-input limit + gauge limit | Remaining of 50 µA for protector, switch, regulators and leakage |
|---|---:|---:|
| Gauge active | 6.5 + 40 = 46.5 µA | 3.5 µA, before other always-on loads |
| Gauge hibernating with `VRESET.Dis = 1` | 6.5 + 5 = 11.5 µA | 38.5 µA, conditional on firmware configuration and entry into hibernate |
| Gauge hibernating at POR default comparator configuration | 6.5 µA + an **unspecified maximum** | No defensible worst-case remainder from the quoted typical current |

These historical limits have different datasheet operating conditions and never established PWR-003 compliance. [ADR 0015](../../../docs/decisions/0015-switch-fuel-gauge-with-application.md) replaces this approach: the gauge's own cell feed is cut by a switch contact, and the separate charger remains on protected BAT. Its USB-absent no-input BAT current leaves a **preliminary 43.5 µA remainder** of the 50 µA goal for all other OFF paths (6.5 µA + 43.5 µA = 50 µA). Contact leakage, pack protection, converters and board contamination still require a combined budget and measurement.

With the gauge OFF, **SOC is not tracked during OFF charging**. On the next ON transition the MAX17048 performs power-on quick-start; the manufacturer cautions that this can be misleading unless the cell is relaxed. Firmware must present initial SOC/runtime as provisional after powering ON, especially following OFF charging; measure recovery using the selected pack. The gauge does not need firmware to meet an OFF hibernate mode, and the <50 µA goal remains unchanged.

**Do not use software SLEEP as an OFF-state workaround.** Power is physically disconnected in OFF. The manufacturer's sleep warning still matters if later firmware chooses to enter SLEEP while ON; it would miss self-discharge/charging and skew SOC. Each ON transition is a POR, so firmware must initialize and read gauge status anew.

## Closure before canonical capture / Gate A

1. Choose an exact two-pole latching switch and pack boundary. In ON, gauge VDD/CELL sees only protected cell voltage within the 2.5–4.5 V operating supply range; in OFF, neither pin nor its bypass receives a battery path. The independent control pole must not carry display current. Confirm contact sequencing and fit.
2. Audit the selected 2.2 kΩ exact resistor and candidate 0.1 µF capacitor with the full bus capacitance, powered-off ESP32/INA232 pins and leakage. Measure both line rise times and idle/LOW levels on the coupon.
3. Specify gauge initialization after every ON transition and an explicit provisional-SOC/runtime policy, then qualify SOC recovery following OFF charging against the selected pack. OFF mode does not rely on VRESET.Dis or hibernate configuration.
4. Complete the switch's isolated battery pole on the canonical KiCad power sheet, replace the gauge's assumed source flag with the physically wired rail and extend source/exported-netlist checks. The gauge, bypass, pull-ups and no-connect are staged; run native ERC, render and visual review of this intermediate sheet and again after completing the switch.
5. Measure PWR-003 on a newly assembled/unconfigured board and after firmware configuration, with USB absent and switch OFF, recording current immediately, after 10 minutes and after one hour. Repeat across relevant battery voltage and temperature conditions; also verify OFF qualified-source charging. These times are observation points, **not** a relaxation of the <50 µA requirement.
