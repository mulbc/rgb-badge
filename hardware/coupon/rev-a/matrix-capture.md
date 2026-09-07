<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Coupon Rev A matrix capture

Status: matrix-only KiCad 10.0.6 ERC/netlist checks passed at `7120e93`; corrected drawing review pending

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
- Nineteen local regression tests pass. They include deliberate colour swaps, missing LEDs, column shorts, duplicate pins, disconnected wire endpoints and labels facing into their wires, plus wrapper/export failure handling.
- `git diff --check` passes. No physical footprint or current-setting circuit changed.

These local checks are source/software checks, not KiCad ERC, native rendering, a simulation or a bench measurement. The owner supplied actual KiCad evidence for the initial matrix below. The authoring environment still has no KiCad executable.

## Owner KiCad run and PDF review at 7120e93

On 2026-09-07 the owner uploaded `matrix-review-7120e93.zip` from commit `7120e93d52876e33144678a6729feb112536b4c5`, reporting a clean working tree and a successful KiCad 10.0.6 run.

| Evidence | SHA-256 |
|---|---|
| Uploaded ZIP | `06f64b3160fb608e9988c1df4bac78de4f190fdf0921a1b14e494ba1eda168ae` |
| `coupon-erc.rpt` | `09c26d7c9fa935d96a25780553ae4fcdea9a0486039a6e1624ae6d355a80b9f3` |
| `coupon-matrix.xml` | `0dbd2af4cdc4d1e1b8ed35788de910498e97fe4f35ff129f45af2fe65276bafe` |
| `coupon-schematic.pdf` | `99a6bdc8d492a79e0d8076adf3d35bbd76bd554539b302d39d66058ad6063ba8` |

The actual ERC report covers the root and all four matrix sheets, with zero errors and warnings under the project's configured checks. The uploaded XML was checked again locally: all 256 components, 1,024 pins and 64 nets match the exact matrix contract. This is native connectivity evidence, not a synthetic fixture.

All five PDF pages were rendered and inspected, with enlarged examples of both LED types. Population, pin labels and row/column grouping were correct, but wires ran through the global-label text. The root revision field also extended beyond its allotted title-block space. The six raw library SVG drawing groups matched the previously reviewed exports, and both numbered copies exactly reproduced the review helper's output.

### Presentation correction

For KiCad's horizontal global labels, angle 0 places text to the right of the anchor and angle 180 places it to the left. Cathode labels now use 180 degrees with right justification; anode labels use 0 degrees with left justification. The attached wires therefore approach from the side opposite the text. The revision field is shortened to `A-draft`.

An S-expression comparison against `7120e93` confirmed that the five schematic files differ only in those label angles/justifications and the revision text. Symbol data, references, pin numbers, net names, UUIDs, wire coordinates and label anchor coordinates are unchanged. A source regression check rejects a label facing into its wire.

The corrected revision still needs a fresh KiCad export and visual inspection before PR #3 is merged. No claim of a successful corrected native render is made here. The owner has granted standing permission to merge once applicable checks pass; library PR #2 has already been merged. Independent Gate A review remains required before fabrication.

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
