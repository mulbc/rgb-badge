<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Charger permission pin boundary for coupon review

2026-10-07, amended 2026-10-09. **Proposed pin and state contract, not a captured or qualified circuit.** This narrows H3 in [ADR 0018](../decisions/0018-complete-power-architecture-proposal.md) without changing the canonical KiCad project. It assumes the two-switch protected USB topology and may use the [lower fixed-ILIM option](../decisions/0022-lower-fixed-usb-input-limit-proposal.md). [ADR 0024](../decisions/0024-lp452845-pack-and-temperature-window.md) now selects the exact LP452845 assembly as the Rev A design target; charger resistor population and the board remain uncaptured.

| Function | Proposed connection | Why it remains conditional |
|---|---|---|
| Protected detector supply | E0 `OUT` → `USB_PROTECTED` → TPS70933 input and E1 `IN` | E0 input transient, OVLO, ILM, capacitor and retry values remain H2. |
| Charger input | E1 `OUT` → `CHARGER_IN` → BQ24074 `IN` pin 13 and its local input capacitor | E1 must reverse-block stored input energy; capacitor inrush and discharge need bounds. |
| E1 enable default | E1 `EN/UVLO` → independent ground pull-down; pull-up only to the same USB 3.3 V rail that powers the permission logic | No raw-VBUS or battery pull-up. The illustrative 220 kΩ / 1 MΩ pair is not an exact selected network. |
| Permission inhibit | `SN74AUP1G125DBVR`: pin 2 `A` to ground, pin 1 active-low `OE` to `USB_CHARGE_REQ`, pin 3 ground, pin 5 to USB 3.3 V, pin 4 `Y` to E1 EN | With request low, Y sinks EN. With request high, Y is high impedance and the weak pull-up may raise EN. Audit exact package, supply transitions, output leakage and OE slew before capture. |
| Temperature inhibit | TMP390 pins 6 `OUTA` and 4 `OUTB` tied to `TEMP_OK` with 10 kΩ to USB 3.3 V; second `SN74AUP1G125DBVR` pin 1 `OE` to `TEMP_OK`, pin 2 `A` and pin 3 to ground, pin 5 to USB 3.3 V, pin 4 `Y` to E1 EN | Either hot/cold fault pulls `TEMP_OK` low and makes the second AUP sink EN. Healthy outputs release `TEMP_OK`, tri-stating Y. This keeps the TMP390 on a 10 kΩ pull-up within its specified 1–10 kΩ range; prove startup, fault and all-condition logic levels. |
| Independent startup inhibit | `TPS3808G01DBVR` pin 1 open-drain `RESET` also sinks E1 EN; its pin 6 `VDD` and pull-up move to USB 3.3 V | Recalculate U34's divider/CT and all existing loads. RESET's 0.8 V POR condition is load- and rise-dependent; fast brownout remains unproven. |
| BQ charging mode | `CE` pin 4 low, `EN1` pin 6 low and `EN2` pin 5 high whenever admitted input is valid | This selects the fixed ILIM mode. EN2 must already be high before BQ accepts input and remain valid through source fall; its exact source/clamp is **not selected**. |

The existing `USB_CHARGE_REQ` and `USB_EN1_RAW_N` on the canonical permission sheet are **test outputs**. U23's current 10 kΩ pull-up is not the proposed E1 EN network, and `USB_EN1_RAW_N` must not be wired directly to BQ `EN1` or E1 EN. A later connected capture must replace the test-only boundary and re-audit U23/U34 loading rather than merely matching net names.

## State invariant to verify before connected capture

| State | Required E1 EN result | BQ mode/input implication |
|---|---|---|
| No USB or E0 output | Below E1's rising threshold by passive pull-down | E1 input absent; no charge. |
| USB logic rail rising below supervisor-valid | RESET or passive rail tracking keeps EN below threshold, regardless of Type-C output glitches | E1 stays open while detector and supervisor start. |
| Valid, ready, Type-C default/USB-A | AUP Y actively sinks EN | E1 stays open; application may use battery and USB data while ON. |
| Valid, ready, Type-C 1.5 A/3 A | AUP Y releases; RESET releases only after its delay; EN may rise | E1 admits `CHARGER_IN`; BQ must see its fixed mode before `IN` becomes valid. |
| Valid source, cell sensor hot or cold | Temperature AUP Y sinks EN independently of source request and physical switch | E1 opens; charger input is removed while BQ TS remains connected. |
| Advertisement downgrade, rail brownout, E0 trip or detach | At least one independent inhibit pulls EN low or E1 loses input; account for propagation and stored capacitance | No continuing unqualified USB draw; residual downstream energy is measured separately. |

At the proposed 220 kΩ pull-up/1 MΩ pull-down values, the previous [static screen](power-architecture-2026-10-05.md#2-usb-admission-and-protection) gives at most 3.67 µA pull-up current at a 0.8 V logic rail and 16.53 µA at 3.6 V, before leakage or other loads. TI specifies the supervisor's 0.8 V POR output at 15 µA RESET load with a VDD rise of at least 15 µs/V; that is **not** a universal transient guarantee. E1's EN rising threshold can be as low as 1.183 V and its falling threshold as low as 1.076 V. The AUP output is three-state only when its supply/input conditions are met. These facts make this a plausible default-off arrangement, not a proof across every intermediate supply and injection path.

**EN2 is the immediate unresolved pin.** BQ24074's EN pins have a 7 V absolute maximum and an internal approximately 285 kΩ pull-down. Tying EN2 directly to E1 `OUT` follows the admitted input and avoids an upstream rail driving an unpowered charger, but E1's output fault overshoot has no proven sub-7 V bound. Pulling EN2 from USB 3.3 V avoids that voltage exposure but can drive the charger while E1 is open and can decay before E1 EN falls. Neither wire is approved yet. Choose one exact protected connection and validate the BQ input-valid/EN2 timing and injection on attach, detach, source downgrade and E0 trip before root-linking the charger.

**Follow-on candidate:** [ADR 0023](../decisions/0023-charger-en2-local-clamp-proposal.md) and its [DC screen](charger-en2-shunt-screen-2026-10-07.md) propose feeding EN2 from E1 OUT through 10 kΩ and locally clamping it to 2.5 V. This resolves the schematic-level source-domain choice, conditional on EN2 input-current verification and fault/transient checks; it does not close H3. [ADR 0024](../decisions/0024-lp452845-pack-and-temperature-window.md) adds the buffered temperature-fault inhibit to E1 EN for the selected pack design target; include it in the next connected permission review.

Sources: [TPS3808 Rev N, §§6.5–6.6](https://www.ti.com/lit/ds/symlink/tps3808.pdf), [SN74AUP1G125 Rev N, §§5–6](https://www.ti.com/lit/ds/symlink/sn74aup1g125.pdf), [TPS25947 Rev C, §6.5](https://www.ti.com/lit/ds/symlink/tps25947.pdf), [BQ24074 Rev N, §§7–9](https://www.ti.com/lit/ds/symlink/bq24074.pdf). All stated currents and thresholds are manufacturer specifications or calculations; there are no simulations or measurements here.
