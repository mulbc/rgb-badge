<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# KiCad 10 setup on macOS

Coupon Rev A is authored and validated with stable KiCad 10.0.x. The initial baseline is 10.0.6 under [ADR 0006](../decisions/0006-kicad-10-workflow.md).

## Open the project

From a synchronized repository checkout:

```bash
git switch main
git pull --ff-only
./tools/check-kicad.sh
open hardware/coupon/rev-a/rgb-badge-coupon.kicad_pro
```

On first opening the project, do not accept a migration to a newer KiCad major release. Project-specific symbol and footprint tables use `${KIPRJMOD}`, so no personal library paths should be added.

## Initial blank-project GUI round-trip (completed history)

This check was completed on the original blank project. The current draft contains a root and seven child sheets; its row-capture run passed and is recorded in the [native evidence record](row-capture-review-eb4129b.md), while the new controller page awaits its native run. Use the validation command again after every schematic increment.

1. Open `rgb-badge-coupon.kicad_pro` from the command above.
2. Open the Schematic Editor from the project manager.
3. Confirm that a blank A4 root sheet opens without a missing-library or rescue-symbol dialog.
4. Press `Command-S` once so KiCad 10.0.6 performs a real save-format round trip, then close the Schematic Editor and project manager. Do not add parts or create a PCB yet.
5. Run `git status --short` and report any changed or untracked files. Changes to the project or schematic are useful round-trip evidence, but do not commit them yet. Local state such as KiCad's `.history/` directory, `.kicad_prl` files, lock files and backups must never be committed.

The schematic is intentionally blank at this stage. Passing this check proves only that the project container and local-library paths load; it does not validate any circuit.

## Validation command

Run this after every schematic change:

```bash
./tools/check-kicad.sh
```

The script requires stable KiCad 10.0.x, checks the controlled LED, driver, row-selection and controller pin/pad geometry plus every captured source connection, exports the project-local libraries, and runs ERC with violations treated as a failure. It then exports KiCad's XML netlist, verifies all 356 PCB items / 1,360 logical pins, and exports the complete schematic to PDF. The script uses the application-bundle CLI automatically on macOS. Set `RGB_BADGE_KICAD_CLI` only when testing a specific alternate executable.

To retain SVGs for human inspection, give the check a new output path that does not already exist:

```bash
RGB_BADGE_KICAD_CHECK_OUTPUT=hardware/coupon/rev-a/build/led-library-review ./tools/check-kicad.sh
open hardware/coupon/rev-a/build/led-library-review
```

The `build` directory is ignored by Git. The current check requires 19 controlled-symbol SVGs and 12 footprint SVGs in each raw view, then creates two derived numbered LED review copies:

| Output folder | What to look for |
|---|---|
| `symbols/` | All 19 controlled symbols. For the LEDs, confirm readable, separated `R_K`, `G_K`, `B_K` and `A` labels; `D?` is an unassigned component reference, not an error. Review the controller items using the page-8 checklist below. |
| `footprints/fabrication/` | Twelve unchanged raw KiCad views: outlined pads, body outlines, silkscreen and courtyards. LED body strokes may cross the small pad numbers. These outlines are not copper connections. |
| `footprints/numbered/` | Two derived review copies with the original pad-number glyphs overlaid on white halos. Use these for readable pad identification; use the raw views and source files for geometry inspection. |
| `footprints/copper/` | Twelve copper-only views. The two LEDs must each have four separate solid pads and no connecting lines. Pad numbers are intentionally absent; identify LED pads in the numbered views. |
| `coupon-schematic.pdf` | Root page, four 64-LED matrix pages, driver page, row-selector page and controller page. Inspect all eight actual KiCad pages for label collisions and wiring clarity. |
| `coupon-matrix.xml` | KiCad's complete connectivity result, checked against matrix, driver/support, row selectors and controller: 356 PCB items / 1,360 logical pins. The filename is retained for compatibility. |

The fabrication export uses `F.Fab,F.SilkS,F.CrtYd` and `--sketch-pads-on-fab-layers`. Copper is exported separately with `F.Cu`. These are [KiCad 10 CLI export options](https://docs.kicad.org/10.0/en/cli/cli.html). `number-footprint-review.py` then copies the existing numbered glyphs over a white halo and adds a small viewing margin. It preserves the raw exports, records each source SVG's SHA-256 in the derived copy, and rejects unexpected or missing labels. The derived view is not a manufacturing drawing. Mask and paste are deliberately absent from these readability views; their review remains a separate DFM task.

For the unrotated footprint top views, confirm this corner-to-pad mapping against the controlled drawings:

| LED | Upper-left | Upper-right | Lower-left | Lower-right |
|---|---|---|---|---|
| `EAST10105RGBA0` | 4 / green | 1 / common anode | 3 / blue | 2 / red |
| `QBLP1515A-RGB2A` | 3 / green | 4 / red | 2 / blue | 1 / common anode |

The pin-1 chamfer and marker must identify the common-anode corner. `REF**` belongs to the fabrication layer, not the physical front silkscreen. If you are unsure, upload the complete output folder as a ZIP together with the command output for review; do not treat uncertainty as approval. The [reviewed examples](led-library-review-27c01b4.md) show the two numbered views and their expected mapping.

Compare with the [LED audit](../../hardware/coupon/rev-a/footprints/led-audit.md) and [controller capture record](../../hardware/coupon/rev-a/controller-capture.md). A successful export checks KiCad parsing; it does not replace drawing comparison or independent Gate A review. ERC now runs on matrix, driver, rows and controller, with explicit draft supply flags. Passing it and the pin-to-net checks does not validate the uncaptured power/input source, RF installation, row timing or hardware VLED inhibition.

Driver exports add the TLC59581, R1/C1 and virtual power-flag symbols plus three footprints. The `footprints/paste/` view reveals the 16 thermal-pad paste apertures; inspect it together with the copper and fabrication views.

Row-library exports add the `74HC4514PW,118`, `DMP2066LSN-7`, `2N7002K-7` and `ERJ-2RKF1001X` symbols plus TSSOP24, SC-59 and SOT23 footprints. Their first-author library render and the complete row-capture review have passed. Neither result authorizes fabrication.

Controller exports add the exact N16R8 module, reset/USB/UART passives and `EVQP7J01P`, plus the module, 0603 capacitor and side-push switch footprints. On page 8, confirm GPIO35–37 are explicitly no-connect, GPIO0 reaches the pull-up/button/test pad, EN reaches its 10 kΩ/1 µF network, USB pins pass through separate 22 Ω resistors, and every recovery/test pad is readable. In the copper/paste views, confirm 40 perimeter module lands plus nine distinct same-numbered pad-41 lands; the switch has two pad-1 and two pad-2 lands.
