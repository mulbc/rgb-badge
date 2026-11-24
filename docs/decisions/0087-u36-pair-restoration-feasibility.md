<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0087: Exact newly clear U36/L1 pair restoration

Date: 2026-11-05
Status: Ignored restoration/cleanup feasibility; source adoption needs its gate.

ADR 0086 finds a clear compact pair outside the earlier search rectangle:
U36 (108.75,12.50) mm at 180°, L1 (111.65,12.75) mm at 90° on B.Cu.
Numbered LX1/LX2 paths calculate to 2.452998/2.238170 mm. The filled first
probe retains the 104 intrinsic clearances but loses U36.1 from its old
+3V3_APP group and U36.4 from its old SYS group. Native opens stay 52:
two new local joins are offset by those two losses. Its exact raw PCB SHA-256
is eaf6b62dc0ad29f15cf6ca4aefb5a7664ee4090ee898cc76c982ffd8cd27b158.

Permit ignored ordinary-width additive restoration only on +3V3_APP and
+SYS_APP_IN_DRAFT, from U36 to current largest physical groups on those nets.
Use exact native endpoint/foreign-shape screening, 0.20 mm width/clearance,
0.30/0.10 mm adjacent microvias, at most 25 mm added track per net and
400,000 expanded search nodes per join. Reject any current-group split after
refill. Preserve all existing/new copper, other 481 poses, canonical local pads,
parts/fields/zones/rules/settings. Require all original 52-edge groups restored
and exactly 50 native/physical opens before treating restoration as successful.

The raw pair also exposes one old 0.015 mm B.Cu VOUT leaf at (103.865,4.75)
and an old SYS In4/B microvia at (103.865,6.25). After restoration, allow only
an ignored bounded native dangling-copper peel within the vacated U36 rectangle
x = 101.5…104.5, y = 3.8…7.2 mm, on those two supply nets. Each retirement
must be a unique item present in the retained 52-edge input, reported dangling
by that round's complete DRC, with origin/contact ledger recorded beforehand.
Do not retire any new route item. Stop at ten rounds/twenty items or a boundary.
Preserve every old/current group and all other copper. No general cleanup or
new original-orphan waiver is granted. Canonical adoption needs a frozen exact
cohort and complete independent ledger/geometry/native/DRC/replay/fault/source/
original-orphan evidence; electrical/process/Gate A and fabrication holds remain.

## Exact shared-leaf trim after the bounded stop

The native peel reaches a 25.05 mm accepted SYS F.Cu leaf outside the window:
(103.865,6.750000) → (103.865,31.800000) mm, width 0.20 mm. It is absent
from the frozen 215-edge source. Its old upper via is now retired, but the
new supply route contacts it at (103.865,13.037450), and another new track/via
contacts its side at (103.950,13.600000). The retained bottom bus is
(84.000,31.800000) → (104.550,31.800000). Do not delete the active leaf.
Permit only exact replacement with its retained lower tail
(103.865,13.037450) → (103.865,31.800000), preserving every current track/via
contact and all old/current pad groups. Record all frozen/current interfaces
before trimming. The 18.762550 mm replacement lies wholly on old copper;
it is retained path geometry, separate from the 6.374988 mm new SYS route
and its 25 mm additive-restoration bound. Total source/retained/new geometry
and net-length deltas must be explicit, with unchanged full intrinsic DRC.
No other boundary extension or source-branch trim is permitted.

## Result

Restoration and the exact eleven-item cleanup/tail trim preserve every old/current
group at 50 native/physical opens and exact 104 intrinsic findings. The four
original/seven accepted retirements and retained active interfaces are selected
only through ADR 0088's frozen cumulative ledger and full acceptance evidence.
