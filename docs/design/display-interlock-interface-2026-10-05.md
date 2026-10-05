<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Display interlock interface review

2026-10-05. Proposed H5 engineering increment for [ADR 0018](../decisions/0018-complete-power-architecture-proposal.md). This is a source review and state contract, **not** a captured or electrically tested interlock. It retains the accepted [row architecture](../decisions/0002-discrete-multiplexed-rgb-matrix.md) and [requirements](../requirements.md); no current setting or canonical KiCad connection changes here.

## Actual captured boundary

The [controller capture](../../hardware/coupon/rev-a/controller-capture.md) connects ESP32-S3 GPIO8 directly to `ROW_ENABLE_N` and GPIO9 to `DISPLAY_ENABLE`. The [row capture](../../hardware/coupon/rev-a/row-capture.md) connects `ROW_ENABLE_N` to U2 `74HC4514PW,118` pin 23, active-low E, with R42 = 100 kΩ to `+3V3_APP`. Each of the sixteen P-channel row gates has a 1 kΩ source-referenced pull-up; each N-channel gate has a 100 kΩ pull-down. The TLC59581 has no independent output-enable pin, and its four serial/clock inputs have pull-downs. Those defaults are useful while the 3.3 V rail is valid, but they do not establish behavior during rail ramps or while VLED retains charge.

**Required net migration:** rename the GPIO8 side to `ROW_ENABLE_REQ_N` and retain `ROW_ENABLE_N` only on the decoder side of a hardware gate. The logical contract is `ROW_ENABLE_N = ROW_ENABLE_REQ_N OR NOT ROW_ARM`. A push-pull gate or properly isolated equivalent must create the decoder-side net. Connecting a second driver directly to the current GPIO8 net would create contention when firmware requests a row. R42 must remain on the decoder-side net or be replaced by an audited default-high arrangement. `DISPLAY_ENABLE` remains only a GPIO9 *request*, never the TPS63020 EN connection by itself. Any revised net names, parts and pin numbers require full library, netlist and native-export review before capture acceptance.

## Two permissions, with separate jobs

1. `POWER_ARM` may enable the TPS63020 LED converter only after the physical switch is ON, application rail qualified, ESP reset released, programming inhibited, a deliberate post-reset arm handshake accepted, **at least one qualified watchdog heartbeat observed**, and an independent watchdog has not timed out. Its converter EN node needs a passive OFF default. A controller GPIO high by itself must not establish `POWER_ARM`.
2. `ROW_ARM` may release U2's active-low E only after `POWER_ARM` and a *qualified* VLED-ready condition. Firmware still selects the row and supplies blanking dead time through `ROW_ENABLE_REQ_N`. Hardware forces every row blank as soon as either permission is lost, even if GPIO8 remains low. VLED readiness must not be inferred from the converter's PG label without checking its actual assertion conditions, pull-up supply, startup behavior and falling response.

The ordering target is: on startup, blank rows → arm VLED → qualify VLED → permit firmware row scans. On shutdown/fault, force row blank → remove converter EN; a real circuit must bound propagation and overlap in both directions. TPS63020's specified shutdown disconnects its input from the load, but does **not** specify immediate discharge of the output capacitor. Residual VLED needs an audited discharge/bleed strategy and measurements with the actual capacitor bank, or a proof that no row can conduct throughout the decay. [TPS63020 §§6.5, 7.3](https://www.ti.com/lit/ds/symlink/tps63020.pdf).

## Inhibit and rearm states

| Trigger | Immediate hardware result | Before display can resume |
|---|---|---|
| Switch OFF or either contact bounces | Remove `POWER_ARM` and `ROW_ARM`; passive defaults keep both disabled | New stable application rail and new post-reset handshake; no assumed pole order. |
| Application rail starts, brownouts or ESP_EN resets | Clear arm memory; rows blank and VLED disabled | Supervisor release, deliberate firmware rearm and watchdog qualification. |
| Mode button (`MODE_BOOT_N`) is pressed | Latch a display inhibit and blank before firmware handles the press | A distinct normal-playback rearm after button release. This also covers a held GPIO0 during ROM recovery. |
| Firmware enters programming after the button is released | Keep the latched inhibit asserted | Explicit normal-playback rearm; firmware must not emit this while programming. Hardware needs a way to distinguish this from a short button action. |
| Watchdog expires or a defined electrical/thermal fault asserts | Clear arm memory, blank rows and disable VLED | Fault cleared, valid rail, new handshake. A watchdog output that later returns high must not automatically restore the display. |
| Firmware asks for a row before power is ready | Decoder remains disabled | `ROW_ARM` after qualified VLED and firmware blanking sequence. |

One spare ESP32 GPIO would be needed for a dedicated watchdog heartbeat if the chosen watchdog cannot safely observe an existing signal. `LED_GCLK` is not assumed suitable: its normal scan rate and pause behavior differ from a watchdog's timing window. Assign a specific module pad only after checking boot strapping, PSRAM reservations, reset defaults and actual watchdog timing. A watchdog whose fault output starts deasserted is **not** a startup arm signal: it must be paired with post-reset arm memory. `TPS3430` is only a candidate family for that function; its output can return high after its fault pulse and its disable pins can force it high, so neither behavior may implicitly rearm VLED. [TPS3430 §§5, 7](https://www.ti.com/lit/ds/symlink/tps3430.pdf).

The mode button is already on ESP32 GPIO0. Any hardware sensing branch must not change its boot-strap levels, load or timing. A button-edge inhibit can act before firmware, but the circuit still needs an explicit normal-playback rearm rule so that programming remains dark after button release. This may require a separate programming-state signal or a latch handshake; the choice is open. A firmware-only declaration of programming state cannot substitute for the physical button/reset and watchdog paths.

## Capture and verification gate

Select exact supervisor, gate, latch/watchdog, converter-discharge and passive MPNs; audit every pin, footprint and reset/power-off specification. Draw their supply and reset domains and all pull directions. Check the row output for GPIO8 driven LOW while every inhibit is asserted, not just a high-impedance controller. Check button bounce, ROM recovery, software programming, stalled firmware, brownout, physical-switch bounce and residual VLED with the final capacitance. Extend the source netlist checker to reject direct GPIO8-to-U2 E and direct GPIO9-to-converter EN connections. Then run native KiCad ERC/XML/PDF and review the changed pages together with the complete power block. Gate A independent engineering review and coupon measurements remain required before fabrication or a claim that the interlock works.
