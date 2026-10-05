<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Product requirements

Status: Baseline accepted; measurements pending
Source: requirements interview completed 2026-09-05

“Coupon” means the production-intent 16 × 16 validation board. “Final” means a complete cased 48 × 16 badge.

| ID | Requirement | Verification | Applies to |
|---|---|---|---|
| DSP-001 | Provide 48 × 16 individually controlled RGB pixels. | Design inspection and pixel self-test | Final |
| DSP-002 | Pixel pitch shall be no greater than 1.95 mm; baseline is exactly 1.95 mm. | PCB dimension inspection | Coupon/final |
| DSP-003 | Accept 24-bit source art and apply gamma and programmable white balance. | Golden-image firmware test and visual test | Coupon/final |
| DSP-004 | Support 60 content-frame updates per second and at least 1 kHz visual refresh. | Logic trace and camera test | Coupon/final |
| DSP-005 | Brightness shall remain at the user-programmed fixed value during normal playback. | Runtime state/telemetry test | Coupon/final |
| DSP-006 | Safety logic may disable the display on an electrical or thermal fault, but shall not silently dim it. | Fault-injection test | Coupon/final |
| DSP-007 | Coupon columns 0–7 shall use `EAST10105RGBA0` and columns 8–15 shall use `QBLP1515A-RGB2A`, both at 1.95 mm pitch; substitutions require written design review. | BOM, placement and incoming-part inspection | Coupon |
| DSP-008 | QBLP1515 LEDs shall keep the manufacturer-recommended pad geometry and use the non-mirrored 0°/90° checkerboard placement defined by ADR 0008. | Footprint audit, generated placement check, PCB DRC, assembly plot and AOI | Coupon |
| MEC-001 | Complete case shall not exceed 110 × 35 × 11 mm, excluding attachment thickness. | Caliper inspection | Final |
| MEC-002 | Complete badge shall aim for ≤75 g and shall never exceed 100 g, including cell, case and magnetic attachment. | Calibrated scale | Final |
| MEC-003 | Development case shall use two M2 screws plus tabs and support a replaceable diffuser. | Fit inspection | Coupon/final prototype |
| MEC-004 | Final design shall tolerate sweat and incidental splashes without claiming an IP rating. | Defined splash demonstration and inspection | Final |
| PWR-001 | A new selected cell shall provide roughly 6 h for the published reference workload and fixed brightness. | Logged full-charge runtime test | Final |
| PWR-002 | Continuous maximum full-white runtime shall be measured and published separately. | Logged stress runtime test | Final |
| PWR-003 | OFF-state battery drain with USB absent shall be below 50 µA. | Ammeter measurement after settling | Coupon/final |
| PWR-004 | Switch OFF shall disable the ESP32, display drivers, 3.3 V rail and LED rail. | Rail/current measurement | Coupon/final |
| PWR-005 | With the switch OFF, charging and status shall operate autonomously only from USB-C sources advertising 1.5 A/3 A; all other sources leave the charger in standby. | State-matrix test (ADR 0013) | Coupon/final |
| PWR-006 | Operation while charging shall remain stable; the charger power path shall respect the input limit. | Load/charge test and USB power log | Coupon/final |
| PWR-007 | The latching switch shall disconnect the fuel gauge in OFF while preserving hardware-only charging/status. On return to ON, initially uncertain SOC/runtime shall be identified as provisional until validated against the chosen pack. | OFF isolation/current test, OFF-charge state matrix and post-ON SOC comparison (ADR 0015) | Coupon/final |
| PWR-008 | The TPS631000 3.3 V application converter shall maintain at least 4.2 µF effective input and 10.4 µF effective output capacitance over the qualified rail, temperature and lifetime conditions, and hold the ESP32 module pads within 3.0–3.6 V during the defined operating/transient tests. Parallel coupon capacitors are a provisional implementation choice (ADR 0017). | Exact-part derating evidence, full-rail source-state review, layout/ERC/DRC, startup/load-step/attach-detach pad measurements and Gate A review | Coupon/final |
| USB-001 | Use a USB-C receptacle on the right short edge with 5 V input only; USB PD is not required. | Inspection and source test | Coupon/final |
| USB-002 | Enumerate native USB in both connector orientations with compliant A-to-C and C-to-C cables while switched ON. | Enumeration matrix | Coupon/final |
| USB-003 | Hardware shall bound total USB input draw for startup, standby, permitted charging and Type-C source changes; higher Type-C current shall not depend on application firmware. | Complete source-state analysis plus unprogrammed-board, configuration, suspend and attach/detach tests (ADR 0009) | Coupon/final |
| USB-004 | USB-A/default-current Type-C sources shall not charge or supply the application through the charger. Native USB data remains available while ON from battery power; recovery with a depleted/absent battery on these sources is not guaranteed. | USB data and power-state tests (ADR 0013) | Coupon/final |
| USB-005 | Use one fixed external input-current setting, bounded by the existing 0.9753 A ceiling, enabled only by qualified Type-C 1.5 A/3 A hardware permission. No switched ILIM resistor or firmware charge grant. Budget all VBUS loads within source allowance. | Complete-port budget and source-transition tests (ADR 0013) | Coupon/final |
| USB-006 | Account for 5.5 V normal VBUS at light load; derive the low-voltage and transient envelopes separately. Do not use a 5.25 V draft assumption as full input qualification. | Source-envelope and protection review (ADR 0014) | Coupon/final |
| CHG-001 | Prioritize the finished size and roughly six-hour reference runtime over charging speed. With the display off and a qualified USB-C source, document an exact-pack-specific time-to-80% and time-to-full planning target before Gate A and measure both on the coupon/final hardware. Charging shall remain within the terminated pack's current, temperature and protection limits; the previous 45–60/75–100 min targets are withdrawn (ADR 0016). | Exact-pack profile and current-limit review; dated charge log showing pack, source, ambient and hardware revision | Coupon/final |
| CHG-002 | Charge current shall never exceed the exact terminated-pack rating. | BOM/calculation review including qualified total ISET resistance error (ADR 0012), exact-pack rating and current log | Coupon/final |
| CHG-003 | A battery-facing NTC connected to the charger and a charger safety timer shall qualify charging without MCU assistance. The NTC may be pack-integrated or board-mounted under ADR 0019; a board-mounted sensor requires measured cell-to-board temperature bounds before final approval. | NTC hot/cold/open/short tests; simultaneous cell-surface and board-sensor logs for a board-mounted NTC | Coupon/final |
| RF-001 | BLE shall be disabled during normal playback. | Firmware state and current test | Coupon/final |
| RF-002 | Holding the mode button for approximately three seconds shall enter programming mode and enable BLE. | Functional test | Coupon/final |
| RF-003 | Programming-mode BLE shall work at 3 m line-of-sight in normal worn orientation. | Range test | Coupon/final |
| CTL-001 | Provide one momentary mode button and one real latching slide switch on the top edge. | Inspection and functional test | Coupon/final |
| STO-001 | Store at least 24 representative assets totalling five minutes alongside two application slots. | Image/partition and playback test | Coupon/final |
| MFG-001 | Maintain vendor-neutral KiCad, Gerber, drill, BOM and placement sources. | Release inspection | Coupon/final |
| MFG-002 | PCBA delivery shall require no manual SMT soldering by the user. | Purchase package and incoming inspection | Coupon/final |
| MFG-003 | Critical component substitutions require a written engineering review and updated BOM. | Release audit | Coupon/final |
| SAF-001 | Use a protected, documented and keyed connectorized LiPo pack. A two-wire pack is permitted when the charger has the independently operating battery-facing NTC arrangement and validation in ADR 0019. | Supplier documentation, connector/polarity inspection and temperature-sensing qualification | Coupon/final |
| SAF-002 | No cell surface may contact a component, solder joint, magnet or screw boss; swelling clearance is required. | CAD interference and physical inspection | Final |
| SAF-003 | An experienced hardware engineer shall review the coupon schematic and preliminary layout before fabrication. | Recorded review disposition | Coupon |
| SRC-001 | Quote JLCPCB, PCBWay and a vetted Alibaba turnkey PCBA supplier against the same frozen package. | Quote comparison | Final |
| CST-001 | Target USD 500–800 for coupon, five final PCBAs, cells, basic test tools and shipping, excluding independent review and case filament/design. | Quote ledger | Project |

## Reference workload

The provisional runtime workload consists of representative text, icons and animations with approximately 35% of pixels lit and brightness fixed at 25% of the validated hardware maximum. It is a repeatable engineering benchmark, not a restriction on user content. Coupon measurements will define the final asset bundle and calibrated power model.

## Power-architecture proposal verification addendum

2026-10-05: [ADR 0018](decisions/0018-complete-power-architecture-proposal.md) is **proposed, not an accepted replacement of the table above**. These verification refinements must be adopted/resolved before its material circuit changes are implemented. No current ceiling, battery rating or fabrication gate is relaxed.

| Existing requirements | Proposed refinement / acceptance evidence |
|---|---|
| USB-003/004/005/006, PWR-005 | Treat an independently disconnected charger input as the proposed physical implementation of unsupported-source standby; preserve battery-only application operation. Prove default-disable and total port current through startup, all partial-supply states, source downgrade and detach, including capacitance outside the charger limiter. |
| PWR-003/004/007 | Verify arbitrary switch-contact order, settling and bus isolation with either gauge or application rail absent/decaying; no reliance on firmware to order physical contacts. Retain provisional SOC after ON. |
| PWR-001/002 | Include added buffer/control losses and exact-pack minimum capacity/cutoff in the model before battery freeze; preserve fixed-brightness workload and separate full-white result. |
| DSP-006, PWR-004/008 | Hardware must keep VLED disabled and rows blank at boot, all reset paths, programming entry and physical OFF; audit residual rail energy, programmer injection and watchdog behavior. Define the exact interlock before capture. |
| CHG-001/002/003, SAF-001/002 | Select ISET, charge voltage, ITERM, NTC network and timer from the exact pack and full thermal budget; the 2.49 kΩ / 396 mA maximum is a conditional numerical proposal, not an approved BOM population. |

The [proposal's six capture holds](design/power-architecture-2026-10-05.md#8-one-consolidated-capture-hold-list) separate required engineering evidence from the remaining supplier information. Native ERC alone does not close them.
