<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Row-selection library rendering review at 0c71860

Status: first-author library/rendering review complete; row circuit capture may start; independent Gate A review pending

## Evidence

The owner ran KiCad 10.0.6 on macOS arm64 at commit `0c718607aa772f32484dd3d1a8a419ad7fdd14df` and uploaded `row-library-review-0c71860.zip` on 2026-09-08. The terminal transcript reported successful static library, matrix and driver checks; all twelve symbols and nine footprints exported; ERC reported zero violations; both native XML validators passed; the six-page schematic PDF exported; and `git status --short` produced no tracked changes.

Archive SHA-256: `5e111012d30e528b6870afc614538712975da1fba414bcb4836fff42b97f787e`.

| Evidence | SHA-256 |
|---|---|
| `coupon-erc.rpt` | `3b3c3e4af80f18999679f23f9a2422896a719d4ae26963205f922bf1c4f245d7` |
| `coupon-matrix.xml` | `c3a6f1606e3c0d8e948eaeac807bee6cc5fcbf05238a2523123fd042e41baa08` |
| `coupon-schematic.pdf` | `d021fecd36c3726195dcaa06840c53bb0b081002bdd712b3abc589aa137c620e` |
| `symbols/74HC4514PW,118_unit1.svg` | `d78a9c7da441c8162a6d9fb70cc3761f8078343a93d75c1b5abfff56644a340b` |
| `symbols/DMP2066LSN-7_unit1.svg` | `227cdf3afb648d1485266fa98ee669d9aa7fe4b4e6c79e2140675d5bd8ef6783` |
| `symbols/2N7002K-7_unit1.svg` | `7c3ac586ad411f6a2b2e49740a77665c9be11c65e2fc151c19e34f33d7bb82f1` |

The archive also contains macOS `__MACOSX` resource-fork entries. Those packaging artefacts were ignored; the actual KiCad outputs above were extracted and checked.

## Electrical and visual findings

The ERC report contains **0 errors, 0 warnings and 0 ERC messages**. Its four ignored categories are unchanged: global-label uniqueness, four-way junctions, SPICE models and footprint filters. Both validators passed against the uploaded XML: 256 LEDs / 1,024 LED pins and 264 PCB items / 1,094 total physical pins. These counts correctly remain at the matrix-plus-driver milestone because the row circuit is not captured yet.

The native SVGs were rendered on a white background and inspected at full resolution:

- `74HC4514PW,118` shows VCC pin 24, GND pin 12, A0/A1/A2/A3 pins 2/3/21/22, LE pin 1, an inversion bubble on E pin 23, and all sixteen separately numbered outputs. The non-sequential Q pin order matches the Nexperia datasheet and the controlled audit.
- Both MOSFET symbols visibly map gate to pin 1, source to pin 2 and drain to pin 3. The exact MPN field distinguishes the P-channel `DMP2066LSN-7` from the N-channel `2N7002K-7`.
- The TSSOP top view numbers pins 1–12 down the left and 13–24 up the right. Its fabrication view has both a chamfer and a pin-1 dot. Copper and paste views show 24 separate lands.
- The SC-59 and SOT23 fabrication views place the pin-1 mark next to the lower-left gate pad. Their copper and paste views each show three separate lands in the audited 1/2/3 arrangement.
- References overlap some package outlines in the automated fabrication renders, as expected for unplaced footprint fields. They do not hide the pin map or pin-1 markers and will be positioned during PCB layout.

The matching copper/paste SVG hashes for each package are expected: these simple footprints use one paste aperture matching each copper land. Solder-mask geometry is recorded in the canonical footprint checks and remains subject to assembler DFM.

## Disposition and limits

This native run closes the first-author rendering gate for the row-selection libraries. It authorizes schematic capture of U2, its decoupling/defaults and the sixteen level-shifted row stages. The acceptance commit changes documentation only; no KiCad library geometry or electrical source changed after the checked commit, so another owner run is not required for this record.

It does **not** approve fabrication. The IPC-derived decoder land pattern still requires assembler DFM and independent Gate A comparison. The 2N7002K's lightly loaded 3.3 V use, decoder timing, MOSFET switching overlap and ghosting require review and coupon measurements. The future power circuit must keep VLED disabled in hardware through boot, reset and rail sequencing; the decoder enable pull-up alone is not a startup interlock.
