<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

ADR 0243 permits the exact ignored PAIR01 supply prototype frozen in
`mechanical/review/pair01-supply-routing-plan.json`: only its 62 retired
leaves, 27 new ordinary-width items and one same-face package transform.
Adoption requires all 212 original groups and retained copper, matching
23 opens, exact104, inverse/replay/fault/visual gates and unchanged holds.

ADR 0121 permits ignored localization of exact R70 and TP31 beside the
existing USB-control logic, replacing only three recorded obsolete leaves
with ordinary B.Cu branches ≤16 mm. Preserve the complete supply group,
all other live groups and hardware current-limit boundaries. No new via or
selection is allowed without the complete source/contact/DRC/replay/fault gate.

ADR 0120 permits a read-only coordinated PAIR01/R6 screen with original
parts, gate association, ordinary widths and a ≤6 mm row-current lead bound.
No PCB migration follows from a clear sample without exact source contacts,
replacement ledger and complete functional-group/DRC/replay/fault validation.

ADR 0119 permits ignored localization of exact R6 near PAIR01 with a gate
lead ≤3 mm, retirement of only the six recorded obsolete supply-leaf items,
retention of the shortened original shared stem and an explicit supported-size
capture to the connected VLED plane. Preserve every old group and all other
copper/parts/settings; full successor validation is required before selection.

ADR 0118 permits a read-only finite placement screen of corrected U49 near
U48. No pose or copper change may be selected from that preliminary screen;
any later migration needs an exact support/contact/replacement ledger and all
functional-group, DRC, replay, fault and qualification boundaries retained.

**2026-11-12 DSP-006/PWR-004 correction (ADR 0117):** Exact
SN74LVC1G74RSER at U49/U50 shall use the RSE-specific PRE-bar/CLR-bar/Q/GND/
Q-bar/D/CLK/VCC assignment on pins 1/2/3/4/5/6/7/8. Preserve the functional
heartbeat-then-arm logic, clear pull-down, defined preset and dark candidate
output isolation. Historical boards must explicitly report the superseded
generic pin map. A corrected routing successor must restore every functional
connection under the recorded terminal permutation, without extra DRC
findings or changes to current/protection limits. The preceding 35-open count
is historical CAD evidence, not acceptance of the flip-flop wiring.

# Product requirements

Status: Baseline accepted; measurements pending
Source: requirements interview completed 2026-09-05

“Coupon” means the production-intent 16 × 16 validation board. “Final” means a complete cased 48 × 16 badge.

**MEC-001 revision, 2026-10-14 (ADR 0033):** The owner accepted 4 mm more PCB length for the working final-badge design. The 114 × 32.5 mm PCB target requires a 118 × 35 × 11 mm outer-case limit in this layout direction. Native placement has not established routing or enclosure fit; the case, USB opening, mass and battery stack remain verification work.

**DSP-002/007/008 revision, 2026-10-18 (ADR 0034):** The owner accepted 2.2 mm horizontal pitch and uniform 0° orientation for the coupon's 1515 half. Its vertical pitch and both axes of the 1010 half remain 1.95 mm. The final badge's maximum 1.95 mm pitch is unchanged. The coupon halves therefore no longer provide an equal-pitch optical comparison.

| ID | Requirement | Verification | Applies to |
|---|---|---|---|
| DSP-001 | Provide 48 × 16 individually controlled RGB pixels. | Design inspection and pixel self-test | Final |
| DSP-002 | Final-badge pixel pitch shall not exceed 1.95 mm in either axis. Coupon pitch shall meet DSP-007. | PCB dimension inspection | Coupon/final |
| DSP-003 | Accept 24-bit source art and apply gamma and programmable white balance. | Golden-image firmware test and visual test | Coupon/final |
| DSP-004 | Support 60 content-frame updates per second and at least 1 kHz visual refresh. | Logic trace and camera test | Coupon/final |
| DSP-005 | Brightness shall remain at the user-programmed fixed value during normal playback. | Runtime state/telemetry test | Coupon/final |
| DSP-006 | Safety logic may disable the display on an electrical or thermal fault, but shall not silently dim it. | Fault-injection test | Coupon/final |
| DSP-007 | Coupon columns 0–7 shall use `EAST10105RGBA0` at 1.95 mm pitch in both axes; columns 8–15 shall use `QBLP1515A-RGB2A` at 2.2 mm horizontal and 1.95 mm vertical pitch. Substitutions require written design review. | BOM, placement and incoming-part inspection | Coupon |
| DSP-008 | Coupon `QBLP1515A-RGB2A` LEDs shall retain the manufacturer-recommended pad geometry and use uniform non-mirrored 0° placement under ADR 0034. | Footprint audit, generated placement check, PCB DRC, assembly plot and AOI | Coupon |
| MEC-001 | Complete case shall not exceed 118 × 35 × 11 mm, excluding attachment thickness. The working PCB length is 114 mm. | Caliper inspection and PCB/case fit review | Final |
| MEC-002 | Complete badge shall aim for ≤75 g and shall never exceed 100 g, including cell, case and magnetic attachment. | Calibrated scale | Final |
| MEC-003 | Development case shall use two M2 screws plus tabs and support a replaceable diffuser. | Fit inspection | Coupon/final prototype |
| MEC-004 | Final design shall tolerate sweat and incidental splashes without claiming an IP rating. | Defined splash demonstration and inspection | Final |
| PWR-001 | A new selected cell shall provide roughly 6 h for the published reference workload and fixed brightness. | Logged full-charge runtime test with external inline battery-current/energy measurement where needed (ADR 0021) | Final |
| PWR-002 | Continuous maximum full-white runtime shall be measured and published separately. | Logged stress runtime test with external inline battery-current/energy measurement (ADR 0021) | Final |
| PWR-003 | OFF-state battery drain with USB absent shall be below 50 µA. | External series ammeter measurement after settling (ADR 0021) | Coupon/final |
| PWR-004 | Switch OFF shall disable the ESP32, display drivers, 3.3 V rail and LED rail. | Rail/current measurement | Coupon/final |
| PWR-005 | With the switch OFF, charging and status shall operate autonomously only from USB-C sources advertising 1.5 A/3 A; all other sources leave the charger in standby. | State-matrix test (ADR 0013) | Coupon/final |
| PWR-006 | Operation while charging shall remain stable; the charger power path shall respect the input limit. | Load/charge test, USB power log and external inline battery-current log (ADR 0021) | Coupon/final |
| PWR-007 | The latching switch shall disconnect the fuel gauge in OFF while preserving hardware-only charging/status. On return to ON, initially uncertain SOC/runtime shall be identified as provisional until validated against the chosen pack. | OFF isolation/current test, OFF-charge state matrix and post-ON SOC comparison (ADR 0015) | Coupon/final |

**2026-10-11 PWR-003/007 buffer capture (ADR 0030):** Use exact `TCA9517ADGKR` with the switched gauge on A and application I²C on B. Provide local pull-ups/decoupling for each supplied segment. Before Gate A, verify all LOW-level margins, rail-contact order and decay, powered-off isolation/leakage, bus recovery and OFF current with the populated board; library and schematic source checks cannot establish these behaviors.
| PWR-008 | The TPS631000 3.3 V application converter shall maintain at least 4.2 µF effective input and 10.4 µF effective output capacitance over the qualified rail, temperature and lifetime conditions, and hold the ESP32 module pads within 3.0–3.6 V during the defined operating/transient tests. Parallel coupon capacitors are a provisional implementation choice (ADR 0017). | Exact-part derating evidence, full-rail source-state review, layout/ERC/DRC, startup/load-step/attach-detach pad measurements and Gate A review | Coupon/final |
| USB-001 | Use a USB-C receptacle on the right short edge with 5 V input only; USB PD is not required. | Inspection and source test | Coupon/final |
| USB-002 | Enumerate native USB in both connector orientations with compliant A-to-C and C-to-C cables while switched ON. | Enumeration matrix | Coupon/final |
| USB-003 | Hardware shall bound total USB input draw for startup, standby, permitted charging and Type-C source changes; higher Type-C current shall not depend on application firmware. | Complete source-state analysis plus unprogrammed-board, configuration, suspend and attach/detach tests (ADR 0009) | Coupon/final |
| USB-004 | USB-A/default-current Type-C sources shall not charge or supply the application through the charger. Native USB data remains available while ON from battery power; recovery with a depleted/absent battery on these sources is not guaranteed. | USB data and power-state tests (ADR 0013) | Coupon/final |
| USB-005 | Use one fixed external input-current setting, bounded by the existing 0.9753 A ceiling, enabled only by qualified Type-C 1.5 A/3 A hardware permission. No switched ILIM resistor or firmware charge grant. Budget all VBUS loads within source allowance. | Complete-port budget and source-transition tests (ADR 0013) | Coupon/final |
| USB-006 | Account for 5.5 V normal VBUS at light load; derive the low-voltage and transient envelopes separately. Do not use a 5.25 V draft assumption as full input qualification. | Source-envelope and protection review (ADR 0014) | Coupon/final |
| CHG-001 | Prioritize the finished size and roughly six-hour reference runtime over charging speed. With the display off and a qualified USB-C source, document an exact-pack-specific time-to-80% and time-to-full planning target before Gate A and measure both on the coupon/final hardware. Charging shall remain within the terminated pack's current, temperature and protection limits; the previous 45–60/75–100 min targets are withdrawn (ADR 0016). | Exact-pack profile and current-limit review; dated charge log showing pack, source, ambient and hardware revision | Coupon/final |
| CHG-002 | Charge current shall never exceed the exact terminated-pack rating. | BOM/calculation review including qualified total ISET resistance error (ADR 0012), exact-pack rating and external inline pack-current log (ADR 0021) | Coupon/final |
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

**2026-10-11 SAF-001 assembly rule (ADR 0029):** Rev A schematic pad J2.1 is protected battery positive and J2.2 is GND. The selected LP452845/PHR-2 lead order is unverified. Before first mating, measure protected pack polarity at its keyed cavities, repin the harness if necessary, and independently check board-header pad polarity and mating orientation. Record lot, drawing revision and readings. Schematic capture alone does not satisfy this requirement.
| SAF-002 | No cell surface may contact a component, solder joint, magnet or screw boss; swelling clearance is required. | CAD interference and physical inspection | Final |
| SAF-003 | An experienced hardware engineer shall review the coupon schematic and preliminary layout before fabrication. | Recorded review disposition | Coupon |
| SRC-001 | Quote JLCPCB, PCBWay and a vetted Alibaba turnkey PCBA supplier against the same frozen package. | Quote comparison | Final |
| CST-001 | Target USD 500–800 for coupon, five final PCBAs, cells, basic test tools and shipping, excluding independent review and case filament/design. | Quote ledger | Project |

## Reference workload

**2026-10-21 DSP-003/STO-001 image preparation (ADR 0042):** Import already-sized static 8-bit PNG and GIF source art without resampling, quantization, frame merging or implicit timing changes. Preserve decoded RGB/composited GIF frames and exact positive delays; require an explicit static duration and background for nonopaque alpha. Reject unsupported sample depth, animation/colour/orientation metadata, malformed input and resource-limit violations. Failed import shall preserve any existing output. Verify against independent pixel/duration expectations through the native decoder. This does not satisfy representative storage or target/hardware acceptance.

**2026-10-21 provisional board definition (ADR 0041):** Derive the machine-readable Coupon Rev A U3 inventory from canonical KiCad source, preserving all module pins, explicit no-connects, exact MPN and package, USB/strapping/Octal-PSRAM restrictions and isolated display-request boundaries. Verify a fresh native XML export, record manufacturer-source identity and detect source/JSON drift in CI. The derived inventory remains provisional and shall not authorize production GPIO configuration or hardware arm; explicit freeze and independent review remain open.

**2026-10-21 repeatable host verification (ADR 0040):** Build the existing software core through one reusable host library and exercise native/cross-language checks plus both capacity reproductions with GNU and Clang compilers. A host asset inspection success shall require decoding/CRC validation of every frame, not only container validation. Input allocation remains bounded by the format limit. Host build/integrity results do not satisfy target, representative storage or hardware acceptance.

**2026-10-21 DSP-003/STO-001 software preparation (ADR 0035):** Host assets shall preserve exact RGB888 pixels and explicit frame durations through deterministic encoding and bounded native decoding. Reject malformed/unsupported containers and corruption, and verify cross-language golden frames before target integration. Parser resource bounds are format limits, not a flash-partition allocation. Representative five-minute capacity, dual application slots and target playback remain acceptance work.

**2026-10-21 lossless delta extension (ADR 0036):** Version 2 may depend on a preceding validated frame, with an independent first frame and at most 59 consecutive deltas. Verify exact reconstructed pixels/durations, reference ownership, failure/rewind behavior and bounded memory alongside version 1 compatibility. No automatic dimming, quantization or frame dropping is permitted; target timing/stack and representative storage acceptance remain open.

The provisional runtime workload consists of representative text, icons and animations with approximately 35% of pixels lit and brightness fixed at 25% of the validated hardware maximum. It is a repeatable engineering benchmark, not a restriction on user content. Coupon measurements will define the final asset bundle and calibrated power model.

**2026-10-21 integrated host session (ADR 0039):** Compose validated source decoding, absolute playback deadlines, fixed colour/brightness and mode-button requests. Boot/reset, raw button interruption, programming, stop, completion and latched session faults shall clear software output. Start shall be explicit after release or completion; ordinary commands shall not clear session faults. BLE shall be requested only in Programming. Software eligibility is never hardware arm permission; physical blanking, radio resources, target timing/memory and the independent interlock remain acceptance work.

**2026-10-21 DSP-003/004/006 playback preparation (ADR 0037):** Host playback shall use absolute monotonic microsecond deadlines and original frame durations, expose any admission lateness, and never silently drop frames or rebase timing. Exceeding an explicit lateness budget, an entirely expired next interval, backward time, timeline overflow or decoding failure shall latch a software error and clear software output. Explicit restart rewinds; completion/stop clear output. This does not qualify target timing, visual refresh or physical blanking.

**2026-10-21 RF-001/002, CTL-001, DSP-006 mode preparation (ADR 0038):** The host mode-button model shall require an initial qualified release, debounce input, qualify one approximately three-second hold, request BLE only in Programming and immediately request display inhibit on a raw press. Backward time shall latch a fault with BLE request withdrawn and inhibit asserted. Explicit reset requires release again; removing inhibit is never a display-arm command. Actual GPIO polarity, sampling cadence, BLE resources/current, ROM recovery and physical interlock behavior remain target/hardware acceptance work.

## Power-architecture proposal verification addendum

2026-10-05: [ADR 0018](decisions/0018-complete-power-architecture-proposal.md) is **proposed, not an accepted replacement of the table above**. These verification refinements must be adopted/resolved before its material circuit changes are implemented. No current ceiling, battery rating or fabrication gate is relaxed.

| Existing requirements | Proposed refinement / acceptance evidence |
|---|---|
| USB-003/004/005/006, PWR-005 | Treat an independently disconnected charger input as the proposed physical implementation of unsupported-source standby; preserve battery-only application operation. Prove default-disable and total port current through startup, all partial-supply states, source downgrade and detach, including capacitance outside the charger limiter. |
| PWR-003/004/007 | Verify arbitrary switch-contact order, settling and bus isolation with either gauge or application rail absent/decaying; no reliance on firmware to order physical contacts. Retain provisional SOC after ON. |
| PWR-001/002 | Include added buffer/control losses and exact-pack minimum capacity/cutoff in the model before battery freeze; preserve fixed-brightness workload and separate full-white result. |
| DSP-006, PWR-004/008 | Hardware must keep VLED disabled and rows blank at boot, all reset paths, programming entry and physical OFF; audit residual rail energy, programmer injection and watchdog behavior. Define the exact interlock before capture. |
| DSP-006, PWR-004/008 | [ADR 0031](decisions/0031-separate-row-request-from-decoder-enable.md) first separates GPIO8 `ROW_ENABLE_REQ_N` from decoder `ROW_ENABLE_N`, leaving R42 to hold rows blank while the gate is absent. Capture an exact hardware gate before either net can permit display operation; verify the distinct native pin nets. |
| DSP-006, PWR-004/008 | [ADR 0032](decisions/0032-two-event-display-interlock-proposal.md) proposes a hardware-recorded watchdog heartbeat followed by a distinct arm edge, asynchronous reset/mode/fault clearing, and measured VLED-window gating of decoder E. The root-linked source now captures this logic with both candidate outputs isolated at test pads; before connecting actual EN/E, verify the exact clear and edge circuits, 3.3 V ramp and retained-VLED response. The dark schematic remains the source baseline. |
| DSP-006, PWR-004/008 | ADR 0032 also proposes an exact 4.7 kΩ passive VLED bleed. Calculate its operating loss and ideal discharge, then verify actual VLED decay and row-off behavior with the built capacitor bank; the bleed alone is not an interlock acceptance test. |
| CHG-001/002/003, SAF-001/002 | Select ISET, charge voltage, ITERM, NTC network and timer from the exact pack and full thermal budget; the 2.49 kΩ / 396 mA maximum is a conditional numerical proposal, not an approved BOM population. |

The [proposal's six capture holds](design/power-architecture-2026-10-05.md#8-one-consolidated-capture-hold-list) separate required engineering evidence from the remaining supplier information. Native ERC alone does not close them.

**2026-10-07 USB-005/PWR-006/CHG-001 proposal:** [ADR 0022](decisions/0022-lower-fixed-usb-input-limit-proposal.md) screens one fixed 3.65 kΩ ILIM resistor, calculated at 0.361–0.476 A, to separate the charger's steady input limit from the screened eFuse breaker threshold. It is not accepted or captured. Before adoption, verify charge-through operation and pack-specific charge times at the lower input limit, as well as the complete USB load/startup/fault envelope. Existing current ceilings and safeguards remain in force.

**2026-10-07 PWR-005/USB-003/005 proposal, provisionally captured 2026-10-10:** [ADR 0023](decisions/0023-charger-en2-local-clamp-proposal.md) screens an EN2 mode source from the admitted charger input with a 2.5 V local clamp. The shunt symbol/pads have been audited and the source is now root-linked; confirm EN2 current across the intended clamp voltage, verify the resistor's local thermal rating, and capture attach/detach/downgrade/trip waveforms. This does not approve the charger gate or fixed-mode timing.

**2026-10-09 CHG-001/002/003, SAF-001/002 design target:** [ADR 0024](decisions/0024-lp452845-pack-and-temperature-window.md) selects the protected `LP452845`/PHR-2 assembly of drawing FD_6225_10 index 1 and mating JST `S2B-PH-SM4-TB` for Rev A design. Keep its +10…+45 °C charge range, 450 mA charge ceiling and 4.20 V ±50 mV charge-voltage limit in the part-specific acceptance case. The BQ24074 TS NTC and safety timer remain active; an additional TMP390 hot/cold switch with a 10 kΩ output pull-up and AUP gate inhibits E1 at nominal 40/15 °C board temperatures. Prove combined sensor tolerance and cell-to-board thermal error leave the cell inside its charge range, test open/short and startup/fault states, and verify exact assembly polarity, discharge duty and current limits before BOM freeze. A source-design target is not a tested pack or fabrication approval.

**2026-10-10 CHG-002 capture part:** ADR 0024 selects exact Panasonic `ERA2AEB2491X` (2.49 kΩ, 0.1%, ±25 ppm/K) as the ISET source part, now placed in the provisional charger core. Preserve the ±1% total resistance allowance and calculated 396 mA maximum; source capture does not approve charge-current, pack thermal or a fabrication BOM.

**2026-10-10 CHG-001/002/003 and USB-005 provisional capture:** The root-linked charger core connects BQ24074 `TS` to the battery-facing Murata NTC, exact `ERA2AEB2491X` at ISET and one exact `ERA2AEB3651X` at ILIM. ADR 0022 selects the single lower ILIM setting for provisional capture, retaining the calculated 0.361–0.476 A interval when external mode is enabled. The initial checkpoint held EN2/EN1 low for 100 mA fallback; the EN2 amendment below supersedes that temporary mode. `ITERM` remains open for internal 10% termination and `TMR` open for TI's active default precharge/fast-charge safety timers, nominal 30 minutes/5 hours. The disconnected IN and BAT nets carry explicitly provisional ERC source flags pending E1 and exact pack connector; they are not physical supplies. Before gate/pack capture, review capacitor effective values and voltage stress, full-port and pack current, charging time versus timer, polarity, temperature tolerance and thermal behavior. Native ERC and XML connectivity do not satisfy these operating acceptance checks.

**2026-10-10 CHG-003/USB-005 EN2 amendment:** [ADR 0023](decisions/0023-charger-en2-local-clamp-proposal.md) selects an exact 10 kΩ `ERJ2RKF1002X` feed from admitted `CHARGER_IN_DRAFT` into a 2.5 V `LM4040A25IDBZT` shunt on BQ EN2. EN1 and CE remain low; ILIM will set the limit when the input and clamp are valid. The previous direct EN2-to-ground capture is superseded. The shunt load margin still assumes an unverified EN2 current at approximately 2.5 V; check that, E1 fault voltage, input-valid/mode timing, compact-board resistor heat and source transitions before approving the gate. The source flags remain nonphysical boundaries, and no fabrication release follows.

**2026-10-11 USB-005/PWR-005 supervisor domain:** [ADR 0025](decisions/0025-usb-supervisor-logic-rail.md) moves U34 VDD/MR and its local bypass/CT pull-up to `+3V3_USB` in the root-linked conditioning sheet, retaining the 2.916 V nominal logic-rail sense threshold and 180–420 ms fixed release interval. The exact connected E1 EN circuit must still bound RESET loading, rail-sequencing/injection and rapid brownout before charger permission can be accepted. This does not alter a current limit or release the charger input gate.

**2026-10-11 USB-005/CHG-003 E1 capture selection:** [ADR 0026](decisions/0026-charger-e1-gate-network.md) selects the exact E1 breaker and a passive-low EN divider with three independent hardware sinks for Type-C source permission, temperature and USB supervisor. The existing supervisor RESET pull-up/pull-down are now revalued to reduce low-voltage load before connecting the third sink. Keep BQ's lower hardware ILIM and E1's own ILM resistor, safety timers, NTC and pack protection. The calculation in ADR 0026 is a source-capture screen; verify E0 fault containment, full-port current, gate rise/fall and startup/brownout waveforms, capacitor effective values and physical layout before charge operation or fabrication release.

## Row-package proposal verification addendum

2026-10-06: [ADR 0020](decisions/0020-dual-row-mosfet-package-proposal.md) proposes a complementary N/P package for each row to recover board area. It is **not accepted or implemented**. The following evidence is required before it could replace the captured row stage; the display, current and fail-safe requirements above remain unchanged.

| Existing requirements | Proposed refinement / acceptance evidence |
|---|---|
| DSP-001/004/006, PWR-004 | Preserve 16 independently selected rows and hardware-default blanking during boot, reset, programming, OFF and VLED faults. Verify turn-off and row dead time under real multiplex timing, including visible ghosting. |
| PWR-006/008, USB-003, CHG-002 | Bound a final 48-pixel row's current, tolerance and overlap/fault cases at the selected VLED rail. Review the candidate P device's hot resistance, switching loss, SOA, gate stress and compact-board copper; the manufacturer's large test-board current rating is not a badge rating. Do not raise existing limits through a package change. |
| MFG-001/003, SAF-003 | Audit the exact manufacturer's N/P pin map, land pattern, polarity/pin-one mark and assemblability into project-local libraries. If selected, use the same stage on the coupon and measure it before relying on coupon results for the final board; include it in the independent Gate A review. |

**2026-10-11 USB-005/CHG-003 E1 source follow-on:** The [root-linked provisional E1 sheet](../hardware/coupon/rev-a/charger-gate.kicad_sch) now connects three independent sink outputs to `CHARGER_GATE_EN`, E1 OUT to BQ IN, and the selected exact ILM/dVdt and bypass parts. Its input now joins the captured E0 protected `+5V_USB` output. Native ERC and XML check wiring only. E0 voltage and current protection, partial-rail behavior, current transient, capacitor effective value, thermal behavior and an independent Gate A review remain required before charge-operation acceptance or fabrication.

**2026-10-11 PWR-005/USB-003 E0 source selection:** [ADR 0027](decisions/0027-e0-protected-usb-source-selection.md) selects exact TPS259474ARPWR E0, a 3.32 kΩ breaker setting, 38.3 kΩ/10 kΩ OVLO divider, 390 kΩ autonomous EN feed and exact input/output/slew capacitors for provisional source capture. The design must bridge connector VBUS to both the protected USB logic rail and E1 input, while retaining an independent hardware charger permission gate. This selection does not prove port transients, inrush, fault containment, sustained current or complete USB compliance.

**2026-10-11 PWR-005/USB-003 E0 source follow-on:** The provisional E0 sheet now connects `VBUS_CONNECTOR` to `+5V_USB` and E1 input, replacing the two old protected-rail ERC source assumptions with a physical eFuse output. #FLG05 denotes the external connector supply only. Exact E0 threshold, input/output capacitors and slew part are populated in KiCad. Native ERC/XML validate source topology, not connector transient containment, port current/inrush, OVLO fault timing or thermal safety; retain those as engineering and Gate A acceptance items.

**2026-10-11 PWR-004/DSP-004 VLED capture sequence:** [ADR 0028](decisions/0028-root-link-dark-vled-converter.md) permits source-capturing the exact TPS63020 VLED stage while EN is connected only to its 100 kΩ pull-down. Removing the VLED source flag validates the physical rail connection, not display operation. Do not add an EN driver or release board fabrication before a hardware interlock forces both converter disable and row blanking through boot, reset, programming, OFF and fault states. The existing DSP/PWR acceptance tests remain required.

**2026-10-23 CTL-001/DSP-006 routing study (ADR 0043):** Narrower signal escapes were screened locally; the selected 150-edge derivative retains 0.20 mm tracks, 0.20 mm other-net clearance and 0.30/0.10 mm adjacent-layer microvias. Its checker shall reject narrower selected copper, preserve every prior physical pad group and all nonzero source copper, and retain the exact 104 recorded intrinsic DRC findings. This does not change current limits or fabrication gates. See [ADR 0043](decisions/0043-bounded-signal-pad-escapes.md).

**2026-10-23 routing-locality study (ADR 0044):** Selected still-unrouted resistor/capacitor poses may change in the separate derivative after proving no direct contact to nonzero frozen-source copper. Exact component/pad/net data and all nonzero source copper shall remain intact. Record original/selected integer poses and preserve every earlier physical pad group using footprint-relative pad identities. Exclude ICs, sensors, connectors, differential USB series resistors and row pairs; require actual edge reductions and unchanged full native DRC findings. See [ADR 0044](decisions/0044-localize-unrouted-study-passives.md).

### Connected-passive placement continuation (2026-10-23)

[ADR 0045](decisions/0045-preserve-connected-groups-during-passive-relocation.md) permits exact resistor/capacitor relocation in an unqualified continuation, excluding R45/R46. Direct earlier copper contact is permitted only while retaining all accepted 150-edge copper and preserving every prior physical pad group after refill and reconnection. ICs, inductors, connectors, sensors, row pairs and test pads remain fixed. Exact parts, values, nets, relative pad geometry, original widths/vias and current settings remain unchanged; sensitive added routes retain the 5 mm limit. Record selected integer poses/copper, independent native/pad counts and the exact unchanged intrinsic DRC findings. Gate A and fabrication restrictions remain open.

[ADR 0046](decisions/0046-retire-displaced-passive-orphan-vias.md) narrowly permits enumerated displaced-passive orphan microvia retirements. Retain all ordinary nonzero source tracks and all other accepted copper. Restore every retired via in an independent native witness: edge counts and all selected physical pad groups must remain identical, with DRC differing only by the exact expected `via_dangling` inventory. The selected board must retain exactly the original 104 intrinsic findings; no current, net, component or fabrication-release change is permitted.

[ADR 0047](decisions/0047-scoped-digital-signal-width-study.md) records a narrower digital-control candidate that is not selected. The 100-edge checkpoint shall retain 0.20 mm tracks and the original 0.20 mm project floor, 0.20 mm clearance and original via/annular dimensions. No narrow-track or reduced-floor exception is accepted by its verifier. Any future width change requires separately pinned scope, native rules and electrical/process review.

[ADR 0048](decisions/0048-local-display-track-detours-for-pad-escapes.md) records an evaluated display-track detour. No ordinary nonzero source track retires in the 100-edge checkpoint. Future selection would require exact, enumerated 0.20 mm display-track replacements and independent endpoint evidence. Preserve both source endpoints, every other original segment, every accepted 150-edge physical pad group, original track/via/clearance dimensions and the exact intrinsic DRC findings. Record replacement geometry, layers and lengths; reject undeclared retirement/restoration. Return-path, current/thermal, SI/process qualification and independent Gate A remain open.

[ADR 0049](decisions/0049-bounded-power-distribution-parcels.md) permits explicitly enumerated inner-layer power-distribution parcels in the unqualified routing derivative. Retain original zone definitions and exact net/layer/priority/clearance/fill data; independently verify replay, every earlier physical pad group and the unchanged 104 intrinsic findings. Preserve original track/via dimensions and current/protection/enable boundaries. Filled area is not current/thermal qualification, and source/switch limits, bypass/return/RF/process review and independent Gate A remain open.

**2026-10-26 routing continuation:** [ADR 0050](decisions/0050-preserve-100-edge-routing-checkpoint.md) requires exact retention of every accepted 100-edge copper item, power-zone definition and completed physical pad group. Additional original-width routing must pass the unchanged full native DRC and independent physical-pad counts. The existing three orphan-via proof, current settings, component constraints and fabrication gates remain in force.

**2026-10-26 bounded pad escapes:** [ADR 0051](decisions/0051-bounded-dsf-pad-necks.md) permits only selected 0.12 mm straight B.Cu necks, 0.50–0.70 mm long, from exact U48/U52 DSF pad centres on the enumerated pins/nets. Enforce these signatures independently and retain 0.20 mm default/other routing with scoped native rules. Keep all prior copper/groups, exact packages, clearance/via dimensions, current settings and fabrication gates. Reject dangling seed vias, broad width exemptions and any new DRC finding. Pin every selected neck and the native rules/profile before accepting a candidate.

**2026-10-26 continuation beyond 94 edges:** [ADR 0052](decisions/0052-preserve-94-edge-routing-checkpoint.md) freezes all accepted 94-edge copper, completed physical pad groups, power parcels and selected neck metadata. Verify any new signal and supply/ground repairs as one transaction, with exact old-net retention, lower independent counts and unchanged native DRC. Existing component, width/current/protection/enable and fabrication constraints remain in force.

**2026-10-26 continuation beyond 91 edges:** The accepted-continuation section of [ADR 0052](decisions/0052-preserve-94-edge-routing-checkpoint.md) additionally freezes the 91-edge plan at 48cdb7a. Retain its selected copper, completed physical groups, power parcels and existing neck records alongside the earlier contracts; independently verify all new signal/repair transactions before selection.

**2026-10-26 continuation beyond 84 edges:** [ADR 0052](decisions/0052-preserve-94-edge-routing-checkpoint.md) freezes the e095f3b plan in addition to every earlier checkpoint. Preserve its copper, completed groups, zone definitions and existing neck records; new pin escapes remain bounded by ADR 0051 and require completed connections and unchanged native DRC.

**2026-10-27 continuation beyond 82 edges:** [ADR 0052](decisions/0052-preserve-94-edge-routing-checkpoint.md) additionally freezes the accepted 88fdcbe integer plan, copper, physical groups, zone definitions and neck records. Require lower independent/native opens and unchanged full DRC for new additive routing. USB connectivity evidence shall remain distinct from impedance, skew, stub and return-path qualification; no fabrication release is authorized.

**2026-10-27 blocked-escape continuation:** [ADR 0053](decisions/0053-enumerated-local-track-replacements.md) permits ignored feasibility trials of exact local 0.20 mm display/row-control track replacements. Canonical selection requires a reviewed signature/junction catalog, preservation of every prior physical group and all other copper, lower independent/native opens, unchanged full DRC, replay and fault evidence. The selected 71-edge study passes those guards for exactly the two catalogued COL_09_R/ROW_SEL_08 originals, preserving twelve original direct contacts and all previous physical groups/additions. Every other original item remains subject to the prior freeze. No current, protection, enable, package, clearance, via or fabrication gate changes are permitted.

**2026-10-27 converter locality experiments:** [ADR 0054](decisions/0054-local-converter-inductor-placement-study.md) permits ignored L1/L2 placement feasibility studies beside their exact fixed converters. Preserve exact parts/pads/nets, all accepted copper/groups and current/protection/enable settings; use short bounded switching-node paths and unchanged native geometry checks. No canonical inductor move or power-width exception is selected. Require exact pose/path policy, native and independent counts, full unchanged DRC, replay and fault evidence before selection; electrical/thermal/EMI qualification and Gate A remain open.

**2026-10-27 continuation beyond 71:** Freeze the accepted abf4f99 integer plan and its additions/groups. ADR 0053 permits evaluating one additional exact ROW_SEL_08 source replacement for PAIR10 ground, with original-layer direct contact evidence. The selected 70-edge continuation passes full unchanged DRC, independent lower counts, stable replay and 31 native/56 portable fault/source guards. This permits no broader row, power or USB deletion and changes no electrical/current/fabrication boundary.

**2026-10-27 continuation beyond 70:** Preserve the selected 70-edge checkpoint's additions and physical groups. Evaluate only the two exact ADR 0053 ROW_GATE_09/ROW_SEL_05 replacements for TH1.2 ground, preserving all direct original-layer contacts and requiring full unchanged DRC, lower independent counts, replay and guards. The selected 69-edge continuation passes 31 native/59 portable guards, stable replay, independent counts and unchanged full DRC. All existing electrical and fabrication restrictions remain in force.

**2026-10-28 isolated test-land experiments:** [ADR 0055](decisions/0055-localize-isolated-test-lands.md) permits ignored localization trials for exactly seven isolated digital/control test lands. Preserve their complete geometry/fields/nets/orientation, back-side courtyard and edge clearance, all 69-edge copper/groups and existing electrical/fabrication boundaries. Selection requires independently proved prior isolation/no copper contact, exact bounded pose/lead policy, full unchanged DRC, lower counts, replay and fault evidence. The selected 65-edge continuation passes that gate for TP1, TP2, TP11 and TP20 only, under the exact pose/lead catalog; the other three candidate lands remain fixed.

**2026-10-28 coupled UART placement experiment:** ADR 0055 narrowly permits ignored joint R47/TP4 trials under the existing R/C and isolated-test-land policies. Preserve the exact 499 Ω MPN/pins/footprint, TP4 geometry/fields/net/orientation, every 65-edge copper item/group and all four selected test-land poses. Bound R47 movement to 5 mm, new input reconnection to 8 mm and output test lead to 3 mm. No additional canonical move or electrical/fabrication exception is selected before full evidence and guards pass.

**2026-10-28 rear VLED parcel experiment:** [ADR 0056](decisions/0056-bounded-rear-vled-distribution-study.md) permits an ignored, bounded B.Cu VLED distribution screen using unchanged 0.20 mm clearance/minimum copper thickness and current/voltage/protection/enable settings. Retain every 65-edge copper item, original zone/parcel definition, component pose and completed group. Reject any prior return/supply/signal split or new full DRC finding. Canonical selection requires exact polygon/fill policy, lower independent counts, stable replay, source and fault evidence; current/thermal, bypass/return/process/fit and independent Gate A remain open.

**2026-10-28 coordinated colour-chain experiment:** [ADR 0057](decisions/0057-coordinated-colour-chain-fanout-study.md) permits ignored coordinated displacement of original 0.20 mm COL_* In4/B chains at the driver ports. Only internal chain vertices may move; all external original-layer pad/via/retained-copper contacts, every accepted added copper item and every 65-edge physical group must survive. Keep widths/clearance/vias and all electrical limits unchanged. Canonical selection requires an exact chain/interface policy, native/independent lower counts, unchanged full DRC, replay and fault evidence. No canonical chain replacement is selected.

**2026-10-28 64-edge candidate:** ADR 0053 permits exactly one further catalogued COL_02_R replacement with all four original-layer direct contacts preserved. The temperature-output join includes two short supply restorations; retain every accepted 65-edge copper item/group, R/C and test-land pose, zone/parcel, earlier replacement and exact neck. Selection requires unchanged full DRC, stable independent counts/replay and fault/source checks. No current, clearance, package, protection/enable or fabrication boundary changes are permitted.

**2026-10-28 scoped spacing experiment:** ADR 0058 permits only an ignored signal-net feasibility comparison with explicit 0.15 mm track-related / 0.18 mm via-pad/via spacing. Keep default, power/ground/analogue/setting and pad-pad clearance at 0.20 mm; retain widths, adjacent via dimensions and every 64-edge copper item/group, pose and zone. The accepted profile is unchanged. Canonical adoption requires an independently enforced exact pair policy, unchanged full baseline, replay/fault/source evidence and recorded engineering consequences; no fabrication exception follows.

**2026-10-28 local ground fanout experiment:** ADR 0059 permits only an ignored, enumerated eleven-track added-GND rework at U48. Retain every original source item, all other accepted additions, components/zones and every 64-edge physical group/external interface. Keep original spacing, widths and via dimensions; added ground length is bounded. Canonical adoption needs a new exact retirement/interface policy, native/replay/fault/source evidence and unchanged orphan restoration. No current, protection/enable or fabrication boundary changes are included.

**2026-10-28 redundant-ground experiment:** ADR 0060 permits ignored removal of exactly 87 native shape-covered added GND tracks and the separate ADR 0059 branch, 90 unique tracks total. Require conservative source coverage proof, original-source/via non-retirement, three stable refills, every 64-edge group and retained interface, unchanged full DRC and original routing dimensions. Canonical retirement remains prohibited until the exact new policy, native/fault/replay/source and lower-count evidence passes.

**2026-10-28 exact USB status width candidate:** ADR 0047 permits only the pinned USB_RAW_OUT2 candidate: 13 narrow digital tracks and three adjacent microvias, with 0.20 mm clearance and the unchanged 120 mm per-net hard bound. Preserve all 64-edge copper/groups/poses and every earlier exception. Native default width remains 0.20 mm; independent metadata/native checks must reject unlisted or undeclared narrow copper. No input/charger/LED/regulator current limit, signal mode, part, net or protection/enable setting changes. Full acceptance evidence is required before selection.

**2026-10-28 selected 63-edge checkpoint:** The exact USB status inventory above passes the full acceptance gate, retaining all 64-edge copper/groups/poses and the unchanged 104 native findings. Freeze the 64-edge plan and exact narrow-copper catalog; independently enforce the status-pin join and reject narrower/unlisted copper. No scoped-spacing or ground-retirement experiment is selected. The 50-edge target and all fabrication/engineering review holds remain open.

**2026-10-28 local UART escape experiment:** ADR 0061 permits only an ignored exact rework of exactly seven original UART0_TX_RAW In4 staircase tracks beside R47, preserving every other original-source item, all accepted additions and every retained external same-layer contact/group. Keep RAW width/clearance at 0.20 mm, parts/poses/settings fixed, and bound added replacement length. No canonical chain retirement is selected; an independently enforced exact policy and complete lower-count/native/replay/fault/source/orphan evidence are required first.

**2026-10-28 UART candidate length review:** The exact ADR 0061 candidate calculates to 5.039244 mm of 0.20 mm RAW replacement versus 1.15 mm retired, preserves five retained In4 contacts and passes the 62-edge preflight. Revise only its local planning bound to retired plus 4 mm; no current/timing rating or other bound is changed. Canonical selection still requires exact original-chain and digital inventories, frozen 63-edge preservation and the full acceptance gate.

**2026-10-28 selected 62-edge checkpoint:** The exact ADR 0061 chain and ADR 0047 UART inventory pass the full gate: 62 native/physical opens, all 63-edge additions/groups/poses, five retained chain contacts/two interfaces, unchanged full 104 findings, stable replay, 50 native/99 portable guards, source/LED checks and unchanged orphan restoration. Only the seven original RAW signatures may retire under the new chain policy; all other original/accepted copper stays protected by existing rules. No additional ground, component/current/protection/enable or fabrication exception is selected.

**2026-10-29 local colour-layer feasibility:** [ADR 0062](decisions/0062-local-colour-layer-transfer-feasibility.md) permits an ignored layer transfer using adjacent microvia stacks over at most 2 mm within exactly one original COL_10_R In4 track to investigate U52.3 ground access. Preserve original endpoints and all direct original-layer contacts, every other original/accepted copper item, pose, zone and completed group. Keep original width/clearance/vias, all current/protection/enable settings and the exact ADR 0051 neck restriction. No canonical replacement is selected; an independent exact retirement/interface policy and full lower-count/native/replay/fault/source/orphan evidence are required before adoption. Electrical/process/fit review and independent Gate A remain open.

**2026-10-29 selected 61-edge checkpoint:** The exact ADR 0062 COL_10_R dogleg and ADR 0051 U52.3 ground neck pass lower native/physical counts, all frozen 62-edge additions/groups/poses, both original In4 contacts, unchanged 104 full findings, stable replay and original-orphan restoration. Independently pin seven individual replacements plus the unchanged seven-track UART chain, all three exact necks and the unchanged narrow digital inventory. No other transfer or ground retirement is selected. The 50-edge target and all engineering/fabrication holds remain open.

**2026-10-29 row-ground feasibility:** [ADR 0063](decisions/0063-row-island-colour-transfer-feasibility.md) permits an ignored bounded In3 dogleg for exactly the original COL_03_B In4 signature obstructing PAIR06/07/08 ground access. Preserve every 61-edge addition/group/pose and all source-layer interfaces, width/clearance/vias, earlier exceptions and electrical settings. No new narrow neck or canonical retirement is selected. Require exact independent scope/length/contact enforcement and complete lower-count/native/replay/fault/source/orphan evidence before adoption; engineering and fabrication holds remain open.

**2026-10-29 accepted-segment feasibility:** [ADR 0064](decisions/0064-exact-accepted-colour-segment-rework-feasibility.md) permits an ignored bounded rework of only the exact already accepted COL_09_R In4 segment obstructing PAIR01 ground. Existing canonical checkpoint and replacement retention still prohibit its retirement. Adoption needs a separate exact policy proving prior presence, native direct contacts, preservation of every other accepted item/group and the original-source replacement's interfaces, plus the full lower-count/native/replay/fault/source/orphan gate. Keep all widths, spacing, parts, settings and fabrication holds unchanged.

**2026-10-29 selected 60-edge checkpoint:** The exact ADR 0063 COL_03_B transfer and full-width ground continuation join PAIR06/07/08, retaining every accepted 61-edge addition/group/pose and seven direct original In4 contacts. Stable native/physical counts, unchanged full 104 findings, replay, fault/source and original-orphan checks pass. Pin eight individual original replacements and the unchanged seven-track UART chain. No accepted-addition retirement, new narrow copper, electrical-setting or fabrication exception is selected; the 50-edge target remains open.

**2026-10-29 LED serial escape feasibility:** [ADR 0065](decisions/0065-led-serial-escape-colour-transfer-feasibility.md) permits an ignored bounded rework of exactly one original COL_10_B In4 signature obstructing U1.42 LED_SOUT. Preserve every 60-edge addition/group/pose/zone and direct original-layer contact, full colour width, original spacing and adjacent vias. LED_SOUT remains an unselected ADR 0047 digital-width trial with the unchanged 120 mm bound. Canonical adoption requires exact independent catalogs and complete lower-count/native/replay/fault/source/orphan evidence. Current/protection/enable and fabrication holds remain unchanged.

**2026-10-30 R1 locality feasibility:** ADR 0045 permits an ignored exact-part R1 placement screen beside U1, retaining all 60-edge copper/groups and reconnecting its former ground group. Keep 39.2 kΩ, exact pins/package, 0.20 mm geometry and the 5 mm aggregate LED_IREF limit unchanged. No canonical move or current change is selected before full independent/native/replay/fault/source/orphan evidence.

**2026-10-30 C32 ground-locality feasibility:** ADR 0045 permits an ignored exact-part C32 pose screen that reconnects both its old USB-3.3-V group and main ground, with original copper, other poses, geometry and settings preserved. Canonical selection still requires the complete lower-count/native/replay/fault/source/orphan gate.

**2026-10-30 C32 land-pattern discrepancy:** The supplied Murata sheet exposes oversized b/c dimensions in the current shared GRM18 land for exact GRM188R60J106ME47D. ADR 0066 permits only ignored C32-specific 0.65 × 0.70 mm lands at ±0.675 mm, with explicit old/new identity mapping and all other copper/groups/geometry retained. No canonical package change or new lower count is selected before exact library/source-contract, native/replay/fault and orphan proofs pass. Do not alter other MPNs' shared footprints without their own datasheets.

**2026-10-30 coordinated serial-escape feasibility:** ADR 0067 permits only ignored exact COL_10_B/In4, COL_15_R/In3, COL_15_G/In2 and COL_14_B/In1 local transfers, with original widths, clearance, adjacent vias, interfaces and all other 60-edge copper/groups retained. No new canonical retirement or narrow inventory is selected before the full independent/native/replay/fault/source/orphan gate. All electrical settings and fabrication holds remain fixed.

**2026-10-30 serial candidate implementation:** ADR 0067's prechecked 59-edge
candidate permits exact catalogs for the four originals and LED_SOUT only,
with the complete 60-edge plan frozen. Preserve all old copper/groups/poses,
24 new direct source contacts, original widths/spacing, the 120 mm narrow-digital
bound and all electrical/fabrication holds. Final promotion requires full
native/replay/fault/source checks in addition to the completed precheck.

**2026-10-30 selected 59-edge checkpoint:** ADRs 0065/0067 select exactly four
source colour replacements and the exact LED_SOUT digital inventory, preserving
every 60-edge added item/group/pose and 24 newly derived original-layer contacts.
Native/physical counts, unchanged full 104 findings, stable replay/fills, original-
orphan restoration and 58 native/116 portable guards pass. The digital length
remains below 120 mm; original widths/spacing, settings, previous exceptions and
fabrication holds stay fixed. No Murata package migration is selected here.

**2026-10-30 clock/latch feasibility:** ADR 0068 permits only an ignored exact
COL_05_B In4 local transfer, retaining every original source-layer interface and
all other accepted 59-edge copper/groups/poses/zones. Keep full colour width,
original clearance/adjacent vias and original-plus-2-mm length. Clock/latch
remain unselected exact ADR 0047 digital trials within 120 mm per net. Full
independent/native/replay/fault/source/orphan evidence precedes any selection;
all electrical and fabrication holds remain fixed.

The bounded ADR 0068 screen completes with zero other-net-clear candidates
across 7,752 doglegs; the separate digital and USB restoration screens likewise
select no new route. The accepted 59-edge board, retention policy and all
electrical/fabrication boundaries remain unchanged. These finite results do not
prove impossibility; source evidence is recorded with the follow-on study.

**2026-10-30 exact Murata migration (ADR 0069):** MFG-001/003 and SAF-003
require a dedicated GRM188R60J106ME47D footprint at C3/C32/C44/C45/C53/C54,
using the supplied exact-part reflow row: 0.65 × 0.70 mm lands at ±0.675 mm.
Preserve numbered nets, exact identities, all accepted 59-edge copper/groups,
poses, zones and electrical settings. Explicitly verify the six old/new pad
identity mappings; keep historical sources/plans unchanged and report legacy
assignments in historical comparisons. Require native XML/ERC, drawing/render,
stable fills, independent counts, unchanged-or-better full DRC, replay,
original-orphan and fault evidence before selecting corrected routing source.
Other MPNs sharing the legacy footprint require their own drawing reviews.
Electrical/process/assembly qualification and independent Gate A remain open.

**2026-10-30 switched-gauge routing continuation (ADR 0070):** PWR-003/007
and MFG-001/003 retain the existing switch/buffer circuit, exact parts, current
settings and provisional switch-mapping/transition holds. Only the exact
ordinary-width additive +BAT_GAUGE_SW inventory may join SW2.6 to C39.1/U46.1.
Freeze all 59-edge copper/groups/poses/zones and the six corrected capacitor
packages. Preserve all prior exceptions, require the source-pin join independently
of plan/catalog fingerprints, and pass lower native/physical counts, unchanged
full DRC, stable fills/replay, source/fault and original-orphan checks before
selection. Other gauge groups and inductor locality remain incomplete;
independent Gate A and fabrication restrictions are unchanged.

**2026-10-30 printed switch-terminal correction (ADR 0071):** MFG-001/003,
PWR-003/007 and CTL-001 retain exact JS202011JCQN and all physical land/net
connections. Transcribe the supplied page-9 row labels as 1/2/3 and 5/6/7,
with commons 2/6; map legacy 4/5/6 to printed 5/6/7 explicitly. Use a dedicated
corrected footprint while preserving historical sources and source snapshots.
The gauge routing witness is SW2.7/C39.1/U46.1 after correction. Require exact
old/new physical identity guards, canonical native XML/ERC/rendering, full
retention/count/DRC/replay/fault/orphan evidence. Independent bottom/top-view,
received-part, actuation, transition and assembly reconciliation remains open;
no current or fabrication restriction changes.

**2026-10-30 coordinated converter feasibility:** [ADR 0072](decisions/0072-coordinated-converter-floorplan-feasibility.md) permits an ignored finite rigid-placement screen of the thirteen current exact VLED footprints using historical local poses only. Retain all accepted copper, other components, exact pads/nets/parts and current/protection/enable settings. No canonical IC/passive move or copper replacement is selected. A future selection requires a bounded exact contact/rework policy, suitable power-path geometry, all prior groups restored, native/independent connectivity, full DRC and replay/fault/source evidence; qualification and Gate A remain open.

**2026-10-30 C32 ground feasibility:** [ADR 0073](decisions/0073-c32-staggered-ground-escape-feasibility.md) permits ignored local replacement of only three enumerated original In4/In3 colour segments to investigate a staggered adjacent-via escape from fixed C32.2. Retain all original-layer contacts, all other 58-edge copper/groups/poses/zones, exact parts and electrical settings. Bound colour length/excursion and ground length; keep ordinary geometry and unchanged full DRC. No source retirement or new narrow route is selected before full native/physical/replay/fault/source/orphan evidence.

**2026-10-31 local VLED switching feasibility:** [ADR 0074](decisions/0074-local-vled-switching-node-feasibility.md) permits ignored two-part and thirteen-part pose comparisons at the recorded clear packing seed. Keep all existing copper, exact parts/pads/nets and electrical settings. Test only two local switching nets on B.Cu at ordinary width, each bounded to 5 mm. Record all old-group losses and native DRC; no canonical IC move, current-capacity approval or incomplete power stage is selected from these geometry experiments.

**2026-11-01 VLED pair supply feasibility:** [ADR 0075](decisions/0075-vled-pair-supply-restoration-feasibility.md) permits ignored ordinary-width additive restoration of U37's SYS and VLED contacts in the two-part switching probe. Retain all existing copper/poses/zones, local switching joins and previous groups; bound new length per net and reject any split after refill. No obsolete-copper retirement, canonical pose selection or power-stage qualification follows from this screen.

**2026-11-01 obsolete-U37 copper feasibility:** [ADR 0076](decisions/0076-obsolete-u37-copper-cleanup-feasibility.md) permits only a bounded ignored dangling-copper simulation inside the vacated U37 window, on four named nets and retained 58-edge items. Enumerate each removal and source/accepted origin; preserve all old groups and unchanged intrinsic clearances. Stop at boundaries/item/round limits. This grants no canonical source retirement; an exact independent policy and complete replay/fault/source/orphan gate remain required.

ADR 0076's exact leaf continuation additionally permits private removal of only
the two documented obsolete SYS F.Cu branches after current/frozen contact
proof. The shared bus, every other copper item and all old groups remain fixed;
no general boundary expansion or canonical retirement is authorized.

**2026-11-01 local VLED stage feasibility:** [ADR 0077](decisions/0077-local-vled-stage-connections-feasibility.md)
permits an ignored finite B.Cu-only ordinary-width local connection screen among
the fixed thirteen exact stage components. Retain all old copper, switching
paths, poses, zones and settings; bound pair/net length and report obstructions
and all prior-group losses. No new via, source retirement, global reconnection,
canonical adoption or power-stage qualification is selected by the screen.

**2026-11-01 exact UART obstruction feasibility:** [ADR 0078](decisions/0078-local-vled-uart-obstruction-feasibility.md)
permits only a private transfer of the two exact accepted UART items, with both
retained interfaces verified. Use one fixed adjacent via and bounded ordinary-
width In4.Cu tracks; preserve every other copper item and current pad group.
Only after successful native/full-DRC restoration may the local-stage screen be
repeated. No canonical source exception or power-stage qualification follows.

**2026-11-01 full VLED supply feasibility:** [ADR 0079](decisions/0079-full-vled-stage-supply-restoration-feasibility.md)
permits ignored additive SYS/VLED restoration in the exact full-stage/UART
candidate. Preserve all current copper/groups/poses/zones/settings and restrict
ordinary-width additions to fixed stage pads and current supply anchors, with
bounded global length and search effort. Reject every collateral split. Complete
restoration requires all earlier accepted groups and full independent/native
evidence; no power-copper retirement or canonical adoption is granted.

**2026-11-01 C47 return/feedback feasibility:** [ADR 0080](decisions/0080-c47-return-and-feedback-combination-feasibility.md)
permits only private combination of the exact bounded feedback path with the
retained global parent, plus a finite local three-via C47.2-to-In2 return screen.
Keep every current group and item, native widths/clearance and all earlier
supply bounds; repeat an outer VLED join only after complete return validation.
No source retirement, current/process qualification or canonical adoption is
selected by this additive experiment.

**2026-11-01 full-stage obsolete-copper feasibility:** [ADR 0081](decisions/0081-full-stage-obsolete-copper-cleanup-feasibility.md)
permits only a bounded ignored dangling-copper simulation in five enumerated old
stage windows, on five named nets and unique retained 58-edge signatures. Keep
all current and earlier groups, all other old/new copper and exact geometry/
settings; record origin/contacts and stop at scope limits. No canonical source
retirement or new orphan waiver is selected without an exact independent policy
and the full adoption evidence.

ADR 0081's exact leaf continuation permits only the three documented obsolete
F.Cu SYS branches after frozen/current contact proof; both shared buses and all
other current geometry/groups remain fixed. The private 52-item cleanup cohort
is separate from the two UART retirements and original three-orphan waiver;
canonical selection still requires the independent full adoption policy.

**2026-11-01 corrected L1/U36 locality:** [ADR 0082](decisions/0082-corrected-l1-u36-locality-feasibility.md)
permits only ignored fixed-U36 L1 screening and a bounded two-part cardinal
placement/short-switching-node template screen on the exact cleaned candidate.
Keep all old copper, other components and settings; record all affected supply/
control groups and reject ground/other-net splits. Pin 7 is U36's ground return,
pin 6 is MODE tied low. No canonical move, footprint/current change or incomplete
old-group restoration is selected.

**2026-11-04 owner MLCC evidence:** The supplied summary screenshot does not
replace a manufacturer land drawing. Its D/J/body data agree with indexed
2025 reference excerpts, while its reflow ranges conflict with the supplied
2021 catalogue. Preserve exact source/approval distinctions and all current
footprint/BOM/qualification holds until the underlying Murata diagram/revision
is verified; no geometry or order-code selection follows from the screenshot.


**2026-11-04 remaining Murata land feasibility:** [ADR 0083](decisions/0083-remaining-murata-land-feasibility.md) permits ignored exact-part pad-only trials for all eight GRM187 and two GRM219 instances, using the supplied June 10, 2026 reference sheets and their verified ±0.20 mm reflow branches. Preserve every other item/pose/field/net/setting and report all old-group losses after native fills. Dedicated candidate lands are 0.75 × 0.90 mm at ±0.775 mm and 0.70 × 1.30 mm at ±0.950 mm respectively. Keep source MPN packaging choices, canonical geometry, approval/assembly/electrical and Gate A holds open; no failed retention result may be promoted.

ADR 0083's exact C49 continuation permits only the documented 0.475 mm
ordinary-width B.Cu VLED contact extension in the ignored cleaned-52 trial.
Preserve every source item and old group; require 52 native/physical opens
and unchanged full 104 findings before calling the reconnection successful.

The supplied June 2026 sheets resolve the previously missing body-tolerance
and reflow-row evidence. ADR 0083's successful ignored trials preserve 58/58
opens without added copper on the accepted source, and 52/52 with only the
exact C49 lead on the cleaned candidate. Both retain all prior groups and
exact full 104 intrinsic findings; stable replays and ten rejection cases pass.
No canonical migration, packaging selection, separate approval or assembly/
electrical qualification is inferred from these native geometry results.


**2026-11-05 remaining Murata source migration:** [ADR 0084](decisions/0084-remaining-murata-source-migration.md) adopts dedicated corrected GRM187/GRM219 lands for exactly C40/C41/C42/C43/C46/C47/C48/C49/C56/C61 after the complete source/native gate. Freeze the preceding 58-edge plan/contract and preserve every copper item, pose, field, numbered net, zone and electrical setting. Require all 246 physical groups, 58 native/physical opens, exact 104 intrinsic findings, stable fills/replay, native XML/ERC/rendering, fault/source checks and original-orphan restoration. The separate ignored converter/C49 rework is not selected. Packaging/approval/assembly/electrical and independent Gate A holds remain open.

ADR 0084's exact ten-capacitor pad-only migration passes the complete acceptance
gate and is selected for canonical source. Preserve the frozen 58-edge plan,
all source copper/groups/poses, prior exceptions and original-orphan waiver.
The source retains 58 native/physical opens and exactly 104 intrinsic findings;
no converter placement/rework or lower routing count is selected. Packaging/
approval/assembly/electrical and independent Gate A holds remain open.


**2026-11-05 checked converter checkpoint:** [ADR 0085](decisions/0085-selected-converter-routing-checkpoint.md) permits a separately validated child of the immutable corrected 58-edge parent. Enforce exactly thirteen VLED poses, 54 catalogued retirements, 102 additions including the C49 lead, all 246 parent groups and new named converter joins. Require 52 native/physical opens, exact 104 findings, stable fills/replay, origin/structure/profile/source/fault/orphan evidence before selection. Parent retention checks stay unchanged; current settings, part/pad geometry, protection/enable/firmware and all qualification/fabrication holds remain fixed.


**2026-11-05 whole-coupon L1/U36 feasibility:** [ADR 0086](decisions/0086-global-u36-l1-pair-feasibility.md) permits an ignored whole-coupon 0.25 mm/cardinal pair screen on the exact corrected child trial, using existing numbered-pin short-node templates and unchanged native clearance/width/edge rules. Keep all other geometry/settings fixed. Report finite results and every filled group loss; no placement may be selected without complete restoration and the full adoption gate.


**2026-11-05 U36 pair restoration:** [ADR 0087](decisions/0087-u36-pair-restoration-feasibility.md) permits ignored bounded ordinary-width SYS/+3V3_APP restoration for the exact new pair, followed only by native-dangling, source-present supply copper cleanup within the vacated U36 window. Preserve every old/current group and all other geometry/settings; require 50 native/physical opens and exact intrinsic DRC before proposing exact source adoption.

ADR 0087's bounded cleanup stops at an active SYS shared leaf. Permit only
its documented exact tail replacement, retaining the new route's two current
interfaces and the original bottom bus. Do not delete the active branch or
count retained original tail geometry as a new supply excursion. Require
full origin/contact/inventory, 50-open and exact-DRC evidence before selection.


**2026-11-05 exact dual-converter routing adoption:** [ADR 0088](decisions/0088-dual-converter-routing-selection.md) permits the final cumulative child ledger only: 15 poses, 65 retirements (20 originals/45 accepted), 134 additions, all 246 parent groups and named dual-converter joins. Preserve the frozen 52-edge plan and unchanged 58-edge parent gate. Select only after 50 native/physical opens, exact 104 findings, stable replay/fills, path-length, source/fault/orphan and exact shared-tail-interface evidence. Remaining circuit opens and all electrical/part/process/fit/Gate A/fabrication holds remain open.

ADR 0088's cumulative dual-converter checkpoint passes the complete parent/child
acceptance gate and is selected at 50 native/physical opens / exact 104 intrinsic
findings. Both numbered switching-node pairs are local and below 5 mm; all 246
parent groups, exact ledger/poses/pads/profiles and original-orphan proof pass.
The local-converter goal and 50-edge planning target are achieved. Remaining
circuit opens and all electrical/part/process/fit and independent Gate A holds
remain open; no fabrication release follows.

**2026-11-05 complete-stage planning (ADR 0089):** Before continuing arbitrary open-count closure, deliver a complete-stage correction plan covering U36 physical feedback/default pull-down and local input/output bypass; U37 control/power returns, exposed-pad heat spreading and power-save/window compatibility; combined effective capacitance and L(I,T); full source/load and finished-copper/HDI process budgets. Retain the 50/104 checkpoint unchanged during this review. Inventory every intrinsic physical pad pair; no global clearance reduction or fabrication acceptance is implied. Subsequent geometry, part, mode, threshold or rule changes require their own bounded design disposition and validation. See the [review and acceptance queue](development/converter-power-layout-review-2026-11-05.md).

**2026-11-06 bounded corrections (ADR 0090):** Use a connector-driven 0.80 mm target and explicitly provisional 2+2+2 geometry while obtaining a controlled finished build; do not adopt the inconsistent 1.6 mm owner proposal or silently reclassify inner microvias. Enforce exact allowed via spans, pad/hole and nominal aspect policies in a fail-closed check, with supplier/release status distinct from geometric eligibility. Screen the complete nine-part U36 stage and retain all prior pad groups/interfaces before canonical selection. Preserve current/protection limits, exact parts, global clearances and independent Gate A. See [ADR 0090](decisions/0090-bounded-stack-and-complete-stage-corrections.md).

**2026-11-06 selected local-stage correction (ADR 0090):** The separate 47-edge routing successor passes exact 9-pose/14-retirement/47-addition, all-238-parent-group, named local-pin, native/physical count, unchanged-104-DRC, replay/fill, source/fault/orphan and visual gates. Enforce primary C40 input and C43 output locality and bounded conductor paths, retaining all exact parts/current/protection settings, B.Cu feedback/default pull-down and the open switch/interlock boundaries. Preserve the 50-edge parent unchanged. Manufacturing eligibility remains fail-closed for the 557 legacy centre microvias, missing controlled stack and supplier/process/fit/Gate A evidence. The 0.80 mm stack is planning intent, not adoption of a fabrication build. See the [implementation evidence](development/bounded-corrections-2026-11-06.md).

**2026-11-06 routing closure goal (ADR 0091):** Continue from the immutable
47-open study to zero native and physical pad-cluster opens, preserving exact
circuit boundaries, all live groups and accepted converter geometry. No added
DRC findings, general width waiver, new unsupported central microvia or
fabrication permission is allowed. Record and validate each selected successor.

**2026-11-06 full-span feasibility (ADR 0092):** Existing 0.50/0.30 mm plated
through-via geometry may be explored for direct plane joins under all-layer
clearance, drilled-hole, live-group and exact-DRC guards. Keep trials ignored
until their exact successor validation passes; supplier/assembly and Gate A
holds remain unchanged.

ADR 0092's exact 43-open switch-routing successor may be selected only after
retaining all 232 immutable 44-open parent groups, exact unchanged intrinsic
DRC, deterministic replay and fault/source/orphan checks. Its two full-span
vias use 0.50/0.30 mm; the new supply bridges require separate current/voltage-
drop/thermal and return-path qualification. No fabrication or electrical
validation is inferred from CAD continuity.

ADR 0091's remaining-routing successor must retain all 231 groups and every
copper item of the immutable ADR 0092 43-open source. Each accepted open-count
reduction requires an exact current ledger, native/physical agreement, no new
DRC finding, stable replay/fills and source/orphan/fault validation. USB signal
quality and added supply-path ampacity remain separate qualification holds.

ADR 0093 keeps the strict three-via retirement proof on the immutable 43-open
parent. A remaining-routing successor with no new retirements must retain all
parent and previously selected pad groups/copper, recheck copper/net identity
after refill, and pass the exact actual-source DRC and all other native gates.
The current-board retired-via restoration experiment is separately reported,
including net reassignment or extra opens; its output is never selected.

ADR 0094 permits only a bounded R90 locality study with unchanged
ERJ2RKF1402X / 14 kΩ programming and fixed U39 thermal position. A selected
pose requires local SETB/ground geometry, ordinary B.Cu routing, complete
41-open group/copper retention, exact unchanged native DRC and all normal
successor validation. Temperature thresholds and protection are not retuned.

ADR 0094 additionally permits exactly one full-width B.Cu GND return replacement
at (59.865,16.000)–(58.365,16.000) mm to open the local cold-pin exit. Its exact
replacement must retain both endpoints and every direct original-layer contact,
stay inside the recorded local bounds, preserve all other accepted copper and
all live groups, and pass the same complete successor checks before selection.

ADR 0095 permits a bounded anchored R8 pull-up rotation with fixed VLED-pad
centre, exact ERJ2RKF1001X / 1 kΩ value and existing source nets. Any selected
local row-gate join must retain all previous groups/copper, introduce no new
retirement/via, and pass exact DRC, replay/source and fault validation. The
paired-device trial marker and fabrication hold remain unchanged.

ADR 0096 permits only the exact five-track TMP390-area ground-plane substitution
recorded there. A selected TEMP_OK join requires the retained boundary contacts
and both endpoints to touch one actual filled B.Cu ground component, with all
previous live groups/copper otherwise retained and no zone/profile/part/net/
current change. Exact native DRC and all successor gates remain mandatory.

ADR 0097 permits an ignored bounded U39/R89/R90 supply-routing study inside
the existing battery-facing sensor reservation, with fixed TH1 and bypass
capacitors. Exact local contact-preserving replacement evidence, unchanged
thermal/current/protection settings and all native successor gates precede
any selection. The selected source remains the validated 39-open checkpoint.

ADR 0098 permits only ignored TP13/TP14 locality trials with their existing
1.0 mm test lands and at most 5 mm of ordinary B.Cu lead. Prior isolation and
no-contact proof, all existing copper/groups/other poses, numbered-pad joins
and full successor validation precede selection. Hardware permissions and
current/protection limits do not change; probe/loading/fit remain unqualified.

ADR 0099 permits only the exact three-track USB_RAW_LOGIC_READY replacement
beside U54 to enable an actual TP14 join under ADR 0098. Both outer endpoints,
every original external B.Cu contact and all prior groups/other copper must
survive; complete successor checks precede selection. Permission logic,
current limits, defaults and protection are unchanged.

ADR 0099 selects the 38-open successor: TP14 joins U54.3 with a 3.125 mm
ordinary B.Cu lead, and the exact permission-lead replacement retains both
outer endpoints and all four external contacts. All 227 prior groups and
219 additions, unchanged full DRC, replay/fills, 25 fault guards and 27 source
checks pass. TP13 stays fixed; all qualification/fabrication holds remain.

ADR 0100 permits only the exact two-track VLED_WINDOW_OK transfer for a
completed TP13 join under ADR 0098. Preserve both outer B.Cu endpoints and
all original external contacts, all prior groups/other copper and unchanged
window/current/protection/default logic. Ordinary widths and adjacent
0.30/0.10 mm B.Cu/In4.Cu vias, bounded local routing and complete successor
validation precede selection; all qualification/fabrication holds remain.

ADR 0100 also permits the same exact window replacement for a complete
ordinary-width ADR 0091 route to fixed TP13, with a recorded adjacent output
escape and unchanged land pose. A partial escape is never selected or counted
as a circuit join; actual routing length/loading and all source/group/DRC
checks remain required.

ADR 0101 permits a bounded TP13 exact-pad-centre escape with unchanged
0.30/0.10 mm B.Cu/In4.Cu microvias and at most 5 mm total ordinary B.Cu/In4.Cu
trace. It changes no other pose or accepted copper and requires exact prior
isolation, all groups/copper, full DRC/replay/source/fault/visual checks before
selection. Via-in-pad/probe/process qualification and fabrication holds remain.

ADR 0101 selects the additive 37-open successor: TP13 joins U55.7 through
two adjacent microvias and a calculated 3.857541315 mm ordinary In4.Cu lead.
All 226 preceding groups and 223 additions survive, with no new retirement;
exact unchanged DRC, stable replay/fills, 30 fault guards, 27 source checks
and native visual review pass. All qualification/fabrication holds remain.

ADR 0102 permits only an ignored 5° anchored-R8 orientation screen with fixed
VLED pad-1 centre, exact part/local geometry, all original direct supply
contacts and every other pose/copper item retained. Ordinary B.Cu gate routing
is limited to 5 mm with at most 3 mm pad-centre separation; no retirement or
new via is permitted. Full successor validation precedes any selection.

After ADR 0102's B.Cu-only screen rejects all 72 orientations, its five
pad/courtyard-clear poses may additionally test a combined lead of at most
5 mm on B.Cu/In4.Cu with at most two adjacent 0.30/0.10 mm microvias. All
original direct supply contacts, other copper/groups/poses and full successor
gates remain mandatory; no central via, retirement or selection is implied.

ADR 0103 permits an ignored local replacement of only the exact ROW_SEL_15
B.Cu segment (68.900,7.850)–(73.350,7.850) mm to support the anchored +90°
R8 flip. The ordinary-width replacement stays inside the recorded bounds,
retains both endpoints and every original contact, and totals at most 12 mm.
A completed gate connection may use at most 5 mm of ordinary B.Cu/In4.Cu
lead and two adjacent microvias. All other copper, poses, source groups,
settings and full successor gates remain mandatory before selection.

ADR 0103's single-track replacement may also test B.Cu/In4.Cu routing with
at most two additional adjacent microvias, retaining the same bounds, 12 mm
combined length and all six original direct B.Cu contacts. Clearance between
both proposed signal paths is mandatory; every other successor gate remains.

ADR 0104 permits an ignored PAIR01-only translation of at most 0.25 mm,
with fixed orientation and exact trial identity/local geometry. Every original
same-net direct external land contact, all previous pad groups and every
accepted copper item must survive. Ordinary routing and the existing adjacent/
provisional buried-via geometry remain mandatory; no new central microvia,
narrowing or retirement is permitted. Complete successor validation precedes
selection; all electrical/process/fit/fabrication holds remain.

ADR 0105 permits an ignored C32-only translation of at most 0.25 mm with
fixed orientation and exact GRM188R60J106ME47D identity/local geometry.
Every original external land contact, old pad group and accepted copper/net
identity must survive. No colour retirement, narrowing, current-limit or
profile change is permitted; ordinary routing and complete successor checks
remain required before selection. All qualification/fabrication holds remain.

ADR 0105 selects the 36-open successor at C32 centre (89.250,10.250) mm,
with its exact original supply contact, all 225 prior groups and 226 additions
retained. No copper is added or retired by this step. Actual main-ground
component contact, exact unchanged DRC, stable replay/fills, 36 fault guards,
27 source checks and native visual review pass; all qualification and
fabrication holds remain.

ADR 0107 permits an ignored U38-only translation of at most 0.25 mm with
unchanged exact LM4040A25IDBZT identity, setting, orientation and local lands.
Every original land contact, accepted copper/net identity and live group
must survive. A completed U38.3/U52.3 main-ground join and all full successor
checks precede selection. No current/protection/profile or other pose change,
retirement or narrowing is permitted; all qualification/fabrication holds remain.

ADR 0108 permits GND-only ordinary routing on the existing In2.Cu ground
layer during ignored exploration; the search restriction remains for all
other nets. Widths, clearances, profiles, zone definitions, source copper,
poses and all prior live groups remain protected. Actual ground continuity
and complete successor checks are required before selection; no electrical
or fabrication qualification is implied.

ADR 0109 permits ignored coordinated ROW_SEL_01/03 B.Cu exploration within
its frozen shunt interface, preserving outside copper, all original contacts
and previous groups. Only full native/physical reduction with unchanged exact
DRC and replay/contact/fault/source/visual evidence permits selection; no
fabrication or electrical qualification follows from routing closure.
ADR 0109's second ignored variant may retain ROW_SEL_01 and use at most two
ordinary 0.50/0.30 mm through vias for a bounded ROW_SEL_03 front-layer transfer,
with every-layer clearance checks and all existing acceptance gates.

ADR 0110 permits ignored coordinated ROW_SEL_00/01/03 back-layer rerouting
within its frozen local interface, using only ordinary-width tracks and no
new vias or poses. Every external contact, outside fragment and prior group
must survive; complete successor checks precede any selection.
ADR 0110 may combine its ignored three-row reroute with U38's exact
(+0.250,0) mm translation under ADR 0107, retaining original anode contacts
and all prior groups. No other pose, part or rule change is permitted.
ADR 0110 may also test a bounded ROW_SEL_01 adjacent In4.Cu/B.Cu transfer
with at most two 0.30/0.10 mm microvias, restoring every previous ground group
and keeping ordinary track width and clearance. No central via is permitted.
ADR 0110 additionally permits ignored ordinary-width additive ROW_SEL_01
restoration on B.Cu/In4.Cu/In3.Cu to actual retained copper, protecting the
restored 196-pad ground group and all prior groups. Retirement remains local;
any dangling fragment and the full successor gates must be resolved before
selection.

ADR 0111 permits ignored additive bridges between any actual disconnected
same-net groups, preserving every previous group and source copper with
ordinary geometry. Native target-group continuity, full source preservation
and all successor gates precede selection; an isolated VLED join is not
proof of a powered or electrically qualified row.

ADR 0112 permits ignored R11/R21 angular screening about unchanged pad-2
centres, preserving exact ERJ2RKF1001X identities and all original contacts,
copper and groups. Only ordinary-width additive leads and full successor
gates can select a pose; all other settings and qualification holds remain.

ADR 0113 permits an ignored R11/R21 relocation by at most 2 mm while replacing
only its exact original gate leaf, retaining every far-end contact, exact
part/local geometry, prior group and accepted addition. Gate and VLED leads
must each be ordinary-width B.Cu and at most 5 mm; no new vias or other
retirement is allowed. Complete successor validation precedes selection.

ADR 0114 permits ignored localization of R11 beside PAIR06 or R21 beside
PAIR16, retaining its exact 1 kΩ identity and transistor association. Retire
only the frozen obsolete gate-net cohort while keeping both local package
straps; new gate/VLED leads must be ordinary-width B.Cu, each at most 3 mm,
with no new vias. Every old pad group and accepted addition and the complete
source/contact/replay/DRC/fault/visual gate must pass before selection.
ADR 0114 may test ordinary-width additive ground restoration after localization,
using the existing adjacent/buried-via policy. Both displaced ground pads must
rejoin the original main group and every other connection must survive; no
new unsupported central microvia or additional retirement is allowed.

ADR 0115 permits an ignored R11 (+0.500,0) mm shift with its sole exact gate
leaf replaced and all other copper retained, to clear the recorded ordinary-
width ground route and one adjacent microvia. Every old group and accepted
addition must survive and complete successor validation precedes selection;
the still-isolated VLED pad is preserved without claiming supply continuity.

ADR 0115 selects the 35-open successor with exact R11 relocation/leaf scope
and strengthened ordinary-width ground landings. All previous groups and
accepted additions, unchanged exact DRC, stable replay/fills, 44 native faults,
28 source checks and visual review pass. No electrical, process or fabrication
qualification is implied; zero-open and independent Gate A work remain open.

ADR 0116 permits ignored PAIR01 (+0,+0.150) mm corridor exploration with
its exact internal drain strap and four selector U-loop tracks replaced,
retaining every external contact and prior group/addition. Standard-width
local ground and adjacent-layer selector restoration and all full successor
gates are mandatory; no new central microvia, limit or protection change.
ADR 0116 may test one exact COL_09_B adjacent-via relocation and equal-length
layer redistribution, retaining every original colour pad/contact and all
source groups/additions. No width, current, assignment or central-via change
is allowed, and full successor validation remains mandatory.


ADR 0117 selects a separate corrected-RSE 35-open successor after exact
8-retirement/73-addition replay, preservation of all 223 functional groups and
244 accepted additions, exact unchanged 104 findings, stable independent
refills/replays and native/source/fault/visual checks. Continue zero-open work
from this corrected source; keep the preceding wrong-map board immutable and
explicitly historical. No electrical/process/Gate A acceptance is implied.


ADR 0121 selects the 34-open USB EN1 successor after exact two-pose,
3-retirement/11-addition validation, all-223-prior-group preservation,
unchanged 104-finding DRC, stable independent replays, source/fault and visual
checks. Continue zero-open work from this corrected child; retain the 35-open
RSE parent unchanged. All electrical/process/Gate A holds remain.

**2026-11-12 fixed thermistor continuation:** ADR 0122 permits an ignored,
contact-preserving local COL_01_R layer-transfer feasibility study from the
34-open source, with TH1 and all other parts fixed. A transfer alone is not a
TS join or selected checkpoint. Complete physical-group, exact DRC, replay and
qualification/Gate A requirements remain unchanged.

**2026-11-12 CC1 continuation:** ADR 0123 permits ignored additive restoration
of complete original APP/battery supply groups cut by a provisional CC1 path.
The isolated CC1 route is rejected until every old group and the exact DRC
baseline are restored and full successor checks pass. Source remains 34 opens.

**2026-11-12 independent supply continuation:** ADR 0124 bounds ignored
supported inner-layer bridging from the immutable 34-open source on VLED,
switched gauge, USB supply and ground. All prior physical groups, exact DRC,
parts, limits, protection and source retention remain required; no search hit
alone is selected progress or power/return qualification.

**2026-11-12 switched-gauge candidate:** ADR 0124 freezes an additive 114-item
33-open candidate joining the switch/repeater supply to its A-side pull-up and
decoupling group, with all 222 preceding groups and exact 104 findings retained.
U35.2/3 remains open. Selection requires the remaining replay/counterfactual,
fault, source and visual gates; no power or fabrication qualification is implied.

**2026-11-12 selected gauge successor:** ADR 0124's exact 114 additive items
reduce opens to 33 native/physical, preserving all 222 preceding groups and
every original copper/part/pose/profile with exact 104 findings. Stable exact
replays, counterfactual geometry/group/DRC restoration, eleven native faults,
32 source checks and visual review pass. U35 supply, current/return/bus,
controlled-stack/process/fit and independent Gate A remain unresolved; the
zero-open goal remains active and fabrication prohibited.

**2026-11-12 remaining gauge capture:** ADR 0125 bounds an ignored native
non-grid capture at U35.2 and supported additive continuation from the immutable
33-open source. All parts/pads/nets, prior groups, exact DRC and safety/current
boundaries remain required; a via alone is not a gauge power connection.

**2026-11-12 complete gauge restoration:** ADR 0126 bounds ignored additive
restoration of all original ground, USB input, APP and protected-battery groups
split by the rejected U35 supply path. The eight-terminal gauge join and every
preceding group must coexist with exact DRC/replay/source/fault/visual gates.
No partial count reduction is selected; source remains at 33 opens.

**2026-11-12 native board-edge routing study:** ADR 0127 permits an ignored
ordinary-width search in a wider centre grid, with explicit native board/cutout
edge screening. All original parts, copper, groups, rules, exact DRC and
successor replay/fault/source/visual gates remain mandatory; no selected change
or electrical/fabrication qualification is implied.

**2026-11-14 U51 locality study:** ADR 0128 permits only ignored ±0.250 mm
translations of exact U51, with every original copper item and live group
retained, for a supported ordinary-width control escape. No other pose, pin,
part, net, rule or safety boundary may change; full successor gates remain.

**2026-11-14 U51 loop-transfer study:** ADR 0129 permits replacement of exactly
three recorded MODE_BOOT_N B.Cu tracks with a bounded supported B/In4 route.
All external contacts, including its interior branch, every source group and
all other source copper/parts/rules/safety boundaries must survive. A temporary
cut or restored loop alone is not a selected reduction in open connections.

**2026-11-14 U52 local capture:** ADR 0130 bounds one exact −0.500 mm U52
translation, one supply-leaf retirement, explicit ground restoration and a
supported input capture. All original groups and other source items remain
required. Only predetermined U52 coordinates translate in the 104-finding
comparison; no finding or safety qualification is waived.

ADR 0130's rejected leftward poses are superseded only for ignored feasibility
by an exact +0.500 mm U52 translation and its recorded two-leaf power/ground
cohort, with direct original ground-capture retention and one explicit supply
branch. Its sole expected intrinsic-finding coordinate transform is +0.500 mm
in x for U52 items; all other fields and full successor requirements remain.

**2026-11-14 local gate/bypass cluster screen:** ADR 0131 permits read-only
native placement/capture proxies for exact U52 and C71 near U51. No relocated
PCB, new footprint or copper retirement is authorized by that screen; an exact
pose/contact ledger and all full successor gates are required before adoption.

**2026-11-14 exact existing DSF escape:** ADR 0132 permits only the recorded
0.450 mm, 0.12 mm B.Cu U52.1 signal neck under its unchanged existing package
rule. All copper beyond that neck stays ordinary width. No pose, capacitor,
rule, protection or new source-retirement change is authorized; actual join,
all original groups, exact DRC and full successor gates remain mandatory.

**2026-11-14 existing DSF neck screen:** ADR 0133 bounds 0.750 mm local escapes
at the five explicitly listed U48/U52 signal pads under their unchanged existing
0.12 mm package/net rules. No part, source copper, clearance or profile changes
are authorized; all remaining copper and full successor gates stay unchanged.

**2026-11-14 local ROW_SEL_14 transfer:** ADR 0134 permits replacement of one
exact recorded track, with all seven native external contacts and its complete
terminal group retained, to assess local cluster space. No part, net, row
assignment, current/default-off setting or new rule changes are authorized.

**2026-11-14 exact gate/bypass prototype:** ADR 0135 freezes two exact U52/C71
poses and six private-leaf retirements following the contact-preserving row
detour. Every original group, all other source items and unchanged rules/safety
boundaries must survive; only predetermined U52 intrinsic-item positions may
follow its frozen pose. No extra finding, substitution or qualification is waived.


**2026-11-14 control checkpoint selected:** ADR 0136 adopts the complete exact U52/C71 migration, eleven-item retirement and 59-item addition ledger at 32 native/physical opens. Preserve all 221 predecessor groups, exact source contacts and full original finding payloads except independently validated U52 pose coordinates. All existing safety, qualification and fabrication holds remain; zero opens is still required.

**2026-11-14 relocated control continuation:** ADR 0137 bounds existing-rule
U52.2/U52.4 local capture screening and supported additive continuation from the
immutable 32-open source. Every prior group/source item and full successor
acceptance/safety boundary remain required; no extra finding or fabrication release.

**2026-11-14 ordinary additive continuation:** ADR 0138 permits ignored
ordinary-width searches on its explicitly listed remaining control/row/clock
nets, preserving every selected source item/group and preliminary join. Native
exact-finding and full successor gates remain required; no safety or qualification
boundary changes, and no lower unvalidated count is selected.

**2026-11-14 clear-output checkpoint selected:** ADR 0139 selects the ordinary-width U52.4–U49.2/R108.1 join at 31 native/physical opens, preserving all 220 predecessor groups and every source item. Exact original findings, source-byte restoration and full successor gates pass. Zero opens and all existing safety/qualification/fabrication holds remain.

**2026-11-14 larger bounded continuation:** ADR 0140 permits a higher bounded
weighted ordinary-width search on its ten explicit nets from the immutable
31-open source. Every current group/source item and exact finding payload,
full successor gate and safety/qualification/fabrication hold remain required.

**2026-11-14 bypass/enable locality study:** ADR 0141 permits only read-only
native proxies for one exact C71 translation, two inventoried private-leaf
omissions and a bounded existing-rule enable neck/capture. No routed part move
or source retirement is authorized without its subsequent frozen contact scope;
all selected groups, safety and full successor gates remain mandatory.

**2026-11-14 enable checkpoint selected:** ADR 0142 selects the complete five-terminal DISPLAY_ENABLE join at 30 native/physical opens, with one exact C71 translation, two private-leaf retirements and 88 additions. All 219 prior groups, source contacts and original finding payloads survive, with no rule or safety change. Full replay/inverse/fault/source/visual gates pass; zero opens and all qualification/fabrication holds remain.

**2026-11-14 exact outer-capture discovery:** ADR 0143 permits only read-only
native screening of supported adjacent transitions at actual retained non-grid
capture positions on its explicitly listed remaining nets. No source item,
part, rule, centre microvia or PCB change is authorized by the discovery screen;
all 218 selected groups and full successor/safety/fabrication holds remain.

**2026-11-14 complete pull-up locality discovery:** ADR 0144 permits only a
read-only exact R8 pose/capture screen and inventory of its one prospective
VLED-leaf cohort. No routed part move or retirement is authorized without its
subsequent frozen scope; all 218 selected groups, complete original pull-up
supply, numbered nets, safety and full successor/fabrication holds remain required.

**2026-11-14 complete selector/pull-up feasibility:** ADR 0145 freezes one
anchored exact R8 flip and one original ROW_SEL_15 retirement for ignored
complete restoration. Every selector branch/interface, the complete original
pull-up supply, all 218 selected groups and full successor/safety/qualification
holds must survive with an actual gate join; no partial lower count is selected.

**2026-11-14 selector capture screen:** ADR 0146 permits read-only anchored
R37 orientation/capture screening with exact ERJ2RKF1003X / 100 kΩ identity,
all original direct and filled-zone contacts and unchanged rules. No relocated
PCB is authorized without a frozen exact follow-up scope; all 218 selected
groups, safety and full successor/qualification/fabrication holds remain required.

**2026-11-14 drill-span semantics fixtures:** ADR 0147 permits isolated ignored
native fixtures with unchanged 0.25 mm hole rules to distinguish actual via
layer spans. It authorizes no source PCB, rule, capture or search-policy change;
all selected-group, full successor, safety and fabrication holds remain required.

**2026-11-14 fixed inverter-neck discovery:** ADR 0148 permits read-only fixed
U48 capture screening under its existing 0.12 mm courtyard rule, with actual
neck length below 0.750 mm and unchanged source parts/copper/rules. No PCB is
authorized without frozen follow-up geometry; all 218 groups and full successor,
safety, qualification and fabrication holds remain required.

ADR 0149 permits an ignored additive supply/return search from the exact selected
30-open source using actual group/filled-zone witnesses and ADR 0147's bounded
supported-span prefilter. Preserve all source groups/items/rules; complete native,
independent, replay, inverse, fault and visual validation precedes selection.
Connectivity evidence does not qualify current capacity or fabrication.

ADR 0150 permits only a read-only exact U48 locality screen near fixed corrected
U49. A later migration requires complete bypass/leaf/contact scope and full
source-preserving successor validation; no source pose or copper is changed.

ADR 0151 permits only the exact ignored U48/C67 complete local prototype with
thirteen additions and no source retirement, followed by bounded restoration
of its actual supply, return and two signal groups. Every original group and
full successor gate must pass before selection; unfinished findings are not waived.

ADR 0152 permits cleanup of exactly two obsolete original U48 APP leaf items
and two unused new input-capture items. Preserve both original external In4
branches and actual filled source-plane contacts, every old live group and
all other source items; complete successor validation precedes selection.

**2026-11-15 inverter clock checkpoint selected:** ADR 0153 selects exact U48/C67
locality, two obsolete original APP leaf retirements and 29 additions at
29 native/physical opens. All 218 prior groups and original external contacts
survive, with exact original 104 finding payloads under the two recorded rigid
transforms. Independent replays/inverse/fault/hole/source/visual gates pass;
zero opens and every qualification/fabrication hold remain unresolved.

ADR 0154 permits only an ignored additive continuation of U48.2's remaining
heartbeat input from the exact selected 29-open source, with its existing-rule
0.500 mm neck and supported adjacent captures. Preserve all 217 source groups
and exact original findings; complete successor gates precede selection.

ADR 0155 permits only a read-only exact-pad capture screen on small disconnected
native groups at the selected 29-open source. No track, via or placement is
implemented without an exact later scope and all source-preserving successor gates.

ADR 0156 permits only ignored additive restoration of GND, +3V3_USB and
+BAT_PROTECTED_DRAFT on the exact bounded reverse-heartbeat snapshot. Restore
all 217 selected-source groups and every original branch, remove every new
finding/native discrepancy, and pass complete successor gates before selection.

ADR 0157 permits exactly two ignored supported adjacent VLED captures at
PAIR07.4 and bounded additive continuation, preserving all 217 source groups
and every source item. Actual plane/group witnesses and full successor gates
precede selection; no VLED limit or current-capacity qualification changes.

ADR 0158 permits only a read-only six-layer 0.50/0.30 mm full-span capture
screen at fixed PAIR07.4 on the selected 29-open source. No PCB is written;
actual filled-main-plane witnesses and later exact scope precede implementation.

ADR 0159 requires public native routing probes to preserve exact source project
and rule context with saved outputs, bind it to PCB/profile hashes and reject
stale or changed manifested inputs before native loading. Historical evidence
is not rewritten; no routing or electrical acceptance policy is relaxed.

ADR 0160 permits only read-only discovery of short explicit +3V3_USB corridors
wholly contained in original connected In3 plane copper, with exact source
contact witnesses and polygon-subtraction proof. No PCB is changed without
an exact later scope and all source-preserving successor gates.

ADR 0161 permits only a read-only complete replacement screen for the exact
three-item private USB bridge, omitting no other obstacle. Original plane
interfaces, all source groups and full successor gates remain required before
any implementation or selection; no part or current-limit change is authorized.

ADR 0162 permits only the exact three-retirement/three-addition private USB
bridge prototype and, after full prototype source/finding preservation, the
previously scoped heartbeat continuation. Both original plane interfaces and
all 217 source groups must survive; only a fully validated lower-open successor
may be selected. No via-process qualification or safety-limit change is inferred.

ADR 0163 permits only read-only exact front-access discovery for the heartbeat
input and actual original source-group copper. No PCB or route is implemented
without an exact later cohort, full group preservation and successor gates.

ADR 0164 permits only the exact nine-item additive heartbeat front-access
prototype from the selected 29-open source, followed by F/In1-only signal
routing. Preserve all 217 source groups/items and exact findings; no deeper
signal path or successor selection is allowed without complete recorded gates.

ADR 0165 permits only a front-dominant heartbeat continuation with transit-only
In1 and at most 24 mm new In2 copper in segments no longer than 4 mm. Retain all
original groups/items, source edge/clearance/width rules and full successor gates;
no deeper planar signal route or fabrication qualification is authorized.

ADR 0166 permits only native-screened diagonal and grid-phase refinements on
the exact heartbeat access prototype. Preserve all existing node/length/layer,
source/group and strict-finding gates; graph exploration does not waive any rule.

ADR 0167 permits only a read-only complete R8/R37 exchange screen with the
exact catalogued nineteen-segment selector leaf prospectively omitted. Preserve
all other source copper and interfaces; an exact later cohort and every full
source-preserving successor gate precede implementation or selection.

ADR 0168 permits only the exact R8/R37 poses, nineteen selector-leaf retirements
and four replacements, retaining all old ground/supply/selector contacts and
all 217 source groups. Matching lower counts and complete native/independent
source/finding/replay/inverse/fault/visual gates precede selection.

ADR 0169 qualifies only the exact ADR 0168 complete row-two exchange; selection requires all source/replay/inverse/contact/hole/fault/visual gates. Zero opens and all fabrication holds remain unresolved.

Selected ADR 0169 successor has 28 matching native/physical opens, all 217 preceding groups and exact original 104 findings. Full source/replay/inverse/contact/hole/fault/visual checks pass as recorded in `docs/development/row2-routing-2026-11-15.md`; zero opens and fabrication holds remain.

ADR 0170 permits bounded ignored additive routing discovery from the validated 28-open row-two source while preserving all 216 current groups and source copper/profiles. Adoption still requires full native/physical/source/replay/inverse/DRC/contact/hole/fault/visual gates; current limits and all fabrication holds remain unchanged.

ADR 0171 permits read-only fixed-orientation ±0.500 mm translation screening of five provisional paired-row footprints for actual disconnected supply/ground contacts. No PCB, source retirement, part approval or fabrication change is authorized; any exact pose requires a separate decision and all continuity/finding/source/replay/inverse/fault/visual gates.

ADR 0172 permits read-only off-pad TMP390 escape discovery within the earlier thermal/programming/bypass bounds and exact seventeen-item local cohort. No replacement, pose or successor is adopted; complete original groups and all electrical/qualification/fabrication holds remain mandatory.

ADR 0173 permits read-only complete local restoration templates at the three exact ADR 0172 sensor escape poses, keeping R89/R90 fixed and preserving all original interfaces. A clear supply escape is incomplete until programming/output/ground/supply restoration and every successor gate pass; no PCB or fabrication release is selected.

ADR 0174 permits only read-only exact R90 relocation discovery within 2 mm and existing 3 mm programming/ground limits at the second recorded TMP390 escape pose, keeping R89 and all other parts fixed. No PCB, threshold/current/protection change or successor selection is authorized.

ADR 0175 permits read-only supported-layer TEMP_OK output restoration and bounded local ground leads only at the recorded sensor/R90 poses. Every original interface, full supply continuity and all successor gates remain required; no source or fabrication release is adopted.

The ADR 0170–0175 continuation selects no successor: source remains 28 native/physical opens with unchanged selected evidence. Three TMP390 off-pad supply escapes and twelve nearby cold-resistor poses remain incomplete. See `docs/development/row2-routing-continuation-2026-11-15.md`; zero opens and every fabrication/qualification hold remain unresolved.

ADR 0176 permits read-only all-pin supported escape screening for one exact three-part sensor/programming cohort, retaining the original seventeen-item study scope, all external contacts and thermal/programming limits. No PCB or successor is selected; all complete-circuit and fabrication holds remain.

ADR 0177 permits only ignored complete sensor-circuit routing feasibility at the exact recorded three-part poses and seventeen-track cohort, within a bounded local window and ordinary supported copper classes. All original groups, external branches, exact104/native/physical/source/replay/inverse/contact/hole/fault/visual gates precede any selection; no threshold/current/protection/fabrication change is authorized.

ADR 0178 permits read-only enumeration of alternative ordinary supported VDD escapes at the exact three-part sensor cohort. A finite escape is not supply continuity; a new alternative requires a separate complete prototype scope and every original group/interface and acceptance gate.

ADR 0179 permits an ignored complete local routing prototype at the exact previously screened second U39 pose and first R90 pose, keeping R89 fixed and preserving the same seventeen-track scope and all original interfaces. All native/physical/exact104/source/replay/inverse/contact/hole/fault/visual and fabrication holds remain.

ADR 0180 permits only read-only complete-interface local hop discovery for the two exact row-gate bus segments blocking the sensor supply feed. No actual extra retirement or successor is selected; all original contacts, groups and acceptance/fabrication holds remain mandatory.

ADR 0181 permits an ignored exact seventeen-item local GND bridge plane-substitution study only. All original groups, external layer-specific contacts, exact104/native/physical counts, source/profile/type preservation and byte-identical inverse proof are required before any further use; no successor or return-path/fabrication qualification is selected.

ADR 0182 permits ignored complete sensor routing using only the verified exact GND bridge plane substitution plus the exact two-part sensor cohort (34 original retirements total). Every original group/contact, complete circuit and exact104/native/physical/source/replay/inverse/hole/fault/visual gate remains required; no canonical successor or fabrication qualification is selected.

ADR 0183 permits ignored dense 0.050 mm witnessed-plane endpoint discovery using actual ordinary-track endcap overlap. Native refill must establish each actual join and retain every current group; no rule/geometry/retirement/qualification hold or final acceptance gate is relaxed.

ADR 0184 permits bounded local native eight-neighbour/fine-grid refinement of the same sensor prototype while preserving all geometric, original-group, length and final acceptance gates. A finite path or miss does not select a board or relax any fabrication/qualification hold.

The ADR 0176–0184 results select no successor: source remains 28 native/physical opens. Exact GND plane-substitution continuity/inverse proof passes in an unselected basis, but complete sensor supply/output restoration and C51/U40 bypass locality remain unresolved. See `docs/development/sensor-routing-2026-11-16.md`; all electrical/qualification/fabrication holds remain.

ADR 0185 permits only read-only coordinated sensor/programming/bypass discovery using the exact forty-item prospective cohort. Sensor discovery radius may reach 4 mm only inside the unchanged thermal reservation/error allowance; C50 must retain its U39 association and C51 must improve to ≤3 mm from fixed U40 VCC. No PCB, part substitution, threshold/current/protection or fabrication change is selected.

ADR 0186 permits read-only exact local B gate-stair replacements and a four-part sensor core landing on the existing supply port, with C50's supply pad fixed and C51 correctly associated with U40. No original via/long bus or other source item may be omitted; no PCB or successor is selected, and all original contacts/groups and acceptance/fabrication holds remain mandatory.

ADR 0187 permits read-only fixed-sensor supply escape by replacing only the one exact private ROW_SEL_08 B trace, retaining every part/capacitor/converter placement and every other source item. No PCB or source successor is selected; all original contacts/groups and acceptance/fabrication holds remain mandatory.

ADR 0188 permits read-only fixed-pose lower-selector inner-bridge and mutually clear sensor-supply escape discovery, retaining every part/power-stage placement and only omitting the exact recorded lower ROW_SEL_08 cohort. No PCB or successor is selected; all original interfaces/groups and acceptance/fabrication holds remain.

ADR 0189 permits read-only replacement-capture discovery for the exact private ROW_SEL_08 B branch from fixed R30.1 to its retained In3 interface. Preserve all parts, other source copper, original interfaces and unchanged copper/hole rules; no PCB, successor or qualification/fabrication change is selected.

ADR 0190 permits read-only extended ordinary fixed-U39 supply escape screening mutually against the exact ADR0189 selector prefixes, without moving parts or changing the prospective cohort, copper/hole rules or complete successor gates. No PCB, successor or qualification/fabrication change is selected.

ADR 0191 permits read-only supported In3 bridge discovery for the exact sole-blocking COL_00_B In4 track, with its original contacts preserved and mutually clear fixed-sensor supply copper. No other prospective retirement, part move, rule relaxation, PCB or successor is selected; all complete-circuit and fabrication holds remain.

ADR 0192 separately permits read-only supported In3 hop discovery for the exact sole-blocking ROW_SEL_06 In4 track while retaining the original colour trace and all outside interfaces. No PCB, successor, rule relaxation or qualification/fabrication change is selected; all complete-circuit gates remain.

ADR 0193 permits read-only ordinary three-segment fixed-sensor supply escapes around the original selector-six endpoint while retaining both ADR0191/0192 obstructing tracks. The exact selector-eight prospective cohort and all parts/rules/gates remain fixed; no PCB or successor is selected.

ADR 0194 permits read-only ordinary fixed-sensor outer escape discovery through its exact bounded diagonal prefix, retaining all neighboring source tracks, parts, rules and complete successor gates. No PCB or successor is selected; all qualification/fabrication holds remain.

ADR 0195 permits only the exact first complete fixed-sensor/selector ignored prototype with the frozen 80-item private selector cohort and supported native-screened prefixes. Complete original groups/interfaces, matching reduced counts, exact104 and every successor gate precede selection; no qualification/fabrication hold changes.

ADR 0196 permits read-only supported layer-access discovery with only the exact additional 0.950 mm private selector In3 wire prospectively omitted, retaining its complete outside interfaces and all parts/other source items/rules. No PCB or successor is selected; all complete-circuit and fabrication gates remain.

ADR 0197 permits only the exact complete selector-port/sensor ignored prototype using its frozen 81-item cohort and mutually native-screened supported captures. Restore every original group and outside contact with matching reduced counts, exact104 and all successor gates before selection; all qualification/fabrication holds remain.

ADR 0198 permits only the exact combined 98-item fixed-sensor/selector/GND plane-substitution ignored prototype with supported full-stack routing and bounded mechanical centre transitions. Preserve all original interfaces/groups and source rules; matching reduced counts, exact104 and every successor gate precede selection. All electrical/qualification/fabrication holds remain.

The ADR0185–0198 continuation selects no successor. Four complete ignored fixed-sensor/selector prototypes retain 215/216 original groups and 29 native/physical opens, with additional rejecting dangling findings. The selected source remains 28 opens; see `docs/development/fixed-sensor-selector-study-2026-11-16.md`. All qualification/fabrication holds remain.

ADR 0199 permits read-only cardinal rotation discovery for exact R71/R21/R11 about their fixed connected pad 2, retaining all source copper and every old layer-specific contact. No PCB, substitution, rule change or successor is selected; all complete successor and fabrication gates remain mandatory.

ADR 0200 permits only the exact R21/R11 fixed-gate-pad ignored prototype and bounded ordinary VLED feed discovery, retaining every source copper item and original group/contact. Matching reduced counts, exact104 and all successor gates precede selection; no current or qualification/fabrication hold changes.

ADR 0201 permits only read-only 15-degree fixed-pad R21/R11 discovery with native pad-centred supported capture checks, retaining every old contact and source rule. No PCB, new retirement, substitution, current change or successor is selected; all acceptance/fabrication gates remain.

ADR 0202 permits only the exact R21 15/165-degree ignored prototypes and the unchanged ADR0200 bounded supported feed search, with R11 and every other part at selected poses. Preserve all original groups/copper/contacts and exact104; complete successor gates precede selection and no current/qualification/fabrication hold changes.

The ADR0199–0202 continuation selects no successor: all three prepared pose prototypes retain 216 original groups/exact104 and 28 native/physical opens, while all four feed searches exhaust without joins. See `docs/development/fixed-contact-resistor-study-2026-11-16.md`; the selected PCB and every qualification/fabrication hold remain unchanged.

ADR 0203 permits read-only small translations at the bounded resistor orientations only when every original pad-2 source contact remains physically touched, with exact source parts/pads/copper/rules and actual retained main-group copper or witnessed main-plane supply targets. No PCB, source retirement or successor is selected; all complete successor and fabrication gates remain.

ADR 0204 permits only the exact supply-anchored R21 ignored prototype, two frozen private gate-leaf retirements and three ordinary B replacements, retaining all other source items and original interfaces/groups. Matching reduced counts, exact104 and every successor gate precede selection; no current or qualification/fabrication hold changes.

ADR 0205 permits only the exact additional R11 supply-anchored ignored prototype, its one frozen private gate-leaf retirement and native-screened ordinary B replacements on the ADR0204 R21 candidate. All immutable source groups/interfaces, exact104 and every full successor gate remain mandatory; no current or qualification/fabrication hold changes.

ADR 0206 permits only the exact two-track B ground-plane substitution after full native branch/fill-witness proof, then its exact combination with ADR0205. No ground pad/via removal, new via or current change is allowed; every immutable source group, exact104 and all full successor/fabrication gates remain mandatory.

ADR 0207 permits only read-only supported outer gate-capture discovery at native B nodes reachable from the exact R11 pose under its unchanged source/cohort/rule bounds. An escape is incomplete until the full gate and all original groups pass every successor gate; no PCB or qualification/fabrication change is selected.

ADR 0208 permits only the exact R11 gate-port relocation and obsolete outer-via retirement, completing a bounded ordinary supported outer-layer route to the exact retained In4 wire endpoint. The six-item original cohort and all immutable groups/interfaces/rules remain frozen; matching reduced counts, exact104 and every full successor gate precede selection. No current or qualification/fabrication hold changes.

ADR 0209 qualifies only the exact minimal R21 exchange: two private gate retirements, two ordinary gate replacements and an actual retained main VLED contact, with no added supply trace/via. All original groups/copper and every serialized/native/physical/exact104/source/contact/replay/inverse/fault/visual gate precede selection; no current or qualification/fabrication hold changes.

Selected ADR0209 successor has 27 matching native/physical opens, all 216 preceding groups and attached source copper preserved, and exact original104. Full source/contact/replay/inverse/serialized/fault/visual gates pass as recorded in `docs/development/r21-routing-2026-11-19.md`; zero opens and all qualification/fabrication holds remain unresolved.

ADR 0210 permits only read-only fine-phase R11 supply gateway discovery on the qualified 27-open source, retaining every old gate contact, all original copper and every other part. Direct targets must be actual main VLED copper; an off-pad gateway still requires complete successor qualification. No PCB or current/qualification/fabrication hold change is selected.

ADR 0211 permits read-only complete R11 gate topology and local supply-anchored pose discovery near PAIR06, with exact source contacts, unchanged parts/rules and actual retained main VLED targets. No source retirement or PCB successor is selected; every complete successor and qualification/fabrication gate remains mandatory.

ADR 0212 permits the exact ignored local R11 prototype: graph-proven 65-item obsolete private gate replacement, unchanged two PAIR06 bridges and two short ordinary B leads, with all other source items/parts/rules fixed. Selection requires all 215 preceding groups, matching 26 native/physical opens, exact104 and all serialized/source/contact/replay/inverse/hole/orphan/fault/visual gates. All qualification/fabrication holds remain.

ADR 0213 permits only nine exact neighboring local R11 ignored pose/refill comparisons with the same 65-item cohort and two ordinary B leads. Every original GND and other live group must survive before qualification; geometry-only clear results do not select a successor. No additional copper retirement or qualification/fabrication hold change is authorized.

ADR 0214 permits read-only ordinary local B ground-bridge discovery for the two actual ground pads isolated by ADR0212/0213, targeting only individually copper-witnessed main-GND polygons with exact endcap overlap. No PCB, extra retirement, via or successor is selected; every original-group and full qualification/fabrication gate remains mandatory.

ADR 0215 permits only read-only supported outer ground-access discovery at the exact ordinary B nodes reachable from the two isolated ground pads of the rejected local R11 prototype, preserving all source obstacles and full-board hole rules. A gateway is incomplete; no PCB, extra retirement, unsupported via or qualification/fabrication change is selected.

ADR 0216 permits read-only exact front-side R11 placement discovery using only the graph-proven 25-item private gate prefix, actual retained main VLED F copper and its exact retained F gate interface. All other source parts/copper/rules and both-face courtyards remain fixed. No PCB or successor is selected; every original-group and qualification/fabrication gate remains mandatory.

ADR 0217 permits only the exact ignored front-side R11 prototype: fixed native flip/pose, graph-proven 25-item obsolete gate prefix replacement and one ordinary F gate lead, with direct retained main VLED contact and no new supply trace/via. All 215 prior groups, all GND contacts and retained copper, matching 26 native/physical opens, exact104 and every full successor gate precede selection. Assembly/fit and all other qualification/fabrication holds remain.

Selected ADR0217 successor has 26 matching native/physical opens, all 215 preceding groups, all 196 main ground pads and attached retained copper preserved, exact original104 and all full source/contact/serialized/side-flip/replay/inverse/fault/visual gates passed. No new via is added; 556 unsupported historical centre microvias and every electrical/assembly/fit/stack/process/Gate A/fabrication hold remain unresolved. See `docs/development/r11-front-routing-2026-11-19.md`.

ADR 0218 permits only read-only supported outer capture and ordinary PAIR01 gate-neck discovery in the exact corridor freed by the qualified front-R11 replacement. All selected parts/copper/rules remain fixed; no PCB or successor is selected, and every complete successor and qualification/fabrication gate remains mandatory.

ADR 0219 permits read-only replacement discovery for one exact sole-blocking COL_09_R In4 wire using its two retained supported In3/In4 via interfaces, mutually with supported row-zero access and bounded ordinary In3 routing. Every other source item/part/rule remains fixed; no PCB or successor is selected and all complete successor and fabrication gates remain mandatory.

ADR 0220 permits only read-only supported B colour-hop discovery for the same one frozen COL_09_R In4 wire and original far interfaces, mutually with the fixed supported row-zero gateway. All source parts/other copper/rules and complete original-ground/successor/fabrication gates remain mandatory; no PCB or successor is selected.

ADR 0221 permits only an independent read-only one-wire COL_09_B alternative using its two exact retained interfaces and mutually checked supported row-zero access/local ordinary In3 hop. The red net and all other source parts/copper/rules stay fixed; no PCB or successor is selected and every complete successor/fabrication gate remains mandatory.

The selected front-R11 validation explicitly checks actual F.CrtYd geometry against all 257 original front footprints and rejects overlap/missing-courtyard controls. The preliminary B-only helper error is recorded with corrected identical pose results; full native exact104 and all PCB/plan/source hashes remain unchanged. No qualification/fabrication hold is relaxed.

ADR 0222 permits only exact read-only additive R71 sense-branch discovery using ordinary conductors, supported staggered microvia/mechanical transitions and the unchanged 0.500 mm lower-edge clearance. All parts/source copper/current settings remain fixed; no PCB or successor is selected and every original-group/full-successor/qualification/fabrication gate remains mandatory.

ADR 0223 permits only bounded read-only fixed-R71 B/In4 discovery using ordinary necks, supported outer captures and actual retained main VBUS targets, with all source copper/parts/rules/current settings fixed. No PCB or successor is selected; every original-group and complete successor/qualification/fabrication gate remains mandatory.

ADR 0224 permits only exact read-only front-side PAIR01/R6 circuit discovery with correct front courtyards, the four frozen obsolete row-output items prospectively omitted and actual retained supply/ground/output/selector targets. Original pin associations, row-current lead bounds, all other source items and full successor/qualification/fabrication gates remain mandatory; no PCB or successor is selected.

ADR0225 authorizes only the frozen front PAIR01/R6 CAD prototype, with exact
source-group preservation and 23-open target; all successor validation and
fabrication holds remain required before adoption or release.

ADR0226 rejects ADR0225's split-supply candidate and authorizes the exact
PAIR01-only ground successor study, targeting 25 matching opens with R6 and
its original main supply intact; full successor gates remain mandatory.

ADR0227 permits only read-only R6 discovery through the vacated R11 corridor
on the selected 25-open source; supported transitions, exact original supply
contacts and every existing group remain mandatory. No PCB adoption is authorized.

ADR0228 separately permits read-only discovery for the R6 pull-up supply
lead (≤8 mm), leaving PAIR01's row-current supply pad explicitly open and its
prior ≤6 mm high-side limit unchanged. All full successor gates still apply.

ADR0229 permits read-only discovery of the reversed R6 B pose and supported
lower-layer pull-up restoration. It does not select a board or imply gate or
row-power closure, and all original groups and qualification holds persist.

ADR0230 permits only the exact R6 combined discovery screen in vacated
PAIR01 space, with separately restored pull-up supply/gate and unchanged
row-power open. Full successor validation and all qualification holds persist.

ADR0231 permits only bounded supported gate-transition and separate supply-
capture discovery on the unchanged 25-open source; no full route or source
replacement may be inferred from a clear local access.

ADR0232 permits exact read-only replacement discovery for fifteen private
COL_06_B In3 staircase segments, preserving all outside contacts and source
groups; any complete successor still requires all full validation and holds.

ADR0233 permits a separately bounded ≤24 mm front-only R6 resistor pull-up
CAD study, with unchanged 1 kΩ/current/default-off and explicit timing/EMI
qualification holds. It leaves row power open and authorizes no via or release.

ADR0234 permits only exact combined discovery with separated R6 gate/supply
captures and a contact-preserving color replacement. Full restoration and all
successor gates are mandatory before source selection; all holds persist.

ADR0235 permits only contact-preserving replacement discovery for the exact
COL_07_G In2 track, with all other source and proposed copper retained and
full restoration/successor checks still required before selection or release.

ADR0236 permits read-only R6 placement/lead discovery using the actual
PAIR02.4 B main-supply port and fixed supported gate transition, retaining
all original color/row copper and every qualification hold.

ADR0237 authorizes only the exact R6 direct-bottom prototype and complete
successor validation, targeting 24 matching opens with all 213 original groups
preserved and no color replacement or changed qualification/current limits.

ADR0238 permits only read-only supported access discovery at PAIR01.4 on
the selected 24-open source, with no source retirement or changed current/
default-off. Full restoration, row-power qualification and successor gates persist.

ADR0239 permits exact read-only PAIR01 supply-locality discovery, retiring
only its frozen obsolete package leaves and restoring all original groups/
contacts; complete 23-open validation and all qualification holds remain required.

ADR0240 permits only bounded In1/In2 selector restoration to witnessed
retained driver Cu for the PAIR01 locality study, with unchanged full source/
new-hole rules and all successor, row-power and fabrication holds.

ADR0241 permits only read-only selector-access relocation below the retained
color bus with an explicit F ground-lead template, preserving all source groups,
unchanged study bounds and full qualification/successor requirements.

ADR0242 permits only bounded F/In1/In2 selector discovery from the actual
new pad, retaining the original direct ground proposal and all source Cu
outside the frozen obsolete leaves; no release or qualification is implied.

ADR0244 permits only bounded read-only exact R9 bottom placement/lead
screening between witnessed PAIR04 supply/gate ports; source copper may
not retire and no PCB may be written without a separately frozen complete
replacement and every successor check. All qualification holds persist.

ADR0245 expands only read-only R9 bottom discovery and its gate conductor
study bound to12 mm, with exact1 kΩ, native mutual/source clearance and
all timing/return/Gate A holds retained. No source retirement or PCB follows
without an exact frozen successor and full validation.

ADR0246 permits only independent read-only B corridor screens of exact
R10/R12/R13 against actual connected supply/gate ports, without source
retirement, additional vias or part/net changes. Every successor gate and
all electrical/qualification/Gate A holds remain prerequisites for adoption.

ADR0247 permits only exact read-only R9 front supply/supported gate-fanout
discovery with a mechanical centre and unchanged source/new drill rules.
Every old group and retained attached copper, full successor validation
and all electrical/qualification/Gate A holds remain mandatory.

ADR0248 permits only read-only staggered R9 lower access discovery, first
checking B to one supported B/In4 via without inferring an aligned In3/In4
transition or complete gate. Source, hole, full successor and qualification
boundaries remain unchanged.

ADR0249 permits only exact read-only contact-preserving replacement
discovery for one recorded COL_05_B segment, with a mandatory original
left stem and fully screened supported gate/color captures. No source
selection, new centre/through via or changed qualification follows from it.

ADR0250 permits only exact read-only two-color gateway prerequisite
screening with both recorded original contact catalogues, ordinary widths
and unchanged source/new drill rules. All old groups and full successor,
color/row qualification and independent Gate A boundaries remain required.

ADR0251 permits only a bounded one-color local hop with native-tested
within-pad gate access and exact original stems/ports; all original red,
green, row and boot Cu remain. No source selection or complete gate may
be inferred without the full successor and qualification gates.

ADR0252 permits only native read-only complete lower/core gateway discovery
before any color replacement is frozen, reserving a supported mechanical
centre and full ordinary-width lower lead under unchanged source/new Cu,
drill, old-group and qualification requirements. No PCB or join is inferred.

ADR0253 permits only independent read-only gate/core routing with the
unselected Blue capture omitted, retaining the original-contact stem and
all original source boundaries. Full color and R9 restoration and every
successor/qualification check still precede any board selection.

ADR0254 permits only read-only additive fixed-U39 B supply discovery to
actual retained main USB-rail Cu. No sensor/capacitor move, bypass
reassignment, source retirement, new via or qualification change is allowed;
all original groups and full successor checks precede22-open selection.

ADR0255 permits only read-only fixed-U39 supply discovery through one
supported B/In4 access with full source/new Cu and drill checks. No source
retirement, part move, other via span or changed electrical/bypass/
qualification boundary is permitted; all successor checks remain mandatory.

ADR0256 permits only exact read-only replacement screening for two B
selector walls and one supported access, with complete original interfaces,
all other source Cu/parts and full source/new hole rules preserved. No
supply join or source selection follows without all successor checks and
unchanged electrical/qualification/Gate A boundaries.

ADR0257 permits only an exact read-only0.15 mm U39 translation with full
original pad-contact, thermal/programming/C50 bounds and four precisely
catalogued selector/TEMP_OK replacements. No original other item or
qualification boundary changes; full22-open restoration and successor
checks remain prerequisites for adoption.

ADR0258 permits only three bounded small sensor/gateway offset templates
with all original contacts, fixed programming/capacitor roles, thermal
reservation and original unsupported-hole floors enforced. No supply or
source selection follows without full22-open successor qualification.

ADR0259 permits only the exact small U39/R90 gateway prerequisite with
unchanged parts/thresholds, complete original contacts and thermal/C50/
programming bounds, all other481 parts and source Cu fixed. No source
selection or supply join precedes the full22-open successor and Gate A
qualification boundaries.

ADR0260 permits only the exact three-part small sensor gateway with six
catalogued source replacements, complete original programming/output/
ground interfaces and unmodified thresholds/thermal/C50 bounds. All other
source items and parts remain; supply and full successor/qualification
checks still precede adoption.

ADR0261 permits only read-only complete sensor supply discovery on its exact
source-preserving gateway, with actual32-pad main targets and per-candidate
refill/all211-group/retained-Cu/orphan checks. No saved PCB or22-open
selection precedes a frozen full prototype and all qualification gates.

ADR0262 permits only finer native B sampling on the same complete sensor
supply gateway, with unmodified copper/clearance/via/hole dimensions and
actual physical connectors. All per-candidate old-group/retained-Cu checks
and full successor/qualification boundaries remain mandatory.

ADR0263 permits only multiscale native supply discovery with explicit
physical fine/coarse connectors and unchanged source/Cu/via/hole rules.
All per-candidate original-group checks, full successor qualification and
independent Gate A/fabrication boundaries remain mandatory.

ADR0264 permits only actual-contact-derived ordinary B tangent polylines,
with every integer segment native-screened and old groups/retained Cu
verified after refill. Waypoints are not electrical witnesses. All physical
rules, full successor and qualification/Gate A boundaries remain unchanged.

ADR0265 permits bounded supply continuation carrying the exact real ADR0264
escape and length, with original group/Cu preservation and actual USB32
contact required. No waypoint witness, profile change or fabrication release.

ADR0266 permits wider seeded sensor geometry discovery at x49..65/y9..21.5
and20 mm total conductor,400000 states, without electrical acceptance or
changes to physical rules, source preservation or fabrication boundaries.

ADR0267 permits a second supported In3/In4 microvia and ordinary In3
routing in the same bounded seeded study. All native source/mutual hole,
contact, group/Cu and full successor qualification boundaries remain.

ADR0268 permits an independent fixed-PAIR03 additive B/In4/In3 supply
study with unchanged physical/part/source rules and explicit25 mm bound.
Only actual filled22/VLED39 with every prior group/Cu retained can advance.

ADR0269 freezes the exact18-item additive PAIR03 route before prototype
write. Selection requires full source/group/Cu/DRC104/replay/inverse/fault/
visual qualification; all electrical, trial-package and fabrication holds remain.

ADR0270 selects the fully qualified22-open additive PAIR03 CAD source,
preserving all211 previous groups/all19349 attached source Cu and exact104.
The zero-open objective and all electrical/qualification/Gate A holds remain.

ADR0271 permits fixed-PAIR05/07/09 additive supply discovery from source22,
with actual VLED39 contact and all210 original groups/all19367 source Cu
preserved. A combined RAM-only19-open/VLED42 trial requires all three
full joins and all new/source hole checks; full qualification remains separate.

ADR0272 permits conservative native configuration-space inspection for
fixed PAIR05/09 using exact source Cu and unchanged0.20 mm routing rules.
Any derived conductor needs native screening/full source preservation;
no global no-path or fabrication/electrical acceptance is inferred.

ADR0273 permits the exact three-item PAIR05 ground-leaf gateway study,
restoring every retained outside contact/group/Cu and GND197 at22 opens.
No partial supply, further retirement or qualification/fabrication release.

ADR0274 permits a shorter PAIR05 ground capture at the exact retained
trunk corridor, with no zero-length segments and unchanged three-item
cohort/full source preservation. Return capacity remains unqualified.

ADR0275 permits one supported0.50/0.30 mm In2/In3 mechanical capture
for fixed PAIR07 with explicit source/mutual hole rules and full original
connection/Cu preservation. No unsupported new centre via or release.

ADR0276 permits read-only coordinated F-side PAIR05/R10 placement
discovery, with exact parts/pins and actual plane contacts, supported
outer access and unchanged physical rules. No source retirement or
partial module selection; full original-group/Cu qualification remains.

ADR0277 permits bounded real F row/selector access and source-contact
backed private-leaf graph cataloguing, without source adoption or PCB write.
All physical/hole rules and complete-module qualification remain unchanged.

ADR0278 expands the read-only front cell to exact R26 ERJ2RKF1003X,
100k1%, preserving its ground/default-off topology, and permits bounded
ROW04 F/In1 access with supported microvias. Native source cataloguing
must reflect the actual PAIR05/R26 versus U2 split; no omitted fixed pad.

ADR0279 freezes the exact111-item front-cell RAM restoration and three
independently specified flips. Temporary ROW/selector splits cannot be
selected regardless of open count; all210 prior groups and retained Cu
must be restored in the full20-open candidate before PCB qualification.

ADR0280 permits a bounded real F hop in the proposed ROW04 path to
preserve the actual VLED40 plane connection, with source/mutual holes
and all other original groups retained. A pending selector is still an
unselected partial state; no source or fabrication boundary changes.

ADR0281 permits F-only row search with actual source goals or a single
later supported layer entry carrying the complete real In1 suffix.
Source VLED40 and all original groups except pending selector must
survive; no waypoint-only join or partial PCB selection is permitted.

ADR0282 permits a real supported VLED surface bridge between the actual
six- and34-pad groups after the proposed row cut. Source/new Cu, holes,
all other original groups and VLED40 are mandatory; no current limit or
source/fabrication boundary changes, and selector restoration remains.

ADR0283 extends only the source-connected supply probe corridor and
permits real existing F ports in the opposite proved supply group.
No zone-label-only contact, extra source retirement, current change or
partial selection; full source/group/Cu/hole boundaries remain mandatory.

ADR0284 permits a bounded ordinary In2 or In3 supply bridge between
actual existing source-connected ports, without new holes or source
retirement. VLED40/GND197 and all other original groups/Cu must survive;
existing unsupported transitions remain held and selector still pending.

ADR0285 permits ordinary B or In4 supply bridging between actual
nearest existing group ports, without new holes or source changes.
Every original group except pending selector and all retained Cu must
survive; a full20-open/all210-group cell still precedes qualification.

ADR0286 permits bounded ordinary surface supply routing between the
actual existing groups, with a calculated8 mm F bound and no new holes.
Complete native continuity and all source/Cu/qualification boundaries
remain mandatory; this is not electrical or fabrication acceptance.

ADR0287 permits a bounded two-layer lower supply bridge using at most
two supported B/In4 microvias. The source-hole cache may not waive an
unsupported source hole, and every candidate must pass the original
full native auditor plus all source/group/Cu continuity requirements.

ADR0288 permits a bounded real front-cell selector join to the retained
U2-side port, with at most one supported F/In1 microvia. A selector-only
RAM state remains unselected; full row/supply restoration and all original
source/group/Cu/hole/qualification boundaries precede any PCB prototype.

ADR0289 permits bounded In2 row routing through supported aligned outer
microvias to avoid severing the actual supply plane. All original groups
except pending selector, source Cu and unchanged native Cu/hole boundaries
must survive; no new centre/through transitions or partial selection.

ADR0290 permits bounded supported F/In1 selector discovery after direct
templates fail; ADR0291 permits bounded supported In1/In2 row discovery
after the fixed aligned capture fails Cu clearance. Every original
source/group/Cu/hole and complete-cell qualification boundary remains.
