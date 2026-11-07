<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# USB4505 drawing and candidate-library review

Status: first-author drawing inspection and recovered host validation complete on 2026-09-14. The owner-generated KiCad 10.0.6 exports passed [native rendering review at `bf1627c`](../../../docs/development/usb-connector-review-bf1627c.md). Cutout relief, stack-up/process qualification and independent verification remain pending. This record is not fabrication approval.

## Evidence

The owner supplied the original GCT USB4505 PDF on 2026-09-10 after direct download was blocked. Both pages and an enlarged recommended-layout view were inspected in the prior development session. Drawing revision A2 is dated 2023-12-18. The recorded SHA-256 is `b1ea604d8e579ee60bf3db78fc55a300bc107cb3bdb3ac3e6c881955898b52ad`. [Manufacturer drawing](https://gct.co/files/drawings/usb4505.pdf).

The document is not redistributed here. After the development environment returned on 2026-09-14, the PDF hash was reconfirmed and both pages were rendered at high resolution and inspected again.

## Contact and land transcription

Exact candidate: `USB4505-03-0-A`: 3 microinch gold, without shell spring, tape/reel. Page 2 specifies 1,400 pieces per reel, 24 mm tape and 12 mm pocket pitch.

The component-side recommended layout has 16 mating contacts on 12 solder lands, plus four shell stakes. Four wide lands each receive two same-function contacts. The following proposed project identifiers represent those shared lands without adding differently numbered overlapping copper pads.

Origin: centre of the signal-land row. Positive X points right in the component-side drawing; positive Y points toward the mating mouth. All dimensions are millimetres.

| Proposed pad | Manufacturer contacts | Function | X | Y | Width × height |
|---|---|---|---:|---:|---|
| A1_B12 | A1, B12 | GND | -3.20 | 0 | 0.60 × 1.10 |
| A4_B9 | A4, B9 | VBUS | -2.40 | 0 | 0.60 × 1.10 |
| B8 | B8 | SBU2 | -1.75 | 0 | 0.30 × 1.10 |
| A5 | A5 | CC1 | -1.25 | 0 | 0.30 × 1.10 |
| B7 | B7 | D- | -0.75 | 0 | 0.30 × 1.10 |
| A6 | A6 | D+ | -0.25 | 0 | 0.30 × 1.10 |
| A7 | A7 | D- | +0.25 | 0 | 0.30 × 1.10 |
| B6 | B6 | D+ | +0.75 | 0 | 0.30 × 1.10 |
| A8 | A8 | SBU1 | +1.25 | 0 | 0.30 × 1.10 |
| B5 | B5 | CC2 | +1.75 | 0 | 0.30 × 1.10 |
| B4_A9 | B4, A9 | VBUS | +2.40 | 0 | 0.60 × 1.10 |
| B1_A12 | B1, A12 | GND | +3.20 | 0 | 0.60 × 1.10 |

The land height derives from 5.70 - 4.60 = 1.10. The nominal minimum adjacent signal-land gap is 0.20. These are drawing-derived values, not measurements or board DRC.

A proposed symbol would expose 12 passive land pins plus one shell pin, with four same-number shell pads in the footprint. Validate this representation in native KiCad before circuit capture. Keep CC1 and CC2 separate; join corresponding D+ and D- contacts in the future schematic, connect all VBUS/GND lands and explicitly handle unused SBU contacts.

## Mechanical findings

| Feature | Recorded geometry |
|---|---|
| Rear stakes | Centres (±5.62, 1.15); oval land 1.00 × 1.80; oval slot 0.60 × 1.40 |
| Front stakes | Centres (±5.62, 5.15); oval land 1.00 × 2.20; oval slot 0.60 × 1.80 |
| Rear/front stake spacing | 4.00 |
| Board-edge datum | Y = 6.75, from 5.70 + 1.60 - 0.55 |
| Cutout straight sides | X = ±4.62; width 9.24 |
| Cutout rear nominal datum | Y = 0.55 |
| Recommended board thickness | 0.80 |

The recommended-layout tolerance note is ±0.05 mm. Do not assume that it independently specifies the acceptable finished-board thickness tolerance.

The cutout drawing includes curved reliefs with no dimensioned radii or centres. Do not scale these from a drawing marked “Not to Scale.” Obtain dimensioned manufacturer CAD or clarification before releasing the board outline. A draft footprint may use clearly labelled Dwgs.User datum guides, but must not contain a guessed Edge.Cuts outline.

Plated shell slots are a proposed interpretation of the surrounding solder lands and grounded shell, not an explicit process approval. Confirm plating, finished-slot tolerances and shell solder application with the assembler. The drawing does not specify a separate stencil; full-size signal paste and 0.05 mm mask expansion were provisional local-draft choices, not approved manufacturer requirements. A simplified body rectangle is not sufficient for case interference checks.

## Recovery and verification boundary

GitHub PR #8 was checked on 2026-09-14 at `833a9e5`, when the connector edits had not yet been pushed. The prior worktree was subsequently recovered intact and applied after the documentation checkpoint `28b3f3a`.

The recovered increment contains:

- one 13-pin passive symbol representing the 12 physical signal/power lands plus the shared shell connection;
- one draft footprint with 12 SMT lands, four same-number plated shell slots, a 0.05 mm provisional mask margin and no guessed `Edge.Cuts`;
- a source checker covering exact MPN/library linkage, functions, land/slot geometry, layer treatment, 0.20 mm minimum nominal copper clearance and datum guides;
- fault tests for mirrored positions, swapped CC functions, split shared lands, altered slots and premature `Edge.Cuts`;
- wrapper checks requiring non-empty symbol plus fabrication, copper, paste and mechanical exports.

All 86 host tests passed after recovery. The subsequent owner KiCad 10.0.6 run and first-author visual inspection are recorded in the [native review](../../../docs/development/usb-connector-review-bf1627c.md). That result validates the project-local library loading and rendered geometry, but it is not an assembler process review or independent electrical/mechanical review.

Next implementation steps:

1. Obtain dimensioned cutout relief geometry or manufacturer CAD before adding the board outline.
2. Confirm the plated-slot, mask and stencil process with the chosen assembler and freeze the 0.80 mm coupon stack-up.
3. Resolve the complete USB source-state/input-current design under ADR 0009, then finish power capture. Connector library validation does not close that electrical hold.

Independent Gate A remains required before fabrication. No component substitution or purchase is authorized by this record.
