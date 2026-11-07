<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0041: Derive a provisional coupon pin inventory from canonical source

- Date: 2026-10-21
- Status: Accepted for source/host verification; pin-map freeze and target use not authorized
- Scope: Machine-readable Coupon Rev A controller definition; no circuit or GPIO change

## Decision

Generate a deterministic JSON inventory of all 41 U3 module pins from the validated canonical controller schematic and controlled module-library pin definitions. Retain module pad number, library/manufacturer name, GPIO where present, connected global net or explicit no-connect, physical land multiplicity and strapping/Octal-PSRAM restrictions. Record exact module MPN, hardware revision, source hashes and the reviewed manufacturer datasheet URL/version/hash. KiCad remains canonical; the derived JSON is not a second editable source of pin assignments.

Check the current manufacturer pin layout/table and N16R8 restrictions. Compare every derived pin with a fresh full native KiCad XML export and retain the native ERC/source-review result separately. Native XML checking must reject missing/duplicate/swapped pins, incorrect part/footprint, incorrect explicit no-connect nets and broken isolation between controller requests, actual decoder enable and isolated interlock outputs.

Default the tool to checking the committed inventory against regenerated source. Require an explicit write option to regenerate. Reject duplicate JSON keys and any metadata/pin/source drift. Exercise source and native-XML faults in host tests and check the source-derived artifact in CI without downloading manufacturer documents.

Mark the inventory provisional with production GPIO configuration disallowed. Do not generate an executable driver, arm command or target configuration from it. Pin defaults/timing, exact peripheral integration, independent hardware review and an explicit pin-map freeze remain outstanding. Keep GPIO35/36/37 unavailable for this Octal-PSRAM module and preserve unused strapping pins and native USB/ROM recovery. No symbol/footprint/BOM/net, current limit, display enable or fabrication gate changes here.
