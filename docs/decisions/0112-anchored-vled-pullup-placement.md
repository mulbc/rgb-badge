<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0112: Anchored VLED pull-up placement exploration

Date: 2026-11-10
Status: Accepted for ignored exploration; no successor selected.

Explore R11 and R21 independently in 5-degree orientations about the fixed
pad-2 gate contact. Retain exact Panasonic ERJ2RKF1001X, 1 kΩ / 1%, local
lands, fields and pin identities. The cached manufacturer sheet's ERJ2R
package dimensions and order code were rechecked; no footprint, BOM or
resistance change is permitted. Keep every original direct external gate
contact, all old copper and all preceding pad groups intact. Other poses,
zones, rules, protections and current settings remain fixed.

A trial may add ordinary 0.20 mm B.Cu lead of at most 7 mm to a physically
different existing VLED group. Check foreign copper including no-net pads
and complete component courtyards. A rotated gate centre alone does not prove
contact preservation. Reject every refill that loses any old group. Do not
select a disconnected seed, or infer regulator continuity from an isolated
VLED group join. Keep outputs ignored until exact unchanged DRC, independent
counts, ledger/replay, fault/source checks and visual review pass. Assembly,
electrical/process qualification and independent Gate A remain unresolved.

The initial B.Cu-only screen leaves four geometry-clear R11 orientations and
nine R21 orientations, without a clear sampled lead. Extend only these poses
to ordinary B.Cu/In4.Cu/In3.Cu routing with at most four adjacent 0.30/0.10 mm
microvias. No central transition is permitted. Retain original contacts and
all old groups before and after routing; combined new lead remains at most
12 mm. A search seed or overlength result cannot be selected. All preceding
source, rule, current and full validation requirements remain unchanged.

Outcome: each resistor has 72 sampled orientations. R11 rejects 41 for pad
copper and 27 for courtyards, leaving four geometry-clear poses. R21 rejects
36 for pad copper and 27 for courtyards, leaving nine. All thirteen preserve
prior groups after refill, but every subsequent B.Cu/In4.Cu/In3.Cu search
exhausts its available graph without a join. No pose or copper is selected.
These are bounded results, not proof that a broader floorplan cannot work.
