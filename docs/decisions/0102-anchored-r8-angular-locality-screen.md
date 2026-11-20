<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0102: Bounded anchored R8 angular locality screen

Date: 2026-11-07
Status: Accepted for ignored feasibility only; no successor selected.

Extend ADR 0095's rejected cardinal-angle R8 experiment to a finite 5°
orientation screen around the unchanged VLED pad-1 centre. The exact part
remains Panasonic ERJ2RKF1001X / 1 kΩ, with identical footprint-local lands,
fields and numbered nets. Keep every other component pose, accepted copper,
zone definition, profile, current limit and protection/default circuit fixed.

A trial may add ordinary 0.20 mm B.Cu routing from R8.2 to PAIR03.5, with
at most 5 mm total lead and at most 3 mm pad-centre separation. No new via
or copper retirement is permitted. Check native foreign copper including
no-net pads and courtyards. Every original direct copper contact to R8.1
must remain in physical contact after rotation; fixed pad centre alone is
not sufficient evidence. All previous pad groups and all accepted copper
must survive refill.

Select nothing without exact unchanged 104-finding native DRC, actual native
and independently counted physical open reduction, exact pose/copper ledger,
stable replay/fills, source/fault checks and visual review. Non-cardinal
placement, assembly/process/fit, gate transients and power/current/thermal
qualification remain unresolved. The 37-open checkpoint stays selected until
all successor gates pass. Independent Gate A precedes fabrication.

The completed B.Cu-only screen rejects all 72 sampled orientations: 27 fail
the separation bound, 40 conflict with foreign pad/track copper, and the five
remaining orientations have no clear sampled direct/L/dogleg lead. No pose is
selected. Extend only those five clear poses (−85° through −65° in 5° steps)
to an ordinary In4.Cu lead with at most two adjacent B.Cu/In4.Cu
0.30/0.10 mm microvias and short ordinary B.Cu capture leads if required.
The combined lead remains at most 5 mm; all source contacts, copper, pose,
current and complete successor constraints above remain mandatory. No central
transition, width exception or new retirement is authorized. This extension
supersedes only the B.Cu-only/no-new-via screening restriction for these five
ignored alternatives; it does not select a non-cardinal assembly pose.

All five adjacent-layer alternatives also fail their sampled ordinary lead
screen. No R8 pose or copper is selected. The bounded subsequent one-track
study is recorded in ADR 0103 and the
[follow-up record](../development/remaining-routing-followup-2026-11-09.md).
