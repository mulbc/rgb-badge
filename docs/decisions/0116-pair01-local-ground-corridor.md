<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0116: PAIR01 local ground corridor and selector transfer

Date: 2026-11-10
Status: Accepted for ignored feasibility; no successor selected.

The selected basis is the 35-open board, SHA-256
`da3764ddf5c8c615529340c33c92974cff3fd036b937b5e4a53c408e0b141637`.
PAIR01.1 is its remaining isolated ground pad. Test a (+0,+0.150) mm PAIR01
translation, retaining exact trial identity, orientation, footprint-local
geometry, pin mapping and all original pad groups. Its manufacturer pin map
and existing package source remain unchanged; no part substitution is allowed.

The shifted ROW_SEL_00 pad approaches the existing internal ROW_00_A
strap. Replace only that exact B.Cu track from (75.750,4.250) to
(76.675,4.400) mm, using ordinary 0.20 mm B.Cu within the local drain-land
region. Preserve both drain lands and the retained external ROW_00_A lead
and through via. Do not raise any current setting or claim power qualification.

Also permit replacing only the four original ROW_SEL_00 B.Cu U-loop tracks
intersecting x=76.3–82.0, y=0.5–6.5 mm (the previously recorded ADR 0110
cohort). Re-derive original contacts and preserve the complete external
selector network and all other copper. Restore the shifted selector pad to
actual retained same-net copper using ordinary tracks and standard adjacent
B.Cu/In4.Cu/In3.Cu transitions, without new central microvias. Any dangling
source fragment prevents selection until its exact reviewed disposition.

Test ordinary ground leads and one adjacent 0.30/0.10 mm In4.Cu–B.Cu
capture at (77.300,3.750) mm, linking shifted PAIR01.1 to the retained main
GND via at (79.250,3.275) mm. Gate/selector/drain and ground continuity must
all be restored together, with all previous groups and 244 accepted additions.
Keep every other pose, net, rule, zone, protection, current and safety setting.

Outputs remain ignored. Selection requires full native/physical reduction,
independent exact original-contact/retirement proof, deterministic replay,
source/fault/visual checks and the original 104 intrinsic finding identities.
If intra-package finding coordinates translate, independently verify the
unchanged package-local geometry and exact translated pad coordinates;
no finding type, item, severity or clearance waiver may be introduced.
Electrical/process/fit qualification and independent Gate A remain open.

The initial selector capture is blocked by COL_09_B's retained In4.Cu
fanout at y=3.750 mm. Permit an ignored relocation of only its In3.Cu–In4.Cu
0.30/0.10 mm via from (77.200,3.750) to (76.000,3.750) mm. Shorten its
original 0.20 mm In4.Cu segment (77.200,3.750)→(59.500,3.750) mm by
1.200 mm at that end and add an equal-length 0.20 mm In3.Cu continuation
to the original same-net endpoint. Re-derive all original track/via contacts;
retain all seventeen physical colour pads and every source group/addition.
No colour assignment, width, current, original central via or other retirement
may change. The final ground capture may be x=77.600 mm instead of 77.300 mm
to leave space for the restored selector; native complete clearance is required.

The restored selector is additionally bounded by the retained ROW_00_A
through via. Permit that same 0.50/0.30 mm full-span via to shift from
(77.250,4.400) to (77.250,4.450) mm, preserving every original same-net
contact on every copper layer. It must retain its exact net, span, diameter
and drill. This small hole relocation allows a 0.20 mm selector lead between
it and a ground capture at (77.950,3.700) mm. No current setting or power
trace width changes; full native clearance and process/fit holds remain.

## Rejected trial outcome

The final ignored selector-complete trial counts 34 native/physical opens
and retains all 223 preceding physical groups, but fails full clearance:
111 findings versus the original 104. Its ground transfer shorts COL_08_B,
the relocated COL_09_B transfer shorts ROW_00_A, and the shifted drain through
via creates three further clearances. Reject the candidate; do not adopt its
poses, retirements or lower count. The 35-open historical source remains
byte-identical. Raw ignored evidence is under
`hardware/coupon/rev-a/build/zero-open-routing/pair01-selector-complete.*`.
ADR 0117's flip-flop source correction now precedes further logic routing.
