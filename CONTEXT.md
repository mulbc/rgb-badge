<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Project context

## Purpose

Create a small, manufacturable 48 × 16 RGB wearable badge that preserves the 1.95 mm pixel pitch of the referenced FOSSASIA Badge Magic board. The owner intends to develop the electronics, firmware and enclosure with AI assistance, then have a turnkey PCBA supplier assemble the SMT hardware.

## Active simplification — ADR 0013

The owner accepted **Type-C-only charging** on 2026-09-18. This section supersedes the historical BC1.2/SDP/boost descriptions below. [ADR 0013](docs/decisions/0013-type-c-only-fixed-current-charging.md) keeps OFF charging and charge-through operation only for Type-C sources advertising 1.5 A/3 A. USB-A/default-current sources provide data while ON from battery power, but no charging or charger PowerPath input. Depleted-battery USB recovery on those sources is not guaranteed.

The revised source removes BQ24392 and its support parts, eleven permission gates, three dual buffers and obsolete grant pull resistors/test pads: **47 fewer PCB items**. Current totals: **396 items / 1,492 logical pins, eleven pages**. The libraries remain 46 symbols / 27 footprints, including retained historical candidates. Native run at cb81e86 stopped on an isolated USB_OUT2 label; TP21 is now source-corrected to observe conditioned OUT2. The revised three-sheet native review remains pending; see [finding](docs/development/type-c-only-review-cb81e86.md).

The fixed ILIM uses the audited 3.65k/3.48k precision pair permanently in parallel, with no analog switch. ADG4612 and its leakage/supply screening are historical, not active blockers. Remaining power work: protected input, VBUS qualification and physical standby control; charger/pack/NTC/timer/thermal design; converter and gauge capture; whole-port budget and layout. Flag meaningful simplification opportunities to the owner before expanding complexity.

## Current state

- Requirements interview: complete.
- Architecture: accepted baseline, subject to coupon measurements.
- KiCad workflow: 10.0.6 stable baseline accepted; Coupon Rev A project and blank schematic scaffold created; the first macOS GUI round-trip opened and saved without errors, and CLI ERC reported zero violations.
- Coupon LED pair: `EAST10105RGBA0` in columns 0–7 and `QBLP1515A-RGB2A` in columns 8–15.
- Coupon LED libraries: first-author exact-MPN transcription and rendering review complete. Owner KiCad 10.0.6 exports at `27c01b4` passed pin/pad comparison; separate derived numbered views resolve body-outline/label overlap. The [review record](docs/development/led-library-review-27c01b4.md) preserves evidence and limits; independent Gate A verification remains pending.
- Coupon schematic: the matrix and TLC59581 driver passed owner KiCad 10.0.6 ERC/exported-netlist and six-page visual review at `8e95eb0`. Exact row-selection libraries passed native rendering review at `0c71860`; the complete row capture then passed zero-violation ERC, 335-item / 1,290-pin native connectivity and seven-page visual review at `eb4129b`. The exact N16R8 controller, reset/mode defaults, USB/UART boundaries and test pads passed the strict staged ERC gate, 356-item / 1,360-pin native connectivity, footprint render and eight-page visual review at `d56e1aa`. The [power pre-capture record](hardware/coupon/rev-a/power-pre-capture.md) freezes charger/current-limit and converter-divider arithmetic while keeping the USB default-current/data topology and pack-dependent NTC limits explicit. The [power-library audit](hardware/coupon/rev-a/power-library-audit.md) controls exact BQ25616J, TPS631000, TPS63020, USB-only LDO/inverter, TUSB320LAI, MAX17048, INA232 and USB ESD symbols/land patterns; corrected native rendering passed at `3638b1d`. The separately audited USB4505 candidate library passed host checks and [owner-generated native rendering review at `bf1627c`](docs/development/usb-connector-review-bf1627c.md). Input protection and remaining power circuits are uncaptured; the active USB interface increment is described below. 3.3 V N-MOS behavior plus hardware VLED inhibition remain explicit review/measurement items. See the [controller review](docs/development/controller-review-d56e1aa.md) and earlier capture/review records.
- Power-library review update: the native run at `c84f8ce` passed its staged electrical checks, but drawing/render review found a charger ground-pad short, wrong converter stencil geometry and overlapping symbol headings. The corrected native exports at `3638b1d` passed first-author review. The follow-on row layout and stale-note repairs passed native electrical and visual review at `91ef697`, closing the recorded first-author findings. PR #8 remains draft. The [finding record](docs/development/power-library-review-c84f8ce.md) also tracks the existing row-page title-block collision and stale annotations, now closed by the [native layout review](docs/development/layout-review-91ef697.md). See the [correction review](docs/development/power-library-review-3638b1d.md).
- USB/input closure: [ADR 0009](docs/decisions/0009-usb-input-current-closure.md) rejects the provisional direct BQ25616J ILIM network. [ADR 0010](docs/decisions/0010-source-qualified-off-charging.md) selects `BQ24074RGTR` + `BQ24392RSER` + `TS3USB31ERSER` + the audited `TUSB320LAIRWBR` for the next capture: fail-safe standby by default; autonomous OFF charging only from a positively classified charging source or Type-C 1.5 A/3 A source; SDP charging only while ON, configured and unsuspended. BQ24392 `GOOD_BAT` stays high with VBUS to avoid its finite dead-battery timer; the application-powered TS3USB31E supplies hard-OFF data isolation. The replacement libraries pass source/host audits and [native rendering review at c054cb4](docs/development/power-replacement-review-c054cb4.md). [ADR 0011](docs/decisions/0011-usb-total-current-headroom.md) corrects the configured-SDP current budget using low external ILIM plus a hardware-only resistor boost; the 1,024-case GPIO permission contract passes static checks. The permission gates and detector/data/LDO capture now exist; auxiliary-current proof, startup inhibition, thermal proof and remaining power capture are pending. See the [replacement-library audit](hardware/coupon/rev-a/power-replacement-library-audit.md), including the corrected unpublished geometry findings. The recovered USB4505 library and owner-generated KiCad 10.0.6 exports passed first-author review; cutout reliefs and stack-up/process qualification remain open.
- Repository workflow: owner granted standing permission on 2026-09-07 to merge PRs after applicable checks pass. LED library PR #2 through controller PR #7 are merged. Power/input is the active increment.
- Hardware testing: none.
- Native permission checkpoint: the owner-generated KiCad 10.0.6 bundle at `6d9a08b` passed first-author ERC/XML/render review: ten pages, 417 items / 1,536 logical pins and only the historical USB-boundary warning pair. See the [evidence record](docs/development/permission-review-6d9a08b.md). All seven new symbols and the corrected DBV5/DBV6 views passed; the supervisor was library-only at that checkpoint.
- USB interface checkpoint (2026-09-17): the [USB interface capture](hardware/coupon/rev-a/usb-interface-capture.md) connects the CC/BC detectors to the Schmitt logic, adds the connector/data path/ESD and USB-only LDO, and removes the old logic-supply flag. Source totals are eleven pages, 437 PCB items / 1,620 logical pin entries. Two exact Panasonic resistor symbols were added; no new footprint. The old USB ERC exceptions are retired: zero violations are required. Owner native review at `d502e65` passed zero-violation ERC and the complete XML; J1/U33 heading overlaps were found and source-corrected and closed by native review at `2bb0e08`. See the [review record](docs/development/usb-interface-review-d502e65.md). Connector VBUS and the draft +5V_USB source remain deliberately separate until input protection is designed. VBUS qualification, startup/ILIM actuation and the rest of the power section remain open.
- Logic-rail supervisor increment (2026-09-17): U34 TPS3808G01DBVR plus five passives now drives LOGIC_READY on the conditioning sheet; VBUS qualification and physical charger/ILIM inhibition remain open. Circuit totals: 443 items / 1,636 logical pins and eleven pages. [Static corner calculations and capture](hardware/coupon/rev-a/usb-supervision-capture.md) are recorded; [native review at `2bb0e08`](docs/development/logic-supervisor-review-2bb0e08.md) passed zero-violation ERC, complete XML and the supervisor/heading visual checks. The same record identifies a temperature-drift counterexample to the provisional ILIM current allocation; no current setting was raised.
- Current safe action: documentation, exact-part research, calculations and coupon design.
- Current stop condition: do not order a PCB or battery until the Gate A engineering review is complete.

- Programming-resistor increment (2026-09-17): [ADR 0012](docs/decisions/0012-programming-resistor-error-budget.md) selects three exact Panasonic ERA2AEB parts (0.1%, 25 ppm/K) while retaining ±1% total resistance error and unchanged current ceilings. Source-audited libraries now contain 45 symbols / 26 footprints; [native resistor rendering at `9e71bb5`](docs/development/precision-resistor-review-9e71bb5.md) passed. Assembly/service drift and actuator leakage still require qualification. No new circuit parts were placed. The next [actuator screening](hardware/coupon/rev-a/charger-actuator-screening.md) investigates ADG4612BCPZ-REEL7; the supplied PDF has now been visually reviewed. Its [candidate library audit](hardware/coupon/rev-a/charger-actuator-library-audit.md) adds one symbol and one project-derived footprint (46 symbols / 27 footprints total), with [native rendering at 2b7a468](docs/development/actuator-library-review-2b7a468.md) accepted. No actuator is selected or captured; intermediate-supply behavior, leakage, control loading and assembly qualification remain open.

## Non-negotiable constraints

| Area | Constraint |
|---|---|
| Matrix | 48 × 16 true RGB; pixel pitch must not exceed 1.95 mm |
| Size | Complete case no larger than 110 × 35 × 11 mm |
| Weight | Aim ≤75 g; never exceed 100 g including cell, case and magnets |
| Runtime | Roughly 6 h for the published reference workload; no automatic brightness reduction |
| Charging | USB-C at 5 V; correct A-to-C/C-to-C behaviour; charge while operating |
| Radio | BLE only in explicit programming mode |
| Controls | One momentary mode button and one latching on/off slide switch |
| OFF state | Application electronics and display off; gauging remains available; autonomous charging only from a hardware-qualified charging source |
| Assembly | Turnkey PCBA; user plugs in the protected battery and assembles the case |
| Quantity | Five assembled full badges after coupon validation |
| Budget | USD 500–800 for coupon, five badges, cells, basic test tools and shipping; case filament/design and independent review excluded |

## Accepted architecture baseline

- Three TLC59581 constant-current drivers, one per 16-column RGB block.
- Discrete four-pad common-anode RGB LEDs in a 1:16 multiplexed matrix.
- Coupon Rev A compares exact `EAST10105RGBA0` and `QBLP1515A-RGB2A` finalists at 1.95 mm pitch.
- The QBLP1515 coupon half preserves the manufacturer land pattern and alternates 0°/90° placement on a checkerboard under ADR 0008.
- Sixteen level-shifted P-channel MOSFET high-side row switches.
- ESP32-S3-WROOM-1U-N16R8 with an external 2.4 GHz FPC antenna.
- `BQ24074RGTR` standalone linear charger/PowerPath selected for capture, with thermal performance and exact pack current still requiring coupon and Gate A validation.
- `BQ24392RSER` BC1.2 detector/data switch, application-powered `TS3USB31ERSER` hard-OFF data isolator, `TUSB320LAIRWBR` Type-C current detection and VBUS-powered fail-safe logic; standby is the passive state and only hardware detection can grant the external high-current mode.
- TPS631000-class 3.3 V rail and TPS63020-class approximately 3.9 V LED rail.
- MAX17048 fuel gauge and INA232 bidirectional battery-current monitor.
- Protected, NTC-equipped, connectorized 750–900 mAh LiPo; 900 mAh is preferred if the 11 mm stack closes safely.
- KiCad 10.0.6 stable with project-local symbols, footprints and 3D models.

## Power states

| Switch | USB | Application and USB data | Charging | Display |
|---|---|---|---|---|
| OFF | Absent | Off | No | Off |
| OFF | SDP, default-only or unclassified | Off | Standby / no charge | Off |
| OFF | BC1.2 charging source or Type-C 1.5 A/3 A | Off | Autonomous, hardware-bounded | Off |
| ON | Absent | Playback | No | Firmware-controlled |
| ON | SDP | Playback/USB data | Standby before configuration and during suspend; lower programmed input limit with auxiliary headroom while configured | Firmware-controlled |
| ON | Qualified charging source | Playback; USB data where supported | Active with load priority and hardware high-current permission | Firmware-controlled |

## Development stages

1. **Documentation:** requirements, ADRs and candidate-part evidence.
2. **Coupon design:** production-intent 16 × 16 mixed-LED test board.
3. **Gate A review:** completed schematic plus preliminary layout reviewed independently.
4. **Coupon fabrication and bring-up:** five PCBs, three assembled.
5. **Gate B:** measured optical, electrical, thermal, runtime, RF and storage results.
6. **Full badge:** final six-layer PCB and enclosure.
7. **Gate C:** second review, frozen BOM and three comparable assembly quotes.
8. **Pilot:** five fully assembled badges.

## Open engineering decisions

- Project-local LED footprints plus pad, polarity, tape-orientation and optical-bin verification.
- Exact protected/terminated cell and connector.
- Confirm supplied TLC59581 RTQ0056E versus RTQ0056G package; qualify the nominal 4.85 mA current calculation and TI table discrepancies.
- Circuit capture using the native-reviewed exact `BQ24074RGTR`/`BQ24392RSER`/`TS3USB31ERSER` libraries, VBUS-powered permission logic, hardware-only parallel ILIM branch and their final `ISET`/`ILIM`/termination/timer/NTC networks.
- Validation of the selected BC1.2/data-switch path, including SDP configuration/suspend, Type-C advertisement changes and conservative reset/detach behavior.
- Validation of the candidate `74HC4514PW,118`, `DMP2066LSN-7` and `2N7002K-7` row chain under real multiplex timing and current.
- Final USB ESD/VBUS protection topology.
- Final converter component values and layout.
- Coupon and final PCB stack-ups.
- Validation of the candidate external antenna's current gain documentation, case placement and worn RF performance.
- Winning LED, diffuser, current correction and GCLK timing after coupon tests.

## Language

- **Coupon:** the first 16 × 16 production-intent validation PCB.
- **Reference workload:** representative text/icons/animations with approximately 35% lit pixels at 25% fixed brightness.
- **Fixed brightness:** user-selected during programming; it is not changed automatically during playback.
- **Programming mode:** mode entered by holding the single button for about three seconds; BLE is enabled only in this state.
- **Release:** an immutable, hashed fabrication/assembly package tied to a tagged repository revision.

- Actuator supply analysis (2026-09-18): [conditional shared-rail calculation](hardware/coupon/rev-a/charger-actuator-supply-analysis.md) finds 0.2 V static UVLO margin, but does not close transient timing or control defaults. The ADG 17-ohm guarantee is restricted to its 4.5 V test envelope; no circuit capture or current-limit change.
