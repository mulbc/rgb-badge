<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0066: Exact C32 reflow-land correction feasibility

Date: 2026-10-30
Status: Historical C32-only feasibility; canonical six-part adoption is recorded in ADR 0069.

The owner supplied GRM188R60J106ME47-61A-EN (1).pdf, specifications dated
14-Jun-2026, SHA-256 f51cff8dad7a6983263ab35b5705f4d1d4b9977b1f03739c653381ba03d94ea8.
It confirms GRM188R60J106ME47D, 10 µF ±20%, 6.3 V, X5R, 1.6 × 0.8 mm
body with ±0.1 mm dimensional tolerances. Page 27 reflow Table 2 gives inner
land gap a = 0.6–0.8 mm, pad length b = 0.6–0.7 mm and width c = 0.6–0.8 mm.
The drawing was visually checked as well as text-extracted. The vendor PDF is
local reference material and must not be committed.

The present shared C_Murata_GRM18_0603 land has two 0.9 × 0.9 mm pads at
±0.8 mm: calculated a = 0.7 mm, b = 0.9 mm, c = 0.9 mm. Its b/c dimensions
exceed the exact part's reflow table, despite its description claiming a midpoint
transcription. The shared-library checker also encodes the oversized geometry;
a passing old check is not evidence that it matches this new supplied sheet.
Do not shrink the shared footprint for other exact MPNs without reviewing their
own dimensional-tolerance rows.

Permit an ignored C32-only candidate using exact reflow midpoints a = 0.70,
b = 0.65, c = 0.70 mm: two 0.65 × 0.70 mm rectangular lands at ±0.675 mm.
Keep the 1.6 × 0.8 mm fabrication body; use a separately recorded 2.5 × 1.3 mm
first-author courtyard. Preserve exact MPN/value/rating/nets, every original and
accepted copper item, every other component pose/geometry and every completed
pad group. A C32 move remains subject to ADR 0045 and reconnection to its full
old supply/ground groups. Keep widths/clearance and adjacent vias unchanged.

The old relative pad coordinates change under this correction. Any later
canonical adoption requires an explicit independently enforced geometry/identity
mapping, exact library and native rendering evidence, canonical-source/contract
updates, frozen 60-edge retention, unchanged full native baseline, stable replay,
fault/source and original-orphan evidence. Never silently rewrite the frozen
215-edge source or prior source-study evidence. No corrected package or reduced
open count is selected by this feasibility authorization. Land/stencil/assembly,
decoupling and electrical qualification plus independent Gate A remain open.

## Independently checked library candidate

The project-local [candidate](../../hardware/coupon/rev-a/staging/library-candidates.pretty/C_Murata_GRM188R60J106ME47_0603.kicad_mod)
and [host drawing check](../../tools/check-c32-land-candidate.py) pin the exact
midpoint transcription; four regressions reject legacy oversized lands, swapped
selected dimensions and a different part identity.
[Native review](../../tools/review-c32-land-candidate.py) restricts output to
ignored build directories and verifies three stable fills, every source copper
item/group, all poses/fields, explicit numbered-pad/net mapping and the unchanged
104 findings at 60 opens. This is a verified unselected candidate, not a
canonical package migration or a lower accepted board count. See the
[review record](../development/c32-exact-land-review-2026-10-30.md).
