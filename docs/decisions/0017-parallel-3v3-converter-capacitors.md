<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0017: Parallel capacitors for the 3.3 V converter coupon

- Status: Provisional coupon capture target; footprint, complete rail and Gate A review pending
- Date: 2026-09-30
- Applies to: TPS631000DRLR 3.3 V application rail, not the USB-only LDO or charger IN capacitor

## Context

The exact TI example parts `GRM187R61A226ME15` (22 µF input, 10 V) and `GRM219R60J476ME44` (47 µF output, 6.3 V) have owner-supplied Murata SimSurfing DC-bias curves at 25 °C and AC 0.5 Vrms. The [capture contract](../../hardware/coupon/rev-a/3v3-converter-capture-contract.md) identifies the CSV by hash and interpolates 6.462 µF at the BQ24074's 4.5 V regulated OUT maximum for one input capacitor, and 16.133 µF at the illustrative 3.433 V application-rail high for one output capacitor. TI's TPS631000 minimum effective values are 4.2 µF input and 10.4 µF output.

If a hypothetical independent 20% initial-tolerance reduction and 15% temperature reduction are multiplied with the 25 °C curves, one input capacitor reaches 4.394 µF and one output reaches 10.970 µF at those biases. These leave little margin for aging or further variation. This calculation is **not** an exact manufacturer's combined worst-case bound: Murata's curve is characteristic data, and the temperature and aging effects under bias still need source evidence.

## Decision

For the **coupon's provisional schematic and placement**, target **two identical input capacitors** `GRM187R61A226ME15` in parallel from local converter VIN to ground, and **two identical output capacitors** `GRM219R60J476ME44` in parallel from local converter VOUT to ground. Keep the two nearest capacitors in short local VIN/GND and VOUT/GND loops; do not place the second capacitor far away and count its nominal value as equivalent high-frequency bypass. These are two extra PCB parts, but no additional MPNs or footprint types. Exact footprint, placement, part suffix, supply-chain and assembly reviews precede capture/release. Do not silently change the charger IN capacitors: TI's charger USB-inrush discussion distinguishes capacitance ahead of its input current limit from system capacitance behind it.

TI explicitly permits increasing TPS631000 input capacitance without limit and specifies no upper limit on output capacitance. This supports the candidate topology, **not** a guarantee of startup or transient performance. The BQ24074 limits input current into its system OUT, but the finished charge-through and switch-ON startup waveforms must be checked with the added capacitance; additional OUT loading may delay startup or cause DPPM/supplement operation. Output capacitance can reduce voltage overshoot/undershoot while increasing transient response time. Keep the existing converter, resistor divider, switch policy and charge-current ceilings unchanged.

## Numerical screen and release conditions

At the stated biases, the two-capacitor 25 °C curve sums are 12.924 µF input and 32.266 µF output. Multiplying by **hypothetical** independent factors `0.80 × 0.85 × 0.90` (initial tolerance, temperature and an additional 10% aging sensitivity) gives approximately **7.909 µF input** and **19.747 µF output**. These exceed TI's respective 4.2 µF and 10.4 µF minima, but the 10% aging factor is an engineering scenario, **not a Murata guarantee**, and correlated lot variation is possible. Doubling the parts doubles a characteristic curve; it does not turn that curve into a certified minimum.

Before freezing the BOM or fabrication package:

1. Obtain the exact-order-code Murata temperature-under-bias and aging evidence, or another defensible combined lower-bound method. Confirm effective input ≥4.2 µF and output ≥10.4 µF throughout their true DC-bias, temperature and life envelopes, including the high rail voltage.
2. Verify the finished `SYS` rail's maximum including USB attach/detach, standby/permission transitions and fault recovery. BQ24074's 4.5 V regulated-OUT maximum is a steady condition, not a transient bound. Respect the converter's 5.5 V operating maximum and the capacitors' ratings.
3. Audit the two exact Murata land patterns and finished PCB placement. Check hot-loop geometry, return path, space behind the LED array, height and assembly process. Record any size/weight/cost effect in the complete badge model.
4. On the coupon, measure cold/hot startup, OFF-to-ON, charging transitions, RF and display load steps at the ESP32 pads, charger OUT and converter VIN/VOUT. Check the 3.0–3.6 V module operating range and restart/overshoot behavior. Independent Gate A review remains mandatory.

Sources: [TI TPS631000 Rev. C](https://www.ti.com/lit/ds/symlink/tps631000.pdf), §§5.3 and 7.2.2.3–4; [TI BQ24074 Rev. N](https://www.ti.com/lit/ds/symlink/bq24074.pdf), §§8.5 and 9.3.2–4; owner-supplied Murata SimSurfing CSV identified and summarized in the capture contract. No PCB or battery order is authorized by this decision.
