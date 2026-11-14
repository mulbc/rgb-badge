<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0113: Relocate a VLED pull-up with its exact gate leaf

Date: 2026-11-10
Status: Accepted for ignored feasibility; no successor selected.

The anchored R11/R21 orientations cannot complete a VLED route. Permit
independent relocation of either exact ERJ2RKF1001X pull-up by at most 2 mm,
with cardinal orientation, while replacing only its original terminal gate
leaf. The 36-open basis is SHA-256
`a24e9220226b77411ae8e8baea5cd629ce0fea8a97c377a708510d6791c2e439`.

R11's sole external gate contact is its 0.20 mm ROW_GATE_05 B.Cu leaf from
(71.750,4.250) to (72.150,4.250) mm, UUID
`19e3ee8e-4132-50aa-8a90-15070af51afc`. Its retained far-end via is
0.30/0.10 mm In4.Cu–B.Cu at (72.150,4.250) mm. R21's sole external gate
contact is the 0.20 mm ROW_GATE_15 B.Cu leaf from (66.750,5.750) to
(66.750,5.000) mm, UUID `e10a833e-5a12-5e19-b8b4-85f4670985f6`.
Its far end touches the retained ROW_GATE_15 horizontal trace. Independently
rederive every original contact before accepting either retirement. Preserve
the far-end endpoint and every external contact except the moved own pad.

Keep the exact 1 kΩ part, local footprint, fields, numbered nets and all
other component poses. A replacement gate lead may use only ordinary
0.20 mm B.Cu tracks, at most 5 mm total, touching both moved pad 2 and the
retained far-end copper. A VLED lead to a genuinely different old group may
use ordinary 0.20 mm B.Cu tracks, also at most 5 mm. No new vias, narrowing,
other retirement, zone/rule/protection/current change is permitted. Check
full courtyards, foreign copper, all old pad groups and all accepted additions.
A linked VLED island alone is not proof of regulator continuity.

Trial outputs stay ignored. Require a true native/physical reduction,
unchanged exact 104 DRC findings, independent historical-contact and scope
proof, deterministic ledger/replay, source/fault checks and visual review
before selection. Electrical/transient/assembly/process/fit qualification and
independent Gate A remain open; source stays 36 opens until all gates pass.

Outcome: each independent 2 mm/cardinal screen tests 788 poses and selects
no VLED join. R11 leaves 110 poses with sampled gate reconnection; R21 leaves
28. None has a complete sampled supply lead. Subsequent localization is
separately controlled by ADR 0114; the selected ground-only variant is ADR 0115.
