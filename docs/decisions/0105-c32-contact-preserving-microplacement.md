<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0105: Bounded contact-preserving C32 microplacement

Date: 2026-11-09
Status: Selected as the validated 36-open CAD successor; fabrication prohibited.

Test a C32-only translation of at most 0.25 mm Euclidean distance, retaining
its exact 180° orientation, GRM188R60J106ME47D / 10 µF / 6.3 V / X5R
identity, footprint-local lands, fields and numbered nets. Keep every other
pose, accepted copper, zone definition, profile and electrical setting fixed.
Every original direct external contact to each land must remain physically
in contact, and every previous pad group and copper/net identity must survive
refill. No retirement, resizing, narrowing or current-limit change is allowed.

This explicitly extends ADR 0073's fixed-C32-pose screen only for the bounded
translation. Its colour-retirement experiments are not part of this trial.
Ground routing retains ordinary 0.20 mm width, adjacent 0.30/0.10 mm vias
and provisional 0.50/0.30 mm In2/In3 buried geometry, screened across each
span. No new unsupported central microvia is allowed. First sample 0.05 mm
translations and exact land-centre captures, checking foreign copper and
courtyards before refill or saved trial output.

The supplied Murata GRM188R60J106ME47-61A reference sheet, dated 14 June 2026,
PDF page 2, was rendered and rechecked for exact part/value/package identity.
Existing approved local geometry is retained. Approval-sheet, effective-
capacitance, bypass/return, assembly/process and fit qualification are not
inferred from a small translation or a geometric join.

Select nothing without a numbered-pad ground join, all old contacts/groups/
copper, exact unchanged 104 native findings, a deterministic pose/copper
ledger, stable replay/fills, source/fault checks and native visual review.
The validated 37-open source remains selected until every successor gate
passes. Independent Gate A and all fabrication holds remain open.

Select centre (89.250,10.250) mm at unchanged 180°, preserving the original
supply contact and every prior group/copper item. A refilled B.Cu ground
corridor joins C32.2 to the main group without added or retired copper.
Native/physical 36 opens, exact 104 findings, stable replay/fills, 36 fault
guards, 27 source checks and native visual review pass. See the
[implementation record](../development/c32-microplacement-2026-11-09.md).
