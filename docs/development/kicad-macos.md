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

The `build` directory is ignored by Git. Compare the symbol pin names/numbers, footprint pad numbers and pin-1 marks with the controlled drawings in the [LED audit](../../hardware/coupon/rev-a/footprints/led-audit.md). A successful export checks KiCad parsing; it does not replace that drawing comparison or the independent Gate A review.
