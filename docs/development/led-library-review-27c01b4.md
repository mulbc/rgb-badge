<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# LED library rendering review at 27c01b4

Status: first-author library/rendering review complete; independent Gate A review pending

## Evidence

The owner ran KiCad 10.0.6 on macOS at commit `27c01b4fb3ddb3a863dc25fdb233b57a9f043403` and uploaded `led-library-review-27c01b4.zip` on 2026-09-06. The terminal transcript reported a successful static audit, six SVG exports, zero blank-sheet ERC violations and a clean working tree. The archive's ERC report records zero errors/warnings and only the blank root sheet.

Archive SHA-256: `8a8deb00438dac0a8090c2dd2ea6b0edf8529f2d3b39d90e54ec53b417815aa8`.

| Original exported SVG | SHA-256 |
|---|---|
| `symbols/EAST10105RGBA0_unit1.svg` | `0ea185e3b0899d63d12b15ac8d6adb3c0bc387d4cbd293982a3637d6901085f6` |
| `symbols/QBLP1515A-RGB2A_unit1.svg` | `57bc8f751a4aaa59212e6f11b8b0a89e9ac1e17d77728e4ac5567d3a106fbce9` |
| `footprints/fabrication/LED_Everlight_EAST10105RGBA0.svg` | `a8ef395dd63e00ee5f37b8a6a7a7b01b0aabe05e71eb6a05a3a8f305499253b3` |
| `footprints/fabrication/LED_QTBrightek_QBLP1515A-RGB2A.svg` | `ea28366960b1ab0234ff44c6f187dc32acd6daae9d301eb89bcd8515b41d1ce7` |
| `footprints/copper/LED_Everlight_EAST10105RGBA0.svg` | `6d6983bb69cd57e18c5e8635a4f74dad2ac058b487463278157be4f2e94ecbd1` |
| `footprints/copper/LED_QTBrightek_QBLP1515A-RGB2A.svg` | `9852406772ff3aa8d4e33436d0cf8f0441780ccd52cd18e81b3269342b1492fc` |

## Findings and resolution

Both symbol drawings were readable. Their exported pin mappings and both copper views' nominal pad sizes/centres matched the [controlled manufacturer drawings and audit](../../hardware/coupon/rev-a/footprints/led-audit.md). The fabrication-label quadrants matched as well, but body strokes still obscured parts of the numbers, particularly Everlight's upper-right pad 1.

The final cleanup adds a separate derived numbered view. `tools/number-footprint-review.py` copies the existing KiCad pad-number paths to the top of the drawing, with a white halo beneath each glyph, and expands the viewing margin by 0.1 mm. It does not infer numbers, move labels, alter the original geometry groups, rewrite raw exports, or modify any symbol/footprint source.

Both derived SVGs below were generated from the uploaded fabrication exports, rendered to PNG for inspection and visually checked. All four numbers are readable in each. XML comparison confirmed that every original geometry group is preserved unchanged. The source SHA-256 is also embedded in each derived SVG.

Helper SHA-256 used for these examples: `4cf420ce2a6efeb76c216aebdbada18775fa151bdd19fc450f22a83621093596`.

| Unrotated top view | Upper-left | Upper-right | Lower-left | Lower-right |
|---|---|---|---|---|
| Everlight | 4 / green | 1 / anode | 3 / blue | 2 / red |
| QT Brightek | 3 / green | 4 / red | 2 / blue | 1 / anode |

### Everlight EAST10105RGBA0

![Derived numbered Everlight review](led-library-review-27c01b4/everlight-numbered.svg)

### QT Brightek QBLP1515A-RGB2A

![Derived numbered QT Brightek review](led-library-review-27c01b4/qt-brightek-numbered.svg)

These are review illustrations, not manufacturing drawings. White halos mask small portions of outline strokes for readability; inspect raw KiCad views and canonical sources for geometry.

## Verification limits

- The real KiCad export/ERC evidence is the owner's `27c01b4` run. No local KiCad installation was available for the final export-wrapper change.
- Twelve local wrapper/SVG-helper regression tests passed, including failure propagation, required outputs, source preservation and rejected ambiguous label structures. Stub outputs are never evidence of a real KiCad render or electrical validation.
- The successful first-author review supports starting circuit capture. ERC on the blank sheet does not validate a circuit. Reel orientation, paste/mask DFM, PCB DRC, electrical design and independent Gate A verification remain open.
