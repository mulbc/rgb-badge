<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Remaining ten-capacitor land source migration

Date: 2026-11-05. Coupon Rev A remains unbuilt. This is first-author source,
drawing and native CAD verification, not a hardware measurement, independent
engineering review or fabrication release.

[ADR 0084](../decisions/0084-remaining-murata-source-migration.md) continues the
[supplied-sheet review](remaining-murata-lands-2026-11-04.md) and adopts its
successful **accepted-source pad-only** correction. The separate 52-edge
converter layout and its C49 contact extension remain unselected. No current,
protection, enable, firmware behavior, component pose, track, via or zone changes
in this source transaction.

Dedicated project-local footprints replace the historical shared assignments:

| Source identity | References | Rectangular lands, mm | Land centres, mm |
| --- | --- | --- | --- |
| GRM187R61A226ME15 | C40/C41/C46/C47/C48/C49/C56/C61 | 0.75 × 0.90 | ±0.775 |
| GRM219R60J476ME44 | C42/C43 | 0.70 × 1.30 | ±0.950 |

The [footprint audit](../../hardware/coupon/rev-a/remaining-murata-footprint-audit.md)
identifies the supplied June 10, 2026 reference sheets and their page-27 reflow
rows. Existing nominal bodies and conservative project courtyards remain fixed.
Both capacitors are nonpolar; passive numbered pins and every assigned net stay
unchanged. Source MPN stems retain their explicit packaging-selection hold;
this is not a procurement BOM or separate manufacturer approval.

Canonical library symbols, embedded and placed schematic symbols, the four
affected root sheets, unlinked 3V3/VLED fixtures and deterministic schematic
generators now share the dedicated assignments. The fresh native XML contract
reconciles the same 465 shared components, 1,718 logical pins and existing
mixed-source study exceptions. The provisional firmware pin inventory changes
only to record updated source/checker fingerprints; firmware logic/pins do not
change. Native copper, paste, body/courtyard and all four affected schematic
sheet exports were visually inspected.

The [separate exact migration policy](../../tools/remaining_murata_migration.py)
pins all ten references, source MPNs/values/manufacturer, old/new pad dimensions
and offsets, numbered nets and layer sets. Geometry and nets are checked before
any historical identity normalization. The earlier six-capacitor policy remains
byte-for-byte unchanged. Source-only reconciliation requires corrected geometry
normally; explicit historical mode checks and reports legacy assignments.
Legacy shared footprint files remain unchanged for historical studies.

The preceding complete [58-edge plan](../../mechanical/review/routing-progress-58-checkpoint.json)
and [canonical source contract](../../mechanical/review/coupon-canonical-net-contract-before-remaining-murata.json)
were frozen before editing. All older plans/native sources/evidence remain
unchanged. The catalogue comparison now explicitly reads the frozen contract,
so its historical discrepancy report remains reproducible after correction.
CI sparse checkout includes both new frozen records.

The accepted PCB changes from SHA-256
`3451177253a021d8706ff818696212afabf539a108f15ef9e5d6921e46435acc` to
`817241b48eee1ae6ccc6ff0a99bf89d6c373bde6b45cba687a71e2309115f3d4`.
There are still **58 native and physical opens**, **104 unchanged intrinsic
clearance findings**, 483 footprints and 18,338 copper items. All 246 prior
physical pad groups remain exactly unchanged. No new route or lower accepted
open count is claimed. The manifest's stale physical-open value of 59 is
corrected to the independently verified 58.

The [direct retention checker](../../tools/check-remaining-murata-retention.py)
compares the exact frozen preceding PCB, every copper signature, all 483 poses/
fields/graphics, exact old/new pads, zone/structure/profile/rule definitions and
all 2,092 persistent pad UUIDs/nets. It checks all 246 connected UUID groups
directly, without the corrected-coordinate identity mapping. Three native fills
retain the same groups and 58 opens. Its
[report](../../mechanical/review/remaining-murata-retention-2026-11-05.json)
records the exact board and checker hashes.

The routing generator replays from the unchanged 215-edge input, applying the
old six-capacitor and switch-label migrations plus only the new pad correction.
An ignored second generation is byte-identical to the selected source. The full
routing gate preserves all retained source interfaces, earlier additions,
completed groups and exact routing exceptions. Restoring the three original
retired orphan vias retains all selected groups and 58 opens, adding only the
same three known dangling-via findings. No waiver or source retirement changes.

Validation covers native XML/ERC/library exports, the direct retention proof,
replay, full DRC, original-orphan restoration, source-only checks and isolated
native failures. New failures reject a legacy assignment for each of the ten
parts, legacy oversized lands under corrected labels, a wrong corrected pad
position and a wrong numbered net. Portable contract checks also reject new
oversized geometry even with the historical opt-out enabled, and require exact
old geometry before reporting a historical assignment. All 69 isolated native
routing guards, 116 portable routing guards, 26 contract guards, 67 source
fixture tests and 24 wrapper fixture tests pass (these suites overlap; they are
not an additive unique-test total). Full results/hashes are
recorded in the [validation manifest](../../mechanical/review/remaining-murata-validation-2026-11-05.json).

Raw local evidence is under
`hardware/coupon/rev-a/build/remaining-murata-migration-2026-11-05/` and
`hardware/coupon/rev-a/build/routing-progress-review/`. Reproduce current source
checks with `./tools/check-kicad.sh`,
`./tools/check-coupon-study-contract.sh` and `./tools/check-routing-progress.sh`.
For the direct before/after comparison, obtain the preceding PCB/project/rules
from commit `b40e36e` in an ignored directory and run KiCad Python on
`tools/check-remaining-murata-retention.py --before PATH --after PATH --report PATH`.
The November 4 trial environment remains reproducible from that earlier commit;
its exact source hashes deliberately reject this later corrected source.

Remaining holds include the 50-edge routing target, 104 intrinsic findings,
the unselected 52-edge converter candidate, L1/U36 locality, packaging selection,
separate approval consultation, effective capacitance under combined bias/
temperature/aging, decoupling/return/power-path/thermal/timing and stencil/HDI/
assembly/RF/enclosure qualification. Independent Gate A precedes fabrication.
Vendor PDFs, rendered vendor pages and local trial/manufacturing output remain
outside Git.
