<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0283: Source-connected supply corridor discovery

Date: 2026-11-24
Status: Accepted for bounded RAM-only supply restoration discovery.

ADR0282's first grid finds133 actual34-pad contacts and no six-pad
contacts; no direct/L bridge qualifies. Native source-plane tracing
locates the six-pad island through retained VLED copper, including
existing F/In1 captureb6e0c786-b624-54b3-8e82-7068b20823f5 at78.8,10.65.
Its In1 filled component spans x75.9505..81.550436/y10.4505..14.057880,
while other same-net filled components are separately identified. Never
infer group membership solely from the zone name or bounding box.

Extend only the supported0.30/0.10 mm F/In1 VLED probe grid to x76..83/
y9..16 mm at0.10 mm spacing. Keep actual native6/34-pad classification,
all source/new Cu and holes. Candidate bridges may use a real existing
F conductor already proved in the opposite group, avoiding an unnecessary
new via, or a newly qualified opposite-group capture. Screen at most4096
closest endpoint pairs, preferring fewer new microvias; refill at most64
clear direct/L candidates. At most two new microvias/4 mm ordinary0.20 mm
F conductor. No new source retirement or current/protection change.

Require actual VLED40/GND197/row18/gate4, every original group except the
explicitly pending selector, all19256 retained attached Cu/no orphans,
21 matching opens. Only final20 opens/all210 prior groups may advance
to a separate frozen prototype. Write no PCB; all power/current-sharing/
electrical/return/trial-package/thermal/stack/process/fit/independent
Gate A holds remain. Fabrication is prohibited.
