<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0174: Read-only cold-programming resistor restoration

Date: 2026-11-15
Status: Accepted for read-only geometry discovery only.

ADR 0173's fixed-resistor templates produce no complete candidate: R90's
courtyard overlaps all three sampled sensor poses; the nearest sensor pose
also overlaps R89. Keep R89 fixed and continue only the second exact sensor
sample, centre (57.900,16.200) mm / 270°, VDD pad (57.900,16.940) and its
ordinary 0.20 mm neck to B/In4 capture (57.950,17.640) mm. Preserve the exact
seventeen-item in-memory study cohort and full original contact catalog.

Screen exact existing R90 ERJ2RKF1402X (14 kΩ, 1%) at cardinal orientations,
0.050 mm centres within 2.000 mm of its current (60.000,16.750) mm position.
Every resistor pad must remain within 3 mm of its corresponding U39 SETB/GND
pin. Retain all other parts/copper as obstacles, including fixed R89, TH1,
C50/C51 and the exact moved sensor/neck/capture. Require native pad/courtyard
clearance and source edge rules. Record exact original connected GND fill
contacts when present; a missing original fill contact remains unresolved.
Screen an ordinary B.Cu cold lead ≤8 mm with the prior straight/one-/two-corner
templates. Record a bounded set of clear poses rather than selecting a PCB.

No part substitution, threshold change, current/protection/NTC/timer/default-off
change, actual retirement or source modification is authorized. Every original
external branch/contact, complete hot/cold/output/ground/supply restoration,
216 prior groups and all native/physical/exact104/source/contact/hole/replay/
inverse/orphan/fault/visual gates remain prerequisites for any successor.
Thermal/electrical/return/stack/process/fit/part/Gate A holds remain open and
fabrication prohibited.
