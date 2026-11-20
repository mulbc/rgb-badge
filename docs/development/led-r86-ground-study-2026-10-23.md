<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# R86 ground with a VLED-preserving colour replacement

Status: **unbuilt noncanonical routing study; fabrication prohibited**.

R86 (`ERJ2RKF1803X`, 180 kΩ ±1%) is the existing VLED feedback-divider bottom
resistor. Pad 1 remains VLED_FB and pad 2 remains GND. A 0.15 mm rear lead from
(64.25, 10.25) to (64.10, 10.25) mm and three adjacent B–In4–In3–In2 microvias
join its ground pad to the main group. Native/physical-pad opens decrease
**216 → 215**, GND **23 → 22**. All prior pad groups, 483 placements, exact
component identities and colour-column membership survive.

## Keep the colour connected and preserve VLED

The displaced original COL_02_G In4 segment runs from (76.35, 10.25) to
(52.7, 10.25) mm. Forward/reverse global searches reach U1 OUTG2 pin 15 in
313,848/437,919 expansions, but both split the old VLED group, losing PAIR11.4
and R7.1 from its anchor. The preserved-group guard rejects both. One whole-
segment detour and 77 single-section F.Cu trials also fail; they remain local.

The accepted transaction moves forty-one of the candidate's forty-three In1
tracks onto a complete F.Cu detour, retaining a **0.9 mm In1 tail** at its
front-layer-blocked endpoint. A bounded native F.Cu search reaches a clear
transition in 6,197 expansions. Its selected path is
**(76.6, 10.75) → (75.5, 23.85) → (74.95, 24.50) mm**. Two adjacent F/In1
microvias connect it. The tail continues through (74.55, 24.50) to
(74.55, 25.00) mm. All old VLED, application, USB and ground groups survive.

Full DRC initially reports 106 findings from two obsolete branch ends. Seven
isolated native cleanup steps remove **four original tracks / three original
vias**, checking all previous pad groups after each step. With the displaced
In4 segment, the increment retires **five original tracks / three vias**.
It returns to exactly the baseline 104 findings. No other original item is
removed. The final green replacement has eight tracks/eight microvias and
**44.636 mm** track length versus **30.750 mm** retired colour track length;
that increase, timing, inductance and return geometry remain unqualified.
Two short exact In2 endpoint leads remain; no planar In2 grid steps are used.

Including the ground escape, the increment adds **nine tracks / eleven
adjacent-layer microvias**, giving **15,517 items**. The cumulative plan adds
953 tracks/99 microvias and pins twenty-five original-track/four-via retirements
across four replaced routes. **14,465 of 14,494 original items remain exact**.
Track width/clearance stays 0.20 mm; adjacent microvias stay 0.30/0.10 mm.

## Feedback and validation boundaries

The exact 1.24 MΩ / 180 kΩ divider and its previously calculated nominal
3.944 V setting are unchanged. No input, charge, LED, regulator or battery
current limit is raised. The actual converter enable and decoder boundaries
remain isolated. The current [TI TPS63020 Rev I datasheet](https://www.ti.com/lit/ds/symlink/tps63020.pdf)
retains FB 3/control GND 2 and requires a short, local feedback/control-ground
layout. Native membership confirms R86.2, U37.2 and U37.15 share a physical
pad group; this does not qualify a quiet return, impedance, converter operation
or stable voltage regulation. These still require layout/engineering review
and hardware evidence. There are no board measurements or firmware changes.

Independent replay/checker contracts pin all retired signatures and added
COL_02_G/GND/power copper. Thirty-four isolated native guard methods pass.
The new witness restores the exact rejected forty-one-track In1 path, proves
that the full colour pad group stays connected while VLED splits, and requires
an explicit physical-group rejection. Other guards detach R86 while proving
all four earlier escapes remain joined, detach COL_02_G and restore each of
27 retired green items individually. The two earlier non-green restoration
cases cover the remaining retired source items.

All 256 LED checks, fresh 21-case schematic comparison, source-only CI and
byte-identical generation pass. GND/VLED/application-3.3-V/USB-3.3-V retain
**22/14/7/4 opens**. TP11, the transmit test-pad leg, six gate terminals and
other power/control/USB routes remain incomplete. Intrinsic findings, quiet
returns/decoupling/current, signal timing, HDI/process, fit/RF/thermal, canonical
package/BOM adoption and independent Gate A remain open before fabrication.
This is existing-net routing; no material circuit or part decision is introduced.

[Increment/cleanup evidence](../../mechanical/review/native-control-r86-ground-escape-2026-10-23.json),
[rejected VLED witness](../../mechanical/review/native-r86-vled-regression.json),
[current checks](../../mechanical/review/native-control-check.json),
[current validation](../../mechanical/review/native-control-validation.json).
Repeat with `./tools/check-native-control.sh` and `./tools/check-coupon-study-contract.sh`.
Current PCB SHA-256: `da3c3e093acef457ce2d0ebe73b57fd5006b9139a57b7fe8acfcd77e612dc246`.
