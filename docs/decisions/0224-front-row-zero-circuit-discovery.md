<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0224: Front-side row-zero circuit discovery

Date: 2026-11-19
Status: Accepted for exact read-only geometry/interface discovery only.

Use only qualified 26-open front-R11 source SHA-256
fb862c0a548599b7acf328ad8bb5006ce5f78d8b98ceec12bb4af9ace21f1d0f.
Earlier B-only PAIR01/R6 templates fail fixed courtyards. Read-only test the
same exact trial NTLJD3119C PAIR01 package and Panasonic ERJ2RKF1001X R6 on
F outside the LED array: native top-bottom flip, PAIR01 (76.800,4.000) mm /
180 degrees and R6 (79.400,4.000) mm / 180 degrees. Keep every numbered net,
package geometry, field/value/identity and all other part poses unchanged.
The trial transistor remains trial-only; there is no schematic/BOM substitution
or manufacturer/electrical/assembly/optical/fit approval.

Use actual F.CrtYd for all source and proposed parts, mutual package spacing,
all foreign/no-net source copper and actual 0.500 mm edge clearance. In this
read-only collision screen prospectively omit only the four obsolete ROW_00_A
items: B wires `329b460c-8db8-5471-aa3d-6bc74fb6328c` and
`a90dd514-65b8-51ed-a644-a16f7b8fa358`, old through via
`58ef0e36-a584-5901-94b7-bdcd21043176`, and In3 tail
`ece50bc8-d79b-5083-b864-e16c9299007a`. First catalogue all outside pad,
copper and filled-plane contacts. Retain the actual LED-row interface at
(74.700,2.599999) mm, both LED-half links and every other source item.

Screen ordinary F local gate/R6 supply leads, a ROW_00_A output lead to that
actual retained F row port, a VLED lead to actual retained main F supply
(79.100,7.800), and a GND lead to actual retained main F ground
(82.600,5.250). Gate ≤3 mm, R6 pull-up supply ≤5 mm; each high-side VLED/
row-output lead ≤6 mm; low-side gate-driver GND lead ≤12 mm. Screen a supported
F/In1 0.30/0.10 mm selector access at PAIR01.2 and discover ordinary In1
restoration to actual retained ROW_SEL_00 copper only if source/mutual copper
and full-board hole rules pass. No new central/through transition is allowed.
Any new via-in-pad remains explicitly unqualified for fabrication/process.

Inventory the obsolete original PAIR01 gate straps, its private selector
branch and R6 supply leaf without retiring them. The old R6 shared stem
must retain every original junction as required by ADR0119. No material
other than the four frozen row-output items may be omitted in this screen.
Write no PCB. A complete prototype needs a separate exact cohort/pose/lead
plan, independent pin transforms and intrinsic-finding normalization, every
214 original group/retained copper/contact restored, reduced matching counts,
exact104 and all full successor gates. Current/protection/default-off and all
electrical/return/thermal/assembly/fit/stack/process/Gate A/fabrication holds
remain unchanged; no hardware performance or current-capacity claim is made.

The first exact 180-degree pair pose has clear courtyards but conflicts with
two retained ROW_A2 F wires. Retain that rejected raw result. Separately
sample PAIR01 F at 0 degrees, x=76.000–82.000 / y=3.000–5.000 mm in
0.050 mm steps, with exact R6 F at 180 degrees placed 2.600 mm right of
the pair centre. This cardinal change is explicit; derive actual pin positions
from native source orientation rather than assuming the original was zero.
In this refinement retain the original ROW_00_A PTH and In3 tail; use the
actual retained PTH at (77.250,4.400) mm as the row-output interface. Only the
two obsolete B row-output wires may be omitted in the collision screen.
Bound a new row-current lead to that original interface by 6 mm and keep
all other source items fixed. Correct front courtyards and all source/mutual
pad copper remain mandatory; no PCB or part/substitution/qualification change.

The bounded 0-degree template yields 269 pad/courtyard-clear poses, but the
retained ROW_A2 F L-route separates the existing front power/row interfaces.
Test one independent exact 270-degree PAIR01 F pose at (75.900,4.300) mm
with R6 F at 90 degrees at (75.900,6.900) mm. In this variant omit only the
original four frozen row-output items listed above and target the original
F row port (74.700,2.599999), leaving all address/control copper untouched.
Use ordinary F package straps/gate and R6 supply leads within the same bounds.
Screen three supported F/In1 0.30/0.10 mm accesses at the actual new PAIR01
GND, selector and VLED pads. Ordinary In1 VLED lead to actual retained VLED
at (79.100,7.800) remains ≤6 mm; GND/selector leads to actual retained same-net
In1 copper remain ≤12 mm. Explicitly retain the fabrication/process hold for
these new via-in-pad transitions; no current rating or process approval is
inferred. No central transition, new through via or other prospective source
retirement is allowed in this read-only variant; write no PCB.

The initial 270-degree pose has all three supported capture copper/hole checks
clear but overlaps two existing LED courtyards. Recheck an exact +0.200 mm X
translation of both proposed parts, keeping all other coordinates/angles and
bounds fixed. Test actual individually witnessed main-net In1 filled polygons
at each proposed capture; a direct plane connection needs that native witness,
not a zone name or assumption. Retain all same source omissions/holds and
write no PCB.

The +0.200 mm variant clears actual front courtyards/pads and all three
supported accesses/holes. Its VLED capture directly touches original main
VLED In1 polygon 4 of zone `566adf1a-30fb-5b01-a217-ee87a01be9a9`, witnessed
by retained main via `ebf485b5-1cef-5855-ae42-f9dce4471a0f`. Omit the separately
blocked exploratory In1 VLED lead; no added power trace is needed on In1.
The direct ordinary In1 GND lead to (82.600,5.250) mm clears all source/mutual
copper. Discover the remaining selector In1 lead with exact native 0.025 mm
eight-neighbour steps, ≤12 mm conductor length and at most 100,000 nodes,
within x=74.500–84.000 / y=2.750–10.750 mm, targeting actual retained main
selector via (77.750,9.650) mm. Keep all selected source items fixed except
the same four prospective row-output omissions; write no PCB. Final native
refill still must preserve the power-plane contact and every original group.
