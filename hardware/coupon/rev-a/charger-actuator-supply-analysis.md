<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Candidate actuator supply analysis

**Superseded for active design by [ADR 0013](../../../docs/decisions/0013-type-c-only-fixed-current-charging.md):** no switched ILIM branch or ADG4612 actuator is planned. Retained as investigation/library history; its unresolved switch-leakage questions are not active design blockers. Physical charger standby control still requires qualification.

2026-09-18. Conditional calculation, not circuit selection, transient simulation or bench evidence. The native-reviewed ADG4612 library remains a candidate. This narrows the unresolved supply question without changing ADR 0011 or current ceilings.

## Shared supply removes one static overlap

[TI BQ24074 SLUS810N](https://www.ti.com/lit/ds/symlink/bq24074.pdf), §8.5 and §9.3.1–2: rising UVLO is 3.2–3.4 V; hysteresis is 0.2–0.3 V. Below UVLO the input FET is off and mode controls are ignored. [ADG4612 Rev. 0](https://www.analog.com/media/en/technical-documentation/data-sheets/ADG4612_4613.pdf), Table 5, gives 2.7 V minimum operating supply. Sources rechecked 2026-09-18 against the supplied/local copies.

If ADG VDD and charger IN share the **same protected node**, with common ground and negligible local voltage difference:

- Earliest charger turn-on: 3.2 V; margin to ADG minimum: 0.5 V.
- Lowest possible falling charger cutoff: 3.2 − 0.3 = **2.9 V**; margin: **0.2 V**.

This is a conservative combination of independent extremes, not a typical-value calculation. Thus the ADG 0.8–2.7 V unspecified interval need not overlap static charger input conduction in that topology. It does not establish signal-pin leakage, battery backfeed or whole-device current below UVLO. A separately switched or filtered ADG supply invalidates the shared-node assumption.

## Voltage versus timing

For a screening calculation define D as the maximum ADG local-supply deficit relative to charger IN, S as falling slew in V/µs, and T as total response delay in µs. The remaining margin is:

`M = 0.2 V − D − S × T`

All three bounds must come from the eventual topology and guaranteed timing; none is currently qualified. A hypothetical D = 0.05 V, S = 0.01 V/µs and T = 20 µs yields M = −0.05 V. This is a counterexample to treating the static margin as a transient proof, not a prediction of board behavior. Positive M is only a necessary voltage-envelope screen: it does not prove control defaults, input thresholds, switch settling or the charger response model.

The existing [TPS3808 source](https://www.ti.com/lit/ds/symlink/tps3808.pdf), SBVS050N §6.6, lists a **typical** 20 µs SENSE-to-RESET delay under its stated overdrive/loading conditions; its MAX entry is blank. Do not silently use that number as a guaranteed 20 µs cutoff. Its reset-release delay is a separate quantity. A source-qualified delay bound or a topology that tolerates the uncovered interval is still needed.

## Do not extend the resistance guarantee

ADG Table 3 characterizes the 17 Ω maximum at VDD = 4.5 V, with its stated signal/current/temperature conditions. The 2.7 V operating minimum does not extend that resistance bound to 2.7 V. The gap between the characterized supply and the worst falling charger cutoff is **1.6 V**.

Accordingly, the earlier two-channel 34 Ω / 0.829568 A boosted-current lower bound remains restricted to its characterized supply envelope and does not describe a collapsing rail. The conservative zero-switch-resistance high-current bound is unchanged, but leakage remains excluded. Future VBUS qualification must distinguish the 4.5 V performance envelope from the 2.7 V operating minimum and include local drop, threshold tolerance and response time.

## Next circuit constraints

- Investigate powering the actuator directly from the same protected input as charger IN; no circuit change is approved here.
- Prove EN1/EN2 standby levels before permission logic operates and when its rail is absent, including their internal pull-downs.
- Keep source permission removal independent of the application MCU, and bound advertisement-loss timing even when supplies remain healthy.
- Resolve control loading, ILIM leakage, input protection and rail-loss timing before treating the candidate as qualified.

`actuator_supply_screen()` in `tools/check-power-design.py` reproduces the voltage margins and explicit hypothetical loss cases. Tests reject non-finite/negative bounds and preserve the exhausted-margin counterexample. The strict USB-closure gate remains blocked. No KiCad source changed and no new native export is required.

Validation: all 17 power-design tests passed on 2026-09-18; the strict closure command returned 1 as intended; `git diff --check` passed. These checks do not rerun or supersede the accepted native library review.
