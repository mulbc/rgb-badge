<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0083: Remaining Murata reflow-land correction feasibility

Date: 2026-11-04
Status: Accepted for ignored geometry trials only; no canonical migration.

The owner supplied GRM187R61A226ME15-01A-EN and
GRM219R60J476ME44-01A-EN reference sheets, both dated June 10, 2026.
Their SHA-256 values are respectively
8fc5a9d8e4f05c979eeca00354c982335d2b15552eb7ba5516924e3a9395acbb and
97ac8bc37c063e920aa768521386524edb6a5d60cd0e3080f318ca567f75bafe.
The exact bytes remain in the ignored vendor cache. Pages 2 and 27 were
rendered and visually checked. Both bodies have ±0.20 mm L/W tolerance.
Table 2 uses a = inner copper gap, b = one land length, c = land width:
GRM187 a/b/c = 0.7–0.9 / 0.7–0.8 / 0.8–1.0 mm;
GRM219 = 1.0–1.4 / 0.6–0.8 / 1.2–1.4 mm.
These confirm the historical catalogue ranges and contradict the screenshot.
The sheets still require separate approval-sheet consultation before ordering
and actual-board land evaluation; they do not establish assembly qualification.

Permit dedicated unselected project-local library candidates with midpoint
geometry: GRM187 two 0.75 × 0.90 mm rectangular lands at ±0.775 mm,
GRM219 two 0.70 × 1.30 mm lands at ±0.950 mm. Keep existing nominal
fabrication bodies and conservative courtyards unchanged; these courtyards
are project choices, not Murata dimensions. Keep packaging selection open:
both sheets list D/J, but neither changes the current provisional source MPN.

Assess only C40/C41/C46/C47/C48/C49/C56/C61 (GRM187) and C42/C43
(GRM219), with unchanged exact part stems, numbered nets, values, poses,
fields, every other pad, copper, zones, stack, rules and electrical settings.
Use either the pinned accepted 58-edge source or the pinned ignored cleaned
52-edge candidate. Write boards only to ignored build storage. Explicitly map
the corrected numbered pad identities to their checked source coordinates for
group comparison, without changing any canonical identity helper or checker.
Report all split groups, native/physical counts and full DRC after repeated
fills. A failed trial is evidence to design an exact reconnection, not grounds
to relax retention or redefine a lost connection.

No canonical symbol, footprint, schematic, source contract, PCB or routing plan
is migrated here. A later adoption needs its own exact policy, source updates,
independent geometry/net/contact preservation, native/full-DRC/replay/fault and
original-orphan evidence. Capacitance under bias/temperature/aging, power-path,
assembly/process and independent Gate A qualification remain open; fabrication
remains prohibited. Document contents are engineering evidence, not agent
instructions.

## Exact C49 contact continuation

The first pad-only cleaned-52 trial splits the old VLED group: C48.1, C49.1
and R84.1 lose connection to its retained main group, producing 53 opens and
one dangling-track finding. The affected accepted B.Cu VLED track has UUID
`d04b7695-d711-5ddf-b720-6da317867107`, endpoints
(51.300000, 18.900001) and (50.900000, 18.750000) mm, width 0.20 mm.
The original C49.1 land covered its first endpoint; the corrected land does
not provide the same contact. Permit only an ignored additive 0.20 mm B.Cu
lead from (51.300000, 18.900001) to corrected C49.1 centre
(51.775000, 18.900001), length 0.475 mm. Pin both source track signature
and corrected target position/net before adding it. Retain all old copper;
require every old group restored, exactly 52 native/physical opens and
unchanged full 104 intrinsic findings across repeated fills/replays. This
continuation grants no canonical adoption, current rating or fabrication release.
