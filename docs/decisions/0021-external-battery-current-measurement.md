<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0021: Measure battery current externally during validation

- Date: 2026-10-06
- Status: **Accepted for coupon and final-badge capture; hardware validation pending**
- Supersedes: the production-intent INA232 battery-path monitor and approximately 10 mΩ shunt in the original project plan and the current-sensing row of proposed ADR 0018
- Retains: switched MAX17048 state-of-charge reporting, exact-pack charge/current limits, OFF-drain limit, runtime and charge-through measurements, hardware safeguards and independent Gate A

## Decision

Do not populate an on-board battery-current monitor or series measurement shunt on Coupon Rev A or the five intended final badges. The `INA232AIDDFR` library remains as historical candidate source, not a selected BOM item. Firmware reports battery voltage and state of charge from the switched MAX17048 while ON; it does not claim live battery-current or battery-power telemetry.

Measure battery charge/discharge and OFF leakage with a correctly polarized **inline instrument or protected-pack test harness** during coupon/final validation. Record instrument model, range, burden voltage, sample rate, pack and board revision with raw logs. Measure USB input separately. The measurement adapter must preserve the pack protection and charger NTC arrangement and must be checked against expected charge and discharge pulses before use. No battery-current limit, current-setting resistor or charger safeguard changes through this decision.

## Reason and consequence

The accepted product requirements call for measured runtime, USB limits, charge current and OFF leakage; they do not require signed current telemetry during normal playback. The MAX17048 estimates state of charge without a sense resistor. Removing the monitor also removes its power/injection review, dedicated shunt/drop/heat, Kelvin routing and I²C traffic. A [tight converter placement screen](../../mechanical/dual-row-package-screen-2026-10-06.md) fits all sixteen proposed dual-row package courtyards when the monitor's IC box is omitted; adding that box leaves one pair unplaced in the same heuristic. This is supporting area evidence, **not** proof of complete final-board fit. Charger/input support, display interlock, routing and the accepted row-stage decision still need engineering work.

The cost is loss of live signed battery-current/power readout and reliance on an inline instrument for validation. The runtime estimate in firmware must use measured board profiles, actual frames and the selected pack rather than pretend to read current. If live current telemetry later becomes a product requirement, reopen this decision with a revised layout, shunt error/current/thermal budget and powered-off behavior review before restoring the part.
