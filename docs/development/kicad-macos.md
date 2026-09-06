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

## First GUI round-trip check

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

The script requires stable KiCad 10.0.x, checks the controlled LED pin/pad geometry, exports the project-local symbol and footprint libraries through `kicad-cli`, and runs ERC with violations treated as a failure. It uses the application-bundle CLI automatically on macOS. Set `RGB_BADGE_KICAD_CLI` only when testing a specific alternate executable.

To retain SVGs for human inspection, give the check a new output path that does not already exist:

```bash
RGB_BADGE_KICAD_CHECK_OUTPUT=hardware/coupon/rev-a/build/led-library-review ./tools/check-kicad.sh
open hardware/coupon/rev-a/build/led-library-review
```

The `build` directory is ignored by Git. The check requires six non-empty raw SVGs and creates two derived numbered review copies:

| Output folder | What to look for |
|---|---|
| `symbols/` | Two symbols with readable, separated `R_K`, `G_K`, `B_K` and `A` labels. `D?` is an unassigned component reference, not an error. |
| `footprints/fabrication/` | Two unchanged raw KiCad views: outlined pads, body outline with pin-1 chamfer, silkscreen marker and outer courtyard. Body strokes may cross the small pad numbers. These outlines are not copper connections. |
| `footprints/numbered/` | Two derived review copies with the original pad-number glyphs overlaid on white halos. Use these for readable pad identification; use the raw views and source files for geometry inspection. |
| `footprints/copper/` | Two copper-only views, each with four separate solid pads and no connecting lines. Pad numbers are intentionally absent; identify them in the numbered views. |

The fabrication export uses `F.Fab,F.SilkS,F.CrtYd` and `--sketch-pads-on-fab-layers`. Copper is exported separately with `F.Cu`. These are [KiCad 10 CLI export options](https://docs.kicad.org/10.0/en/cli/cli.html). `number-footprint-review.py` then copies the existing numbered glyphs over a white halo and adds a small viewing margin. It preserves the raw exports, records each source SVG's SHA-256 in the derived copy, and rejects unexpected or missing labels. The derived view is not a manufacturing drawing. Mask and paste are deliberately absent from these readability views; their review remains a separate DFM task.

For the unrotated footprint top views, confirm this corner-to-pad mapping against the controlled drawings:

| LED | Upper-left | Upper-right | Lower-left | Lower-right |
|---|---|---|---|---|
| `EAST10105RGBA0` | 4 / green | 1 / common anode | 3 / blue | 2 / red |
| `QBLP1515A-RGB2A` | 3 / green | 4 / red | 2 / blue | 1 / common anode |

The pin-1 chamfer and marker must identify the common-anode corner. `REF**` belongs to the fabrication layer, not the physical front silkscreen. If you are unsure, upload the complete output folder as a ZIP together with the command output for review; do not treat uncertainty as approval. The [reviewed examples](led-library-review-27c01b4.md) show the two numbered views and their expected mapping.

Compare with the [LED audit](../../hardware/coupon/rev-a/footprints/led-audit.md). A successful export checks KiCad parsing; it does not replace that drawing comparison or the independent Gate A review. ERC still runs on a blank schematic and therefore does not validate the eventual circuit.
