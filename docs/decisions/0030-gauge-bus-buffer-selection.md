<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0030: Exact switched-gauge bus buffer for capture

- Date: 2026-10-11
- Status: Accepted for library and provisional schematic capture; powered transition and LOW-level qualification pending
- Relates to: ADR 0015, ADR 0018 and PWR-003

## Decision

Select exact TI `TCA9517ADGKR` (8-pin VSSOP DGK) for the MAX17048 I²C boundary. Put the switched battery/gauge segment on A (VCCA pin 1, SCLA 2, SDAA 3), and the application 3.3 V segment on B (SDAB 6, SCLB 7, VCCB 8); GND is pin 4 and EN pin 5. Give each segment its own SDA/SCL pull-ups to its local rail, use 100 nF local decoupling at both supplies, and keep the gauge VDD/CELL plus its A-side pull-ups on the physical switch's second pole. The B-side remains on `+3V3_APP`. Do not connect the gauge directly to the controller bus after capturing this boundary.

TI's Rev E datasheet allows A at 0.9–5.5 V, B at 2.7–5.5 V, arbitrary supply ordering, and says I/O is high-impedance with either supply zero. It specifies a nearly-ground A-side LOW but a buffered B-side LOW near 0.5 V; the MAX17048 belongs on A because its LOW-input limit is 0.5 V. The manufacturer package drawing gives an eight-contact 0.65 mm-pitch DGK body and a 1.4 × 0.45 mm example land. Use an exact project-local symbol/land with no external model dependency. `TCA9517A` without the `A`, other packages or alternate ICs are not silent substitutions.

## Open qualification

The buffer's powered-off statement does not by itself prove isolation while either rail decays through intermediate voltage. Check pull-up current, B-side LOW margins for every controller/target, A-side MAX17048 limits, EN behavior, back-power/leakage, rail-order/contact bounce, bus recovery and current consumption in the complete circuit. Verify the switch throw and footprint orientation before board release. No gauge or board has been electrically tested, and Gate A remains required.

Sources: [TI exact orderable part](https://www.ti.com/product/TCA9517A/part-details/TCA9517ADGKR); [TI TCA9517A Rev E datasheet](https://www.ti.com/lit/ds/symlink/tca9517a.pdf), §§4, 5, 8–10 and DGK package drawing; [C&K JS switch drawing](https://www.ckswitches.com/media/1422/js.pdf).
