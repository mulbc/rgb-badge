<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Current coupon power path: native netlist audit, 2026-10-13

This records **KiCad schematic connectivity**, not a standby, charging, USB-current or hardware test. The exact input/output regulator limits and startup behavior remain subject to the existing design holds and Gate A review. KiCad CLI 10.0.6 exported the 20-page root netlist with 497 PCB items and 1,814 logical pin entries. The `DRAFT` suffix on several net names is historical; the native XML shows physical component-pin joins, not isolated supply flags.

| Path or control | Native XML evidence |
|---|---|
| Connector to protected USB rail | `VBUS_CONNECTOR`: J1.A4_B9/J1.B4_A9 and E0 U45.5. `+5V_USB`: E0 U45.6, E1 U44.5 and U29.1. |
| Gated charger input | `CHARGER_IN_DRAFT`: E1 U44.6, BQ24074 U41.13, C52.1/C56.1 and the EN2 clamp feed R88.1. E1 EN U44.1 joins `CHARGER_GATE_EN` with U40.4, U42.4 and U43.4. U42 OE receives `USB_CHARGE_REQ`; U43 OE receives `USB_RAW_LOGIC_READY`. The gate's analog behavior remains unverified. |
| Charger settings and pack | U41.16 joins exact 2.49 kΩ R92 on `CHARGER_ISET`; U41.12 joins exact 3.65 kΩ R93 on `CHARGER_ILIM`. U41.1 and TH1.1 join `CHARGER_TS`. U41.2/3, J2.1 and SW2.5 join `+BAT_PROTECTED_DRAFT`. J2.2 is ground. |
| Application system power | BQ U41.10/11, SW2.2, TPS631000 U36.4 and TPS63020 U37.1/10/11 join `+SYS_APP_IN_DRAFT`. SW2.3 drives U36.5 `APP_ON_SW_DRAFT`; U37.12 remains on `VLED_ENABLE_DRAFT` with its pull-down R87. |
| OFF gauge supply | SW2.6, MAX17048 U35.2/3 and buffer U46.1 join `+BAT_GAUGE_SW`. SW2.5 is on protected BAT; actual leakage through all paths still needs measurement. |

The exact captured settings calculate to **0.317–0.396 A charge current** and **0.361–0.476 A charger input limit** under the retained ±1% total-resistance assumption, before other USB loads and transient behavior. The corrected `tools/check-power-design.py` now checks its R92/R93 identities against the deterministic charger-core generator. The stable Type-C permission checker now models the E1 gate request; BQ EN1 is grounded and EN2 is locally fed from the admitted charger input, so the old BQ-mode standby output was removed from that checker.

**Still open:** physical E1 inhibit through all attach/detach, supply-ramp, advertisement-change, thermal and fault states; whole-port current; exact delivered-pack qualification; charger temperature/charge-time behavior; converter and gauge transitions; and the output-isolated display interlock. Native ERC and a Boolean permission table do not close these. The two interlock candidate outputs still end at TP13/TP14, while the real VLED EN/decoder E remain held dark.

Reproduce with `kicad-cli sch export netlist --format kicadxml` on `hardware/coupon/rev-a/rgb-badge-coupon.kicad_sch`, then inspect the named XML nets and their `<node ref=... pin=...>` entries. Run `python3 tools/check-power-design.py` for current-setting calculations and `python3 tools/check-power-design.py --require-usb-closure` to confirm the operating qualifications remain explicitly open.
