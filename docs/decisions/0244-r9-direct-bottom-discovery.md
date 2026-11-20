<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0244: R9 direct bottom discovery

Date: 2026-11-20
Status: Accepted for bounded read-only discovery.

Use only selected23-open PAIR01 supply source SHA
9574949d6bd56caa6f79b9db78af3531b0150cfba1f110d727c829effcaf62b3.
Read exact Panasonic ERJ2RKF1001X R9 and actual PAIR04 VLED/gate03 port
memberships. R9.1 currently belongs to main VLED38 and its isolated gate
pad must join the original three physical PAIR04 gate pads.

Screen R9 only, on B, without substitution, changing current/default-off,
changing any field/pin/net/local package or moving another part. Use
x=75.000–82.000 /y=7.000–13.000 mm at0.100 mm increments and orientations
0/90/180/270°. Require actual B courtyards, all moved pads and both ordinary
0.20 mm B leads clear against source Cu/pads. Connect supply to actual
PAIR04.4 and gate to each actual PAIR04.5/6 pad centre independently.
Keep power lead≤6 mm and gate≤3 mm. Add no via, retire no source Cu, and
write no PCB during this preliminary screen. Preserve all qualification holds.

A sampled success is not a complete successor: first freeze any exact
obsolete R9 leaf retirement and native outside contacts, retain every shared
junction and all old groups/attached retained copper. A later frozen prototype
must prove matching22 opens with all211 previous groups preserved, exact104,
full source/identity/profile, hole/courtyard, replay/inverse/fault/visual gates.
Trial package, timing/return/thermal, controlled-stack/process, optical/fit
and independent Gate A/fabrication holds remain open.
