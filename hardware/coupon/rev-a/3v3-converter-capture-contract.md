<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Coupon Rev A 3.3 V application converter capture contract

Status: **pre-capture engineering calculation, 2026-09-30**. No 3.3 V converter circuit has been placed in the canonical KiCad schematic, no complete input rail or physical switch is connected, and no board has been built. This increment does not select the battery, charger ISET, or a PCB order. It applies the hard-OFF decision in [ADR 0004](../../../docs/decisions/0004-standalone-charging-and-hard-off-state.md), the independently switched gauge in [ADR 0015](../../../docs/decisions/0015-switch-fuel-gauge-with-application.md), and PWR-003/004 in [requirements](../../../docs/requirements.md).

## Circuit boundary and defaults

| TPS631000DRLR pin | Planned net or connection | Capture condition |
|---|---|---|
| 1 VOUT | `+3V3_APP` | Output capacitor and divider upper resistor return here; do not connect to USB-only 3.3 V. |
| 2 LX2, 3 LX1 | Opposite ends of the 1 µH inductor | Short, wide switching loop per TI layout guidance; no global power labels on LX. |
| 4 VIN | Protected charger `SYS` after its voltage/permission design is completed | Input capacitor to local ground. Never connect to the gauge's `+BAT_GAUGE_SW` pole. The source must be bounded to the IC's 1.6–5.5 V operating range including the qualified USB/charger corner. |
| 5 EN | The application pole of the latching ON/OFF switch drives it high from a valid protected source; an independent resistor pulls it to GND in OFF and throughout an open/bouncing contact. | Switch contact may drive *only control current*, not application load. Candidate 100 kΩ pull-down needs an exact resistor MPN, contact and OFF-leakage audit; it is not yet captured. Do not rely on MCU GPIO or an internal pull-down. |
| 6 MODE | GND | Fixed auto-PFM default for light-load efficiency; do not float or make boot behavior firmware-dependent. |
| 7 GND | Local power return | Tie input/output capacitors and feedback lower resistor into a suitable ground layout. |
| 8 FB | Junction of 511 kΩ VOUT-to-FB and 91 kΩ FB-to-GND | Keep the sense node clear of LX and high-current traces. |

The gauge uses a **separate** switch pole for its cell feed. VLED needs the physical ON condition **and** a hardware-qualified display request, with VLED disabled at boot/reset/programming. Sharing an ON-permission signal with the LED interlock is a later reviewed circuit decision, not a reason to route LED current through the switch. When OFF, the 3.3 V converter must disconnect its output and the unpowered application must not be back-fed from USB data, gauge I²C, debug pads, or another rail. TI calls the TPS631000 behavior *true shutdown with load disconnect*, but whole-board OFF isolation and <50 µA remain measured requirements. The separately powered USB-only logic is allowed to operate when USB is attached while the application switch is OFF.

## Manufacturer starting point and arithmetic

TI's [TPS631000 Rev. C datasheet](https://www.ti.com/lit/ds/symlink/tps631000.pdf), §§4, 5.3, 5.5, 6.3 and 7.2, gives the 2.7–4.3 V, 3.3 V/1.5 A typical design and these proposed parts/values. The precise passive order codes below are **candidates from TI's example**, not yet audited land patterns or a released BOM.

| Function | Starting value / candidate | Unresolved qualification |
|---|---|---|
| U | `TPS631000DRLR`, already audited project-local DRL0008A library | Native circuit ERC/XML, thermal and startup validation. |
| L between LX1/LX2 | 1 µH `DFE252012P-1R0M=P2` (Murata), ±20% initial tolerance, 42 mΩ max DCR, 2.5 × 2.0 × 1.2 mm max | Murata distinguishes 4.3 A at a 30% inductance drop from **3.2 A at a 40 °C winding temperature rise**, both referenced to 20 °C ambient. Exact land drawing, in-enclosure thermal/current derating and placement height remain open. |
| CIN | 22 µF `GRM187R61A226ME15` (Murata), TI-listed candidate | Effective capacitance at worst SYS voltage and temperature must stay ≥4.2 µF, including aging/tolerance. TI's Table 7-4 labels the row 6.3 V, while a [Murata-authored exact-part product sheet hosted by a distributor](https://img.ozdisan.com/ETicaret_Dosya/737402_1890026701..pdf) lists 10 V; resolve the inconsistency against current Murata documentation before BOM release. |
| COUT | 47 µF `GRM219R60J476ME44` (Murata), TI-listed candidate | Effective capacitance at 3.3 V and other corners must stay ≥10.4 µF; verify exact voltage rating, impedance and assembly profile. |
| Feedback | 511 kΩ upper / 91 kΩ lower | Select exact MPNs and tolerances, audit their footprint, and confirm output limits for all powered loads. TI requires the lower resistor ≤100 kΩ. |

With TI's 500 mV nominal feedback reference, the nominal output is `0.500 × (1 + 511/91) = 3.3077 V`. An **illustrative, independent ±1% initial tolerance** on both resistors combined with TI's 495–505 mV reference limits gives `3.2196–3.3981 V`. This is a calculation, not a guaranteed delivered voltage: reference conditions, resistor temperature drift, loading, routing drop, ripple and transients require a full worst-case check. Divider standing current is about `3.3077 V / (511 kΩ + 91 kΩ) = 5.49 µA` while ON; this divider belongs entirely on the switched output, so it cannot drain the battery through an enabled output in hard OFF.

The candidate 100 kΩ EN pull-down, if connected as specified and if **only** the published ±0.3 µA maximum EN input bias at 5.5 V opposes it, develops at most 30 mV in OFF; TI lists a 0.5 V minimum falling threshold. This is a component-level margin illustration, **not** a bound on switch contamination, PCB leakage, an attached debug tool, or an upstream driver. In ON it draws about 27–43 µA from a 2.7–4.3 V control source; the closed switch contact must keep EN above TI's 1.2 V rising threshold at all valid SYS voltages. The pull-down must return to GND, never to unswitched SYS.

TI specifies >1.65 V for startup, but its 1.5 A example and front-page output-current claim require VIN ≥2.7 V at 3.3 V output. Do not infer full-load operation down to converter UVLO or the cell protector's cutoff. Confirm minimum `SYS` at the final protected-pack end of discharge and while source qualified charging is present, with simultaneous ESP32/radio/logic loads. TI's typical example output current is a **capability condition**, not a measured badge load or efficiency promise.

**Inductor first-order screen:** Applying TI's boost-mode Equation 3 to the *example* 1.5 A output at VIN 2.7 V, VOUT 3.3 V, assumed 90% efficiency, 0.8 µH (the candidate's nominal 1 µH minus its initial 20% tolerance), and 1.8 MHz (TI's stated minimum switching frequency) gives `D = 0.1818`, average inductor current `2.037 A`, half ripple `0.170 A` and `Ipeak ≈ 2.207 A`. TI's suggested 20% saturation margin would require `≥2.649 A` against Murata's **4.3 A 30%-drop** figure at the specified reference condition. The separate **3.2 A / +40 °C** criterion is not a board thermal result; its winding rise, local ambient, inductance under DC bias, and actual peak current must be qualified in the small enclosure. Efficiency was assumed, not measured. A pack/charger SYS below 2.7 V or a higher load needs a fresh calculation.

## Next capture and release checks

1. Audit exact passive manufacturer drawings and effective-capacitance curves, then create project-local symbols/land patterns or reuse already audited exact-MPN libraries. Check the inductor-current margin against TI's worst operating-condition equation and derating, not only its table saturation value.
2. Finish the protected `SYS` source and exact two-pole switch (including orientation/contact sequencing), then wire VIN and EN. The USB-only rail must remain distinct. Do not make a draft PWR_FLAG look like a real `SYS` source.
3. Capture a dedicated schematic sheet, extend exported-netlist invariants to the eight IC pins, feedback network, switched enable, MODE, caps, inductor and output loads; require zero configured ERC. Inspect native KiCad 10.0.6 PDF and footprint layers. Replace/reconcile old draft supply flags at the real source boundary.
4. Before Gate A, calculate tolerance/ripple/derating and startup/inrush over minimum pack voltage, charging and 5.5 V input envelope; review hot loops, thermal copper, EMI and assembled thickness. On the coupon, log the rail during switch bounce, USB attach/detach, RF bursts, simultaneous LED switching and output load steps. Measure OFF rail voltage and battery current both before firmware has ever run and after normal use, with USB absent and present separately.

Sources: [TI TPS631000 Rev. C (August 2026)](https://www.ti.com/lit/ds/symlink/tps631000.pdf) for electrical limits, Equation 3 and its reference circuit; [Murata DFE252012P series sheet](https://www.murata.com/~/media/webrenewal/products/inductor/chip/tokoproducts/wirewoundmetalalloychiptype/m_dfe252012p.ashx) for distinct current limits, inductance tolerance, dimensions and land-pattern sketch; [Murata GRM187R61A226ME15 product page](https://pim.murata.com/en-us/pim/details/?partNum=GRM187R61A226ME15%23) for exact-family identification; [power library audit](power-library-audit.md) for the already audited IC symbol/footprint. The Murata capacitor page did not expose numeric DC-bias data through the accessible text view; no effective-capacitance claim has been made. Full characteristic curves and assembly evidence remain to be gathered.
