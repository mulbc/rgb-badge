<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Coupled CC1 continuation, 2026-11-12

**No successor is selected.** The immutable board remains at 34 native/physical
opens. [ADR 0123](../decisions/0123-usb-cc1-return-and-supply-restoration-study.md)
bounds these ignored trials; none changes canonical parts, pins, poses,
profiles, rules, zones or accepted-source copper.

A 600,000-node through-enabled search finds a 345-item USB_CC1 path, but native
refills split the original APP and battery supply groups. Two subsequent
ordinary-width joins restore both APP branches, adding seven items. Native
DRC also identifies two mixed-drill co-location warnings in the new CC1 stack.
The same-point through-via substitute is blocked on F.Cu and is rejected before
saving a PCB.

A finite central-via offset screen samples 2,516 positions. It rejects 1,020
at copper and 147 at hole clearance; 1,349 are shape-clear. The first native
trial offsets only the new central via by 0.50 mm to (105.60,17.80) mm and
adds two ordinary-width In2/In3 stubs. All preceding trial groups survive three
stable refills. Full native DRC now equals the **exact original 104 findings**.
Independent comparison confirms every selected-source copper item, part,
local pad, pose, profile, zone/net/setup/outline structure is unchanged.

That corrected trial has **34 native and 34 physical opens**, but loses the
original battery group while gaining CC1 continuity. The unchanged count
therefore does not establish source retention or progress. It is rejected.
Its 354 additions are recorded only as an unselected ledger.

A 2,400,000-node restricted-layer battery restoration reaches its bound.
Expanding actual filled-component endpoints to 45 mm also selects no join.
Finite direct and bottom-edge In3 bridge templates are obstructed; only three
full-span sites survive the corresponding broader site screen, with no
complete bridge. These results do not prove impossibility.

An ignored search allowing supported In2 routing finds a 46-item battery
bridge after 34,855 expansions. Refills restore the battery but split seven
original USB-supply members. The trial has **35 native versus 34 physical
opens**, with two historical USB vias newly dangling. Its 106 findings and
source-group loss both reject it. Subsequent bounded USB restoration from
U11 and from an actual affected via selects no join. No source via is deleted,
renamed or retyped to hide those findings or reduce the count.

The [machine record](../../mechanical/review/cc1-coupled-continuation-2026-11-12.json)
contains independent group/retention audits, exact additive ledgers, raw
hashes and explicit rejection reasons. Temporary search changes and all trial
boards remain ignored; canonical search policy is unchanged. The retained
34-open board and all original safety/current/default-off settings remain
unchanged. New power bridges demonstrate CAD continuity only, with current,
return, thermal, controlled-stack/process/fit and independent Gate A still
unresolved. Fabrication remains prohibited.
