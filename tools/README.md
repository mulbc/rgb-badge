<!-- SPDX-License-Identifier: Apache-2.0 -->

# Software tools

Host-side utilities will include the deterministic content compiler, schema validation, release-manifest generation and analysis of power/runtime logs. Tools must be testable without a connected badge and must not rewrite measured evidence.

`check-led-libraries.py` audits the exact Coupon Rev A LED symbol pin maps, source drawing layout, footprint pads, polarity geometry and the nominal 1.95 mm checkerboard-clearance calculation. `check-kicad.sh` runs that audit, loads and exports the project-local libraries through KiCad 10, and runs schematic ERC. Raw fabrication views and solid copper-only views are exported into separate directories.

`number-footprint-review.py SOURCE.svg NEW_OUTPUT.svg` creates a separate numbered review copy of a four-pad KiCad 10 fabrication export. It overlays KiCad's own glyph paths on white halos so body lines do not obscure the pad numbers. It preserves source evidence and geometry, adds a viewing margin, records the source SHA-256, and fails if the expected label structure changes. The wrapper places these derived files in `footprints/numbered/`; they are not manufacturing outputs. The [recorded review](../docs/development/led-library-review-27c01b4.md) used the owner's actual KiCad exports.

`check-coupon-matrix.py` checks the matrix source: it verifies cached symbols, traces short wires to global labels, and checks all 256 LEDs and 1,024 pin-to-net assignments. This source subset checker is not KiCad ERC and does not support arbitrary buses, rotations or mid-wire junctions. Its historical `--netlist` mode remains available for matrix-only fixtures; the row checker now owns complete native XML validation. `check-kicad.sh` runs every source checker around the real KiCad ERC/netlist export and also exports `coupon-schematic.pdf`.

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

`python3 tools/check-coupon-rows.py` traces the captured decoder, all sixteen P/N-MOS stages, 37 resistors, decoupling and draft VLED boundary. With `--netlist`, it is the comprehensive matrix + driver + row validator and requires 335 PCB items / 1,290 physical pin assignments. `generate-coupon-rows.py --output NEW_DIRECTORY` deterministically reproduces the initial row sheet and refuses existing paths; never regenerate over canonical KiCad edits.

The wrapper exports all project-local symbols and footprints, including separate paste views, and requires their files to be nonempty. `coupon-matrix.xml` retains its historical filename but contains the whole captured schematic. Local fixture tests do not run KiCad. Follow the [row-capture review instructions](../hardware/coupon/rev-a/row-capture.md#macos-validation) for the current seven-page circuit.

`generate-coupon-matrix.py` is the historical one-time matrix-only capture helper. It must not replace the current root schematic: that would remove the driver sheet. The current KiCad files are canonical.
