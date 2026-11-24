<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0206: R11 local ground-plane substitution

Date: 2026-11-16
Status: Accepted for exact ignored complete-circuit feasibility only.

ADR0205's R11 courtyard and supply lead clear, but its gate pad meets only
two retained 0.20 mm B GND traces. Freeze their full native source contacts:

- b28e3949-8fca-5e9b-8f67-c8d64ef424af: (71.000,7.250)–(70.850,7.200) mm.
- 5dbd65a2-997f-5eef-a3c8-37793576a7ff: (71.750,7.250)–(71.000,7.250) mm.

Permit only an exact filled-ground substitution study for these two tracks
on the complete ADR0204 R21 candidate; no ground pad, via or other source
item may be removed or changed. Before combining the R11 move, retain all
original/current pad groups, 27 matching native/physical opens and exact104.
Every original outside B ground copper/pad branch must remain in the original
main ground group and touch actual refilled B ground with a retained source
witness. Record original layer-specific contacts; do not invent a plane anchor.

Only if that proof passes, combine the exact ADR0205 R11 pose and ordinary
B replacements with these same two ground retirements. Require every original
ground branch to remain connected through actual filled copper after the
complete R11 gate/supply join. All 216 immutable source groups, matching
reduced native/physical opens and exact104 remain mandatory. The combined
cohort has five original track retirements total, no original via removal
and no new via. Full source/part/pad/type/profile/contact/hole/replay/inverse/
orphan/fault/visual gates precede selection.

This is CAD continuity evidence only, not return-path/electrical/thermal
qualification. No current/resistance/protection/default-off/part/stack/process/
fit/Gate A or fabrication hold changes; incomplete ground proof rejects use.
