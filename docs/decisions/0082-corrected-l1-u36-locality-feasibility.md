<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0082: L1/U36 locality on the cleaned full-stage candidate

Date: 2026-11-01
Status: Ignored finite geometry screen only; no new source selection.

The ADR 0081 cleaned VLED candidate has 52 native/physical opens / 104 intrinsic
findings and preserves every earlier group. Its remaining U36 LX1/LX2 nets are
open to remote L1. Use exact cleaned replay SHA-256
`7c5196b19decc3a4fbaf5724a24aae479a0fdb9c2679706f3cc5f86253992e11`;
canonical source remains the accepted 58-edge checkpoint.

Re-read the cached TPS631000 Rev C (August 2026) pin table/layout/DRL0008A
land drawing (PDF pages 3/18/26) and supplied Murata DFE252012P page 1. Exact
parts stay TPS631000DRLR U36 and DFE252012P-1R0M=P2 L1. U36.3 is LX1 and
U36.2 is LX2; U36.7 is power ground. U36.6 is MODE tied low, not a substitute
ground-return pin. Retain the current 0.67 × 0.30 mm DRL lands at ±0.74 mm,
0.5 mm pitch and exact current DFE 0.80 × 2.00 mm lands at ±1.00 mm. No footprint
or value migration is permitted. Manufacturer guidance still requires short,
wide power/bypass paths and quiet FB routing; geometric ordinary-width probes
do not satisfy that qualification by themselves.

First repeat the finite L1-only screen with U36 and every other component fixed:
0.10 mm positions, 15° angles, at most 8 mm from U36, unchanged 0.20 mm native
foreign clearance and 0.50 mm copper-edge clearance. Record exact courtyard/
pad obstructions and clear poses. Centre distances remain planning observations,
not pad-edge routing bounds or an impossibility proof.

If useful, a separate compact-pair screen may move only U36/L1. U36 centres use
0.125 mm offsets in dx = -12…+2 mm, dy = -4.5…+2.5 mm from its current centre,
within a 12 mm displacement radius, and cardinal rotations only. L1 centres lie
2.65/2.90/3.15/3.40 mm outward from the actual native LX pin side with -0.25/0/
+0.25 mm tangential offset; choose its cardinal orientation to align pad 1 with
U36.3 and pad 2 with U36.2. This is a finite template screen, not a global optimum.
Use actual native pin positions so bottom-side rotation/polarity is explicit.

Retain every copper item and all other 481 poses/parts/local pads/fields, zones,
structure, profiles/rules and electrical settings. No retirement, new via or
other net is unlocked. Test only two local B.Cu switching paths, 0.20 mm wide
at unchanged 0.20 mm clearance, at most 5 mm new track per switching net. Begin
with a short outward lead then a direct fanout to each numbered coil land.
Check both new paths against old copper, foreign pads and each other. Reject
courtyard/pad/edge violations and report all accepted prior-group losses after
fill. Intermediate SYS/+3V3_APP/APP_ON_SW_DRAFT/APP_3V3_FB losses may be recorded
as unselected observations; reject any new GND or other-net split. No pose may
be selected before every old/current group is restored and full independent
native/physical/DRC/replay/fault/source/original-orphan evidence passes.

Retain all current limits, protection, MODE/EN connections, hardware interlock
and firmware. Nearby bypass/feedback/return layout, power widths, exact capacitor
lands/order codes/effective capacitance, electrical/thermal/EMI/process/assembly/
fit qualification and independent Gate A remain open. No fabrication is allowed.

## Recorded result, 2026-11-04

The [finite native evidence](../development/l1-cleaned-locality-2026-11-04.md)
records zero clear poses across 481,944 fixed-IC samples and 302,640 regional
pair templates. All 86 fixed-IC pad failures and 351 external coil failures
have witnesses; the 51 clear IC poses cannot accept a clear coil template.
Seven source/output/basis rejection cases pass. No board/route is exported,
source bytes remain unchanged, and broader coordinated floorplanning remains
open. This finite result is not a global impossibility claim.
