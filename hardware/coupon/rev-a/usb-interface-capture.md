<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Staged USB interface capture

**Active update (2026-09-19):** ADR 0013 removes BC1.2 and ADR 0014 replaces U29 with TPS70933DBVR, EN intentionally open. The output-capacitance requirement is now 1.5–47 µF effective for the 3.3 V part, ESR ≤0.2 ohm. Earlier TLV755/BC counts and 0.47 µF requirements below are historical. See [current audit](usb-input-protection-screening.md); native review of this U29 change is pending.


Date: 2026-09-17. Status: [native ERC/XML passed at d502e65](../../../docs/development/usb-interface-review-d502e65.md); two drawing overlaps were found and source-corrected, awaiting the next native PDF. Implements the detector/data topology already accepted by ADRs 0010/0011. It does not complete the power section.

## Captured circuit

`usb-interface.kicad_sch` adds **20 PCB items / 84 logical pin entries**, including eleven explicit NCs. At d502e65 the coupon had **437 PCB items / 1,620 logical pin entries across eleven pages**. The follow-on supervisor raises these to 443 / 1,636 without adding a page. Repeated same-number connector shell lands are one netlist pin, as are other repeated ground-pad lands. Power flags are virtual and excluded.

| Reference | Exact part / role | Connections and intent |
|---|---|---|
| J1 | USB4505-03-0-A | Both D+ contacts joined; both D- contacts joined; separate CC1/CC2; both VBUS and GND lands used; shell grounded; SBU1/2 NC |
| U33 | TPD4E05U06DQAR | Four shunt channels on connector D+/D-/CC1/CC2; both GND pins used; four NCs explicit |
| U31 | TUSB320LAIRWBR | +3V3_USB supply; PORT and EN_N grounded; ADDR floating selects GPIO mode; unused OUT3/ID NC; built-in Rd, no parallel external CC pull-downs |
| R71 | ERJ-2RKF8873X | 887 kohm, 1%, connector VBUS to U31 VBUS_DET |
| U30 | BQ24392RSER | VBUS-domain detector; GOOD_BAT tied to its local supply, independent of the application rail |
| R72/R73/R74 | ERJ-2RCF2R20X | 2.2 ohm, 1%, ballast on detector VBUS, connector-facing D+ and D- respectively |
| U32 | TS3USB31ERSER | Powered only by +3V3_APP; OE grounded; detector faces D pins, ESP32 faces HSD pins; NC explicit |
| U29 | TLV75533PDBVR | USB-only 3.3 V regulator; IN and EN on the staged +5V_USB input, OUT on +3V3_USB, NC explicit |
| C30/C31, C33/C34 | GRM155C71A105KE11D | Two parallel 1 uF / 10 V X7S capacitors at LDO input and detector input respectively |
| C32 | GRM188R60J106ME47D | 10 uF / 6.3 V X5R on the USB-only 3.3 V output |
| C35/C36/C37 | GRM155R71C104KA88D | 100 nF / 16 V X7R at BC detector, CC detector and application-powered data switch |
| TP32/TP33 | Copper test pads | VBUS_CONNECTOR / +5V_USB boundary observability |

The two Type-C outputs and three BC1.2 outputs now connect to the previously captured Schmitt inputs. Their existing pull-ups R60/R61/R62/R64 remain on +3V3_USB. This does not introduce a battery-powered pull-up onto an unpowered TUSB320. The follow-on [logic supervisor](usb-supervision-capture.md) drives LOGIC_READY; four other supervisor/application inputs remain staged.

The data path is J1 → ballast → BQ24392 → TS3USB31E → existing 22-ohm controller resistors → ESP32. U33 is shunt ESD protection, not a series-through device. The two historical isolated USB_D-/USB_D+ warnings should disappear: the ERC gate now accepts **zero violations only**. No new exception has been added.

## Source review and passive audit

The already native-reviewed IC and connector libraries retain their pin maps and footprints. Sources were reread for the circuit connections:

- [BQ24392, SLIS146G](https://www.ti.com/lit/ds/symlink/bq24392.pdf): pin table, GOOD_BAT/timer behavior, GPIO outputs, ballast and bypass guidance. The supply-domain connection avoids using GOOD_BAT for product OFF isolation.
- [TUSB320LAI, SLLSEQ8D](https://www.ti.com/lit/ds/symlink/tusb320lai.pdf): GPIO/UFP straps, internal Rd, VDD ramp requirement, open-drain pull-up domain and VBUS_DET resistor table. Although prose says 900 kohm, the electrical table specifies 855/887/920 kohm min/typ/max. R71 at 887 kohm fits this interval; 1% tolerance plus ±100 ppm/K over -40..85 C gives a conservative calculated **872.422155–901.693155 kohm** interval, using 25 C as reference and multiplying initial-tolerance and TCR factors (including their cross term).
- [TS3USB31E, SCDS256A](https://www.ti.com/lit/ds/symlink/ts3usb31e.pdf): D/HSD polarity, OE and partial-power-down conditions. Zero-VCC isolation applies specifically to the detector-facing D pins; it does not prove safe behavior at every intermediate supply voltage.
- [TLV755P, SBVS320D](https://www.ti.com/lit/ds/symlink/tlv755p.pdf): DBV pin map, bypass, stability and startup/dropout cautions.
- [TPDxE05U06, SLVSBO7O](https://www.ti.com/lit/ds/symlink/tpd4e05u06.pdf): four channel pins, two grounds and four NC pins. No VBUS protection is claimed from this data/CC array.
- GCT drawing A2 and the [USB4505 audit](usb-connector-audit.md) control the previously accepted contact/land mapping. Its mechanical and assembly holds are unchanged.

New exact passive symbols: `ERJ-2RKF8873X` and `ERJ-2RCF2R20X`. Both use the existing audited nonpolar 0402 resistor land pattern and passive pins 1/2. [Panasonic's ERJ datasheet](https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf), dated 2025-05-29, specifies **2RK** for 10 ohm–1 Mohm and **2RC** for 1–9.76 ohm. The different letter is intentional, not a substitute. Code 8873 means 887 kohm, 2R20 means 2.20 ohm, F is 1%, X is the stated tape option. The downloaded PDF SHA-256 is `78825b819853a63f57cc18214f321d2f1da9dc205a7e58af7db18ae73563e378`. No new footprint was added. The two capacitor families are reused from the [controller capture](controller-capture.md); their nominal ratings do not establish effective capacitance in this new application.

TI source hashes match the controlled audits: TS3USB31E `b33c728a099c9f32d3acae56125b13bb88bad6f8925ddf32be69a3bd8908d940`, TPD4E05U06 `c167cf1e72a5473a4d2c59b6a3c0251498701da05b7785919b9ceaae3b3e02c6`. Other source hashes remain in the power/replacement-library audits.

## Deliberate unfinished boundaries

1. **No connector-to-supply bridge.** VBUS_CONNECTOR and +5V_USB are different nets. The missing input protection must be designed before joining them. #FLG05 marks a draft 4.80–5.25 V source assumption at +5V_USB; it is not a regulator, protection device, or an approved external bench-power instruction. The old #FLG04 is removed because U29 now drives +3V3_USB. #FLG06 declares power on USB_BC_VBUS after the passive ballast R72 for ERC; it is derived from +5V_USB, not an independent supply. The checker requires R72 and both sides of that connection. The schematic cannot be treated as a powered USB prototype yet.
2. **Voltage and transient closure.** BQ24392's recommended 4.75–5.25 V supply range, its 2.2-ohm ballast drop, valid detection under cable droop, 5.5 V Schmitt input ceiling, USB overshoot and the LDO input limit must all be reconciled with the actual protection stage. A nominal 5 V label is insufficient. TUSB320 requires a VDD ramp within 25 ms; the regulator's startup/dropout recovery behavior also requires qualification.
3. **Capacitance and inrush.** Nominal input capacitance is 4.1 uF across the LDO/detector branches before adding protection/charger capacitance. Behind the LDO are 10 uF plus the nineteen existing logic 100 nF capacitors and the CC detector's 100 nF. Neither number is a worst-case connector inrush result. Each two-capacitor input bank must retain at least 1 uF effective capacitance after voltage, tolerance, temperature and aging. U29's output must retain at least 0.47 uF, with its ESR/stability requirements met. Those effective-capacitance bounds remain unqualified; parallel nominal values are not evidence of compliance. The X7S input capacitors must be assessed for this application; the LDO output uses X5R.
4. **Current.** Detector currents published only as typical do not close the whole-port maximum. Include every default/pull-up, buffer, logic gate, detector, LDO and later supervisor in separate configured, unconfigured and suspend budgets. No input/charge-current setting is increased by this increment.
5. **Data and power sequencing.** Verify both cable orientations, BC timing, the combined series resistance, full-speed signaling, OFF leakage, attach/detach and both switch supply ramps. Static connectivity cannot establish enumeration or prevent every intermediate-voltage back-power condition.
6. Supervisors, startup/brownout inhibition, actual charger/ILIM actuation, application grants, battery/NTC, switched converters and monitors remain pending. Shell grounding requires layout/EMC review; the GCT cutout relief/stack-up/process holds remain. There is no PCB and no bench result.

## Validation and native checkpoint

`generate-coupon-usb.py --output NEW_DIRECTORY` reproduces the one new canonical sheet and refuses overwrite. The shared constrained wire tracer validates each source pin, explicit NC, controlled symbol cache and population property. `check-coupon-usb.py` checks the two new exact resistor symbols and the independent circuit pin map. The full exported-XML checker now requires all 437 items / 1,620 logical pins, including the eleven new NCs.

Fault tests cover a CC short, reversed data, swapped current-advertisement outputs, mixed BC status signals, wrong power domains, bypassed input protection/isolation, altered passives, missing NCs and duplicate XML pins. Synthetic XML is test-only, never a KiCad result.

Host validation: **126 tests passed** on 2026-09-17, including six new USB capture tests with multiple fault cases. Canonical regeneration and the unchanged 1,024-state permission comparison passed. The strict USB-closure gate still returns 1 for the documented incomplete circuitry. No native or bench result is claimed for this increment.

The owner completed the d502e65 run below; its [review record](../../../docs/development/usb-interface-review-d502e65.md) preserves the findings. The next required run is the combined [supervisor checkpoint](usb-supervision-capture.md). Historical expected outputs for d502e65: **41 symbols, 25 footprints per raw view, eleven PDF pages, 437 items / 1,620 pins and zero ERC violations**. Inspect the new USB interface page and updated conditioning page. Power closure remains blocked even if those checks pass; independent Gate A still precedes fabrication.
