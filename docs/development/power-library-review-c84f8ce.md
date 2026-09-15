<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Power-library native review: c84f8ce

Disposition: **rejected pending corrections and a new native export**. The owner's KiCad run completed correctly; the design errors described below are first-author transcription/review errors, not an owner setup problem. PR #8 remains draft and is not eligible to merge or fabricate.

Follow-up: corrections to findings 1–3 passed native review at `3638b1d`; see the [correction record](power-library-review-3638b1d.md). Finding 4 passed [native confirmation at `91ef697`](layout-review-91ef697.md). The disposition above records the original run.

## Evidence

The owner ran KiCad 10.0.6 at `c84f8ce2c07dfe9080a3c3e7fd757e721ac01882`, supplied the complete output archive and transcript, and reported no tracked changes. AppleDouble metadata was ignored.

| Supplied evidence | SHA-256 |
|---|---|
| `power-library-review-c84f8ce.zip` | `1c537050874c7b32db3c4ac49917683501d4aea8ab03a94a3b6ee49b055607f6` |
| `Pasted text(6).txt` | `497207203ade80c3f610636de53d2925fe6438be04201c6ac45af686ec068deb` |
| `coupon-erc.rpt` | `d794707b89361ccabdf676c89e295fd64b350cbab8c1f9abac4d7d3c0efa5cd2` |
| `coupon-matrix.xml` | `e9fe5dba2b00c857dc6019f63bc6ddc33512bea3e3b6dfd3869904acc51bab8d` |
| `coupon-schematic.pdf` | `e33b4e89369f2bbefc7474d1e6cfad8022f5c6f7756cec19f53bae6280652677` |

The strict ERC report checker and complete controller netlist checker were rerun against the uploaded files. They passed 0 errors plus exactly the two permitted isolated `USB_D-` / `USB_D+` warnings, and 356 PCB items / 1,360 logical pins. Power components are library-only: these results do not validate their uncaptured circuits or physical copper. The archive contains 28 symbol exports, 20 footprints in each of three raw views and two numbered LED review copies.

## Findings and source corrections

All eight schematic pages and the nine new power symbols/eight new footprint sets were rendered and inspected. Relevant TI package drawings were reopened for the charger and LED converter; their source URLs and SHA-256 values remain in the [power-library audit](../../hardware/coupon/rev-a/power-library-audit.md).

1. **BQ25616J: exposed ground land shorted to all 24 signal lands.** The old 3.1 mm square pad reached every signal land's inner edge. TI thermal drawing 4206249-5/P specifies 2.70 ±0.10 mm, and land drawing 4211120-3/D uses 3.1 mm for the opening between opposing signal lands. Corrected the central land to 2.7 mm, restoring 0.20 mm copper clearance. Corrected signal paste to 0.80 × 0.23 mm and mask margin to 0.07 mm; removed corner silkscreen crossing signal lands. Capsule-ended board lands remain a documented shape difference from TI's rounded-inner/square-outer illustration, pending assembler review.
2. **TPS63020: incorrect central stencil dimensions and opening count.** TI 4210895-2/E specifies central rectangles 1.25 × 0.66 mm at y = ±0.46 mm, not 1.25 × 0.46 mm at y = ±0.33 mm. Corrected the dimensions/positions and used rectangular thermal-paste primitives. The twelve primitives join into four compound openings. Nominal paste-to-thermal-copper area is now 81.14%; the previous claim of 81% was not supported by the old geometry.
3. **Four power-symbol headings overlapped upward pins.** Moved Reference/Value fields above BQ25616J, SN74LVC1G04, INA232 and TUSB320LAI pins. Pin names, numbers, electrical types and coordinates are unchanged.
4. **Existing schematic readability debt remains.** R37 / `ROW_SEL_15` on page 7 crowds/crosses the upper title-block boundary. This was missed by the earlier row/controller visual pass. Matrix/driver/row annotations still contain pre-controller scope text, already noted in the controller review. Repair both before the complete power/input increment merges, and verify the resulting native PDF. This library correction does not claim those pages are visually accepted.

## Regression checks and next gate

The corrected source passes 75 host tests. New regression coverage rejects the original charger short with a geometry check independent of the expected-dimension table, rejects touching/overlapping distinct pad numbers, allows connected same-number thermal pieces, rejects the old four heading positions, and checks signal paste/mask settings. DSJ stencil positions/dimensions and nominal coverage are also checked. The original bad charger geometry was reproduced and rejected before correction.

These are source-level checks, including stubbed CLI workflow tests, not a native rerun or PCB DRC. A fresh owner KiCad export of the corrected source is required before closing the library-render gate. Keep the USB-C connector drawing, remaining parts, full power/input capture, stale page annotations, row title-block collision, assembler stencil review and independent Gate A open. No PCB or battery order is authorized by this record.
