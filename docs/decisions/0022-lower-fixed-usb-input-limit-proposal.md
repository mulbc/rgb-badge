<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0022: Proposed lower fixed charger input limit

- Date: 2026-10-07
- Status: **Selected for provisional Rev A charger-core capture on 2026-10-10; gate/pack and operating qualification remain open**
- Would amend: the two-resistor fixed ILIM population in accepted ADR 0013 and the current-setting assumption in proposed ADR 0018
- Retains: Type-C-only hardware charging permission, 5.5 V normal input, battery/NTC/timer safeguards, existing current ceilings and independent Gate A

## Proposal

Populate only the already audited Panasonic `ERA2AEB3651X` 3.65 kΩ resistor at BQ24074 `ILIM`, omitting the parallel `ERA2AEB3481X` 3.48 kΩ branch. The input limit remains fixed in hardware, with no firmware grant or current increase. This lower setting is now selected for the provisional charger core; it does not approve the still-absent input gate, pack connector or fabrication BOM.

Using the previously required **±1% total effective-resistance envelope**, TI's `KILIM` range for 200–500 mA gives a calculated BQ24074 input-limit interval of **0.3608–0.4760 A**. The existing parallel pair instead calculates to **0.834–0.975 A**. At TI's published nominal `RILM=3.32 kΩ` test point, the TPS259474 breaker threshold is 0.850–1.150 A, leaving **0.374 A arithmetic separation** between the charger's calculated upper input limit and that test point's minimum threshold, before USB-logic load. This is a DC comparison, not a guaranteed eFuse resistor-tolerance or transient bound. The nominal 1.5 A Type-C source has more than 1.024 A arithmetic margin above the charger limit for USB logic and other port loads; all loads and transients still require a full-port budget.

The separate proposed 2.49 kΩ `ISET` setting reaches **0.396 A** at its high calculation corner, while the lower `ILIM` setting can reach only **0.361 A** at its low corner. Input limiting can therefore reduce actual charging even with the display off; system load gets priority, and the protected pack may supplement bright operation. This is acceptable only if the eventual exact pack, charge-time plan and PWR-006 operating tests allow it. It cannot be described as guaranteed 396 mA charging. A 950 mAh pack's ideal 80%-capacity time at 396 mA is about 115 minutes before input limiting, precharge, taper or thermal effects. ADR 0016 permits slower pack-rated charging, but exact-pack charge timing remains open.

## Why this helps and what remains

The single existing resistor removes one placed component and the present **DC threshold overlap** between the 0.975 A charger corner and the 0.850 A eFuse test-point minimum. It also lowers the maximum USB-delivered charger power available for linear dissipation. It does **not** settle H2: choose exact eFuse ILM, OVLO, dVdt and ITIMER parts; include RILM tolerance, USB-logic current, both switch start-up capacitors, retry, short-circuit energy and disconnect/reverse behavior. It does **not** settle H3 default-disabled permission or H1 pack qualification. The 2026-10-10 canonical BQ core connects the ILIM resistor but holds EN2 low, so the resistor does not yet determine operating current. Native ERC/netlist validate that capture, not USB transient or thermal behavior.

The arithmetic is reproduced in [`analyze-power-architecture.py`](../../tools/analyze-power-architecture.py) and its [JSON output](../design/power-architecture-2026-10-05.json), under `lower_fixed_input_limit_screen`. Manufacturer sources: [BQ24074 Rev N, electrical table and §9.3.4](https://www.ti.com/lit/ds/symlink/bq24074.pdf), and [TPS25947 Rev C, electrical table and §7.3.5](https://www.ti.com/lit/ds/symlink/tps25947.pdf). The manufacturer data do not establish this circuit's compact-board thermal or fault performance.
