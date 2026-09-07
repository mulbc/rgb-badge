<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0008: Preserve the QBLP1515 land pattern with checkerboard rotation

- Status: Accepted
- Date: 2026-09-06

## Context

Coupon Rev A places `QBLP1515A-RGB2A` LEDs on a 1.95 mm square pixel grid. Page 7 of the QT Brightek version 1.0 datasheet specifies four 0.60 × 0.40 mm rectangular solder pads. Their centres are 1.40 mm apart horizontally and 0.80 mm apart vertically, producing a nominal 2.00 × 1.20 mm copper envelope.

If every LED has the same orientation, the 2.00 mm envelope overlaps the neighbouring footprint by 0.05 mm along one grid axis. Shrinking or moving the pads would depart from the manufacturer land pattern and reduce soldering margin.

A geometric calculation using the nominal rectangular pad geometry and 1.95 mm centre spacing found that alternating unmodified footprints by 0 degrees and 90 degrees eliminates the overlap. The calculated minimum pad-to-pad copper clearance is 0.35 mm. This is a geometry calculation, not a DFM approval or assembly measurement.

## Decision

- Keep the manufacturer-recommended 0.60 × 0.40 mm QBLP1515 pad geometry and pad centres unchanged.
- Place QBLP1515 LEDs in columns 8–15 with rotation determined from zero-based coordinates: even `(row + column)` uses 0 degrees and odd `(row + column)` uses 90 degrees.
- Do not mirror any LED footprint.
- Generate and check the placement pattern rather than rotating 128 parts manually.
- Include a human-readable pin-1/rotation plot with the assembly package.
- At Gate B, compare neighbouring QBLP1515 pixels for visible colour or uniformity effects caused by alternating the internal RGB-die orientation.

## Consequences

- The copper pads retain the manufacturer's soldering recommendation while meeting the 1.95 mm pitch geometrically.
- The QBLP1515 half has two component rotations, increasing placement and AOI complexity.
- A diffuser may make the alternating die orientation invisible, but that is an unverified hypothesis until coupon testing.
- PCB DRC, paste/mask review, assembler DFM and measured solder yield remain required before this approach can be used in the final badge.
- If the orientation pattern is optically visible or produces unacceptable assembly yield, the QBLP1515 candidate is rejected or this ADR is superseded.

## Evidence

- [QT Brightek QBLP1515A-RGB2A datasheet, version 1.0, 2025-12-16](https://www.qt-brightek.com/datasheet/QBLP1515A-RGB2A.pdf)
- [Coupon Rev A LED footprint audit](../../hardware/coupon/rev-a/footprints/led-audit.md)
