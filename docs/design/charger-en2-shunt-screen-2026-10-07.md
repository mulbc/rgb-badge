<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Charger EN2 local-clamp DC screen

**Calculated candidate, not a connected or measured circuit.** Proposed `CHARGER_IN → ERJ2RKF1002X (10 kΩ ±1%) → BQ24074 EN2`, with `LM4040A25IDBZT` cathode on EN2 and anode/third DBZ pin at ground. E1 OUT supplies `CHARGER_IN`; charger `IN` is on that same node. BQ `CE` and `EN1` stay low. No USB 3.3 V rail is connected to EN2.

| Scenario | Calculation | Meaning |
|---|---:|---|
| Minimum BQ operating input, full-range high clamp, high resistor | (4.35 − 2.519) V / 10.1 kΩ = 181.3 µA | Feed current available at the EN2 node. |
| Same, with assumed 20 µA EN2 load | 161.3 µA shunt current | Above TI's 80 µA full-range minimum by 81.3 µA **if** the assumed EN2 load holds. |
| 5.5 V input, nominal values | (5.5 − 2.5) V / 10 kΩ = 300 µA | Normal-mode feed, plus existing charger input draw. |
| 28 V at charger IN, low clamp, low resistor | (28 − 2.481) V / 9.9 kΩ = 2.578 mA | Below TI's 15 mA recommended shunt maximum. BQ IN itself is at its absolute limit; this is a stress comparison, not normal operation. |
| Same 28 V case | 65.8 mW resistor, 6.4 mW shunt | Resistor is below its 100 mW room-temperature rating. Board-local temperature derating remains open. |

TI gives A-grade 2.5 V shunt tolerance ±19 mV over −40…85 °C at 100 µA and maximum minimum-cathode current 80 µA over that range. DBZ pin 1 is cathode, 2 anode, and pin 3 must float or join anode; grounding pin 3 follows TI's recommendation for switching-noise environments. TI specifies BQ EN high at ≥1.4 V, maximum 6 V recommended, 7 V absolute; its 10 µA input-current table point is at **1.4 V only**. The provisional 20 µA load at the 2.5 V clamp is an engineering allowance, not a guaranteed bound. Do not mark H3 closed from this arithmetic.

The proposed node rises from the same admitted input as BQ IN. Its DC level reaches BQ's 1.4 V high threshold before BQ's 4.35 V operating minimum if the actual EN2 leakage stays within the assumed allowance. Attach, source downgrade, detach and E0/E1 trip still require waveform review because stored `CHARGER_IN` energy, shunt turn-on and BQ mode sampling are dynamic. The lower fixed ILIM proposal remains independent; no charger resistor is changed here.

The unlinked [KiCad candidate](../../hardware/coupon/rev-a/staging/charger-en2/charger-en2-candidate.kicad_sch) uses exact resistor and shunt MPNs. Native KiCad 10.0.6 netlist connects R88 pin 1 to `CHARGER_IN`, R88 pin 2 to U38 cathode pin 1 / `CHARGER_EN2`, and U38 anode pin 2 and optional pin 3 to ground. ERC finds zero errors and one expected standalone input-label warning; E1 and BQ are absent. The source has not been independently reviewed or laid out.

Sources: [LM4040 Rev Q, pins and electrical limits](https://www.ti.com/lit/ds/symlink/lm4040.pdf); [BQ24074 Rev N, EN thresholds/current and operating sequence](https://www.ti.com/lit/ds/symlink/bq24074.pdf); [Panasonic exact resistor rating](https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ2RKF1002X). The arithmetic is reproduced in `tools/analyze-power-architecture.py`.
