<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# R11 clearance and shunt-ground join, 2026-11-10

The selected CAD checkpoint reaches **35 native and independently counted
physical opens**, down from 36. Main ground grows from 194 to 196 pads by
joining the existing U38.3/U52.3 island. PAIR01.1 remains isolated. The
zero-open objective is still in progress; the board is unbuilt.

The selected source SHA-256 is
`da3764ddf5c8c615529340c33c92974cff3fd036b937b5e4a53c408e0b141637`.
[ADR 0115](../decisions/0115-r11-clearance-for-ground-join.md), the
[exact plan](../../mechanical/review/remaining-routing-plan.json) and
[native evidence](../../mechanical/review/r11-ground-join-2026-11-10.json)
record the change and its scope.

R11 remains exact Panasonic ERJ2RKF1001X, 1 kΩ / 1%, with unchanged local
lands and 180° orientation. Its centre moves from (72.250,4.250) to
(72.750,4.250) mm. Only the original 0.400 mm ROW_GATE_05 B.Cu terminal
leaf is retired. A 0.100 mm ordinary-width lead retains the original via
and R11's gate connection. Its VLED pad remains disconnected; no supply or
current-limit change is inferred.

The new ground route adds sixteen 0.20 mm tracks totalling a calculated
6.580096 mm and one adjacent 0.30/0.10 mm In4.Cu–B.Cu microvia. Both ends
reach actual retained ground-via centres. Two 0.195 mm landing extensions
strengthen the search's original end-cap contacts. An isolated native fault
confirms that continuity alone would accept the weaker cap contact, while
the independent via-centre guard rejects it.

All 224 previous live pad groups and 226 accepted copper additions survive.
All 231 groups in the immutable 43-open parent survive as well. Relative to
that parent the ledger now has 244 additions, ten exact retirements and five
controlled component poses. Relative to the preceding 36-open source it has
18 additions, one retirement and only the R11 pose change. Every other old
copper/net identity, part, local pad, field, pose, zone, rule and profile is
retained. The capacitor witness explicitly identifies the one independently
reviewed R11-leaf exception to historical copper retention.

Validation passes:

- Full native DRC matches the exact original 104 findings, including item
  identities, positions, descriptions and severity. No findings are waived.
- Canonical generation and two independent replays have identical bytes;
  each performs three stable fills and a complete source/group audit.
- Historical R11 contacts and both original ground endpoints are independently
  re-derived. The old gate via and actual gate-network continuity remain.
- All 44 native rejection cases pass, including actual shunt/C32 ground
  disconnections, a forged matching retirement ledger, omitted original
  contacts, a lost far-end contact and a missing via-centre landing.
- The strict original-orphan proof on the immutable parent and the rejected
  selected-source restoration probe pass. All 28 source-workflow commands pass.
- Native before/after B.Cu and In4.Cu crops were inspected. Ignored raw views
  are in `hardware/coupon/rev-a/build/remaining-routing/35-views/`.

The preceding ignored localization studies are not selected. They temporarily
removed a much larger remote gate cohort and exposed a usable ground path,
but lost other ground groups. Comparing that path with the complete source
identified the single terminal leaf and R11 pad as its actual obstruction.
Every other original gate item is retained in this selected checkpoint.

These are native CAD continuity calculations, not measurements of hardware
operation or return impedance. Current limits, protections and default-disabled
permissions remain fixed. The 557 historical central microvias, controlled
stack, electrical/thermal/process/fit qualification and independent Gate A
remain unresolved; fabrication is prohibited.
