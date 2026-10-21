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
| [0007](0007-coupon-led-finalist-pair.md) | Populate the coupon with two final-product LED candidates | Accepted LED pair; equal-pitch clause superseded by 0034 |
| [0008](0008-qblp1515-checkerboard-placement.md) | Preserve the QBLP1515 land pattern with checkerboard rotation | Superseded for coupon by 0034 |
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
| [0019](0019-board-mounted-battery-temperature-sensing.md) | Trial a board-mounted battery temperature sensor with protected two-wire packs | Accepted direction; cell-to-board thermal validation pending |
| [0020](0020-dual-row-mosfet-package-proposal.md) | Evaluate one complementary N/P package per row to recover PCB area | Proposed; no schematic or BOM change |
| [0021](0021-external-battery-current-measurement.md) | Measure battery current with an inline instrument during validation; omit the on-board monitor/shunt | Accepted for capture; instrument/harness and hardware validation pending |
| [0022](0022-lower-fixed-usb-input-limit-proposal.md) | Evaluate one existing 3.65 kΩ ILIM resistor to simplify charger/eFuse current coordination | Proposed; no schematic or BOM change |
| [0023](0023-charger-en2-local-clamp-proposal.md) | Feed charger EN2 from admitted input through a local 2.5 V clamp | Proposed; transient and EN2-load checks pending |
| [0024](0024-lp452845-pack-and-temperature-window.md) | Design Rev A around the exact protected LP452845/PHR-2 assembly with NTC and buffered hardware temperature inhibit | Accepted design target; source capture and physical qualification pending |
| [0025](0025-usb-supervisor-logic-rail.md) | Power USB-side supervision from the USB-only logic rail | Provisional source capture; timing qualification pending |
| [0026](0026-charger-e1-gate-network.md) | Capture three independent hardware inhibits on the E1 charger gate | Provisional source capture; fault and timing qualification pending |
| [0027](0027-e0-protected-usb-source-selection.md) | Bridge connector VBUS to protected USB logic and E1 through autonomous E0 | Provisional source capture; input fault qualification pending |
| [0028](0028-root-link-dark-vled-converter.md) | Link the VLED power stage with EN held low until the display interlock exists | Provisional source capture; display operation blocked |
| [0029](0029-provisional-battery-header-polarity.md) | Assign J2 pad 1 to protected BAT+ and pad 2 to ground, with measured/re-pinned harness acceptance | Provisional source capture; delivered pack polarity unverified |
| [0030](0030-gauge-bus-buffer-selection.md) | Use exact TCA9517ADGKR with switched gauge on A and application bus on B | Accepted for library and source capture; transitions and LOW levels unqualified |
| [0031](0031-separate-row-request-from-decoder-enable.md) | Separate GPIO8 row request from decoder E before hardware gating | Provisional source capture; hardware display interlock absent |
| [0032](0032-two-event-display-interlock-proposal.md) | Require a heartbeat followed by a distinct arm pulse before hardware can enable the display | Compact exact parts selected for provisional library capture; circuit and fit unqualified |
| [0034](0034-uniform-qt-coupon-pitch-proposal.md) | Uniform 1515 coupon pitch for routable matrix | Accepted |
| [0035](0035-host-asset-container.md) | Deterministic lossless host assets and bounded native decoding | Accepted for host software; production storage/transfer format provisional |
| [0036](0036-bounded-xor-asset-deltas.md) | Opt-in lossless XOR frame deltas with bounded reference chains | Accepted for host software; target memory/timing and content capacity pending |
| [0037](0037-host-playback-deadlines.md) | Absolute host playback deadlines with explicit lateness and latched failure | Accepted for host software; target scheduling/blanking unqualified |
| [0038](0038-host-mode-button.md) | Debounced host mode-button qualification and explicit software requests | Accepted for host software; target radio/interlock behavior unqualified |
| [0039](0039-host-content-session.md) | Compose host decoding, colour, playback and mode control | Accepted for host software; target integration unqualified |
