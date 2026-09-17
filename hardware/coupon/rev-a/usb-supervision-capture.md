<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# USB logic-rail supervisor capture

Date: 2026-09-17. Status: staged source capture; native review pending. Implements the already required hardware LOGIC_READY input of ADR 0011. It does not connect a charger, authorize charging or establish complete startup safety.

## Added circuit

Six items / sixteen logical pins are added to the unused lower-right area of `usb-conditioning.kicad_sch`. Totals become **443 PCB items / 1,636 logical pins on eleven pages**. One resistor symbol is new; all footprints and the TPS3808 symbol already passed native library review.

| Reference | Exact MPN | Role |
|---|---|---|
| U34 | TPS3808G01DBVR | VDD and MR on +5V_USB; SENSE on the divider; open-drain RESET drives USB_RAW_LOGIC_READY |
| C38 | GRM155R71C104KA88D | 100 nF bypass from +5V_USB to GND |
| R75 | ERJ-2RKF6203X | 620 kohm, 1%, from +3V3_USB to SENSE |
| R76 | ERJ-2RKF1003X | 100 kohm, 1%, from SENSE to GND |
| R77 | ERJ-2RKF1003X | 100 kohm from +5V_USB to CT; selects long fixed reset delay |
| R78 | ERJ-2RKF1002X | 10 kohm pull-up from +3V3_USB to RESET |

R66 remains the existing 100 kohm pull-down. U27 buffers RESET into USB_LOGIC_READY; TP26 observes the raw signal. U34 is powered from the input domain, rather than the rail it measures. VBUS_VALID, SWITCH_ON, ESP_RUNNING and USB_REQUEST remain four staged inputs. The two actuator outputs are still test boundaries.

## Source and static calculation

[TI TPS3808 SBVS050N](https://www.ti.com/lit/ds/symlink/tps3808.pdf), checked 2026-09-17: DBV pins 1=RESET, 2=GND, 3=MR, 4=CT, 5=SENSE, 6=VDD. Adjustable threshold is 0.405 V with ±2% error; maximum hysteresis is 3%, SENSE bias ±25 nA. The fixed long delay is 180–420 ms when CT connects to VDD through 40–200 kohm. PDF SHA-256: `74d889c0f68af88032f1633c26381817cc03e10d9fd3b4c177a044ad3ed86eed`.

[Panasonic ERJ](https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf), 2025-05-29, controls the new passive identity: ERJ2RK, F=1%, 6203=620 kohm, X=tape option; ±100 ppm/K TCR. It reuses the audited passive symbol and 0402 land pattern. PDF SHA-256: `78825b819853a63f57cc18214f321d2f1da9dc205a7e58af7db18ae73563e378`.

For initial tolerance at 25 C followed by temperature displacement up to 65 K (-40..85 C), resistance bounds multiply the factors: `Rmin=Rnom×0.99×0.9935`; `Rmax=Rnom×1.01×1.0065`. This includes the tolerance/TCR cross term. It does not include aging, reflow drift or resistor temperature outside this assumed interval.

With bias positive into SENSE, the rail trip is `Vtrip=VIT×(1+R75/R76)+Ibias×R75`. Exhausting both resistor endpoints, threshold error and signed bias gives:

| Calculated quantity | Result |
|---|---|
| Nominal falling threshold | 2.916 V |
| Falling threshold interval | 2.7626–3.0760 V |
| Worst rising threshold, including conservative maximum hysteresis | 3.1678 V |
| Delay after threshold recovery, CT fixed selection | 180–420 ms |

The divider statically removes permission above the Type-C detector's 2.7 V minimum at its worst low threshold, and can release below a **3.20 V design target**. The latter is a comparison target, not a proved minimum loaded LDO voltage. Its load/line/startup/capacitance qualification remains separate. This is circuit arithmetic, not a transient simulation.

## Limits still requiring closure

- U34 does not qualify VBUS at the BC detector, detect input overvoltage or replace missing protection. Do not reuse the 620k/100k divider as a 5 V-valid detector.
- The TPS3808 SENSE-to-RESET delay is listed as typical, not a guaranteed worst-case brownout cutoff. Its low-voltage RESET guarantee has supply-rise and load conditions. The quoted 0.8 V power-on point must not be treated as an unconditional clamp. The final charger sink/boost actuator needs an independent reviewed inhibition path.
- The delayed signal is a logic-supply qualification only. It is not evidence that either detector has completed classification; their actual GPIO states remain required by the permission gates.
- R78 and R66 form a loaded pull-up: with 3.3 V nominal and zero leakage, high is 3.0 V, not 3.3 V. Include resistor corners, supervisor output leakage, U27 input leakage and non-rail-input supply current in the electrical budget. Do not interpolate a guaranteed Schmitt threshold across supply voltages from typical curves. [SN74LVC2G17](https://www.ti.com/lit/ds/symlink/sn74lvc2g17.pdf), SCES381N, is the controlling input-level source.
- Keep resistor aging/reflow qualification, +5V_USB sequencing, LDO ramp/loaded voltage and fast-fall behavior open. There is no bench evidence or complete fail-safe actuator yet.

## Additional current-budget finding

ADR 0011's 497.993 mA total is an **initial-tolerance-only calculation**. If the pending 3.65 kohm ILIM resistor used the ordinary ERJ2RK 100 ppm/K family, the temperature corner becomes `1720/(3650×0.99×0.9935)+0.020+0.002 = 0.501107 A`. Thus that candidate exceeds the 500 mA allocation even before aging and reflow. This is a counterexample, not a claim that the unbuilt badge draws that current; the 20 mA and 2 mA remain allocations, not measured loads.

Do not populate those generic resistor candidates. Select qualified precision parts or reduce the programmed limits in a documented follow-on decision. Recheck boosted ILIM and ISET with the same complete resistance envelope. No current setting is raised or resistor substitution approved here. `check-power-design.py --require-usb-closure` retains this explicit blocker.

## Validation checkpoint

Host validation on 2026-09-17: **132 tests passed**, including source regeneration, fault injection and the unchanged 1,024 logic states. The strict power-closure command exits 1 for the documented blockers; this is expected, not a waived native/ERC failure.

Host checks trace every new pin, verify the exact resistor library, reproduce both conditioning/permission sheets, reject wrong supply/sense/CT paths and missing bypass capacitance, and calculate threshold corners. The 1,024-case logic test still exhausts both resolved LOGIC_READY states; it does **not** simulate U34. CLI/XML fixtures are synthetic and never native evidence.

Run the normal native wrapper and review the lower-right supervisor group on page 9, corrected headings on page 11 and new 620 kohm symbol. Expected output: **42 symbols, 25 footprints per raw view, eleven pages, 443 items / 1,636 pins, zero ERC violations**. No fabrication release follows from a pass.
