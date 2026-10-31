<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Supplied Murata catalogue: remaining converter land findings

Date: 2026-10-31. Coupon Rev A is unbuilt. This is a first-author document and
source-geometry review, not hardware or assembly evidence. No firmware, current,
part, footprint or PCB geometry is changed.

The supplied `490_Chip_Multilayer_CAT2021_MLCC.pdf` and
`Chip_Multilayer_CAT2021_MLCC.pdf` are byte-identical: 20,196,532 bytes,
SHA-256 `40827b0048b9af98017b011f5497ee063e5c4382c2d9eef3d95b5e8141530bb4`.
Both original filenames and bytes are preserved in the ignored vendor-reference
cache. Neither the PDFs nor rendered pages are committed. The document is the
287-page Murata C02E catalogue dated January 18, 2021; page 2 dates its product
specifications to November 2020. Document content supplies engineering data,
not agent instructions.

Rendered pages 277–278 were visually checked. The diagram labels **a as the
inner copper gap, b as one copper land length, and c as transverse land width**.
Table 2 is for reflow; the flow-soldering table on page 277 is a different table.
GRM187R61A226ME15# and GRM219R60J476ME44# appear on pages 107 and 109. The
catalogue is historical family guidance, not the current exact-part approval
sheets requested earlier. Its notice retains a board-specific land evaluation
and product/approval specification requirement before ordering.

| Current source | Measured a / b / c, mm | Catalogue comparison |
|---|---|---|
| GRM187R61A226ME15, shared GRM18 land, C40/C41/C46–C49 | 0.70 / 0.90 / 0.90 | One-land length exceeds both listed size-18 reflow rows; their b maxima are 0.70 and 0.80 mm. |
| GRM219R60J476ME44, shared GRM21 land, C42/C43 | 0.70 / 1.20 / 1.30 | Inner gap is below every listed GRM size-21 row and land length exceeds every row; a is at least 1.0 mm and b at most 0.8 mm. |

Both part-list entries carry Mo and D1 symbols. Page 4 describes the mobile
category, including watches among its examples, and discusses reference lifetime
estimation. D1 describes the durability-test voltage condition; it is not a
50% operating-voltage rule. No badge lifetime or combined bias/temperature/aging
capacitance guarantee is inferred from these catalogue annotations.

Thus the historical audit's a/b interpretation is independently contradicted
by this supplied catalogue. The present lands match neither relevant family
row, regardless of which listed body-tolerance branch is ultimately verified.
This finding does not determine the exact correct land for either orderable
part. Source identities still omit the packaging suffix, and the current exact
body/termination drawing, application restrictions, assembly process and
combined electrical derating remain unqualified. No shared-library shrink or
part substitution is adopted from generic catalogue dimensions.

The [read-only comparison](../../tools/review-murata-catalogue-lands.py) derives
a/b/c from the actual KiCad pad coordinates and sizes, records every relevant
family/tolerance row and the eight current references, and keeps approval and
fabrication flags false. The [machine-readable review](../../mechanical/review/murata-catalogue-reflow-review-2026-10-31.json)
records the results. Four regression checks guard the observed GRM18 and GRM21
label inversion, distinguish the already corrected GRM188 fine-tolerance row,
and prohibit family-catalogue evidence from granting exact-part approval.
They run in source-only CI without KiCad or vendor PDFs.

Run `python3 tools/review-murata-catalogue-lands.py --verify-report
mechanical/review/murata-catalogue-reflow-review-2026-10-31.json`. Optional
`--vendor-pdf PATH` verifies the supplied catalogue bytes. JSON output is
restricted to ignored build storage. The existing historical library checker
continues to freeze geometry without claiming manufacturer conformity.

The accepted PCB remains SHA-256
`3451177253a021d8706ff818696212afabf539a108f15ef9e5d6921e46435acc`, with 58
native/physical opens and 104 unresolved intrinsic findings. The six exact
GRM188 migrations under ADR 0069 are unchanged. The local converter floorplan,
current exact-part capacitor drawings/order codes, electrical/thermal/process
qualification and independent Gate A remain open; fabrication is prohibited.
