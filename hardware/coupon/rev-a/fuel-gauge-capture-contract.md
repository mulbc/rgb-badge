<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Switched MAX17048 gauge capture contract

Status: provisional root-linked source, 2026-10-11. [ADR 0015](../../../docs/decisions/0015-switch-fuel-gauge-with-application.md) requires a physically disconnected gauge in OFF; [ADR 0030](../../../docs/decisions/0030-gauge-bus-buffer-selection.md) selects exact `TCA9517ADGKR` isolation. [The source review](../../../docs/development/switched-gauge-capture-review-2026-10-11.md) records native KiCad checks. No board, pack or OFF current has been measured.

## Captured pin and rail map

| Device/contact | Captured connection | Operating meaning |
|---|---|---|
| SW2.5 common / SW2.6 B2 | Protected BAT / `+BAT_GAUGE_SW` | Second pole carries only gauge-domain supply; SW2.4 A2 open. Throw direction, contact sequencing and JCQN mechanical fit remain unqualified. |
| MAX17048 pins 2 CELL and 3 VDD | `+BAT_GAUGE_SW` | Gauge and C39 100 nF bypass lose direct battery supply in physical OFF. |
| MAX17048 pins 1 CTG, 4 GND, 9 EP; 6 QSTRT | GND | Pin 5 ALRT is explicitly no-connected. |
| MAX17048 pin 7 SCL / pin 8 SDA | `GAUGE_I2C_SCL` / `GAUGE_I2C_SDA` | Separate gauge-side A segment. No direct connection to application SDA/SCL. |
| TCA9517A pins 1 VCCA, 2 SCLA, 3 SDAA, 4 GND | Switched BAT, gauge SCL, gauge SDA, GND | Buffer A domain tracks the gauge supply. R101/R102 pull up SCL/SDA to switched BAT; C64 bypasses VCCA. |
| TCA9517A pins 5 EN, 6 SDAB, 7 SCLB, 8 VCCB | `+3V3_APP`, application SDA, application SCL, `+3V3_APP` | Buffer B domain has separate R79/R80 application pull-ups and C65 bypass. |

The exact [MAX17048 manufacturer datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX17048-MAX17049.pdf) controls its pin map, 2.5–4.5 V supply range and 300 ns SDA/SCL rise-time limit. The [TI TCA9517A Rev E datasheet](https://www.ti.com/lit/ds/symlink/tca9517a.pdf) controls the buffer pin map, powered-off behavior and A/B LOW levels. The [C&K JS drawing](https://www.ckswitches.com/media/1422/js.pdf) controls switch contacts; the local symbol's A/B names alone are not physical actuation evidence. No INA232 is populated under [ADR 0021](../../../docs/decisions/0021-external-battery-current-measurement.md).

## Pull-up and timing screen

Both bus segments use exact Panasonic `ERJ2RKF2201X` 2.2 kΩ ±1% pull-ups. For a simple RC line, 30–70% rise time is approximately `0.8473 × R × C`. At an illustrative 1.023 resistance factor, the 300 ns limit gives **157 pF modeled capacitance per segment**; this is a calculation, not a production guarantee because device and PCB capacitance maxima are incomplete. The gauge datasheet lists 60 pF per line. At the 4.23 V planning corner and a 0.977 resistance factor, a gauge-side LOW draws about **1.97 mA** through its pull-up before other contributions. Actual LOW voltage, voltage translation, rise time, intermediate-rail behavior and bus recovery must be measured with the populated coupon. Start firmware at 100 kHz, but retain the 300 ns device rise requirement.

TCA9517A A drives a nearly-ground LOW toward the MAX17048; its B output can be near 0.5 V. The MAX17048's 0.5 V LOW-input limit is why it is on A. Check the B-side LOW margin for every application target, including ESP32, at actual pull-up current. TI's powered-off I/O statement and arbitrary supply-order allowance do not prove isolation through slow rail decay or switch bounce. Record OFF leakage with USB absent at pack voltage/temperature corners and after both cold insertion and normal ON operation. The <50 µA target remains unchanged.

Every ON transition resets the gauge's SOC history while the switch was OFF. During OFF charging it cannot track charge; firmware must label initial SOC/runtime provisional and measure recovery against a known-charge reference. The physical switch, not firmware hibernate, establishes the OFF gauge state.

## Remaining acceptance

Confirm fitted switch throw, footprint orientation, enclosure access and arbitrary contact order. Measure powered-off and intermediate-voltage injection into both buses, line rise/LOW levels, buffer current, boot/reset recovery and USB-absent OFF drain. Verify MAX17048 behavior across the selected pack voltage and after OFF charge. Record hardware/firmware revisions, setup and raw data for every measurement, then include the result in independent Gate A review before fabrication.
