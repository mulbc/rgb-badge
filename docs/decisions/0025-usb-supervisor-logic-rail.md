<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0025: Supply the USB permission supervisor from USB logic power

Date: 2026-10-10. Status: selected for the Rev A schematic; source and hardware qualification remain open.

The charger input gate needs a supervisor that cannot be held up by connector power after the USB logic supply has failed. Move `TPS3808G01DBVR` U34 VDD pin 6, MR pin 3, its C38 bypass and R77 CT pull-up from `+5V_USB` to the existing `+3V3_USB` logic rail. Keep the R75/R76 SENSE divider on `+3V3_USB`, the R78 RESET pull-up on `+3V3_USB`, and the selected 100 kΩ CT connection. This leaves the nominal 2.916 V sense trip and TI's 180–420 ms fixed release interval unchanged. No USB, battery-charge or LED current limit changes.

The supply-domain move is an enabling connection for the proposed E1 gate, not charger permission by itself. U34 RESET still feeds only the current staged logic path; E1 EN remains unconnected. The 3.3 V regulator is also still behind the unresolved E0 source protector. Before E1 capture, recalculate combined RESET load and input injection, then verify startup, shutdown and rapid brownout against the final gate; TI specifies the low-voltage power-up RESET state under a supply-rise condition, not arbitrary waveforms. Independent Gate A review remains required before fabrication.

Source: [TI TPS3808 Rev N](https://www.ti.com/lit/ds/symlink/tps3808.pdf), pin table, RESET loading and delay conditions; [charger permission boundary](../design/charger-permission-boundary-2026-10-07.md).
