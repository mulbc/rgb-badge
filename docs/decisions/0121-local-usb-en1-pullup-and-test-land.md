<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0121: Localize the USB EN1 pull-up and test land

Date: 2026-11-12
Status: Selected for the validated 34-open corrected-source successor;
electrical/process qualification and independent Gate A remain open.

Use the corrected 35-open board, SHA-256
`3967bb66e89e0005f6859ce78a766b4536d06883b76fce130e75a6fdeefaf96e`.
U23.4 is isolated from the R70.2/TP31.1 USB_EN1_RAW_N group. R70.1 and
U23.5 already belong to the same 32-pad +3V3_USB group. Moving the exact
10 kΩ pull-up and its test land nearer U23 can shorten this control wiring
without changing the captured USB-permission circuit or its default state.

Retain exact R70 `ERJ2RKF1002X`, its value, local lands and pin nets. Test
R70 centre (10.55,6.5) mm, angle 270°, and TP31 centre (11.9,7.75) mm, with
the existing test-land shape, size and orientation. Only these two poses may
change in the first trial. Source switch/logic/module courtyards, copper-edge
clearance, probe access and all previous interfaces remain constraints.

Retire only the following three obsolete items, re-deriving their original
contacts from the immutable source:

- `8c491cd1-dd01-5b1a-9d4e-340b2b65fe19`: the sole B.Cu EN1 leaf from
  (95.751262,22.750001) to (96.251262,24.250001) mm, joining the old R70/TP31.
- `9ced2287-042b-5ca1-9293-c90554a352a8`: R70's +3V3_USB In4/B microvia
  at (95.751262,21.750001) mm.
- `4e80acb9-3235-5100-af33-030e33569108`: the coincident In3/In4 microvia,
  whose In3 contact reaches the existing connected USB logic-supply plane.

Restore the pull-up supply to actual retained U23.5 copper and the EN1 node
to actual U23.4 and TP31.1, using ordinary 0.2 mm B.Cu only. Each new supply,
output and test-land branch must be ≤16 mm. No new via, arbitrary zone anchor,
current-limit change or additional retirement is allowed. Both control and
supply branches must be restored together, with the old 32-pad supply group
and every other source physical group retained. All ADR 0117 additions,
converter geometry, part identities, rules, nets and safety boundaries stay.

TI SCES295AB, October 2025, Figure 4-1 and Table 4-1 confirm U23's exact DBV
package map: NC 1, A 2, GND 3, open-drain Y 4, VCC 5. The present symbol and
footprint mapping are retained. Preserve USB_EN1_RAW_N as a separate hardware
node; application firmware does not gain control of the fail-safe limit.

Selection requires exact pose/copper/contact ledgers, all prior groups,
native/physical reduction, exact unchanged 104-finding DRC, stable independent
replays/refills, current source, injected faults and visual review. Test-land
access, pull-up/permission timing, controlled stack, electrical/process/fit
qualification and independent Gate A remain open. No fabrication release or
hardware operation is claimed.


The initial unsaved (11.2,4.5)/(11.3,2.5) mm template intersects fixed U53's
courtyard and is rejected before routing or PCB output. The revised poses
above use the space below U53 and above the controller module, with the EN1
lead passing below the U23/U24 pad row. The same three-item retirement and
16 mm ordinary-width branch bounds apply; no other source interface changes.


The intermediate (11.5,6.25)/(11.5,8.0) mm candidate preserves all 223
source groups and counts 34 opens, but adds two findings at the retained
USB_OUT2 track. It is rejected. The revised vertical R70 pose above reserves
separate ordinary-width supply/output paths through the existing inter-part
channel. TP31 shifts upward 0.25 mm to clear that fixed track. All three
original retirements, unchanged source interfaces and ≤16 mm bounds remain.


The (10.25,6.5) mm resistor trial still approaches the retained USB_RAW_OUT1
capture too closely. Shift R70 right by 0.30 mm and TP31 right by 0.40 mm,
using the exact revised poses above. Keep that source capture untouched;
reserve x=9.90 mm for the EN1 vertical lead and y=5.45 mm for its upper
horizontal lead, with the independent supply lead at x=10.45/y=5.00 mm.
No additional retirement, via, source-group loss or branch-length increase.


## Selected source

The [implementation review](../development/usb-en1-routing-2026-11-12.md)
selects 34 native/physical opens, with all 223 preceding groups retained,
exact unchanged 104 findings, deterministic independent replays, twelve native
fault rejections, source and visual checks. Only the two recorded poses,
three retired items and eleven ordinary B.Cu tracks are selected. Every
other copper item, corrected RSE pin and safety boundary remains unchanged.
