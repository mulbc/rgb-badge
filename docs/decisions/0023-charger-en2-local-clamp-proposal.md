<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0023: Proposed charger EN2 local clamp

- Date: 2026-10-07
- Status: **Selected for provisional Rev A source capture on 2026-10-10; load/transient qualification and fabrication approval open**
- Relates to: ADR 0018 H3 and the charger pin-boundary review

2026-10-09 revision: use the same-family 2.5 V shunt instead of the initial 3.0 V candidate. It increases the calculated minimum-input cathode-current margin without adding a part or changing the 10 kΩ feed; the unbounded EN2 load and transition holds remain.

## Proposal

Derive BQ24074 `EN2` from the admitted `CHARGER_IN` domain through an exact 10 kΩ ±1% Panasonic `ERJ2RKF1002X` resistor. Clamp that node to ground with a 2.5 V TI `LM4040A25IDBZT` shunt reference. Connect its DBZ pin 1 cathode to `EN2`, pin 2 anode to ground, and pin 3 to ground as TI permits. Keep `EN1` and `CE` low. This is a local, passive mode source: an open E1 gate cannot be back-powered through EN2 from USB logic, and a powered E1 output cannot directly apply its fault voltage to the 7 V-rated EN2 pin.

The [EN2 screen](../design/charger-en2-shunt-screen-2026-10-07.md) records the DC calculations and limits. The exact resistor already has a project-local symbol/footprint and its manufacturer lists 0.1 W rated power. The formerly unlinked [KiCad candidate](../../hardware/coupon/rev-a/staging/charger-en2/charger-en2-candidate.kicad_sch) remains as historical source evidence; the exact resistor and shunt are now included on the root-linked charger core, joining BQ EN2 to its admitted-input boundary. The shunt's canonical pin/pad and land geometry were checked against TI Rev Q and its native KiCad SVG before this source capture. E1 itself remains absent. This source setting does not alter the charger current ceilings or bypass NTC, protection or safety timers.

## Acceptance boundary

At BQ's 4.35 V minimum operating input, the network has a calculated 181.3 µA minimum feed current at the resistor and shunt voltage corners. Reserving an **assumed**, unverified 20 µA for BQ EN2 leaves 161.3 µA for the shunt, above TI's 80 µA full-range minimum. TI only publishes EN2 high-state input current at a 1.4 V test voltage, so the 20 µA reserve at about 2.5 V is not a manufacturer bound. Confirm it or measure it on a coupon before accepting this as a guaranteed clamp. E1 OUT waveforms, resistor derating on the compact board, and transient behavior remain H2/H3 work. No board exists and no hardware validation is claimed.

Sources: [TI LM4040 Rev Q](https://www.ti.com/lit/ds/symlink/lm4040.pdf), [TI BQ24074 Rev N](https://www.ti.com/lit/ds/symlink/bq24074.pdf), [Panasonic ERJ2RKF1002X](https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ2RKF1002X).
