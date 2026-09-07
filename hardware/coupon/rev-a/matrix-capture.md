<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Coupon Rev A matrix capture

Status: first-author matrix-only schematic draft; source checks pass; real KiCad validation pending

## Circuit included

The first circuit increment contains 256 RGB LEDs and their electrical connections. It implements the already accepted population under ADR 0007; it does not change the architecture or current limits.

| Sheet | Rows | Columns | Population |
|---|---|---|---|
| `matrix-r00-c00.kicad_sch` | 0–7 | 0–7 | 64 × Everlight `EAST10105RGBA0` |
| `matrix-r00-c08.kicad_sch` | 0–7 | 8–15 | 64 × QT Brightek `QBLP1515A-RGB2A` |
| `matrix-r08-c00.kicad_sch` | 8–15 | 0–7 | 64 × Everlight `EAST10105RGBA0` |
| `matrix-r08-c08.kicad_sch` | 8–15 | 8–15 | 64 × QT Brightek `QBLP1515A-RGB2A` |

The root links these four A2 sheets. Matching global labels connect electrically across sheets. There are no powered outputs, driver ICs, row stages, controller, charging or supply circuits yet. This draft cannot operate as a display.

## Reference and net contract

Coordinates are zero-based, with row 0 at the top and column 0 at the left of the future display. Reference numbering is row-major: `D(16 × row + column + 1)`. For example, D1 is row 0/column 0, D9 is row 0/column 8 and D256 is row 15/column 15.

| Net family | Function | LED pins per net |
|---|---|---:|
| `ROW_00_A` … `ROW_15_A` | Common anodes in one row, eventually driven by one high-side row stage | 16 |
| `COL_00_R` … `COL_15_R` | Red cathodes in one column, eventually connected to one constant-current sink | 16 |
| `COL_00_G` … `COL_15_G` | Green cathodes in one column | 16 |
| `COL_00_B` … `COL_15_B` | Blue cathodes in one column | 16 |

These 64 nets carry LED current; they are not MCU logic signals. Assignment to the exact TLC59581 output pins comes with driver capture. Each part uses its distinct audited pin map: Everlight A/R/G/B = 1/2/4/3; QT Brightek = 1/4/3/2.

All schematic symbols are unrotated for readability. No PCB exists. The required 1.95 mm placement pitch and QBLP1515 0°/90° checkerboard remain PCB implementation checks under ADR 0008; they are not established by schematic drawing positions.

## Verification completed

- Source parsing succeeds for the root and all four matrix sheets.
- Every cached symbol matches the controlled project-local library.
- Unique references, UUIDs and hierarchy instance paths are checked.
- Source graph tracing finds the expected net at every one of 1,024 LED pins: 16 row nets and 48 colour-column nets, each joining 16 pins.
- Eighteen local regression tests pass. They include deliberate colour swaps, missing LEDs, column shorts, duplicate pins and disconnected wire endpoints, plus wrapper/export failure handling.
- `git diff --check` passes. No physical footprint or current-setting circuit changed.

These are source/software checks, not KiCad ERC, native rendering, a simulation or a bench measurement. The previous blank-sheet ERC does not cover this increment. Real KiCad 10 loading, ERC, exported netlist validation and PDF inspection are pending because the authoring environment has no KiCad executable.

## macOS validation

From the repository root, close KiCad and run:

```bash
git fetch origin
git switch coupon-matrix-rev-a
git pull --ff-only
git rev-parse --short HEAD
review_dir="hardware/coupon/rev-a/build/matrix-review-$(git rev-parse --short HEAD)"
RGB_BADGE_KICAD_CHECK_OUTPUT="$review_dir" ./tools/check-kicad.sh
git status --short
```

The output directory must be new. If it already exists, use another suffix; preserve earlier evidence. A successful run includes the matrix source check, LED library exports, ERC, a KiCad XML matrix-connectivity pass and a schematic PDF. Any failure is useful evidence: share the complete terminal output and do not disable checks to obtain a pass.

After a successful run, package the output:

```bash
ditto -c -k --keepParent "$review_dir" "$review_dir.zip"
open -R "$review_dir.zip"
```

Upload the ZIP and terminal output. We will inspect the PDF's five pages and the XML result. No manual schematic editing is required for this check.

## Next circuit increment

Capture the exact TLC59581 symbol/footprint, hardware current-reference calculation, decoupling and column-output mapping, then the row-switch/inhibit stages. Those additions require their own controlled datasheet audit and an expanded connectivity check. Independent Gate A review still applies before fabrication.

## Format references

- [KiCad schematic file format](https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/index.html): hierarchy, instance paths and global-label scope.
- [KiCad 10 CLI](https://docs.kicad.org/10.0/en/cli/cli.html): native ERC, XML netlist and multi-page PDF export.
- [LED manufacturer drawing audit](footprints/led-audit.md): exact electrical pin maps and footprint evidence.
