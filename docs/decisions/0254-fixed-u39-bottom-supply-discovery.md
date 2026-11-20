<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0254: Fixed U39 bottom supply discovery

Date: 2026-11-20
Status: Accepted for bounded read-only additive discovery.

Use selected23-open source SHA
9574949d6bd56caa6f79b9db78af3531b0150cfba1f110d727c829effcaf62b3.
Native inventory witnesses isolated U39 TMP390A2DRLR VDD pin5 at
56.885,15.500 and the original32-pad main +3V3_USB group. Rechecked cached
TI SBOS904A, revised August2020, pages3/13 confirms pin5 VDD and the local
bypass/programming guidance. Preserve U39, C50, C51, R89/R90, TH1 and
all other parts, fields, local pads, nets and original Cu exactly.

Discover only ordinary0.20 mm B conductor from the actual U39 supply pad
to physically connected main-group B Cu. Native inventory identifies C51.1
at54.485,17.750 and C50.1 at57.285,19.295 as existing ports; C51 remains
U40's capacitor, while C50 remains U39's capacitor. No bypass reassignment,
capacitor move or relaxation of their existing locality/qualification holds
is permitted. The sensor's reservation and temperature/programming limits
are unchanged.

Use x=52.000–60.000 /y=13.000–20.000 mm,0.025 mm eight-neighbour B
steps,≤100,000 expanded nodes and≤12 mm conductor. Require actual source
Cu/pads on every point/edge/merged segment and actual retained main-port
contact. Add no via, retire no Cu, move no part and write no PCB during
this discovery. A clear path needs a separate frozen prototype and all211
old groups, retained attached Cu, main GND197/VLED38, complete sensor
programming/output/ground, native/physical22, exact104, source/identity,
replay/inverse/fault/visual gates before selection. Electrical/bypass/thermal,
current/NTC/timer/default-off, stack/process/fit and independent Gate A holds
remain open; fabrication is prohibited.
