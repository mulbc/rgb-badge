<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Rev A USB supervisor supply-domain amendment, 2026-10-11

[ADR 0025](../decisions/0025-usb-supervisor-logic-rail.md) changes U34 `TPS3808G01DBVR` VDD pin 6 and MR pin 3, C38 bypass pin 1 and R77 CT pull-up pin 1 from `+5V_USB` to `+3V3_USB`. The SENSE divider and RESET logic/test boundary are unchanged; E1 is still absent. The generator, source checker, independent synthetic XML fixture and source fault-injection test were updated together. The generated `usb-permission.kicad_sch` remains byte-identical to canonical.

Native first-author check: KiCad CLI 10.0.6, output `/private/tmp/rgb-supervisor-native-final-20261011/`, 2026-10-11. ERC reported zero configured violations; full native XML contained 428 PCB items and 1,594 logical pins. Page 9 of the 16-page PDF was inspected: U34 VDD/MR and the nearby C38/R77 labels show `+3V3_USB`, with no label overlap; text extraction confirms the updated USB 3.3 V supervisor note. These are schematic/source checks, with no hardware or firmware connected.

The complete host regression suite passed 169 tests. One pre-amendment fault-injection fixture still searched for the old 5 V supply label; it was updated to inject the fault at U34's new VDD connection and the suite rerun. `git diff --check` found no whitespace errors.

The independent E1 gate, E0 source protection, transient default-off behavior and RESET loading remain to be qualified. Historical 2026-09-17 supervisor evidence covers the earlier `+5V_USB` circuit, not this revision. Gate A remains required before fabrication.
