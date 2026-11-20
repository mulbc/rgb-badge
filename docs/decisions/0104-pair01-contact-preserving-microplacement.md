<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0104: Bounded contact-preserving PAIR01 microplacement

Date: 2026-11-09
Status: Accepted for ignored feasibility only; no successor selected.

The full-layer 37-open ground search exhausts its sampled graph at PAIR01.1
without an additive escape. Test only a translation of PAIR01 by at most
0.25 mm Euclidean distance from its selected centre, retaining its exact
orientation, trial-only NTLJD3119CTBG identity, entire local footprint, fields
and numbered nets. All other component poses, original/accepted copper,
zone definitions, profiles and electrical/current/default settings stay fixed.
No source copper retirement, resizing or narrowing is permitted.

Each physical land must retain every original direct same-net external B.Cu
contact after movement, in addition to preserving all previous live groups.
Check foreign pad/track clearance and native courtyards before a trial.
An actual ground join may use ordinary 0.20 mm routing, adjacent
0.30/0.10 mm transitions and provisional 0.50/0.30 mm In2/In3 buried vias,
screened over every traversed layer. Do not add unsupported central microvias.
The first experiment samples 0.05 mm translations within the bound and
screens exact pad-centre captures; no grid-rounding assumption replaces
native shape checks.

The existing local lands remain those transcribed from onsemi NTLJD3119C/D
Rev. 6 (April 2024), top-view map on PDF page 1 and CASE 506AN Issue H
(25 January 2022) recommended land drawing on PDF page 10. Both pages were
rendered and visually rechecked: S1=1, G1=2, D2=3, S2=4, G2=5, D1=6, with
separate exposed drain islands; 0.65 mm pitch and six 0.45 by 0.39 mm lands.
This is still a geometric trial package, with no schematic/BOM substitution
or part/process/electrical qualification inferred.

Selection requires an actual numbered-pad ground join, all previous groups
and copper/net identities, exact unchanged 104 native findings, a complete
pose/copper/contact ledger, stable replay/fills, source/fault checks and
visual review. The validated 37-open source remains selected until all gates
pass. Switching/return/thermal, assembly/process/fit and independent Gate A
qualification remain open; fabrication is prohibited.

All 81 sampled positions are screened: 74 fail foreign-copper clearance;
seven retain contacts and courtyards but their first capture is obstructed
on In4 by COL_09_R and/or COL_09_G. Six nonzero retained poses also exhaust
their forced ground-routing graphs at 259–300 nodes. No PAIR01 pose or
copper is selected. ADR 0105 separately selects a C32-only change.
