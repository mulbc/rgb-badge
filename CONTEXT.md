<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Project context

## Purpose

Create a small, manufacturable 48 × 16 RGB wearable badge that preserves the 1.95 mm pixel pitch of the referenced FOSSASIA Badge Magic board. The owner intends to develop the electronics, firmware and enclosure with AI assistance, then have a turnkey PCBA supplier assemble the SMT hardware.

## Current state

- Requirements interview: complete.
- Architecture: accepted baseline, subject to coupon measurements.
- KiCad workflow: 10.0.6 stable baseline accepted; Coupon Rev A project and blank schematic scaffold created; the first macOS GUI round-trip opened and saved without errors, and CLI ERC reported zero violations.
- Coupon LED pair: `EAST10105RGBA0` in columns 0–7 and `QBLP1515A-RGB2A` in columns 8–15.
- Coupon LED libraries: first-author exact-MPN transcription and rendering review complete. Owner KiCad 10.0.6 exports at `27c01b4` passed pin/pad comparison; separate derived numbered views resolve body-outline/label overlap. The [review record](docs/development/led-library-review-27c01b4.md) preserves evidence and limits; independent Gate A verification remains pending.
- Coupon schematic: first matrix-only draft captured on four child sheets: 256 LEDs, 16 common-anode row nets and 48 colour-column cathode nets. Owner KiCad 10.0.6 ERC and exported-netlist checks passed at `63afa77`. All five corrected PDF pages passed visual review; net labels are clear and the revision field fits. The matrix milestone is merged. A fifth child sheet now captures TLC59581 U1, 39.2 kΩ R1, four 100 kΩ logic pull-downs and 100 nF C1, with an audited provisional RTQ0056E footprint and explicit draft supply flags. Driver source checks pass; native KiCad ERC/XML and six-page drawing review are pending. Row stages, controller and power source remain uncaptured. See the [matrix capture record](hardware/coupon/rev-a/matrix-capture.md) and [driver capture record](hardware/coupon/rev-a/driver-capture.md).
- Repository workflow: owner granted standing permission on 2026-09-07 to merge PRs after applicable checks pass. Library PR #2 and matrix PR #3 are merged; driver capture is the next draft increment.
- Hardware testing: none.
- Current safe action: documentation, exact-part research, calculations and coupon design.
- Current stop condition: do not order a PCB or battery until the Gate A engineering review is complete.

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
| OFF state | Application electronics and display off; autonomous charging and gauging remain available |
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
- BQ25616J standalone switching charger and NVDC power path.
- TUSB320LAI sink/current-advertisement detection with a passive 500 mA input-limit state.
- TPS631000-class 3.3 V rail and TPS63020-class approximately 3.9 V LED rail.
- MAX17048 fuel gauge and INA232 bidirectional battery-current monitor.
- Protected, NTC-equipped, connectorized 750–900 mAh LiPo; 900 mAh is preferred if the 11 mm stack closes safely.
- KiCad 10.0.6 stable with project-local symbols, footprints and 3D models.

## Power states

| Switch | USB | Application and USB data | Charging | Display |
|---|---|---|---|---|
| OFF | Absent | Off | No | Off |
| OFF | Present | Off | Autonomous | Off |
| ON | Absent | Playback | No | Firmware-controlled |
| ON | Present | Playback/USB data | Active with load priority | Firmware-controlled |

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
- Final charger `ICHG` and USB `ILIM` resistor networks.
- Validation or replacement of the provisional isolated charger D+/D− approach, including default-current behaviour before USB enumeration.
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
