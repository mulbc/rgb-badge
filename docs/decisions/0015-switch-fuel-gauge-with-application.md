<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0015: Switch the fuel gauge with the application

- Status: accepted for coupon capture; exact latching switch, pack, native schematic and Gate A pending
- Date: 2026-09-26
- Supersedes: the always-on fuel-gauge placement in ADR 0004 and the pre-capture power table
- Retains: autonomous qualified-source OFF charging (ADR 0013), physical latching OFF, protected/NTC pack and the <50 µA USB-absent OFF requirement

## Decision

The owner's 2026-09-26 choice is to **disconnect `MAX17048G+T10` battery power when the physical latching switch is OFF**. The charger BAT path and hardware charge indication remain connected to the protected battery so supported Type-C 1.5 A/3 A sources can charge autonomously with the switch OFF. The slide switch must not carry display or application load current.

For capture, seek a two-pole latching ON/OFF slide switch. One pole supplies only the gauge VDD/CELL and its local bypass from protected BAT; the other pole controls application-converter enable/interlock as already planned. Both gauge and application are OFF whenever the switch is OFF. A different circuit that offers the same hard-disconnect and worst-case leakage proof needs its own review before substitution. Choose the exact switch MPN, land pattern, actuation orientation, contact rating, contact sequence, envelope and service life before capture. Do not replace the separate charger/source permission logic with this switch.

**Sourcing/fit candidate:** C&K / Littelfuse `JS202011JAQN` is a right-angle surface-mount DPDT latching slide switch with a 2 mm travel, 6 V / 300 mA contact rating and a published manufacturer drawing; it can be arranged at the badge's top long edge and use only its two commons and one throw per pole. The unused throws are explicitly no-connected. DigiKey listed 24,719 in stock at $0.96 each on 2026-09-26; LCSC lists exact MPN as C221664, though current lot/traceability and assembler acceptance remain unverified. Its contact timing is **not specified** by the distributor: independent enable pull-downs must default the application/display OFF throughout bounce or one-pole-before-the-other movement. Mechanical fit, pad map and enclosure access are still to be audited against the manufacturer drawing; this is a candidate, not yet a frozen assembly MPN.

The I²C pull-ups are supplied solely from switched `+3V3_APP`. The provisional exact 2.2 kΩ candidate is Panasonic `ERJ-2RKF2201X`, sharing the audited 0402 Panasonic ERJ2 land pattern. It is a first-order RC choice, not permission to exceed the gauge's 300 ns rise-time or to back-power an unpowered device during switching. The [capture contract](../../hardware/coupon/rev-a/fuel-gauge-capture-contract.md) controls the pin map and measured bus checks.

## Rationale and consequences

The MAX17048 datasheet gives 40 µA maximum active supply current. Its 5 µA **maximum** hibernate current requires `VRESET.Dis = 1`; the default comparator-on hibernate row only states 4 µA typical. On a cell first connected while the slide switch is OFF, the MCU cannot configure the gauge. With the charger's 6.5 µA no-input limit, an active gauge would leave only 3.5 µA of the 50 µA budget for protection and all other leakage. Cutting gauge supply removes this firmware-at-battery-insertion dependency; the remaining charger, pack protection and disabled-rail leakage still need a complete worst-case budget and physical measurement. No PWR-003 compliance is claimed by this decision alone.

The gauge **cannot track discharge, self-discharge or OFF-state charging** while unpowered. On ON it performs power-on reset and estimates SOC from voltage; the manufacturer warns that quick-start can be misleading while the cell is not relaxed, particularly after OFF charging. Firmware must treat the first post-ON SOC as provisional, avoid showing an unjustified precise runtime estimate until qualified, and compare recovery behavior against a known-charge baseline on the coupon. If that behavior proves unacceptable, revisit the trade-off in a new ADR; do not reconnect the gauge to BAT silently. No automatic display dimming is introduced.

## Verification

1. Confirm the switch pole isolates gauge VDD/CELL and the bypass from protected BAT in OFF, and has no unexpected sneak path through SDA/SCL/ALRT/QSTRT, connector or ESD networks. The MAX17048 datasheet does not specify powered-off SDA/SCL leakage: check the interval when the application bus remains high but the gauge pole has opened, and provide a bounded isolation/sequence design or qualified evidence before direct connection. Check break/make transitions with converter enable under switch bounce.
2. With USB absent, measure OFF battery drain before firmware has ever run and after normal operation, at several protected-pack voltages and ambient conditions. Account for the exact pack protector, charger and regulators; require **<50 µA after settling** as PWR-003 specifies.
3. While OFF, confirm permitted Type-C charging and charge status still function without the MCU/gauge; default-current sources remain in charger standby. Confirm the charge current and pack NTC/timer hardware independently.
4. Record gauge boot delay, I²C rise/LOW levels, powered-off leakage and SOC error following an OFF full-charge interval, an OFF partial-charge interval and battery insertion. Compare the reported SOC with an independently logged discharge/charge reference; do not claim a tolerance before setting it against the chosen pack.
5. Verify physical switch fit, footprint, assembly orientation and accessibility in the complete 110 × 35 × 11 mm badge, then include this decision in independent Gate A review.

Sources: [Analog Devices MAX17048/MAX17049 Rev. 7](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX17048-MAX17049.pdf) (supply-current table, POR/quick-start and pin descriptions); [TI BQ24074](https://www.ti.com/lit/ds/symlink/bq24074.pdf) (no-input BAT current); [Littelfuse/C&K JS series drawing](https://www.littelfuse.com/assetdocs/littelfuse-ck-slide-js-series-datasheet?assetguid=aba42b08-0d2c-423b-813d-a2faa5a3bb14); [DigiKey exact-part listing](https://www.digikey.com/en/products/detail/c-k/JS202011JAQN/6137629); [LCSC C221664](https://lcsc.com/product-detail/Slide-Switches_C-K-JS202011JAQN_C221664.html). These are datasheet calculations, candidate sourcing and a mechanical proposal, not a hardware measurement.
