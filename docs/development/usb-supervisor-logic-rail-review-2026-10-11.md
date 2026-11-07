<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Rev A USB supervisor supply-domain amendment, 2026-10-11

[ADR 0025](../decisions/0025-usb-supervisor-logic-rail.md) changes U34 `TPS3808G01DBVR` VDD pin 6 and MR pin 3, C38 bypass pin 1 and R77 CT pull-up pin 1 from `+5V_USB` to `+3V3_USB`. The SENSE divider and RESET logic/test boundary are unchanged; E1 is still absent. The generator, source checker, independent synthetic XML fixture and source fault-injection test were updated together. The generated `usb-permission.kicad_sch` remains byte-identical to canonical.

Native first-author check: KiCad CLI 10.0.6, output `/private/tmp/rgb-supervisor-native-final-20261011/`, 2026-10-11. ERC reported zero configured violations; full native XML contained 428 PCB items and 1,594 logical pins. Page 9 of the 16-page PDF was inspected: U34 VDD/MR and the nearby C38/R77 labels show `+3V3_USB`, with no label overlap; text extraction confirms the updated USB 3.3 V supervisor note. These are schematic/source checks, with no hardware or firmware connected.

The complete host regression suite passed 169 tests. One pre-amendment fault-injection fixture still searched for the old 5 V supply label; it was updated to inject the fault at U34's new VDD connection and the suite rerun. `git diff --check` found no whitespace errors.

The independent E1 gate, E0 source protection, transient default-off behavior and RESET loading remain to be qualified. Historical 2026-09-17 supervisor evidence covers the earlier `+5V_USB` circuit, not this revision. Gate A remains required before fabrication.

## E1 preparation follow-on

[ADR 0026](../decisions/0026-charger-e1-gate-network.md) selects an isolated third AUP sink for supervisor inhibition. The canonical USB conditioning sheet now revalues R78 to exact `ERJ2RKF1003X` 100 kΩ and R63 to exact `ERJ2RKF1004X` 1 MΩ before that sink is attached. Native KiCad CLI 10.0.6 output `/private/tmp/rgb-e1-prep-native-20261011/` again reported zero configured ERC violations and 428 PCB items/1,594 logical pins. The new 1 MΩ library symbol and page 9 were rendered and inspected; R63, R78 and the explanatory note display the intended values. `USB_RAW_LOGIC_READY` still has no physical connection to E1, so the native check is only a source review of this preparation step. The selected E1 network's assumed leakage screen and the actual RESET/AUP/U27 combined load remain to be qualified.

The selected EN divider's reproducible [static screen](../../tools/check-charger-gate-screen.py) gives a calculated minimum 1.434 V at a 3.0 V logic rail and maximum 1.116 V at 1.65 V using ±1% resistance, ±100 ppm/K over 65 K and an **assumed** 1.6 µA combined node leakage. This is a design calculation, not a measurement or a guaranteed partial-rail bound. The final wrapper rerun with this screen included is under `/private/tmp/rgb-e1-prep-final-20261011/`.

After the R63/R78 change, the complete host regression suite passed 169 tests, including all 18 wrapper tests. The first full run overlapped an edit to the wrapper and caught a transient incomplete shell file; `bash -n`, the focused wrapper suite and the complete suite then passed on the final source. The final native wrapper also reported zero configured ERC violations and the same 428/1,594 XML count. `git diff --check` found no whitespace errors.
