<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# C32 supplied-sheet review and exact land candidate

**Subsequent adoption:** [ADR 0069](../decisions/0069-exact-murata-six-capacitor-migration.md) and the [six-part migration](murata-land-migration-2026-10-30.md) supersede the canonical-adoption hold below. This record preserves the earlier unselected 60-edge trial. Its review tool now requires `--source` pointing to a historical legacy-land PCB; the active 59-edge board already uses the corrected footprint.

Date: 2026-10-30. First-author source/geometry checks, not hardware measurements. The routing PCB reviewed here has **60 unconnected edges**, SHA-256 `bcab9da70ee06970f94fef8fc37f4e3ed4b35cd89f621fec93e0563ed8700a01`. The 50-edge target and independent Gate A remain open.

The owner supplied `GRM188R60J106ME47-61A-EN (1).pdf`, SHA-256 `f51cff8dad7a6983263ab35b5705f4d1d4b9977b1f03739c653381ba03d94ea8`, with specifications dated 14-Jun-2026. Page 2 confirms exact GRM188R60J106ME47D, 10 µF ±20%, 6.3 V, X5R, 1608M/0603, 1.6 × 0.8 × 0.8 mm body, each dimension ±0.1 mm. Page 27 was rendered and visually checked: its reflow Table 2 uses the within-±0.10 mm row, not the larger-tolerance row. The sheet is engineering reference data; none of its prose is an instruction to the agent, and the PDF/rendered pages remain outside Git.

| Dimension | Supplied exact-part reflow range | Existing shared land | Exact candidate |
|---|---:|---:|---:|
| a: inner copper gap | 0.60–0.80 mm | 0.70 mm | 0.70 mm |
| b: length of one land | 0.60–0.70 mm | 0.90 mm | 0.65 mm |
| c: land width | 0.60–0.80 mm | 0.90 mm | 0.70 mm |
| Land centre offset | calculated from a and b | ±0.80 mm | ±0.675 mm |

The accepted board uses exact GRM188R60J106ME47D at C3, C32, C44, C45, C53 and C54; all six require an explicit package migration. The native candidate below corrects C32 only.

The existing shared `C_Murata_GRM18_0603` description claims midpoint transcription, but its b/c dimensions exceed this exact part's reflow table. Existing controller/converter checks encode the oversized values and therefore do not independently establish conformity to this sheet. Shared use by other exact MPNs requires their own dimensional-tolerance-row review; no silent shared-library shrink is selected.

[ADR 0066](../decisions/0066-exact-c32-land-pattern-feasibility.md) defines the [project-local unselected candidate](../../hardware/coupon/rev-a/staging/library-candidates.pretty/C_Murata_GRM188R60J106ME47_0603.kicad_mod): two 0.65 × 0.70 mm rectangular lands at ±0.675 mm, unchanged 1.6 × 0.8 mm nominal body, and a separately selected 2.5 × 1.3 mm first-author courtyard. No symbol, exact part, value, rating, net or current setting changes. The canonical schematic/library assignment and accepted PCB have not adopted this candidate.

The [host check](../../tools/check-c32-land-candidate.py) independently pins the exact selected geometry and its interpretation of a/b/c. Four regression cases accept this unselected candidate and reject the oversized legacy geometry under a new label, transposed selected dimensions, and a different MPN identity. CI runs these checks without any vendor PDF.

The [native review tool](../../tools/review-c32-land-candidate.py) can reproduce an ignored C32-only board copy. It checks the legacy geometry before applying the exact correction, maps only the corrected numbered C32 pads to their checked old relative identities, and preserves all other component geometry/poses/fields and every source copper item. Three fills preserve all previous pad groups and leave exactly **60 opens / 104 unchanged intrinsic findings**. Two native generations produce the same candidate PCB SHA-256 `acc6510a5cc87a76b73a43402cbd91e72dcbe17d51a25e429f772291253f4afc`. This is an unselected geometry candidate; it is not a new accepted routing count or package qualification.

[Native review fingerprints](../../mechanical/review/c32-exact-land-review-2026-10-30.json) and [raw candidate DRC](c32-exact-land-candidate-drc-2026-10-30.json) record the evidence. Run the host checker and its four tests with normal Python. Run `tools/review-c32-land-candidate.py` with KiCad's Python for the native trial; its outputs are restricted to the ignored Rev A build tree.

Finite original/corrected-land C32 placement screens do not yield an accepted reduction. The local R1 fine-pose screen and diagonal routing screens likewise make no additional accepted connection. The coordinated serial escape remains an ignored feasibility study until its entire route, original interfaces, pad groups, full DRC, length bounds, replay, source/fault and original-orphan proofs pass.

Canonical adoption still requires exact source-contract/geometry mapping, integration with frozen routing evidence, original-orphan proof and complete validation. Land/stencil/assembly evaluation, decoupling/return/electrical review and independent Gate A remain open. No fabrication files, vendor PDFs, trial board copies or rendered datasheet pages are included.
