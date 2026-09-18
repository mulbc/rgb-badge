<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Charger actuator screening

Status: candidate investigation, 2026-09-18. Candidate library added; no selected BOM change or captured circuit. ADR 0011's hardware-only boost and passive charger-standby requirements remain controlling.

## Candidate direction

Investigate exact `ADG4612BCPZ-REEL7` for the actuator. Its [manufacturer page](https://www.analog.com/en/products/adg4612.html) lists the exact LFCSP model in production and the family as recommended for new designs on the inspection date. Stock, price and assembler acceptance have not been checked; this is not purchase advice.

The [ADG4612/ADG4613 Rev. 0 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/ADG4612_4613.pdf), Tables 3 and 5 and the operating-mode discussion, documents powered-off signal isolation and four active-high switches. At the specified 5 V supply conditions, maximum on resistance is 17 ohm per channel and normal off leakage is 80 nA through 85 C. Isolation-mode leakage has a separate, larger specification. Do not use the headline dual-supply resistance or room-temperature leakage as this design's limits.

A candidate arrangement uses two series channels for the boost resistor and two for the EN1 sink. In each path, one channel would follow the normal permission output and the other an independently qualified supply signal. This could keep the final control boundary in the input domain even when the 3.3 V logic rail fails. The exact qualification signal, loading and timing are **not yet designed**. Reusing the same unqualified gate signal twice provides no independent inhibition.

## Useful calculation without circuit approval

Using two 17-ohm channels as a conservative 34-ohm ON-resistance allowance, the existing calculation returns a boosted lower bound of **0.829568 A**. The upper bound remains **0.975238 A**, conservatively allowing zero switch resistance. This follows:

`python3 tools/check-power-design.py` → `selected_input_bounds(boost=True, switch_resistance_max="34")`

These values include the retained ±1% total resistance envelope and TI's high-range programming factors. Positive switch resistance reduces the minimum available current; it does not raise the maximum. The low-branch leakage contribution is excluded, so these results do not close the 2 mA programming-network allocation.

## Alternatives screened

- [TMUX1101](https://www.ti.com/lit/ds/symlink/tmux1101.pdf): very low powered leakage, but fail-safe SEL is not powered-off protection for S/D. Do not connect a potentially live ILIM node to an unpowered signal pin without proving its voltage range and supply sequence.
- [TMUX1511](https://www.ti.com/lit/ds/symlink/tmux1511.pdf): powered-off protection is limited to 3.6 V. It cannot automatically be used for a charger control node pulled to the 5 V input. An ILIM-only application would need a separately justified signal envelope, including charger startup.
- The existing row `2N7002K-7` is not automatically qualified for this precision actuator. Gate threshold alone does not bound ON resistance at the actual drive voltage or leakage over temperature.

These are application-specific screening observations, not claims that these parts are generally unsuitable.

## Required work before selection and capture

1. Package/pin review is complete using the owner-supplied PDF; see the [candidate library audit](charger-actuator-library-audit.md). [Native rendering at 2b7a468](../../../docs/development/actuator-library-review-2b7a468.md) passed; assembly qualification remains pending.
2. Define normal, unpowered, rising and falling supply conditions, including a grounded reference before other signals. A powered-off isolation specification is not a guarantee for every intermediate rail voltage or a replacement for an undervoltage detector.
3. Prove EN1/EN2 high/low levels including charger input current and pull-down behavior; control-input specifications at one test voltage are not universal current bounds. Ensure both mode inputs default to standby before the logic LDO starts.
4. Bound ILIM-node voltage, off leakage and their effect on charger current. The BQ24074 `K/R` specification alone is not a guaranteed conversion factor from arbitrary externally injected pin current to input current. Do not invent a minimum ILIM voltage to make the leakage calculation pass.
5. Budget control loading and supply current at the actual 3.3 V control levels with a 5 V switch supply. A supply-current limit specified with rail-to-rail controls does not necessarily cover those intermediate levels.
6. Close supply-loss/advertisement-change timing and programming-node charge injection, then document the chosen topology in an ADR before changing requirements or source.

Manufacturer sources were inspected as online text on 2026-09-18. The existing [TI BQ24074 source](https://www.ti.com/lit/ds/symlink/bq24074.pdf), pin descriptions, startup sequence and logic/current tables remain controlling. No new source should be considered visually audited until its drawing has been inspected.

The supplied Rev. 0 drawings were visually inspected on 2026-09-18. Table 11 specifies isolation for VDD = 0–0.8 V, while the operating prose says up to 1 V and normal operation starts at 2.7 V. Use the narrower tabulated range; behavior throughout 0.8–2.7 V remains unproven. The earlier PDF-access blocker is closed.
