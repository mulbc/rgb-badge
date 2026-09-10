<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Power-library correction review: 3638b1d

Status: first-author native review of the copper, stencil and symbol-heading corrections passed. This closes findings 1–3 in the [previous review](power-library-review-c84f8ce.md). It does not close the complete power/input increment or authorize fabrication.

## Native evidence

The owner supplied the KiCad 10.0.6 output for commit `3638b1d577c5aa740ee0b76a829a8e4140f898ef`. The transcript ends after the successful wrapper result, with no reported tracked changes. AppleDouble metadata was ignored.

| File | SHA-256 |
|---|---|
| `power-library-review-3638b1d.zip` | `26b8a116a4920bad23199518e446f792973d77451f611dbac137e1bff3a96644` |
| `Pasted text(7).txt` | `0384d231f738365da3239967d42e2244b19c95955d45e7070c2be573b35b7e29` |
| `coupon-erc.rpt` | `b4c18df9103cac474d4fbbd961848dae60966e1056a1f518951fa3486c69148d` |
| `coupon-matrix.xml` | `9861105c71c29e984b4838a8a74cbacdaa3a2cd07edb3766f3c9617aac102c3e` |
| `coupon-schematic.pdf` | `aa2aa8e6c7ae83e7204907e62f9bf10b6e3378773718e102e9692830705dd3ed` |

The strict report checker was rerun against the supplied ERC: zero errors and exactly the two temporary isolated `USB_D-` / `USB_D+` warnings. The supplied XML passed the complete captured-circuit contract: 356 PCB items / 1,360 logical pins. These components are still matrix, driver, rows and controller; the new power libraries are not instantiated in a power circuit.

## Visual disposition

The corrected BQ25616J fabrication/copper/paste views, TPS63020 paste view and four corrected symbol views were rendered and inspected. The BQ copper view now visibly separates all 24 perimeter lands from the central ground land; its paste view shows reduced signal openings and four separate thermal openings. The TPS63020 thermal paste has four compound openings. The BQ25616J, SN74LVC1G04, INA232 and TUSB320LAI headings clear the upward pins. The dimensions and remaining assembler considerations are controlled in the [power-library audit](../../hardware/coupon/rev-a/power-library-audit.md).

Comparing the 88 raw SVG exports against `c84f8ce`, after removing only the SVG title containing its timestamp, yields exactly eight changed files: four symbols, three BQ views and the TPS63020 paste view. The other 80 raw SVGs are identical. Derived numbered LED views are not part of this byte comparison.

The eight-page PDF was present; page 7 was rendered and inspected specifically for the outstanding R37/ROW_SEL_15 title-block collision. That known issue remains visible in this supplied run. This correction review does not reclassify the existing schematic readability findings as passed.

## Follow-on source repair

After accepting the supplied library corrections, the row generator and canonical sheet were updated together: the four stage bands now use 63.50 mm vertical spacing instead of 71.12 mm. The final band's lower resistor centre moves from y=378.46 mm to y=355.60 mm, leaving room above the title block. Matrix/driver/row scope notes now acknowledge the captured controller and identify power/VLED interlock as pending. The driver note points to the existing GPIO10–14 assignment.

All 75 host tests pass after this repair. An additional before/after parsed comparison confirms identical row circuit structure after removing coordinates and free text/title annotations. This is source evidence, not native ERC of the moved circuit. The next native run must confirm its connections and PDF layout before this finding can close. No component library geometry changed after the accepted `3638b1d` export.

Remaining work includes the controlled USB-C connector drawing, exact remaining interfaces/passives, full power/input capture and hardware VLED inhibition, native validation of the complete schematic, preliminary PCB layout and independent Gate A. PR #8 remains draft. A fresh attempt to retrieve the GCT connector page on 2026-09-10 returned HTTP 403; no connector footprint was inferred from a product photograph or a similar part.
