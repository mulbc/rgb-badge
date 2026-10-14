<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# onsemi row-pair candidate, isolated capture

This is a standalone, **unapproved** 16-row schematic for exact onsemi `NTLJD3119CTBG`. It is not linked into the coupon root, and the canonical `rows.kicad_sch` and BOM remain unchanged. It retains the decoder, one 1 kΩ P-gate pull-up and one 100 kΩ N-gate pull-down per row. The manufacturer-numbered map is audited in the [dual-row library record](../../dual-row-package-library-audit.md); use this schematic only with the separate onsemi footprint.

`tools/generate-coupon-rows.py --variant onsemi-candidate --output NEW_DIRECTORY` deterministically generates this sheet. The generator's default canonical output remains byte-for-byte identical to the previous version (SHA-256 `e332b3a7d50a1e66fba1797a9481fff820d7df3dd5a5181797295764b742aa28`). The local symbol/footprint tables and project file allow KiCad 10.0.6 to resolve the project libraries when this candidate is opened independently.

2026-10-14 source checks: KiCad XML netlist contains 16 candidate packages, 37 resistors, the decoder and its bypass capacitor. Each pair connects pin 4 to VLED, pin 3 to its unique row anode, pins 5/6 together at its gate node, pin 2 to the corresponding decoder select, and pin 1 to GND. Native ERC reports 18 expected standalone-boundary findings: two power inputs without a source and sixteen row-output labels with only the pair pin connected. It reports no library, footprint or other topology findings in this project context. These boundary findings must be resolved by root integration, not suppressed here.

This schematic is a topology and library trial. The nominal 0.15/0.18 mm package copper gaps, solder-mask-defined land recommendation, hot-device loss, switching behavior, battery clearance and Gate A engineering review remain open. It is not a fabrication file.
