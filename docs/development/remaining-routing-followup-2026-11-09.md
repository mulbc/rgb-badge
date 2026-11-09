<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Remaining-routing follow-up at the 37-open source

The selected source remains commit `e17fa35`, PCB SHA
`ed6d3ff570f2481b47423d8375d9d4a40d756145cdd49e2c222bacc36edbfa57`,
with **37 native/physical opens and the unchanged 104 intrinsic findings**.
None of the following ignored trials is selected. These are finite CAD
calculations and native shape/connectivity screens, with no hardware or
firmware measurement. The zero-open goal remains in progress; all existing
qualification and independent Gate A holds still prohibit fabrication.

The [machine-readable record](../../mechanical/review/remaining-routing-followup-2026-11-09.json)
preserves raw-result fingerprints, named-pad losses and search limits.
Raw scripts, rejected boards, profiles, reports and native layer crops remain
ignored under `hardware/coupon/rev-a/build/zero-open-routing/`. They are local
engineering evidence, not release outputs. A failed finite screen does not
establish that wider coordinated routing is impossible.

## Exact captures and ground approaches

An actual-pad-centre B.Cu/In4.Cu and F.Cu/In1.Cu capture screen covers all
27 nets with opens. No complete direct, diagonal or L-shaped candidate joins
two existing groups in this screen. Some captures are clear, so this result
does not rule out multi-segment routes.

The isolated U52.3/U38.3 ground group already reaches a retained three-via
stack at (70.800,1.150) mm. Direct B.Cu/In2.Cu main-ground-plane lead screens,
including C32.2 and PAIR01.1, find no clear sampled lead within 10 mm.
A separate radial In3.Cu approach to a provisional 0.50/0.30 mm In2/In3
buried via finds no complete candidate within 20 mm. An ordinary native-grid
In3/In2 search from the retained via UUID
`97ccc3b4-b320-5590-a539-8e61e5b2d653` exhausts its 285-node reachable
sampled graph. No new via, retired copper or ground connection is selected.

## R8 placement and one-track detour

[ADR 0102](../decisions/0102-anchored-r8-angular-locality-screen.md) extends
the earlier fixed-supply-pad R8 study to 72 orientations in 5° increments.
The exact ERJ2RKF1001X / 1 kΩ part, pad-1 centre and original direct supply
contact remain fixed. Twenty-seven poses exceed the 3 mm gate-pad separation
bound, forty interfere with foreign pad/track copper, and five have no clear
sampled ordinary B.Cu direct/L/dogleg lead. Those five also find no complete
sampled B.Cu/In4.Cu path with two adjacent captures. No pose is selected.

For the earlier +90° flip, the rotated gate pad and its capture are blocked
by exactly the B.Cu ROW_SEL_15 segment (68.900,7.850)–(73.350,7.850) mm.
An ordinary direct In4.Cu gate path to PAIR03.5 is clear in this hypothetical
pose; a direct B.Cu gate path additionally crosses the adjoining ROW_SEL_15
vertical and ROW_SEL_01/00 conductors. None is silently removed.

[ADR 0103](../decisions/0103-local-row15-detour-for-r8.md) bounds a replacement
of only that one horizontal ROW_SEL_15 segment. All six original direct B.Cu
contacts and both endpoints must survive. Rectangular-jog screening and a
0.05 mm native-shape B.Cu search find no replacement; the latter exhausts
851 reachable nodes. A B.Cu/In4.Cu transfer screen finds zero eligible left
and right captures in its sampled regions. The direct endpoint captures and
inner lead interfere with COL_06_R, and the left capture also interferes
with ROW_SEL_14 on B.Cu. Clearance between the proposed gate and selector
paths is included. No retirement or component move is adopted.

## Control routing and power-plane cuts

B.Cu/In4.Cu searches for USB_EN1_RAW_N, HEARTBEAT_SEEN and +BAT_GAUGE_SW
produce intended joins or exhaust their sampled graphs, but no transaction
preserves every accepted group. The rejected joins split VBUS_CONNECTOR,
+3V3_APP and/or +BAT_PROTECTED_DRAFT. A full six-layer search favouring B.Cu
reaches the 1,000,001-node bound for each of the two control nets.

The source has full-board +3V3_USB on In3.Cu, plus a higher-priority local
charger-input parcel. In4.Cu contains the application supply and higher-
priority battery/connector supply parcels. A full six-layer search favouring
In3.Cu finds a USB_EN1_RAW_N path after 154,394 expanded nodes. It splits the
original 32-pad USB-supply group into groups of 12, 12 and 8, and separates
the original battery-supply group into groups of three and two. Its native
and physical open counts differ: **40 native / 39 physical**. It is rejected.
The HEARTBEAT_SEEN search reaches the 1,000,001-node bound.

With the accepted local library table and rule profile, native DRC on the
rejected In3 trial reports **107 findings: the same 104 clearance pad pairs
and three additional dangling-via warnings**. The affected retained USB
centre vias are at (76.151904,30.849096), (76.951904,30.049096) and
(25.550,25.500) mm. These are actual trial faults; no waiver or report
filtering is used. The accepted 37-open PCB is untouched.

## Explicit supply restoration

Adjacent-layer bridge screening uses individual filled components with an
actual same-group copper witness, never a zone object's identity alone.
Each attempted bridge must preserve all trial baseline pad groups and every
source copper/net identity after refill. Sampled offsets through 8 mm find
clear In3/In4 capture pairs for the USB supply but no clear straight In4
lead. The battery supply has no complete candidate in this screen.

A separate B.Cu bridge with adjacent transitions restores the two 12-pad
USB groups into one 24-pad group. The remaining eight-pad USB group and the
three-/two-pad battery split persist. This partial restoration has **39
native / 38 physical opens** and remains rejected. Horizontal bridge screens
near the filled-component boundaries, including a wider 12 mm reach into
each component, find no further complete route. A
full native-grid supply search from retained via
`6a7f2d9e-27b0-5d5c-8875-67df650467f8`, protecting all current trial groups,
reaches its 700,001-node bound without another join.

Native B.Cu and In3.Cu crops at x=68–84 mm were rendered and inspected.
They confirm dense surface routing and multiple inner-layer trace bundles
around these gaps; colours alone are not used to infer net identity.
The numbered-pad/filled-polygon data establishes the reported splits.

Further useful routing must coordinate the remaining supply restoration
with the signal path, or replace an explicitly bounded obstructing cohort
while retaining its original contacts. Repeating the same shortest path,
counting only its intended join, or accepting disconnected planes would not
advance the zero-open objective. The selected source still requires actual
native/physical agreement, all previous groups/copper, exact full DRC,
replay/source/fault checks and visual review for any successor.
