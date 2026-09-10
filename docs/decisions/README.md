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
| [0009](0009-usb-input-current-closure.md) | Reject unqualified direct USB input-current network | Accepted constraint; replacement pending |
