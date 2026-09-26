<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Use input protection as the charger permission switch

2026-09-24. Engineering proposal, **not selected or captured**. ADR 0013 remains the implemented policy. This is a concrete simplification to evaluate before adding a separate EN1 actuator; it is not permission to bridge the current draft supply boundary.

## Proposed power domains

Keep the Type-C detector and USB logic available upstream of the permission-controlled power switch. Otherwise an OFF switch would remove its own permission source and prevent startup. TPS70933DBVR can supply the upstream logic from connector VBUS within its specified positive input range. Move the supervisor supply, MR, CT pull-up and bypass to the regulated USB logic domain; do not expose TPS3808 directly to unprotected connector faults. Recheck every upstream capacitor rating and fault limit: the existing 10 V input capacitors do not inherit TPS709's 30 V rating.

Place the eFuse between connector VBUS and **charger IN only**. Fixed charger mode would be EN1 low / EN2 high, with the unchanged permanent ILIM pair. When Type-C permission is absent, disable the eFuse. The charger then behaves as it does with USB power removed: battery operation remains available. ON data over USB-A/default-current sources remains battery-powered; qualified Type-C sources retain OFF charging and charge-through operation.

### Upstream transient and capacitor blocker

This placement leaves the USB-only U29 regulator and C30/C31 on the **connector side** of the switch, so eFuse cutoff does not protect those capacitors. Both are currently `GRM155C71A105KE11D`, **1 µF / 10 V**. The selected U29 has a wide input rating, but the complete upstream rail does not inherit that rating. TI's TPS25947 transient-protection guidance recommends a close input capacitor rated at least **twice the input supply voltage** to withstand positive inductive ringing. At the accepted 5.5 V normal maximum, this gives **11 V minimum by that recommendation**; the current 10 V parts fail even this simple comparison. Any replacement capacitor must be assessed for the actual connector fault/transient waveform, effective capacitance and placement; a nominal 16 V marking by itself would not establish protection. If the input switch is instead placed ahead of U29, its enable logic and Type-C detector need another safe way to boot and classify the source. There is no approved direct VBUS-to-`+5V_USB` bridge.

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
   The screened TPS259474 37.4k/10k OVLO divider has just **16.1 mV** between the 5.5 V normal maximum and its lowest calculated rising trip of 5.5161 V. This is a nominally positive DC comparison, not verified noise/ripple or component-drift margin. Its calculated falling trip spans **5.0168–5.3779 V**: returning to a steady 5.0 V is below even the lowest screened threshold, while returning to 5.5 V after an OV fault may leave the output off until the source falls further or detaches. These DC comparisons do not prove transient recovery or automatic operation on every source in the normal range. Decide the desired recovery behavior before fixing the divider.
2. Define how both source voltage and logic validity inhibit EN. The present three-input permission expression cannot be removed without an equivalent state table and an ADR. A same-rail supervisor and eFuse intrinsic UVP alone are not automatically equivalent to the current VBUS_VALID boundary.
3. Select the actual inhibit network with startup/off/high-level leakage and slew bounds. Remove or recalculate all existing pull-ups and Schmitt-input loads attached to its node. No floating enable or direct raw-VBUS pull-up.
4. Strap BQ24074 EN1/EN2 with valid levels over powered/unpowered states, including input leakage and possible injection when charger IN is disconnected. Review stored input-capacitor energy during revocation; it is not continuing draw from the USB source.
5. Include both upstream USB logic and downstream charger current, inrush, discharge/retry behavior and source-advertisement changes in one power-state assessment. Preserve pack protection, NTC, timers and Gate A.

No user preference is needed to perform this engineering comparison. A material architecture change must be recorded before changing the canonical schematic. The current source and native acceptance remain unchanged.

## Simpler fallback if upstream exposure cannot be closed

Keep an always-enabled input protector **ahead of both** U29 and the charger, then control the BQ24074 standby mode with a single charge-permission sink. Unlike the eFuse-as-permission proposal, this keeps the USB logic capacitors behind the input switch and avoids asking the detector to operate from an unprotected VBUS rail. It still requires a fail-safe charger-mode actuator: EN1/EN2 both high must hold standby until qualified Type-C permission; only then may EN1 be pulled low while EN2 remains high to select the fixed ILIM setting. CE high alone is insufficient because BQ24074 still powers OUT from the input when charging is disabled.

Pulling EN2 high from **BAT** would spend battery current in the charger's approximately 285 kΩ internal pull-down even with USB absent (about 15 µA at 4.2 V by nominal arithmetic), consuming a substantial fraction of the 50 µA OFF-state allowance. Powering that pull-up from the protected USB domain avoids this specific absent-USB draw, but its high level across startup, brownout and overvoltage faults needs an exact source and resistor/leakage calculation. EN1 needs an independent low-voltage sink whose guaranteed output is below the charger's 0.4 V logic-low limit across the active supply range. The existing `2N7002K-7` library does **not** establish that behavior at 3.3 V gate drive: its manufacturer bounds ON resistance at 5 V and 10 V gate drive, not at 2.5 V or 3.3 V. No actuator, pull-up or protection placement is selected by this fallback.

An actuator reuse worth investigating is **U23, already captured** as the `SN74LVC1G06` open-drain `USB_EN1_RAW_N` request output. TI specifies at most **0.1 V LOW at 100 µA sink** over its 1.65–5.5 V supply range, below BQ24074's 0.4 V LOW limit. The existing R70 pull-up of 10 kΩ to 3.3 V sources up to 330 µA by nominal arithmetic, so that 100 µA row alone does not qualify a direct connection. A weaker or divided pull-up would need a full EN1 HIGH/LOW, U23 Ioff (±10 µA at VCC = 0), unpowered, intermediate-rail, input-fault and power-up timing budget; it must also keep U23's output at or below its 5.5 V recommended maximum during input faults. Reusing a footprint or test net does not bypass the control proof. The current schematic explicitly labels `USB_EN1_RAW_N` as a **test output, not a charger EN1 wire**.

### Conditional two-resistor U23 screen (2026-09-26)

Screen a protected-USB pull-up of **64.9 kΩ**, with **180 kΩ** from EN1 to ground, replacing—not paralleling—R70. This is an illustrative network only; neither resistor is selected by MPN. EN2 also requires its own defined high level. For ±1% resistor error and an **assumed** combined signed current of ±20 µA at EN1, Kirchhoff's current law gives `VEN1 = (VUSB/Rtop ± 20 µA)/(1/Rtop + 1/Rbottom)`. The assumed current provisionally assigns 10 µA to each of U23's zero-supply Ioff and the charger's high-input current. It is **not a component-guaranteed bound**: the BQ24074 table specifies its 10 µA `IIH` at **VIH = 1.4 V**, and describes its internal approximately 285 kΩ pulldown without a resistance tolerance. Its current at other EN1 voltages has not been bounded. Its maximum low-input current is 1 µA at VIL = 0 V and should be included in a final low-state budget.

| Static illustration | Worst calculated EN1 | Reference limit / caveat |
|---|---:|---|
| 3.3 V protected input; both 10 µA currents sink; maximum top/minimum bottom resistance | 1.454 V | 54 mV above BQ24074's 1.4 V HIGH threshold **only under the assumed currents** |
| 6.0056 V protected input; both 10 µA currents source; minimum top/maximum bottom resistance | 5.387 V | 113 mV below U23's 5.5 V recommended output maximum, assuming the protected rail cannot exceed this value |
| 6.1 V protected input; same sourcing assumptions | 5.457 V | 43 mV below U23's output maximum; 6.1 V is an illustrative test voltage, **not a proven transient clamp** |
| 6.1 V protected input; U23 LOW | At most 94.94 µA through the top resistor at 0 V output | Below TI's 100 µA / 0.1 V sink test load before additional pin currents; total LOW loading still needs proof |

The 3.3 V input floor is illustrative too: it is not a guarantee that every source voltage at which BQ24074 can turn on exceeds 3.3 V at this protected node. If the total EN1 sink is 25 µA instead of the assumed 20 µA, the first calculation falls to **1.215 V**, which is not a valid HIGH. Equally, source-voltage overshoot beyond 6.1 V can exceed U23's rated output voltage before the eFuse disconnects. A static resistor pair therefore cannot yet close charger standby, even if its nominal two-resistor arithmetic looks attractive. The EN1 pulldown and U23 leakage must be bounded together across the applicable voltage and temperature range, and a protector-off, U29-off, partial-ramp and fault/recovery state test must show both EN pins HIGH before BQ24074 accepts input. Directly using U29's 3.3 V output as the sole pull-up fails that requirement whenever protected USB is present but U29 is absent: EN1/EN2 would lose their HIGH defaults.

This screen narrows the parts needed for a future implementation but does not select a circuit or justify a native capture. It also reinforces that BQ24074 `CE` alone cannot replace EN1/EN2 standby: TI states that the input-to-OUT FET turns on when valid IN is present and the EN inputs are not both HIGH, even if charging is disabled.

The architecture comparison is therefore conditional: the upstream-detector eFuse option saves the EN1 actuator but incurs a second exposed VBUS domain; the whole-rail protector plus a qualified EN1 sink keeps one protected USB domain and **may reuse U23**. Compare their actual footprints, upstream leakage, startup cases and overvoltage behavior before recording a new ADR. No battery-side pull-up or raw connector bridge should be added merely to reduce the schematic part count.

## Controlled sources

- TI TPS25947 SLVSFC9C, May 2026, sections 6.3/6.5, 7.3 and 8.3.1 (input transient capacitor rating): https://www.ti.com/lit/ds/symlink/tps25947.pdf. SHA-256 `8f96de389903091650d4f462dcfad3210071c3ae7093623a7978f34baf8a65b4`.
- TI TPS3808 SBVS050N, August 2026, electrical characteristics and power-up-reset footnotes: https://www.ti.com/lit/ds/symlink/tps3808.pdf. SHA-256 `74d889c0f68af88032f1633c26381817cc03e10d9fd3b4c177a044ad3ed86eed`.
- TI BQ24074 SLUS810N, October 2021, EN1/EN2 mode table and logic electrical limits: https://www.ti.com/lit/ds/symlink/bq24074.pdf.
- TI SN74LVC1G06 SCES295AB, October 2025, electrical table and partial-power-down conditions: https://www.ti.com/lit/ds/symlink/sn74lvc1g06.pdf.
- Diodes Incorporated 2N7002K DS30896 Rev. 20-2, July 2024, page 3 ON characteristics and test conditions: https://www.diodes.com/datasheet/download/2N7002K.pdf.
- TPS709 input/capacitor scope remains controlled by ADR 0014 and the existing U29 audit.
