<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0177: Complete coordinated sensor routing feasibility

Date: 2026-11-16
Status: Accepted for ignored complete-circuit feasibility only; no successor selected.

ADR 0176 verifies a mutually pad/courtyard-clear exact three-part cohort with
all programming/ground distances ≤3 mm. Only one output admits sampled outer
microvia escapes; those finite misses do not establish planar impossibility.
Permit an ignored complete-circuit routing prototype at exactly those poses:
U39 TMP390A2DRLR (58.200,15.700) mm / 270°; R89 ERJ2RKF2151X, 2.15 kΩ / 1%,
(60.015,15.000) mm / 270°; R90 ERJ2RKF1402X, 14 kΩ / 1%, (60.550,16.750) mm
/ 0°. Independently transform all original integer pad coordinates. Keep all
fields, lands, pin nets and other 480 part poses unchanged. Retain the thermal
reservation, ≤3 mm sensor movement, original C50 pad-distance bound and all
unchanged temperature/current/NTC/protection/timer/default-off boundaries.

Retire only the exact seventeen ordinary B.Cu local study tracks already
catalogued under ADRs 0097/0172/0176; freeze their UUIDs/signatures and full
native contacts against the immutable selected 28-open source before writing.
No source via or other copper may be retired or changed. Add the exact first
ADR0172 VDD neck, 0.20 mm B.Cu from (58.200,16.440) to (58.300,15.790) mm,
and supported 0.30/0.10 mm B/In4 capture there. Other replacements are ordinary
0.20 mm supported-layer tracks and outer adjacent 0.30/0.10 mm microvias;
In2/In3 transitions must be 0.50/0.30 mm mechanical buried vias. No centre
microvia, skipped layer, narrow rule or clearance exception.

This explicitly extends the prior read-only template scope to a bounded
complete-circuit prototype, without selecting it. Search only within
x=52–64 mm / y=12–21 mm, at 0.050 mm cardinal grid positions, ≤500,000 nodes
per attempt. Route only TMP_HOT_SET, TMP_COLD_SET, TEMP_OK, GND and +3V3_USB.
Bound each added join to 8 mm (ground joins 4 mm), hot/cold/new USB copper to
8 mm per net including the fixed VDD neck, TEMP_OK to 16 mm total and GND to
8 mm total. Reject any split of the current live groups after each refill.
Record each generated exact route ledger, bound and rejection. Finite misses
or a temporary lower count are not acceptance.

A successor must restore every original external source-layer contact and
branch, including retained source copper without pads, all 216 original live
groups and complete programming/output/local-return/bypass/supply continuity.
Ground substitution requires individual actual filled components and retained
source-copper witnesses at every outside contact. Reject native/physical
count disagreement, new original-copper dangling items or any new DRC finding.
Only matching reduction below 28 and exact original 104 payloads under existing
rigid transforms permit proceeding to full independent source/contact/hole/
replay/inverse/orphan/fault/visual qualification and a separate selection ADR.
No current, temperature setting, thermal-error allowance, part approval, layer
stack/process/fit or independent Gate A acceptance changes. Fabrication remains
prohibited; zero opens remains unfinished.
