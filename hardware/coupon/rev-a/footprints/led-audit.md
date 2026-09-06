<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Coupon Rev A LED symbol and footprint audit

Status: first-author transcription complete; independent Gate A verification pending; not authorization to fabricate

Retrieval date: 2026-09-06

## Controlled source records

| Exact MPN | Controlled drawing | Document identity | Retrieved SHA-256 |
|---|---|---|---|
| `EAST10105RGBA0` | [Everlight manufacturer datasheet mirrored by Mouser](https://www.mouser.com/datasheet/2/143/EAST10105RGBA0-1709851.pdf) | Release 2015-12-24, issue `DSE-0014497`, Rev. 1 | `f21890e8c38fb37d3dc1d76646b094f6d5626c361fca5c576045a52af5029688` |
| `QBLP1515A-RGB2A` | [QT Brightek manufacturer datasheet](https://www.qt-brightek.com/datasheet/QBLP1515A-RGB2A.pdf) | 2025-12-16, version 1.0 | `7887877eff9113d944502923fdd6771ce375b0ae4007342bdf0522604dee439d` |

The hashes identify the exact PDF files inspected. The PDFs are not redistributed in this repository. A changed upstream hash requires a drawing comparison before source updates.

## Pin and pad transcription

Coordinates below use the footprint's top view, with positive X to the right and positive Y downward as displayed by KiCad. Dimensions are nominal millimetres.

### Everlight `EAST10105RGBA0`

| Pad | Electrical function | Centre X | Centre Y | Copper size |
|---:|---|---:|---:|---:|
| 1 | Common anode | +0.425 | −0.425 | 0.45 × 0.45 |
| 2 | Red cathode | +0.425 | +0.425 | 0.45 × 0.45 |
| 3 | Blue cathode | −0.425 | +0.425 | 0.45 × 0.45 |
| 4 | Green cathode | −0.425 | −0.425 | 0.45 × 0.45 |

- Package: 1.00 × 1.00 mm; height 0.25 ±0.05 mm.
- Manufacturer land-pattern envelope: 1.30 × 1.30 mm.
- The package drawing identifies pad 1 with the anode mark at the upper-right corner in the drawing view.
- The footprint uses the manufacturer pad dimensions without adjustment.

### QT Brightek `QBLP1515A-RGB2A`

| Pad | Electrical function | Centre X | Centre Y | Copper size |
|---:|---|---:|---:|---:|
| 1 | Common anode | +0.700 | +0.400 | 0.60 × 0.40 |
| 2 | Blue cathode | −0.700 | +0.400 | 0.60 × 0.40 |
| 3 | Green cathode | −0.700 | −0.400 | 0.60 × 0.40 |
| 4 | Red cathode | +0.700 | −0.400 | 0.60 × 0.40 |

- Package: 1.55 × 1.50 mm; height 1.00 mm; unspecified package dimensions have ±0.20 mm tolerance.
- Manufacturer land-pattern envelope: 2.00 × 1.20 mm.
- The package drawing places pad 1 at the lower-right corner in the drawing view.
- The footprint uses the manufacturer pad dimensions without adjustment.
- [ADR 0008](../../../../docs/decisions/0008-qblp1515-checkerboard-placement.md) requires alternating 0°/90° placement; rotation is not encoded by changing this footprint.

## Pitch calculation

Assumptions: exact nominal rectangular QBLP1515 pads, 1.95 mm square centre pitch, no mirroring, and no copper or mask expansion.

| Placement | Calculated result |
|---|---:|
| Same orientation in every grid cell | 0.05 mm copper overlap along one axis |
| `(row + column)` even: 0°; odd: 90° | 0.35 mm minimum pad-to-pad copper clearance |

This calculation proves only nominal pad geometry. It does not cover manufacturing tolerances, solder-mask registration, paste behaviour, body clearance, pick-and-place accuracy or optical performance.

## KiCad rendering review

- Owner-reported check at `cccb65c8b1e8d7060252b9af014dd14caf550c5c`: KiCad 10.0.6 on macOS exported both symbols and both footprints, the static audit passed, blank-sheet ERC reported zero violations, and no tracked files changed.
- The four attached SVGs were inspected in the project conversation. The symbol pin labels overlapped, and the combined all-black footprint export obscured the pad numbers. Parsing success was therefore not treated as visual approval or independent engineering review.
- The readability correction removes redundant symbol body text, widens the schematic boxes while retaining pin names/numbers/types and MPN-to-footprint links, and separates numbered fabrication and copper-only exports. The two physical footprint source files are unchanged.
- The corrected files still require an actual KiCad export and visual check. Local wrapper tests use a stub CLI and cannot provide that evidence. See the [macOS review instructions](../../../../docs/development/kicad-macos.md).

## Open verification items

- A second reviewer must independently compare every symbol pin, footprint pad and polarity marker to both controlled drawings.
- Obtain an explicit pin-1 pocket-orientation confirmation for each production reel; the available tape drawings do not label the pocket orientation clearly enough to infer it safely.
- Export and inspect KiCad symbol and footprint SVGs after every library edit.
- Run PCB DRC on the generated 1.95 mm placement, including solder-mask settings.
- Ask the selected assembler to approve paste, mask, courtyard and alternating-rotation handling before ordering.
- Record incoming reel labels, optical bins, lot codes and first-article polarity inspection.
