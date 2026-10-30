<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# 3.3 V converter capacitor land audit — first author

**2026-10-30 remaining exact-drawing hold:** GRM187R61A226ME15 at
C40/C41/C46/C47/C48/C49 and GRM219R60J476ME44 at C42/C43 still use the
historical shared lands. Their suffix-free source identities are provisional;
confirm the orderable packaging code explicitly before a purchase BOM. The
checker now describes its actual scope as frozen library identity/geometry,
not conformity to current manufacturer recommendations. Neither its passing
result nor the historical a/b table below closes the drawing hold. A current
search finds indexed January 2025 manufacturer reference sheets, but normal
opens of both official PDF links return 404. The owner has been asked for local
copies; no geometry or part code is changed while awaiting them. Reference
sheet URLs: [GRM187](https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM187R61A226ME15-01A.pdf)
and [GRM219](https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM219R60J476ME44-01A.pdf).
These unavailable files have not been downloaded or visually reviewed in this
continuation. Any later supplied revision must be cached, hashed and checked
directly; do not infer a corrective land pattern from another part's sheet.

**2026-10-30 exact-part adoption:** [ADR 0069](../../../docs/decisions/0069-exact-murata-six-capacitor-migration.md) migrates GRM188R60J106ME47D to its dedicated `C_Murata_GRM188R60J106ME47_0603` footprint at all six affected references. The supplied sheet's Table 2 uses inner gap a = 0.70 mm, ONE-land length b = 0.65 mm and width c = 0.70 mm. The shared GRM18/GRM21 dimensions below remain historical and are not qualified by this correction; other exact MPNs still require their own drawing review.

**2026-10-30 land-pattern review hold:** The [supplied exact-part review](../../../docs/development/c32-exact-land-review-2026-10-30.md) exposes oversized shared GRM18 lands for GRM188R60J106ME47D. In the supplied drawing, a is the inner gap and b is one land length. The historical geometry/label claims below do not establish conformity to that drawing. All exact MPNs sharing these lands require their own drawing review before migration; the new C32-only candidate is unselected. No fabrication approval follows from the older passing checks.

2026-09-30. This checks only the two **provisional exact MPNs** in [ADR 0017](../../../docs/decisions/0017-parallel-3v3-converter-capacitors.md). Two project-local exact-MPN capacitor symbols are staged in the library but unplaced; no PCB has been routed or fabricated. The checker `tools/check-3v3-capacitor-footprints.py` verifies symbol identity, two passive pins and footprint references, plus the actual project-local KiCad pad coordinates, sizes, layers, body drawing and courtyard. Owner KiCad 10.0.6 export/first-author visual review [passed at 8014947](../../../docs/development/3v3-passive-library-review-8014947.md). Assembler DFM and independent Gate A review remain pending.

Manufacturer-authored reference sheets consulted: Murata `GRM187R61A226ME15-01A` (2017 revision, [copy of manufacturer PDF](https://s3.amazonaws.com/snapeda/datasheet/GRM187R61A226ME15J_Murata_Electronics.pdf), page 25) and `GRM219R60J476ME44-01A` ([copy of manufacturer PDF](https://www.mouser.lt/datasheet/2/281/1/GRM219R60J476ME44_01A-1986316.pdf), page 26). Murata's [current product list](https://www.murata.com/-/media/webrenewal/tool/library/common-pdf/dynamic-model/component-list-d-mlcc-2506.ashx?cvid=20250805040419000000&la=en) independently identifies the MPN dimensions and ratings. The reference sheets explicitly direct board-specific land evaluation and use the wording "For only mobile devices" under limited application; confirm whether the intended wearable use is covered by the current approval conditions. Their manufacturer-hosted historic PDF URLs returned 404 on 2026-09-30; the copies are reference-sheet evidence, not an assertion that the recommendations are current approval sheets. Confirm the orderable packaging suffix and current approval drawing before PCBA release.

The Murata reflow diagram labels `a` as copper land length along the chip, `b` as the inner gap and `c` as copper width perpendicular to the chip. All units below are mm. Both parts are two-terminal nonpolar MLCCs; pad 1/2 orientation has no electrical polarity. For the 0603 part the existing project footprint is reused. The new 0805 footprint uses the midpoints of the exact-part GRM21 ±0.20 mm body-tolerance reflow row.

| Exact MPN | Body L × W / height | Murata reflow a, b, c | Project footprint / selected a, b, c | KiCad pad centers and sizes |
|---|---|---|---|---|
| `GRM187R61A226ME15` | 1.6 ±0.2 × 0.8 ±0.2 / 0.7 ±0.1 | a 0.7–0.9, b 0.7–0.8, c 0.8–1.0 | `C_Murata_GRM18_0603`: 0.9, 0.7, 0.9 | x = ±0.8; each 0.9 × 0.9; F.Cu/F.Paste/F.Mask |
| `GRM219R60J476ME44` | 2.0 ±0.2 × 1.25 ±0.2 / 0.85 ±0.1 | a 1.0–1.4, b 0.6–0.8, c 1.2–1.4 | `C_Murata_GRM21_0805`: 1.2, 0.7, 1.3 | x = ±0.95; each 1.2 × 1.3; F.Cu/F.Paste/F.Mask |

The 0805 footprint's F.Fab body is the 2.0 × 1.25 nominal outline. Its F.CrtYd is 3.6 × 2.0, giving ≥0.25 mm to the outer copper and ≥0.275 mm to the largest stated body width. No silk polarity mark, separate solder-mask expansion or custom paste reduction is invented. The 0603 footprint's existing 3.0 × 1.3 courtyard is retained; its pad is at the top of the recommended a range. Component-side routing and panel-break/screw flex need review because Murata cautions against MLCC cracking from board bending. Solder volume and reflow profile require assembler qualification.

This audit establishes staged symbol/footprint identity and land geometry against manufacturer-authored **reference** sheets only. It does not establish the combined bias/temperature/aging capacitance floor, dynamic behavior of two parallel parts, or final placement within the LED badge. The [converter capture contract](3v3-converter-capture-contract.md) tracks those electrical conditions.
