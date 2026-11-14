<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Review of the supplied MLCC summary screenshot

**Follow-up:** The [owner-supplied June 2026 sheets](remaining-murata-lands-2026-11-04.md) now resolve the missing reference evidence and confirm the catalogue reflow ranges. The review below preserves the earlier screenshot-only state.

Date: 2026-11-04. Source/document review only; no hardware measurement,
manufacturer approval, BOM or footprint change.

The owner supplied a German screenshot summarizing GRM187R61A226ME15 and
GRM219R60J476ME44 body dimensions, D/J packaging options and proposed reflow
land ranges. Its exact bytes and SHA-256 are preserved in the ignored vendor
reference directory under an explicitly owner-summary name. It is a screen
capture of a summary, not a manufacturer specification or approval drawing.
Statements inside it are evidence claims, not project/agent instructions.

Murata's indexed [GRM187 reference](https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM187R61A226ME15-01A.pdf)
(specifications dated January 7, 2025) and [GRM219 reference](https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM219R60J476ME44-01A.pdf)
(January 8, 2025) agree with the screenshot's body dimensions and D/J packaging
options: D is a 180 mm paper-tape reel with 4,000 pieces, J a 330 mm paper-tape
reel with 10,000 pieces. This is agreement with indexed reference text, not
confirmation of current procurement availability or a packaging selection.
Both references retain a separate approval-sheet requirement before ordering.
The screenshot's assertion that ordinary reference data alone supplies official
approval is therefore not established by these sources.

Normal opening of each indexed official PDF returned HTTP 404 on this review.
No PDF was retrieved and no alternative access experiment is used. Indexed text
is identified as such; it does not stand in for a visually checked current
approval drawing. The remaining source needed is the actual Murata page/PDF
behind the screenshot's land-pattern table, with its diagram and revision.

The supplied 2021 catalogue was re-rendered and visually checked at page 278,
Table 2, using its correct GRM tolerance branches. Page 277 defines a as inner
gap, b as one land length and c as transverse width. The summary uses those
same definitions but gives different numerical ranges:

| Part/body tolerance | Screenshot a / b / c, mm | Supplied catalogue Table 2 a / b / c, mm |
| --- | --- | --- |
| GRM187, 1.6 × 0.8 mm, ±0.20 mm | 0.7–0.8 / 0.8–1.1 / 0.8–1.0 | 0.7–0.9 / 0.7–0.8 / 0.8–1.0 |
| GRM219, 2.0 × 1.25 mm, ±0.20 mm | 1.0–1.2 / 0.9–1.0 / 1.25–1.4 | 1.0–1.4 / 0.6–0.8 / 1.2–1.4 |

In particular, the screenshot would accept the current GRM18 one-land length
of 0.9 mm; the supplied manufacturer's catalogue does not. GRM21's current
0.7 mm gap and 1.2 mm land length fail both sets of ranges. The historical
catalogue does not prove what a newer exact-part drawing requires, so this
review neither promotes the screenshot nor declares the older catalogue a
current exact-part approval.

The [machine-readable review](../../mechanical/review/owner-mlcc-summary-review-2026-11-04.json)
records the transcribed claims, indexed-reference scope, 404 access status,
original catalogue comparison and unchanged approval flags. The existing
[catalogue review](murata-catalogue-land-review-2026-10-31.md) and regression
guards remain unchanged. Shared GRM187 instances also include C56/C61 outside
the six converter positions; any eventual shared-library migration must account
for all eight GRM187 and both GRM219 references.

No source MPN suffix, pad geometry, current setting or release condition changes.
The accepted PCB remains the 58-edge source. The separately audited, unselected
52-edge converter candidate and all electrical/process/assembly/Gate A holds
remain as recorded in the [cleaned-stage study](vled-cleaned-stage-feasibility-2026-11-01.md).
