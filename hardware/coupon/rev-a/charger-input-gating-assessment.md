<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Use input protection as the charger permission switch

2026-09-24. Engineering proposal, **not selected or captured**. ADR 0013 remains the implemented policy. This is a concrete simplification to evaluate before adding a separate EN1 actuator; it is not permission to bridge the current draft supply boundary.

## Proposed power domains

Keep the Type-C detector and USB logic available upstream of the permission-controlled power switch. Otherwise an OFF switch would remove its own permission source and prevent startup. TPS70933DBVR can supply the upstream logic from connector VBUS within its specified positive input range. Move the supervisor supply, MR, CT pull-up and bypass to the regulated USB logic domain; do not expose TPS3808 directly to unprotected connector faults. Recheck every upstream capacitor rating and fault limit: the existing 10 V input capacitors do not inherit TPS709's 30 V rating.

Place the eFuse between connector VBUS and **charger IN only**. Fixed charger mode would be EN1 low / EN2 high, with the unchanged permanent ILIM pair. When Type-C permission is absent, disable the eFuse. The charger then behaves as it does with USB power removed: battery operation remains available. ON data over USB-A/default-current sources remains battery-powered; qualified Type-C sources retain OFF charging and charge-through operation.

This could eliminate the separate charger-mode sink and remove PG from the charge-permission path. It does not remove the need for verified enable defaults, source-voltage qualification or the complete-port current budget. Upstream logic consumption still comes from USB when the charger path is disabled.

## Why it is worth pursuing

The eFuse EN/UVLO falling threshold is at least 1.076 V. A TPS3808 RESET low of 0.4 V under its specified supply/load conditions would therefore have **0.676 V static disable margin**. Directly treating that same RESET level as a BQ24074 logic low only reaches the charger's 0.4 V limit. The power-switch approach provides a much more forgiving control threshold and avoids generating a charger standby high before the logic supply is ready.

The input switch must still be current-limited and slew-controlled. Its fault threshold is not a replacement for the BQ24074's 0.9753 A maximum programmed input current. No current setting is raised by this proposal. The existing 3.32k eFuse example can act below the charger ceiling; the selected threshold must account for this without importing typical arithmetic as a guaranteed limit.

## Enable-node screening, not an approved network

A pull-up to the **same regulated rail powering the supervisor**, with independent open-drain inhibit paths, avoids a raw-VBUS pull-up asserting EN before the supervisor has power. The existing 10k RESET pull-up cannot simply remain in parallel with a new weak pull-up.

For illustration only, a 270k pull-up with ±1% total error gives:

| Calculated check | Result | What it does and does not establish |
|---|---:|---|
| Pull-up current at 1.3 V, conservatively allowing zero output voltage | 4.86345 µA maximum | Below the 15 µA load used for TPS3808's low-voltage power-up RESET specification |
| Remaining allowance within that 15 µA condition | 10.13655 µA | All other currents sourcing into RESET must fit; no bound is yet established for intermediate-rail logic leakage |
| Total sink leakage allowing EN to exceed its 1.223 V maximum rising threshold at 3.234 V | 7.37440 µA | Static high-state budget only, before noise margin |
| Budget after 0.3 µA supervisor and 0.1 µA EN leakage allowances | 6.97440 µA | Not a verified bound for the proposed logic sink or PCB leakage |

These use KCL and the published threshold/leakage limits, not a circuit simulation. 270k is not an exact selected resistor MPN. TPS3808's 0.8 V power-up RESET figure has a supply-rise condition (at least 15 µs/V) and specified loading. Do not extend SN74LVC1G06's Ioff specification at VCC=0 across the entire intermediate rail range. Below the supervisor's guaranteed range, a same-rail pull-up is helpful but only if other pins cannot inject enough current to raise EN. Falling-supply response remains a transient qualification task.

## Decision needed from engineering before capture

Resolve these together as one functional increment, rather than generating a separate owner export for each:

1. Choose the eFuse variant and exact ILM/dVdt/OVLO parts. TPS259474 retains cutoff instead of sustained clamp dissipation. TPS259472's recommended-input note limits normal operation to its selected clamp threshold, whose low corner is 5.25 V for the open setting; it cannot be presented as an unconditional pass-through at 5.5 V merely because downstream parts tolerate 6.2 V. Neither candidate is selected here.
2. Define how both source voltage and logic validity inhibit EN. The present three-input permission expression cannot be removed without an equivalent state table and an ADR. A same-rail supervisor and eFuse intrinsic UVP alone are not automatically equivalent to the current VBUS_VALID boundary.
3. Select the actual inhibit network with startup/off/high-level leakage and slew bounds. Remove or recalculate all existing pull-ups and Schmitt-input loads attached to its node. No floating enable or direct raw-VBUS pull-up.
4. Strap BQ24074 EN1/EN2 with valid levels over powered/unpowered states, including input leakage and possible injection when charger IN is disconnected. Review stored input-capacitor energy during revocation; it is not continuing draw from the USB source.
5. Include both upstream USB logic and downstream charger current, inrush, discharge/retry behavior and source-advertisement changes in one power-state assessment. Preserve pack protection, NTC, timers and Gate A.

No user preference is needed to perform this engineering comparison. A material architecture change must be recorded before changing the canonical schematic. The current source and native acceptance remain unchanged.

## Controlled sources

- TI TPS25947 SLVSFC9C, May 2026, sections 6.3/6.5 and 7.3: https://www.ti.com/lit/ds/symlink/tps25947.pdf. SHA-256 `8f96de389903091650d4f462dcfad3210071c3ae7093623a7978f34baf8a65b4`.
- TI TPS3808 SBVS050N, August 2026, electrical characteristics and power-up-reset footnotes: https://www.ti.com/lit/ds/symlink/tps3808.pdf. SHA-256 `74d889c0f68af88032f1633c26381817cc03e10d9fd3b4c177a044ad3ed86eed`.
- TI BQ24074 SLUS810N, October 2021, EN1/EN2 mode table and logic electrical limits: https://www.ti.com/lit/ds/symlink/bq24074.pdf.
- TI SN74LVC1G06 SCES295AB, October 2025, electrical table and partial-power-down conditions: https://www.ti.com/lit/ds/symlink/sn74lvc1g06.pdf.
- TPS709 input/capacitor scope remains controlled by ADR 0014 and the existing U29 audit.
