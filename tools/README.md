<!-- SPDX-License-Identifier: Apache-2.0 -->

# Software tools

`python3 tools/screen-preliminary-placement.py --output mechanical/review` reads four project-local footprint courtyards plus the USB cutout guide and regenerates the [final-badge bounding-box screen](../mechanical/preliminary-placement-screen-2026-09-26.md). It produces an SVG and JSON, **not** a KiCad PCB or DRC clearance. Its 700 mAh pack rectangle is a coupon-only mechanical comparison; no battery has been selected for the final badge.

**Current functional checkpoint — ADR 0013:** Type-C-only fixed-current charging. `check-usb-permission.py` checks 16 resolved detector/supply states; `check-coupon-permission.py` independently traces the reduced three-gate/two-buffer circuit. The three revised USB sheets remove 47 PCB items. Complete source/fixture expectations are 396 items / 1,492 pins. Older dual-limit and BC1.2 tests/calculations are historical regressions, not active charging policy. Native KiCad review is pending; see [capture record](../hardware/coupon/rev-a/type-c-only-capture.md).

`generate-coupon-permission.py --output NEW_DIRECTORY` produces the conditioning and permission sheets without overwriting canonical files. `check-coupon-permission.py` traces 61 items / 176 pins and evaluates actual gate connections against the independent 1,024-state contract. This checkpoint passed native review at `6d9a08b`.

`generate-coupon-usb.py --output NEW_DIRECTORY` produces the USB interface sheet. `check-coupon-usb.py` checks its 20 items / 84 logical pins and domain/data connections. The added logic supervisor brings complete XML validation to **443 items / 1,636 logical pins**. Native review at [2bb0e08](../docs/development/logic-supervisor-review-2bb0e08.md) passed zero ERC violations and the eleven-page export. The precision-resistor increment added three ERA2 symbols and one footprint. The subsequent candidate ADG4612 library brings exports to **46 symbols and 27 footprints per raw view**; its [native rendering at 2b7a468](../docs/development/actuator-library-review-2b7a468.md) passed. Its [native rendering at 9e71bb5](../docs/development/precision-resistor-review-9e71bb5.md) passed; older counts below are historical.

`check-programming-resistors.py` validates the exact ADR 0012 symbols, ERA2 lands/courtyard and conditional multiplicative error budget. The existing current ceilings retain ±1% total resistance error. The assembly/service drift allocation, switch leakage and complete USB-current budget remain qualification items. `check-kicad.sh` requires each new native export; test fixtures only exercise wrapper behavior.

The [permission-library audit](../hardware/coupon/rev-a/permission-library-audit.md) covers the six new exact gate/supervisor symbols and shared DBV5/DBV6 package checks. `check-power-libraries.py` now guards ground-pin differences, open-drain electrical types, output polarity, package body/courtyard geometry and DBV6 mask/paste settings. Native permission-library rendering passed at `6d9a08b`; TPS3808 is now captured as U34 and passed native review at 2bb0e08.

Host-side utilities will include the deterministic content compiler, schema validation, release-manifest generation and analysis of power/runtime logs. Tools must be testable without a connected badge and must not rewrite measured evidence.

`check-led-libraries.py` audits the exact Coupon Rev A LED symbol pin maps, source drawing layout, footprint pads, polarity geometry and the nominal 1.95 mm checkerboard-clearance calculation. `check-kicad.sh` runs that audit, loads and exports the project-local libraries through KiCad 10, and runs schematic ERC. `check-erc-report.py` requires zero ERC messages; the historical `USB_D-` / `USB_D+` boundary exceptions are retired. Raw fabrication views and solid copper-only views are exported into separate directories.

`number-footprint-review.py SOURCE.svg NEW_OUTPUT.svg` creates a separate numbered review copy of a four-pad KiCad 10 fabrication export. It overlays KiCad's own glyph paths on white halos so body lines do not obscure the pad numbers. It preserves source evidence and geometry, adds a viewing margin, records the source SHA-256, and fails if the expected label structure changes. With `--profile rpw`, it requires the exact 14-glyph/10-pad multiplicities, removes numeric glyphs only from the derived copy and overlays the first unchanged source glyph per pad. This resolves repeated corner numbers on the compound RPW lands without moving geometry. The wrapper places these derived files in `footprints/numbered/`; they are not manufacturing outputs. The [recorded review](../docs/development/led-library-review-27c01b4.md) used the owner's actual KiCad exports.

`check-coupon-matrix.py` checks the matrix source: it verifies cached symbols, traces short wires to global labels, and checks all 256 LEDs and 1,024 pin-to-net assignments. This source subset checker is not KiCad ERC and does not support arbitrary buses, rotations or mid-wire junctions. Its historical `--netlist` mode remains available for matrix-only fixtures; the controller checker now owns complete native XML validation. `check-kicad.sh` runs every source checker around the real KiCad ERC/netlist export and also exports `coupon-schematic.pdf`.

`generate-coupon-matrix.py --output NEW_DIRECTORY` reproduces the initial matrix capture with stable UUIDs. It writes only a new directory and refuses existing paths. The generated draft was reviewed before its files were copied into the canonical project. Do not regenerate over subsequent KiCad edits; compare a temporary regeneration and integrate deliberate changes. Schematic orientation does not set PCB placement rotation.

Run the wrapper regression tests without KiCad:

```bash
python3 -m unittest discover -s tools/tests -p 'test_*.py' -v
```

The wrapper tests use a stub executable to check CLI arguments, output separation and failure handling. SVG-helper tests check original-geometry and glyph preservation, rejection of missing/duplicate/transformed labels, and protection against overwriting evidence. They do not render KiCad files, run real ERC, prove legibility or approve hardware. Actual KiCad output and human inspection remain required.

Matrix regression tests deliberately inject a colour swap with unchanged net sizes, a missing LED, a short between columns, a duplicated pin, a wire endpoint that misses its LED pin, and a global label facing into its wire. The label-direction check came from actual PDF review at `7120e93`. Synthetic XML tests prove checker behaviour; only a real KiCad-exported netlist can verify KiCad's interpretation of the new schematic.

## Driver increment

`python3 tools/check-coupon-driver.py` checks the controlled driver/support library, footprint geometry and simple source wiring. Its `--netlist` mode preserves the historical matrix-plus-driver 1,094-pin contract for regression evidence. The full current project must use `check-kicad.sh`, which delegates the complete XML to the row checker.

`python3 tools/check-row-libraries.py` independently checks the exact row decoder, P/N MOSFET and 1 kΩ pull-up symbols against their manufacturer pin tables, plus the TSSOP24, SC-59 and SOT23 pad geometry.

`python3 tools/check-coupon-rows.py` traces the captured decoder, all sixteen P/N-MOS stages, 37 resistors, decoupling and draft VLED boundary. Its `--netlist` mode preserves the historical 335-item / 1,290-pin matrix + driver + row contract. `generate-coupon-rows.py --output NEW_DIRECTORY` deterministically reproduces the initial row sheet and refuses existing paths; never regenerate over canonical KiCad edits.

`python3 tools/check-controller-libraries.py` checks the exact N16R8 module symbol/pad map, reset/USB/UART passives, capacitor lands and duplicate-contact mode-button footprint. `python3 tools/check-coupon-controller.py` traces the controller source and explicit no-connects; its `--netlist` mode owns the complete current contract; the original controller-stage contract was 356 items / 1,360 logical pins. `generate-coupon-controller.py --output NEW_DIRECTORY` deterministically reproduces the initial controller sheet and refuses existing paths.

The wrapper exports all project-local symbols and footprints, including separate paste views, and requires their files to be nonempty. `coupon-matrix.xml` retains its historical filename but contains the whole captured schematic. Local fixture tests do not run KiCad. Follow the [controller review instructions](../hardware/coupon/rev-a/controller-capture.md#native-review-still-required) for the current eight-page circuit.

`generate-coupon-matrix.py` is the historical one-time matrix-only capture helper. It must not replace the current root schematic: that would remove the driver sheet. The current KiCad files are canonical.

## Power pre-capture

`python3 tools/check-usb-connector.py` checks the GCT USB4505 candidate's 16-contact/12-land mapping, four plated shell-slot interpretations, 0.20 mm nominal copper clearance and non-manufacturing cutout datums. `check-kicad.sh` also exports a separate `footprints/mechanical/` view. See the [connector audit](../hardware/coupon/rev-a/usb-connector-audit.md) for source evidence, native review status and the unresolved cutout relief/process limits. The connector is not yet instantiated.

`python3 tools/check-power-design.py` freezes the selected BQ24074 `ISET`/external-`ILIM` arithmetic, ADR 0010 source/switch/configuration/suspend state table, initial TPS631000/TPS63020 feedback dividers, and maximum charger-plus-gauge allocation within the 50 uA OFF-state budget. It deliberately does not approve the captured BQ24392/TS3USB31E/priority logic as a complete power system, VBUS auxiliary-current budget, pack-dependent NTC/current limit, linear thermal behavior, converter passives or layout. See the [power/input pre-capture record](../hardware/coupon/rev-a/power-pre-capture.md).

`python3 tools/check-power-libraries.py` checks the selected `BQ24074RGTR`, `BQ24392RSER`, `TS3USB31ERSER`, legacy `BQ25616JRTWT`, `TPS631000DRLR`, `TPS63020DSJT`, `TLV75533PDBVR`, `SN74LVC1G04DBVR`, `MAX17048G+T10`, `INA232AIDDFR`, base-suffix `TPD4E05U06DQAR` and `TUSB320LAIRWBR` symbols against manufacturer pin tables. It verifies every RGT/RSE/RTW/DRL/DSJ/DBV/DDF/DQA/RWB/T822+3 land, exposed-pad splits, the RWB side-pad copper/paste difference, layers and pin-1 marks. The [power-library audit](../hardware/coupon/rev-a/power-library-audit.md) records source hashes and the intentionally unresolved connector/control packages. `check-kicad.sh` requires nonempty native symbol plus fabrication/copper/paste exports for every new footprint; the selected replacement libraries passed [native render review at c054cb4](../docs/development/power-replacement-review-c054cb4.md). Their [audit](../hardware/coupon/rev-a/power-replacement-library-audit.md) records the narrower RSE middle pads, 0.05-mm radii, body axes and corresponding fault tests.

`python3 tools/check-usb-permission.py` checks ADR 0011's detector GPIO contract over 1,024 stable input combinations, including hardware-only resistor boost and default-deny supply/reset behavior. This is a static contract, not a captured or simulated gate circuit. The power arithmetic check reserves configured-SDP auxiliary headroom, rejects the historical fixed-USB500 budget and prints the remaining capture blockers explicitly. Run `python3 tools/check-power-design.py --require-usb-closure` to require an implemented USB topology: it still exits 1 by design until protected input, supervisors, charger/ILIM actuation and complete power qualification are finished. State-table or library success alone is not USB-current closure. The rejected BQ25616J arithmetic remains as regression evidence.

## Logic-rail supervision checkpoint

`check-usb-supervision.py` audits the TPS3808 divider/CT selection and exact 620 kohm resistor. It is called by the permission capture check. Source totals are now 443 items / 1,636 logical pins on eleven pages. The native d502e65 bundle passed ERC/XML; its two heading findings and the added supervisor passed native review at 2bb0e08. See [capture and limits](../hardware/coupon/rev-a/usb-supervision-capture.md). The ordinary-resistor temperature counterexample remains regression evidence; ADR 0012 precision selection addresses it conditionally, with assembly/service drift still requiring qualification.

`check-power-design.py` also reports the candidate actuator shared-rail static UVLO margin. `actuator_supply_screen()` accepts explicit hypothetical local-drop/slew/delay bounds; it is a sensitivity calculation, not a transient guarantee. See the [supply analysis](../hardware/coupon/rev-a/charger-actuator-supply-analysis.md).

## Input protection screening

`python3 tools/check-input-protection.py` calculates candidate OVLO and PGTH divider corners with signed leakage and total resistor error, and records fixed-clamp/current-threshold limitations. It does not select a protection IC or validate transients. `--require-closure` deliberately fails until the input circuit is qualified. See ADR 0014 and `hardware/coupon/rev-a/usb-input-protection-screening.md`.
