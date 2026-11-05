<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0084: Remaining ten-capacitor source land migration

Date: 2026-11-05
Status: Accepted for canonical source and the exact 58-edge pad-only migration; hardware qualification remains open.

Continue ADR 0083's verified manufacturer reference transcription and successful
accepted-source pad-only trial. Adopt dedicated project-local GRM187 and GRM219
footprints at exactly C40/C41/C46–C49/C56/C61 and C42/C43 respectively.
Use the checked midpoint lands: 0.75 × 0.90 mm at ±0.775 mm, and
0.70 × 1.30 mm at ±0.950 mm. Preserve conservative source courtyards and
nominal fabrication bodies. Preserve exact source MPN stems, packaging-selection
holds, values, pins/nets, fields, poses, every existing copper item, zones,
profiles, rules and current/protection/enable settings. No copper is added or
retired in this transaction. The C49 lead belongs only to the still-unselected
cleaned converter candidate and is not adopted here.

Update canonical library symbols, their embedded/placed schematic assignments,
deterministic schematic/routing generators, source checkers and the fresh native
XML contract together. Keep legacy shared footprints unchanged for historical
replay; freeze the entire preceding 58-edge plan and canonical contract before
editing. Preserve earlier native sources, plans and evidence. Reconciliation
of a historical board must explicitly report its legacy assignments rather than
claiming corrected geometry. Add a separate exact migration/identity policy;
do not broaden or rewrite ADR 0069's six-part policy or earlier waivers.

Map only verified corrected numbered pads to their old reference coordinates
for historical comparisons. Check exact full geometry, numbered nets and all
other pad attributes before normalization. Independently compare the preceding
58-edge board using persistent UUID pad groups, all copper/poses/fields and
unchanged structural/rule data. Require all 246 old physical groups preserved,
58 native/physical opens, exact unchanged full 104 intrinsic findings, three
stable fills, deterministic replay, native XML/ERC and visual library/source
review, source-only/native fault checks and restoration of the three original
retired orphan vias. Do not promote partial acceptance.

The existing routing manifest's physical-open field says 59 although the latest
native evidence says 58. Refresh it to the independently verified value as part
of the new manifest; this is metadata correction, not another routed join.
Regenerate the provisional firmware board inventory only for source traceability;
firmware behavior and pins do not change.

This source geometry correction is not a part/order approval, electrical or
assembly qualification, converter-layout adoption or fabrication release. The
52-edge candidate, L1/U36 locality, the routing target, current/power/thermal/
return/process/fit qualification and independent Gate A remain open.

## Selection evidence

The [source review](../development/remaining-murata-migration-2026-11-05.md)
and [validation manifest](../../mechanical/review/remaining-murata-validation-2026-11-05.json)
record all ten exact assignments, all 246 prior physical groups/copper/poses,
58 native/physical opens and exact 104 intrinsic findings. Native XML/ERC,
visual exports, stable fills/byte-identical replay, original-orphan restoration,
69 native and 116 portable routing guards plus 26 contract guards pass.
No additional copper, component/current/protection/enable or fabrication
exception is selected. The 52-edge converter candidate remains unselected.
