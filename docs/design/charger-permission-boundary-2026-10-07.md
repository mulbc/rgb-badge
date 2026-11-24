<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Charger permission pin boundary for coupon review

2026-10-07, amended 2026-10-11. **Proposed E1 pin and state contract, not a qualified charger circuit.** This narrows H3 in [ADR 0018](../decisions/0018-complete-power-architecture-proposal.md). The temperature NTC/TMP390/AUP subcircuit is [root-linked](../../hardware/coupon/rev-a/charger-temperature.kicad_sch); `CHARGER_TS` joins the root-linked BQ24074 core and `CHARGER_GATE_EN` now joins the provisional E1 sheet. The contract assumes the two-switch protected USB topology. [ADR 0022](../decisions/0022-lower-fixed-usb-input-limit-proposal.md) now selects the single lower ILIM resistor for the provisional BQ core, and [ADR 0024](../decisions/0024-lp452845-pack-and-temperature-window.md) selects the exact LP452845 assembly as the Rev A design target. E1 is provisionally captured; E0, the pack connector and PCB remain uncaptured.

| Function | Proposed connection | Why it remains conditional |
|---|---|---|
| Protected detector supply | E0 `OUT` → `USB_PROTECTED` → TPS70933 input and E1 `IN` | E0 input transient, OVLO, ILM, capacitor and retry values remain H2. |
| Charger input | E1 `OUT` → `CHARGER_IN` → BQ24074 `IN` pin 13 and its local input capacitor | E1 must reverse-block stored input energy; capacitor inrush and discharge need bounds. |
| E1 enable default | E1 `EN/UVLO` → independent ground pull-down; pull-up only to the same USB 3.3 V rail that powers the permission logic | ADR 0026 selects exact 220 kΩ / 270 kΩ parts for provisional capture; source and partial-rail qualification remain open. |
| Permission inhibit | `SN74AUP1G125DBVR`: pin 2 `A` to ground, pin 1 active-low `OE` to `USB_CHARGE_REQ`, pin 3 ground, pin 5 to USB 3.3 V, pin 4 `Y` to E1 EN | With request low, Y sinks EN. With request high, Y is high impedance and the weak pull-up may raise EN. Exact package and source nets are captured; supply transitions, output leakage and OE slew still require qualification. |
| Temperature inhibit | TMP390 pins 6 `OUTA` and 4 `OUTB` tied to `TEMP_OK` with 10 kΩ to USB 3.3 V; second `SN74AUP1G125DBVR` pin 1 `OE` to `TEMP_OK`, pin 2 `A` and pin 3 to ground, pin 5 to USB 3.3 V, pin 4 `Y` to E1 EN | Either hot/cold fault pulls `TEMP_OK` low and makes the second AUP sink EN. Healthy outputs release `TEMP_OK`, tri-stating Y. This keeps the TMP390 on a 10 kΩ pull-up within its specified 1–10 kΩ range; prove startup, fault and all-condition logic levels. |
| Independent startup inhibit | `TPS3808G01DBVR` pin 1 `RESET` drives a third AUP active-low OE; that AUP sinks E1 EN while RESET is low. U34 VDD/MR are now on USB 3.3 V | R78/R63 now use 100 kΩ / 1 MΩ to reduce RESET load. Verify U27 and AUP input levels, RESET current and partial-rail behavior; fast brownout remains unproven. |
| BQ charging mode | `CE` pin 4 low, `EN1` pin 6 low; `EN2` pin 5 rises through the local 10 kΩ/2.5 V shunt only with admitted `CHARGER_IN` | This selects fixed ILIM mode after the clamp reaches a valid high. EN2 load and attach/detach timing remain unqualified. |

The existing `USB_CHARGE_REQ` and `USB_EN1_RAW_N` on the canonical permission sheet are **test outputs**; ADR 0026 now connects `USB_CHARGE_REQ` to U42 AUP OE in the provisional E1 capture. U23's current 10 kΩ pull-up is not the proposed E1 EN network, and `USB_EN1_RAW_N` must not be wired directly to BQ `EN1` or E1 EN. The E1 source connection adds U42/U43 loads; U23/U34 loading and transitions still require physical qualification.

## State invariant to verify before connected capture

| State | Required E1 EN result | BQ mode/input implication |
|---|---|---|
| No USB or E0 output | Below E1's rising threshold by passive pull-down | E1 input absent; no charge. |
| USB logic rail rising below supervisor-valid | RESET or passive rail tracking keeps EN below threshold, regardless of Type-C output glitches | E1 stays open while detector and supervisor start. |
| Valid, ready, Type-C default/USB-A | AUP Y actively sinks EN | E1 stays open; application may use battery and USB data while ON. |
| Valid, ready, Type-C 1.5 A/3 A | AUP Y releases; RESET releases only after its delay; EN may rise | E1 admits `CHARGER_IN`; BQ must see its fixed mode before `IN` becomes valid. |
| Valid source, cell sensor hot or cold | Temperature AUP Y sinks EN independently of source request and physical switch | E1 opens; charger input is removed while BQ TS remains connected. |
| Advertisement downgrade, rail brownout, E0 trip or detach | At least one independent inhibit pulls EN low or E1 loses input; account for propagation and stored capacitance | No continuing unqualified USB draw; residual downstream energy is measured separately. |

At ADR 0026's exact 220 kΩ pull-up/270 kΩ pull-down values, the pull-up alone sources at most 3.67 µA at a 0.8 V logic rail and 16.53 µA at 3.6 V under ±1% resistance; the selected divider and assumed aggregate leakage are screened in that ADR. TI specifies the supervisor's 0.8 V POR output at 15 µA RESET load with a VDD rise of at least 15 µs/V; that is **not** a universal transient guarantee. E1's EN rising threshold can be as low as 1.183 V and its falling threshold as low as 1.076 V. The AUP output is three-state only when its supply/input conditions are met. These facts make this a plausible default-off arrangement, not a proof across every intermediate supply and injection path.

**EN2 source selected for provisional capture.** BQ24074's EN pins have a 7 V absolute maximum and an internal approximately 285 kΩ pull-down. The root-linked shunt now derives EN2 from the admitted input, avoiding an upstream rail driving an unpowered charger. The shunt's guaranteed operating margin depends on an unverified EN2 high-voltage input-current bound; E1 output fault and attach/detach waveforms are also unmeasured. Validate those limits and BQ input-valid/EN2 timing on source attach, detach, downgrade and E0 trip before treating the mode as qualified.

**Captured source setting:** [ADR 0023](../decisions/0023-charger-en2-local-clamp-proposal.md) and its [DC screen](charger-en2-shunt-screen-2026-10-07.md) supply the provisional 10 kΩ/2.5 V local source for BQ EN2. The source-domain choice is represented in KiCad, conditional on EN2 input-current verification and fault/transient checks; it does not close H3. [ADR 0024](../decisions/0024-lp452845-pack-and-temperature-window.md) adds the buffered temperature-fault inhibit to E1 EN for the selected pack design target; include it in the next connected permission review.

**2026-10-11 supervisor-domain amendment:** [ADR 0025](../decisions/0025-usb-supervisor-logic-rail.md) moves U34 MR/VDD, C38 and R77 to `+3V3_USB` in the root-linked conditioning sheet. This satisfies the proposed common-supply connection in row 5 of the pin contract. It does not connect U34 RESET to E1 EN or prove intermediate-rail and fast-brownout behavior. The existing 10 kΩ R78 RESET pull-up still belongs to the staged logic output and must be re-audited when the gate is wired.

Sources: [TPS3808 Rev N, §§6.5–6.6](https://www.ti.com/lit/ds/symlink/tps3808.pdf), [SN74AUP1G125 Rev N, §§5–6](https://www.ti.com/lit/ds/symlink/sn74aup1g125.pdf), [TPS25947 Rev C, §6.5](https://www.ti.com/lit/ds/symlink/tps25947.pdf), [BQ24074 Rev N, §§7–9](https://www.ti.com/lit/ds/symlink/bq24074.pdf). All stated currents and thresholds are manufacturer specifications or calculations; there are no simulations or measurements here.

**2026-10-11 E1 capture amendment:** [ADR 0026](../decisions/0026-charger-e1-gate-network.md) is represented in the [root-linked gate sheet](../../hardware/coupon/rev-a/charger-gate.kicad_sch). Native XML confirms the U42/U43/U40 gate and E1 OUT→BQ IN joins. E1 IN is a nonphysical `USB_PROTECTED_DRAFT` boundary; no E0 protection or startup/fault measurements are implied by this capture.
