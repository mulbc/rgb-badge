<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Two-event display interlock: circuit proposal

Date: 2026-10-12. Calculation and source study only; no interlock is yet connected in KiCad. [ADR 0032](../decisions/0032-two-event-display-interlock-proposal.md) records the proposed change. The existing converter EN pull-down and decoder E pull-up keep the canonical coupon display-dark.

## Proposed parts and signals

| Function | Exact candidate | Supply / connection | Manufacturer evidence |
|---|---|---|---|
| Application supervisor and independent watchdog | TI `TPS3823A-33DBVR`, SOT-23-5 | VDD = `+3V3_APP`; WDI = dedicated heartbeat with TI's 1 kΩ-to-ground default; active-low RESET joins the asynchronous-clear qualification; MR high | [TI TPS382x Rev O](https://www.ti.com/lit/ds/symlink/tps3823.pdf), §§5, 7.3.4 |
| Heartbeat-seen and display-arm memory | 2 × TI `SN74LVC1G74DCUR`, 8-pin VSSOP | Both VCC = `+3V3_APP`, PRE high, CLR low on any inhibit; first D high / CLK = inverted WDI, second D = first Q / CLK = arm pulse | [TI SN74LVC1G74 Rev G](https://www.ti.com/lit/ds/symlink/sn74lvc1g74.pdf), §§5–6 |
| Watchdog-edge inverter | TI `SN74LVC1G04DRLR`, SOT-5X3 | Input = WDI; output clocks the first flop after WDI's falling edge | [TI SN74LVC1G04 Rev AF](https://www.ti.com/lit/ds/symlink/sn74lvc1g04.pdf) |
| Asynchronous-clear combiner | TI `SN74LVC1G11DCKR`, 6-pin SC70, followed by `SN74LVC1G08DRLR`, 5-pin SOT-5X3 | First ANDs supervisor RESET, `ESP_EN` and `MODE_BOOT_N`; second ANDs that result with `DISPLAY_ENABLE` to drive both CLR pins | [TI 3-input AND](https://www.ti.com/lit/ds/symlink/sn74lvc1g11.pdf); [TI 2-input AND](https://www.ti.com/lit/ds/symlink/sn74lvc1g08.pdf) |
| VLED voltage window | TI `TLV6700DSER`, WSON-6 | VDD = `+3V3_APP`; INA+ and INB− sense VLED through separate dividers; both open-drain outputs share a pulled-up `VLED_WINDOW_OK` node | [TI TLV6700 Rev B](https://www.ti.com/lit/ds/symlink/tlv6700.pdf), §§5–7 |
| Row and power logic | TI `SN74LVC2G00DCUR` (dual NAND), `SN74LVC2G08DCUR` (dual AND) | All from `+3V3_APP`; retain R42 on decoder E and R87 on VLED EN | [TI NAND](https://www.ti.com/lit/ds/symlink/sn74lvc2g00.pdf); [TI AND](https://www.ti.com/lit/gpn/sn74lvc2g08) |

This is an exact-IC shortlist, not a completed BOM. Every new passive needs an exact MPN and its land checked before capture. The clear combination is now logically specified, but input thresholds on the slow `ESP_EN` RC node, GPIO0 strap loading, output state below valid VCC and physical fit remain to be audited before capture. TI currently lists the exact 3-input AND as active but with no direct TI stock; distributor/assembler availability needs checking at order time.

The ESP32-S3-WROOM-1U datasheet lists GPIO15 on module pad 8 and GPIO16 on pad 9. They are not GPIO0/3/45/46 strapping pins or the N16R8's reserved GPIO35–37 PSRAM group, and both are presently no-connect in the coupon. [Espressif module datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf). GPIO9 `DISPLAY_ENABLE` is the live request; GPIO8 remains the active-low row request. The heartbeat is normally LOW and makes a short HIGH pulse followed by a falling edge; its 1 kΩ WDI pull-down makes float a LOW, since a floating TPS3823 WDI otherwise disables the watchdog. The arm pulse also needs a defined LOW idle.

## State equations and order

`CLEAR_OK = APP_SUPERVISOR_OK AND ESP_EN AND MODE_BOOT_N AND DISPLAY_ENABLE`. A low on any input asynchronously clears *both* flops. The supervisor's watchdog RESET is the `APP_SUPERVISOR_OK` input. `HEARTBEAT_SEEN` captures one on the inverter's rising edge **after WDI falls** while `CLEAR_OK` is high. `ARM_LATCH` captures `HEARTBEAT_SEEN` only on a later rising arm-pulse edge. This gives the watchdog and first flop the same qualifying physical edge, though actual setup/propagation and pulse-width limits still need an audit. Firmware may pulse arm only after the heartbeat. No level returning high clocks either flop.

`VLED_EN = ARM_LATCH AND DISPLAY_ENABLE`; the existing R87 pulls it low whenever the driver is absent. `ROW_ARM = ARM_LATCH AND VLED_WINDOW_OK`. `ROW_ENABLE_N = NOT(ROW_ARM AND NOT ROW_ENABLE_REQ_N)`. The two NAND gates can invert the row request and implement the final NAND; the two AND gates can implement VLED_EN and ROW_ARM. R42 remains a pull-up at the decoder, but a push-pull gate must itself have a qualified supply. The proposal does not assume that an unpowered logic output is a valid high.

Startup sequence: hold `DISPLAY_ENABLE=0`, row request high and arm pulse low; set the request high only after controller initialization; issue a heartbeat edge; issue one distinct arm pulse; wait for `VLED_WINDOW_OK`; begin row scanning. On any inhibit, the arm latch clears, forcing the row request path off and removing EN. The mode button clears immediately and a subsequent heartbeat **plus a new arm pulse** is needed after release. A software/ROM reset must make `DISPLAY_ENABLE` fall via its external pull-down, not merely stop heartbeat; this needs bench confirmation at the GPIO and VLED EN pins. A stalled firmware heartbeat trips RESET after the specified watchdog interval, clearing the latches. The watchdog is **not** a power-on permission; it is initially inactive until its timeout.

| Event, including GPIO8 stuck low | Arm latch | Converter EN | Decoder E |
|---|---:|---:|---:|
| Cold start / application rail below threshold | cleared | low by driver/default | high by driver/default when rail valid |
| GPIO9 request high, no heartbeat | cleared | low | high |
| Heartbeat received, no later arm edge | cleared | low | high |
| Armed, VLED below window | set | high | high |
| Armed, VLED inside window | set | high | follows `ROW_ENABLE_REQ_N` |
| Mode press, ESP_EN low, request low, or watchdog RESET | asynchronously cleared | low | high while logic remains powered |
| Fault recovers without new heartbeat and arm edges | cleared | low | high |

The final row assumes the logic rail remains in its valid range. The fault response when it collapses while VLED retains energy must be proved with transistor defaults and measurements; the table does not certify this condition.

## VLED window calculation, not a verified limit

The existing divider targets 3.944 V nominal. Candidate 1% Panasonic 0402 parts `ERJ2RKF1603X` above `ERJ2RKF2002X` put the TLV6700 INA+ rising threshold at `0.4 × (1 + 160/20) = 3.60 V`. Candidate `ERJ2RKF1963X` above a second `ERJ2RKF2002X` put INB− rising threshold at `0.4 × (1 + 196/20) = 4.32 V`. OUTA sinks below the lower threshold and OUTB sinks above the upper one; their wired-AND open-drain outputs need a pull-up to the application rail and a local bypass capacitor. These are nominal arithmetic values. Reference tolerance, hysteresis, resistor drift, VLED startup ripple, comparator output leakage, and the converter's actual output range must be checked before selecting the divider. The comparator does not replace row blanking or establish safe VLED discharge. The output bank is 88 µF *nominal*; `0.5 × 88 µF × 3.944² = 0.684 mJ` is nominal stored energy, not a decay-time or effective-capacitance measurement.

As a first arithmetic corner, TI's 396–404 mV rising-threshold range over temperature and opposing ±1% initial resistor values give 3.501–3.701 V for the lower rising trip and 4.200–4.443 V for the upper rising trip. This omits resistor temperature coefficient, input bias, layout noise and falling-trip hysteresis, so it is not a guaranteed display window. TI also specifies up to 450 µs after its supply exceeds 1.8 V before comparator outputs are correct. The selected supervisor's specified release delay is 120–300 ms after its 2.83–3.00 V threshold, a large nominal startup interval for the comparator on a monotonic common rail; rail interruption and clearing still need dynamic review. Below the comparator's power-on-reset voltage, its outputs are indeterminate, another reason to prove the decoder's unpowered behavior. [TI TLV6700 electrical table](https://www.ti.com/lit/ds/symlink/tlv6700.pdf); [TI TPS3823A tables](https://www.ti.com/lit/ds/symlink/tps3823.pdf).

## Pin audit for capture

- `TPS3823A-33DBVR` DBV top view: RESET 1, GND 2, MR 3, WDI 4, VDD 5. RESET is push-pull; do not wire-OR it directly to another push-pull output.
- `SN74LVC1G74DCUR` DCU top view: CLK 1, D 2, inverted Q 3, GND 4, Q 5, CLR 6, PRE 7, VCC 8. PRE must have a defined high; CLR low dominates the intended arm state.
- `TLV6700DSER` **DSE**, not DDC, top view: OUTB 1, VDD 2, INB− 3, INA+ 4, GND 5, OUTA 6. The package-dependent reversal makes a copied SOT-23 symbol unacceptable.
- `SN74LVC2G00DCUR` DCU: 1A 1, 1B 2, 2Y 3, GND 4, 2A 5, 2B 6, 1Y 7, VCC 8. Check the AND part independently before capture.
- `SN74LVC1G04DRLR` DRL: NC 1, A 2, GND 3, Y 4, VCC 5; do not route pin 1 as an input.
- `SN74LVC1G11DCKR` DCK: A 1, GND 2, B 3, Y 4, VCC 5, C 6. `SN74LVC1G08DRLR` DRL: A 1, B 2, GND 3, Y 4, VCC 5. Check exact footprints against the package drawings before generating symbols.

## Acceptance checks before connecting the dark stage

Qualify the clear gate's actual input levels and timing, including GPIO0 strap loading and ESP_EN's reset RC. Check both flip-flops' CLR/PRE behavior during their VCC ramp. Calculate the remaining voltage-window corners and resistor power. Verify the decoder sees HIGH with GPIO8 forced LOW during every inhibit, including application rail loss while VLED is charged. Demonstrate that an internal ESP restart pulls GPIO9 low soon enough to blank rows and remove EN, and that a stuck or floating heartbeat produces a watchdog reset. Check pulse current through the 1 kΩ WDI bias and choose a heartbeat duty cycle. Decide a discharge/bleed value from measured effective output capacitance and allowable decay; do not presume the converter discharges VLED. Reserve the **actual** new courtyards in the final-board XY screen. Then capture and run deterministic regeneration, native ERC/XML/PDF, visual schematic review and the independent Gate A review. A physical fault-injection matrix is required after the coupon exists.
