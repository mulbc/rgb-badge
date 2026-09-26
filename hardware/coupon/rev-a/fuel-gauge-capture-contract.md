<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# MAX17048 fuel-gauge capture contract

Status: source-based circuit requirements and calculations, 2026-09-26. No gauge is placed in the canonical schematic; no PCB or bench result exists. This is the pack-independent portion of the power capture. The source is the [MAX17048/MAX17049 Rev. 7 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX17048-MAX17049.pdf), especially the pin table, electrical specifications, HIBRT/VRESET sections and I²C timing table. The existing [exact-MPN library audit](power-library-audit.md) controls the symbol and footprint.

## Capture connections

| `MAX17048G+T10` TDFN pin | Net / treatment | Basis and limitation |
|---|---|---|
| 1 CTG; 4 GND; exposed pad 9 | GND | Manufacturer pin table. |
| 2 CELL; 3 VDD | Protected battery positive, on the board side of the pack's protection circuit | CELL is internally unconnected for this one-cell part, but the pin table still directs it to battery positive. VDD senses cell voltage and must remain powered with the application OFF. Verify the chosen pack's connector and protection topology before assigning the final net name. |
| 3 VDD | 0.1 µF ceramic bypass to GND at the device | Manufacturer pin table; the existing audited `GRM155R71C104KA88D` is a candidate, subject to its rated bias/temperature behavior at cell voltage. |
| 5 ALRT | Unconnected with explicit KiCad no-connect marker | Firmware can poll SOC/status while ON. If a wake interrupt becomes a requirement, reassess the OFF domain and pull-up supply. |
| 6 QSTRT | GND | No hardware quick-start requested. |
| 7 SCL; 8 SDA | Existing `SYS_I2C_SCL` / `SYS_I2C_SDA` respectively | Shared with the ESP32 and application-only INA232. Place exactly one pull-up on each bus line to **switched `+3V3_APP`**, after checking the entire bus. Never pull these lines up to always-on battery positive: the unpowered application pins could conduct, and the two resistors would add OFF battery current. |

The controller already exports both labels and TP11/TP12. A pulled-up line's voltage is lower than the gauge's allowed I²C pin maximum when VDD is supplied by the cell, but **powered-off injection into the ESP32/INA232 and residual line current must still be checked on the actual circuit**. An always-on gauge does not by itself authorize always-on I²C pull-ups. Power-off must leave each line without a source that back-powers the application.

## Pull-up sizing: do not reuse the convenient 10 kΩ

The manufacturer's I²C table specifies a **300 ns maximum rise time** for SDA and SCL (regardless of whether the clock is run at 100 or 400 kHz), and lists **60 pF gauge input capacitance per bus line**. For a simple open-drain RC rise, 30%–70% rise time is approximately `0.8473 × Rpullup × Cbus`. This is a first-order calculation, not a bus waveform measurement; the 60 pF entry itself has no stated production maximum.

| Candidate resistance | Calculated rise with gauge's 60 pF alone | Maximum *total* modeled capacitance at 300 ns | Assessment |
|---|---:|---:|---|
| 10 kΩ (existing audited `ERJ-2RKF1002X`) | 508 ns | 35 pF | Fails the device's stated limit even before other pins/traces. Do not copy it for this bus. |
| 4.7 kΩ (new exact MPN needed) | 239 ns | 75 pF | Only 15 pF nominal allowance for ESP32, INA232, PCB and test points; insufficient evidence to freeze. |
| 2.2 kΩ ([Panasonic `ERJ-2RKF2201X`](https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ2RKF2201X)) | 112 ns | 161 pF | Selected draft 0402 pull-up, 1%, ±100 ppm/K, using the project's audited ERJ2 land pattern. At 3.3 V its simple current into a LOW output is 1.5 mA per line, beneath the gauge's 4 mA low-output test condition. Actual LOW voltage and bus rise still require review. |

Use 100 kHz for initial firmware bring-up, but do **not** treat a slower clock as a waiver of the manufacturer's rise-time specification. Espressif lists 2 pF **typical** for the module GPIO, TI lists 3 pF INA232 digital input capacitance, and Analog Devices lists 60 pF for the gauge: 65 pF before PCB/test pads. At a conservative illustrative 2.2 kΩ × 1.023 resistance including initial tolerance and a 130 °C × 100 ppm/K excursion, modeled rise time with those listed capacitances is about 124 ns. This is **not a worst-case capacitance proof** because the published gauge and MCU entries lack production maximums. Keep the total line capacitance below the calculated ~157 pF at that resistance, and verify SCL/SDA rise times and LOW levels on the assembled coupon. No extra bus switch or level shifter is selected unless OFF isolation fails. Sources: [Panasonic ERJ series](https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf), [Espressif module](https://documentation.espressif.com/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf), [INA232](https://www.ti.com/lit/ds/symlink/ina232.pdf).

## OFF current and SOC behavior

The gauge draws **up to 40 µA in active mode**. The quoted **5 µA maximum in hibernate** applies when `VRESET.Dis = 1`; with the comparator enabled the datasheet shows 4 µA **typical**, but no hibernate maximum in that row. The previous 11.5 µA charger-plus-gauge estimate therefore depends on configuration and operating state, and cannot be asserted on a newly assembled, unprogrammed board.

| USB-absent OFF state | Charger no-input limit + gauge limit | Remaining of 50 µA for protector, switch, regulators and leakage |
|---|---:|---:|
| Gauge active | 6.5 + 40 = 46.5 µA | 3.5 µA, before other always-on loads |
| Gauge hibernating with `VRESET.Dis = 1` | 6.5 + 5 = 11.5 µA | 38.5 µA, conditional on firmware configuration and entry into hibernate |
| Gauge hibernating at POR default comparator configuration | 6.5 µA + an **unspecified maximum** | No defensible worst-case remainder from the quoted typical current |

These limits have different datasheet operating conditions and must not be treated as a single qualified temperature-range bound. Default HIBRT settings automatically enter hibernate only after the rate remains below its threshold for **longer than six minutes**. Do not assume OFF current falls immediately or that every protected-cell condition triggers automatic hibernate. The datasheet also permits forcing hibernate with `HIBRT = 0xFFFF`; that command remains a **candidate firmware action**, since qualification of SOC behavior across OFF charging and switch cycling is outstanding. A power-on reset restores defaults, so a one-time configuration is not permanent.

This remaining issue is a design choice, not a resistor calculation. Keeping the gauge on continuously preserves SOC tracking during switch-OFF charging, but the worst-case current of a never-configured board remains unproved. Cutting its battery supply with a second pole of the latching slide switch makes the <50 µA goal much easier to budget without any gauge firmware, while forfeiting OFF-period SOC tracking. On the next ON transition the MAX17048 performs power-on quick-start; its datasheet cautions that quick-start is accurate when the battery is relaxed, which cannot be assumed during or immediately after charging. A third option is relaxing PWR-003 to a measured, justified limit. None of these changes is authorized by this calculation alone: the current schematic still has no gauge, and the accepted design retains an always-on gauge pending a deliberate choice.

**Do not force SLEEP to meet the current budget.** The manufacturer warns that in sleep the gauge misses self-discharge and charging and SOC can become wrong. Keep `MODE.EnSleep = 0` and `CONFIG.SLEEP = 0`; this also prevents a low unpowered I²C bus from unintentionally selecting the software-enabled sleep behavior. Firmware should read back and restore configuration on every gauge reset before relying on the 5 µA bound. If a cell is connected while the slide switch remains OFF, the MCU cannot perform this initialization until the next ON cycle. The OFF budget must therefore also be checked on a never-programmed board.

## Closure before canonical capture / Gate A

1. Choose a pack-independent battery-net boundary consistent with the charger and selected protected-pack pinout; confirm gauge VDD always sees only the protected cell within its 2.5–4.5 V operating supply range.
2. Audit the selected 2.2 kΩ exact resistor and candidate 0.1 µF capacitor with the full bus capacitance, powered-off ESP32/INA232 pins and leakage. Measure both line rise times and idle/LOW levels on the coupon.
3. Decide and specify gauge initialization, VRESET.Dis handling and hibernate behavior after POR and while the switch is OFF. Record SOC accuracy trade-offs before forcing hibernate.
4. Capture the gauge, bypass, pull-ups and no-connect in the canonical KiCad sheets; extend source and exported-netlist checks; run native ERC, render and visual review.
5. Measure PWR-003 on a newly assembled/unconfigured board and after firmware configuration, with USB absent and switch OFF, recording current immediately, after 10 minutes and after one hour. Repeat across relevant battery voltage and temperature conditions. These times are observation points, **not** a newly approved relaxation of the <50 µA requirement.
