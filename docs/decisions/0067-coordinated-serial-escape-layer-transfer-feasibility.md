<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0067: Exact coordinated serial-escape layer transfers

Date: 2026-10-30
Status: Selected only as the exact independently checked 59-edge source transaction.

The ADR 0065 local search cannot reach In3. Native frontier analysis identifies
38 reachable sites where exactly one original COL_15_R In3 track obstructs an
adjacent microvia. Its potential In2 transfer is itself obstructed by COL_15_G
on In2. These are exact original RGB fanout tracks, not generic deletion rights.

Permit one ignored coordinated experiment using only these source signatures,
all at the original 0.20 mm width:

- COL_10_B: In4, (84.40, 1.60) → (61.70, 1.60) mm, under ADR 0065's exact
  local source interfaces and original-plus-2-mm aggregate length bound.
- COL_15_R: In3, (82.75, 1.75) → (74.10, 1.75) mm; transfer only the interval
  x = 80.50–81.70 mm to In2, retaining both original-layer end portions.
- COL_15_G: In2, (82.75, 1.75) → (74.60, 1.75) mm; transfer only the interval
  x = 79.90–82.30 mm to In1 or F.Cu through adjacent microvias, retaining both
  original-layer end portions. Stagger its via sites outside the red interval.

The latter two aggregate replacement lengths may not exceed their originals
plus 2 mm each. Preserve every original direct same-layer contact, all other
source/accepted copper, every 60-edge pad group, component pose, zone and earlier
exception. Keep 0.20 mm clearance and 0.30/0.10 mm adjacent microvias. The only
trial narrow copper remains ADR 0047 LED_SOUT, with its unchanged 120 mm bound.
The unchanged TLC59581RTQT output maps/settings are covered by the already
reviewed [TI TLC59581/82 Rev. A](https://www.ti.com/lit/ds/symlink/tlc59581.pdf).
No current, protection, enable, part or package change is permitted.

Selection needs a new exact independently enforced source/interface/length
catalog for all three originals, frozen 60-edge retention, lower native/physical
counts, unchanged full 104 findings, stable fills/replay, source/fault checks and
unchanged original-orphan restoration. In1 power-plane interruption is a
rejection, not permission to reduce clearances or discard old pad groups.
Electrical/current/thermal/return/process/assembly review and independent Gate A
remain open; this is not a fabrication release.

## Exact fourth-layer obstruction

The initial three-track candidate is rejected before refill: original COL_14_B
on In1 occupies the proposed green transfer sites. Extend only this ignored
coordinated case to its exact original signature, In1 (82.75, 1.75) →
(74.60, 1.75) mm, width 0.20 mm. Retain the In1 portion to x = 79.30 mm and
transfer x = 79.30–82.75 mm to F.Cu with adjacent In1/F microvias, retaining the
original right endpoint/interface on In1 through its exact new via. Move green
only to In1 over x = 79.90–82.20 mm, with staggered In2/In1 sites. Keep each
aggregate colour length within original plus 2 mm and derive every original-
layer contact independently. No other original, prior addition or package may
change. The same lower-count, full DRC, group, replay, fault/source and orphan
requirements apply before any canonical selection.

The ignored search may include retained right-side COL_10_B fanout contacts up
to x = 85.20 mm. The earlier x = 84.40 mm box omitted retained staircase/portal
contacts beyond the retired horizontal segment. Joining an existing same-net
portal is allowed without recreating it; this does not authorize retirement or
new clearance violations at that portal. Original-plus-2-mm length bounds and
all other source/geometry/validation requirements stay unchanged.

## Prechecked candidate and exact-policy implementation

The 59-edge candidate preserves all 60-edge copper other than the four originals,
all poses/zones/physical groups and all 24 newly derived original-layer contacts.
Calculated COL_10_B length is 24.537006 mm versus 22.7 mm original; the other
three lengths remain 8.15/8.15/8.65 mm. A short serial detour and three full-width
ground bridges preserve old plane groups. Straightening only unaccepted serial
copper yields 117.886618 mm of 0.12 mm LED_SOUT track, below the unchanged
120 mm bound. Three fills and original-orphan restoration pass at 59 opens with
104 unchanged findings (+3 original dangling vias only in the restoration).
Implement only these exact source/interface and digital catalogs, freezing the
complete 60-edge plan. Promotion still requires full replay/native/fault/source
checks. No accepted added copper or original zone is retired.

## Selected checkpoint

The [59-edge study](../development/led-routing-progress-59-study-2026-10-30.md)
passes full native/physical counts, all prior groups/copper/poses, 24 new source
contacts, 104 unchanged findings, stable fills/replay, original-orphan restoration
and 58 native/116 portable guard methods. The exact catalogs are selected for
only the four enumerated originals and LED_SOUT. All preceding exceptions and
electrical/fabrication holds remain fixed; the 50-edge target remains open.
