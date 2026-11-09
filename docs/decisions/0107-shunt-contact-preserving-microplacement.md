<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0107: Bounded U38 ground-island microplacement

Date: 2026-11-09
Status: Accepted for ignored feasibility only; no successor selected.

Test a U38-only translation of at most 0.25 mm Euclidean distance from the
36-open source. Retain its exact LM4040A25IDBZT identity, 2.5 V setting,
180° orientation, entire local footprint, fields and numbered nets. Every
original direct external land contact and every preceding live pad group and
copper/net identity must survive. Keep all other poses, profiles, zones,
current limits, charger/NTC/protection and default-disabled permissions fixed.
No source copper retirement, resizing or narrowing is permitted.

First sample 0.05 mm translations without adding copper, checking foreign
pad/track shapes and courtyards before refill. A lower aggregate count alone
is insufficient: U38.3/U52.3 must join the existing main ground, U38.2 must
retain its original main-ground contacts, and every prior group must survive.

TI LM4040 Rev Q (SLOS456Q, April 2026), PDF page 4, retains DBZ pin 1 cathode,
pin 2 anode and pin 3's permitted connection to the anode. The current local
mapping and both ground nets remain unchanged. PDF page 54's DBZ0003A board
example uses the existing three 1.3 by 0.6 mm lands and 2.1/0.95 mm spacings.
Both pages were rendered and visually rechecked; no footprint or BOM
substitution or shunt-load/transient qualification is implied.

Selection requires an independent historical contact inventory, real main-
ground component witness, exact unchanged 104 native findings, all old
copper/groups and source contracts, stable replay/fills, isolated faults and
native visual review. The validated 36-open source remains selected until
all gates pass. All return/current/thermal/stack/process/fit and independent
Gate A holds remain open; fabrication is prohibited.

Outcome: all 81 positions were screened. Seventy-nine fail foreign-copper
clearance, one loses an original land contact, and the original pose alone
passes geometry but makes no ground join. No isolated U38 pose is selected.
The later coupled trial is governed separately by ADR 0110.
