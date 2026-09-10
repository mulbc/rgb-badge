<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0009: Reject the provisional direct USB input-current network

- Status: Accepted constraint; replacement topology not yet selected
- Date: 2026-09-10
- Supersedes: the provisional 500 mA / 1.2 A direct-ILIM network in ADR 0004, not autonomous charging or the physical OFF switch

## Evidence and decision

Reopening TI SLUSDF7A confirmed that BQ25616J `ILIM` is used only for an unknown adapter and its documented programming range starts at 500 mA. With the table's typical KILIM=478 A-ohm, the proposed 1 kohm setting is nominally 478 mA; the earlier 454–505 mA tolerance calculation alone did not establish a supported operating point. Nor does this network implement the lower pre-configuration USB-host state. `CE` stops charging but does not remove the system's USB power path.

Do not capture or approve that network as the complete USB safety solution. Keep the corrected BQ symbol/footprint as audited library work, without treating it as a frozen production selection. Preserve the product requirements: autonomous OFF-state charging, native USB data while ON, a hardware-bounded source limit and the weight/size/runtime targets. Select either a suitable standalone charger or a separately qualified input-control circuit before power/input capture resumes.

The [input-current assessment](../../hardware/coupon/rev-a/usb-input-assessment.md) records alternatives and remaining proof obligations. No replacement IC has been adopted by this decision. In particular, supporting a 100 mA mode alone does not prove suspend behavior, total port current, OFF leakage or charge timing.

## Verification

`check-power-design.py` preserves historical arithmetic for traceability, labels it unaccepted, and separately checks programmed-range/source-limit constraints. Its explicit `--require-usb-closure` gate fails while these circuit findings remain open. Ordinary library/ERC checks may pass for the existing partial schematic; they do not close this gate. The wrapper prints the blocker list without pretending to validate uncaptured circuits.

## Consequences

This is a necessary correction before finishing the power sheet, not a change to user-facing requirements. The candidate list and charger-dependent calculations may change. No new owner KiCad run is useful for this documentation/calculation increment. Independent Gate A remains required before fabrication.

## Sources

- [TI BQ25616/BQ25616J datasheet](https://www.ti.com/lit/ds/symlink/bq25616.pdf), SLUSDF7A, pin functions, KILIM characteristics and sections 9.3.3–9.3.6.
- [Analog Devices LTC4088 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/4088fb.pdf), candidate hardware current modes and associated limits.
