<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0098: Remaining isolated enable test lands

Date: 2026-11-07
Status: Accepted for ignored bounded feasibility; no successor selected.

Extend ADR 0055's feasibility scope only for the still-isolated TP13
(VLED_ENABLE_CANDIDATE) and TP14 (ROW_ENABLE_N_CANDIDATE) in the validated
39-open source. Their remote draft positions do not set hardware permissions;
these are the existing one-pin 1.0 mm circular PCB probe lands, not added
components or a circuit substitution.

Permit a B.Cu placement and ordinary 0.20 mm lead within 5 mm of the actual
same-net source pad, superseding the earlier 3 mm experimental lead bound for
these two lands only. Retain exact footprint, copper/mask/paste shape, layer,
orientation, pin number, fields and net. Preserve every other component pose,
all existing copper and every prior live pad group. Before selection prove
that the old land is isolated and has no direct nonzero source-copper contact.
Require a completed numbered-pad join, unchanged full native 104 findings,
independent physical/native reduction, stable replay/fills, exact source
contract and negative guards. No new via, retirement or rule relaxation is
included. A clear geometric trial alone does not select a pose.

The 5 mm bound is a limited CAD study choice, not a timing/loading guarantee.
Record actual lead length; probe/fixture/enclosure access, capacitance and
signal/return behaviour remain engineering holds. Current limits, cell/charger
protection, hardware enable logic and default-disabled settings are unchanged.
Independent Gate A and all fabrication restrictions remain mandatory.

The 0.10 mm centre-grid screen within 5 mm finds no complete direct/L-shaped
lead for either land. TP14 first-failure counts are 7,365 courtyard and 313
pad-copper rejections, with 496 obstructed lead paths; TP13 counts are 7,013,
763 and 92 respectively. Lead counts are paths, not additional poses. No
test land is selected or moved in the accepted source. These finite shapes
do not rule out a wider coordinated contact-preserving rework.
