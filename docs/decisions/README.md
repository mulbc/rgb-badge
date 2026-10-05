<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Architecture decision records

Decision records explain choices that materially constrain later work. Accepted records are not silently rewritten when a decision changes: add a superseding record and update the affected requirements and project context.

| ADR | Decision | Status |
|---|---|---|
| [0001](0001-coupon-first-development.md) | Validate a production-intent coupon before the full badge | Accepted |
| [0002](0002-discrete-multiplexed-rgb-matrix.md) | Use a discrete multiplexed RGB matrix | Accepted |
| [0003](0003-esp32-s3-module-and-external-antenna.md) | Use ESP32-S3 N16R8 with an external antenna | Accepted |
| [0004](0004-standalone-charging-and-hard-off-state.md) | Use standalone charging and switched application rails | Input-current proposal superseded by ADR 0009; functional requirements retained |
| [0005](0005-project-licensing.md) | Use CERN-OHL-S for hardware and Apache-2.0 for software | Accepted |
| [0006](0006-kicad-10-workflow.md) | Target KiCad 10 stable with controlled upgrades | Accepted |
| [0007](0007-coupon-led-finalist-pair.md) | Populate the coupon with two final-product LED candidates | Accepted |
| [0008](0008-qblp1515-checkerboard-placement.md) | Preserve the QBLP1515 land pattern with checkerboard rotation | Accepted |
| [0009](0009-usb-input-current-closure.md) | Reject unqualified direct USB input-current network | Accepted constraint; replacement selected by ADR 0010 |
| [0010](0010-source-qualified-off-charging.md) | Charge while OFF only from a qualified source | Accepted for capture; thermal/Gate A pending |
| [0011](0011-usb-total-current-headroom.md) | Reserve current for USB detection and permission logic | Accepted; resistor specification amended by ADR 0012 |
| [0012](0012-programming-resistor-error-budget.md) | Include temperature and drift in programming-resistor limits | Exact parts selected; assembly/service qualification pending |
| [0013](0013-type-c-only-fixed-current-charging.md) | Use Type-C-only charging with a fixed limit | Accepted for coupon capture; hardware verification pending |
| [0014](0014-usb-voltage-envelope-and-logic-ldo.md) | Correct USB voltage envelope and logic regulator | Draft circuit reviewed; input-stage qualification pending |
| [0015](0015-switch-fuel-gauge-with-application.md) | Disconnect the gauge with the physical switch | Accepted for coupon capture; exact switch and SOC recovery validation pending |
| [0016](0016-runtime-and-fit-over-charge-speed.md) | Prioritize badge runtime and fit over charging speed | Accepted; exact terminated pack and charge times pending |
| [0017](0017-parallel-3v3-converter-capacitors.md) | Parallel exact capacitors on the coupon application converter | Provisional coupon target; complete derating and rail qualification pending |
| [0018](0018-complete-power-architecture-proposal.md) | Review the complete power topology as one functional block | Proposed; six capture holds, no circuit changes |
