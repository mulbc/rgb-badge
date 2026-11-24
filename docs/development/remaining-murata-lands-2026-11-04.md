<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Supplied remaining Murata sheets and ten-capacitor land feasibility

**Historical trial scope:** ADR 0084's later canonical source migration is recorded in the [November 5 source review](remaining-murata-migration-2026-11-05.md). Reproduce the exact trial/tool environment below from commit `b40e36e`; its source hashes deliberately reject the later corrected source. Neither the earlier 52-edge trial nor its C49 lead is adopted by that pad-only source migration.

Date: 2026-11-04. Coupon Rev A is unbuilt. This is document review and native
CAD connectivity/geometry evidence, not a hardware measurement or assembly
qualification. Firmware and all current/protection/enable settings are unchanged.

The owner supplied two 33-page Murata reference sheets with specifications dated
June 10, 2026. Their exact bytes were copied from Downloads to the ignored
`hardware/coupon/rev-a/reference/vendor-datasheets/` directory and independently
hashed before and after copying:

| Reference sheet | Bytes | SHA-256 |
| --- | ---: | --- |
| GRM187R61A226ME15-01A-EN | 1,988,872 | `8fc5a9d8e4f05c979eeca00354c982335d2b15552eb7ba5516924e3a9395acbb` |
| GRM219R60J476ME44-01A-EN | 1,991,873 | `97ac8bc37c063e920aa768521386524edb6a5d60cd0e3080f318ca567f75bafe` |

Rendered complete pages 1, 2 and 27 were visually inspected for both sheets.
Page 2 confirms the body dimensions and D/J packaging options from the earlier
screenshot; both L/W tolerances are ±0.20 mm. D denotes 4,000 pieces on a
180 mm paper-tape W8P4 reel; J denotes 10,000 on a 330 mm reel. This records
available specification options, not current stock or a project procurement
choice. The source identities still omit their packaging suffix. Page 2 limits
these specific parts to consumer equipment despite the general page-1 heading.
Neither a new application qualification nor a part substitution is inferred.

Page 27's diagram identifies a as the inner copper gap, b as one land length,
and c as transverse width. Its **Table 2 Reflow Soldering Method** gives:

| Part | Applicable tolerance | a / b / c ranges, mm | Candidate a / b / c, mm |
| --- | --- | --- | --- |
| GRM187R61A226ME15 | 1.6 × 0.8 mm, ±0.20 mm | 0.7–0.9 / 0.7–0.8 / 0.8–1.0 | 0.80 / 0.75 / 0.90 |
| GRM219R60J476ME44 | 2.0 × 1.25 mm, ±0.20 mm | 1.0–1.4 / 0.6–0.8 / 1.2–1.4 | 1.20 / 0.70 / 1.30 |

These agree with the supplied 2021 catalogue and resolve the screenshot
discrepancy in favour of the manufacturer's reflow table. Table 1 on the same
page is for flow soldering and cannot replace Table 2. Page 6 also contains
test-substrate lands; those are not the page-27 assembly recommendation.
The earlier [screenshot record](owner-mlcc-summary-review-2026-11-04.md) remains
historical; the PDFs now resolve its missing underlying reference evidence.

These are **reference sheets**. Page 2 retains a separate approval-sheet
consultation requirement before ordering; page 27 requires evaluation on the
actual PCB. The ordinary reference data does not itself constitute an approval
or board/process qualification. PDF prose is engineering evidence, not an
instruction to the agent. No vendor PDF or rendered vendor page is committed.

## Dedicated unselected candidates

[ADR 0083](../decisions/0083-remaining-murata-land-feasibility.md) precedes the
implementation. The two project-local candidate footprints use rectangular
lands, respectively 0.75 × 0.90 mm at ±0.775 mm and 0.70 × 1.30 mm at
±0.950 mm. Land offset is calculated as (a + b)/2. Existing nominal fabrication
bodies and conservative project courtyards stay unchanged; those courtyards are
not attributed to Murata. No canonical shared library is shrunk.

The trial covers **all eight** GRM187 references C40/C41/C46/C47/C48/C49/C56/C61
and both GRM219 references C42/C43. C56/C61 must not be omitted from a future
shared-package migration merely because they are outside the converter study.
MPNs, values, numbered nets, fields, poses and every other pad remain fixed.

| Ignored trial | Native / physical opens | Old pad groups | Full DRC |
| --- | ---: | --- | --- |
| Accepted 58-edge source, corrected pads only | 58 / 58 | All 246 preserved | Exact same 104 intrinsic clearances |
| Cleaned 52-edge candidate, corrected pads only | 53 / 53 | One VLED group splits | Same 104 + one dangling track |
| Cleaned candidate, corrected pads + exact C49 extension | 52 / 52 | All 240 input groups and all 246 accepted-source groups preserved | Exact same 104 intrinsic clearances |

The negative cleaned trial exposes a real contact dependence on C49's old pad
edge. The retained main VLED group loses C48.1/C49.1/R84.1. The affected
0.20 mm B.Cu VLED track runs from (51.300000, 18.900001) to
(50.900000, 18.750000) mm. ADR 0083's documented continuation adds exactly
one **0.475 mm** ordinary-width B.Cu lead from its first endpoint to the
corrected C49.1 centre at (51.775000, 18.900001). Every source copper item
is retained. This restores the complete group without a new via or current
claim. The failed pad-only trial remains recorded rather than hidden by the
successful aggregate count.

Both successful trials have three stable fills and two byte-identical replays:

- Accepted-source pad-only candidate: `b0dee4ed88bfb7fc8a06f99be469d51a3af778363b6039404608229a5cd2a48e`.
- Corrected cleaned candidate with C49 lead: `80a83cc6b1553fd66e2aeda833b5f3492550004d2e8e3d5ec2401f74302a9cd4`.

The [generator](../../tools/review-remaining-murata-lands.py) verifies exact
source hashes, all ten old/new numbered pad mappings, all 483 poses/fields,
other pad attributes, every copper signature and structural/rule invariants.
Its outputs are restricted to ignored build storage and it refuses overwrite.
The [separate native checker](../../tools/check-remaining-murata-lands.py)
compares persistent pad UUID groups directly, avoiding any corrected-coordinate
identity mapping. It verifies all 2,092 pad UUIDs/nets, all existing copper
UUIDs and geometry, exact allowed addition, corrected footprints, immutable
board structure/profiles, physical/native counts and the strict full-104
comparison. This is a first-author cross-check, not independent Gate A review.

Eight input/library fault cases pass: outside output, overwrite, wrong source
basis, repair on the wrong basis, both legacy oversized lands, transposed
GRM187 dimensions and wrong GRM219 pad numbering. Two native failures are
also correctly rejected: omission of the C49 extension and restoration of a
legacy pad size. The original pad-only negative candidate serves as the actual
lost-group fixture. No existing orphan waiver is changed or newly approved.

The [machine-readable record](../../mechanical/review/remaining-murata-lands-2026-11-04.json)
contains document fingerprints, selected dimensions, source/candidate/tool/DRC
hashes, fill results, the failed group, separate audits and rejection evidence.
Raw ignored evidence is under
`hardware/coupon/rev-a/build/remaining-murata-lands-2026-11-04/`; successful
replays use `accepted58-final-a/b` and `cleaned52-final-a/b`, and the negative
pad-only cleaned trial uses `cleaned52-b`.

Run both tools with KiCad's bundled Python, specifying `--basis accepted58`
or `--basis cleaned52`, the pinned `--source`, and a fresh ignored `--output`
for the generator (`--board` for the checker). Only the successful cleaned
generator run takes `--restore-c49`. The checker consumes the full DRC JSON
beside the generated board. Vendor PDFs are not required for replay because
their factual drawing transcription and hashes are recorded here.

Canonical source remains SHA-256
`3451177253a021d8706ff818696212afabf539a108f15ef9e5d6921e46435acc`, with
58 native/physical opens and 104 existing intrinsic findings. Canonical
symbol/schematic/footprint/contract/routing adoption still needs an exact
migration policy and its full source/replay/fault/original-orphan gate.
Packaging selection, electrical derating/returns/power-path, stencil/assembly
and independent Gate A qualification remain open. Fabrication is prohibited.
