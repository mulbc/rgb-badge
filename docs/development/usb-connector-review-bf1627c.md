<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# USB4505 native library review: bf1627c

Status: **passed** for first-author native symbol and footprint rendering. This closes the native-rendering item in the [USB4505 audit](../../hardware/coupon/rev-a/usb-connector-audit.md). It does not qualify the undimensioned board-cutout reliefs, PCB stack-up, assembler process or complete USB/input circuit, and it is not fabrication approval.

## Evidence

The owner ran KiCad 10.0.6 at `bf1627cb3cc4ba0ce7f0d4e02a377a9a1dba5ea7` and supplied the complete export archive and terminal transcript. The initial literal placeholder `cd` failed harmlessly because the command was already run from the repository root; all project commands then completed, and `git status --short` produced no tracked changes. AppleDouble metadata in the macOS archive was ignored.

| File | SHA-256 |
|---|---|
| `usb-connector-review-bf1627c.zip` | `b2c07559e719ec682c2d90b406d497b8bc2d29a98d129f86d131f9b8cacaf57f` |
| `Pasted text(9).txt` | `248c0829581802e7900c8f4d837e0b703620b42541f3dbdb365b60144b240d54` |
| `coupon-erc.rpt` | `6dfb846f04514922bc40aec2cfdccaec3ae5e96e53a5b6851650725aa46d424f` |
| `coupon-matrix.xml` | `ea94654c904e27b1b6bbbf62df8420e4876faac396970d33ef9a0d83e8221c85` |
| `coupon-schematic.pdf` | `0203beeee8ad70e0755f16d3ddaeda4b3b581d356cdf51a9bf561913141baf38` |

The non-metadata bundle contains 29 symbol SVGs, 21 footprint SVGs in each of the fabrication, copper, paste and mechanical views, two derived numbered LED views, the ERC report, the XML netlist and the eight-page schematic PDF.

## Review result

- All source checks passed, including the exact USB4505 symbol/pad map, land/slot geometry, layer treatment, nominal 0.20 mm signal clearance, datum guides and absence of guessed `Edge.Cuts`.
- Native ERC reported zero errors and exactly the two allowed isolated `USB_D-` / `USB_D+` warnings at the still-open controller-to-power boundary.
- The native XML checker passed 356 PCB items and 1,360 logical pins for the captured matrix, driver, row and controller circuits.
- The symbol shows twelve physical land pins plus `S1 SHIELD`. CC1 and CC2 remain distinct, and the two D− and two D+ lands remain separately exposed for deliberate joining in the future input sheet. All headings and pin labels are legible and clear of the body.
- The fabrication and copper views show twelve separate signal lands and four separate oval shell lands. The four outer GND/VBUS lands are visibly wider than the eight inner lands; no adjacent copper touches. The pin-one mark, body outline and courtyard are readable.
- The paste view shows twelve filled SMT apertures. KiCad also draws the four plated shell drill slots as unfilled outlines; inspection of the SVG and footprint source confirms these are not paste apertures and the shell pads have no paste layer.
- The mechanical view shows the 9.24 mm dashed opening datum, board-edge datum, 0.80 mm PCB note and explicit unqualified-corner warning. It contains no `Edge.Cuts`. The undimensioned curved relief geometry therefore remains intentionally unresolved.
- All eight schematic pages were rendered and inspected. Their matrix, driver, row and controller contents remain intact and legible; the connector is library-only and correctly does not yet appear on a schematic page.

The recurring Fontconfig cache-version warning did not affect KiCad exports, ERC or netlist generation.

## Disposition

The project-local USB4505 symbol and draft footprint are accepted for continued schematic development at the first-author level. No library correction or repeat owner run is required for this checkpoint.

Before fabrication, obtain dimensioned corner-relief geometry or manufacturer CAD, qualify the 0.80 mm board and plated-slot/mask/stencil process with the selected assembler, complete the USB source-state/input-current design under ADR 0009, and obtain the independent Gate A review. PR #8 remains draft because the input, charger, gauge and switched-power circuits are not captured.
