<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0028: Capture the VLED converter with its enable held low

Date: 2026-10-11. Status: selected for provisional source capture; display operation remains blocked.

Root-link the existing exact-part TPS63020DSJT VLED converter candidate to the provisional BQ24074 `+SYS_APP_IN_DRAFT` output and the existing `VLED` row rail. Remove the fictitious VLED ERC source marker only when the physical converter output is linked. Keep its EN node connected **only** to the exact 100 kΩ pull-down, with no MCU, switch or other arm source. This adds the real power-stage component and capacitor footprint demand to the complete schematic while keeping VLED disabled throughout boot, reset, programming and OFF. The captured circuit is intentionally unable to light the display.

This staged connection changes the prior [capture contract](../../hardware/coupon/rev-a/vled-converter-capture-contract.md) only in sequencing: it permits a default-disabled converter to be root-linked before the display interlock is selected. It does not waive the [interlock interface](../design/display-interlock-interface-2026-10-05.md) or PWR-004/DSP-004. A future material decision must select an independently safe hardware arm and row-blanking circuit before any source drives EN or a powered display is claimed. GPIO9 `DISPLAY_ENABLE` remains a request, and GPIO8 still must be separated from decoder E before hardware row inhibition can be accepted. The exact 13-part stage and its pin/land audits remain unchanged.

Validate deterministic source equivalence, all native pin nets including `+SYS_APP_IN_DRAFT` and `VLED`, zero configured full-project ERC, whole-project item/pin totals, and both the converter and row schematic pages. This is source validation only. SYS transient/input range, VLED output capacitance under bias, layout loops, residual output energy, fault recovery and independent Gate A review remain open. Do not fabricate or enable the converter from this decision alone.

Source: [TI TPS63020 Rev I](https://www.ti.com/lit/ds/symlink/tps63020.pdf), especially pins 4/5, 10/11, 12, 14 and the shutdown-load-disconnect description; [existing exact-part stage](../../hardware/coupon/rev-a/vled-converter-capture-contract.md).
