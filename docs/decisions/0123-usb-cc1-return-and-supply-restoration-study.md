<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0123: Restore supply groups during USB CC1 routing

Date: 2026-11-12
Status: Accepted for ignored feasibility; no successor selected.

The ADR 0091/0092 additive search from the selected 34-open source
`92f942e46281475cbdadf6e9a0ad7a0d531e38c3032f85a4206bbf9e9bc1fccd`
finds a provisional USB_CC1 path from J1.A5 to U31.1, but rejects it after
native zone fills split existing +3V3_APP and +BAT_PROTECTED_DRAFT groups.
The rejected snapshot hash is
`ccc636909faeca02a8f29096945cb6670eb6db361278811751947b107326d345`.
No lower open count or isolated CC1 join authorizes adoption.

Permit additive restoration feasibility on an ignored copy of that exact
snapshot. Restore the former +3V3_APP members R106.1/U32.8 and the former
battery group C53.1/U41.2/U41.3 to their complete original source groups.
Retain every source part, pose, net, copper item and accepted addition,
including the corrected RSE mapping and ADR 0121 USB join. Preserve the full
original supply groups, rather than reconnecting only these listed members.
No current, charge, protection, permission or firmware boundary may change.

Use ordinary 0.20 mm copper and the existing supported adjacent microvia,
0.50/0.30 mm central buried-via or full-span via rules. No skipped-layer or
new centre microvia, arbitrary plane anchor, narrowing or DRC waiver is
allowed. Any native-filled plane destination must identify its actual
connected component. Restoration alone is not evidence of power-path current,
return, signal-integrity or thermal qualification.

Selection requires a frozen full copper/endpoint ledger, all 222 preceding
live groups, matching native/physical count below 34, exact unchanged 104
findings, stable independent replays/refills, source/fault checks and visual
review. Any remaining group loss rejects the candidate. The immutable source
remains at 34 opens until every acceptance gate passes. All controlled-stack,
557 centre-via, electrical/process/fit and independent Gate A holds remain;
fabrication is prohibited.

The provisional CC1 stack at (106.1,17.8) mm contains three newly added
coincident In1/In2, In2/In3 and In3/In4 vias. Native DRC reports two
`holes_co_located` warnings where their drill sizes differ. This trial is
rejected independently of its supply splits. An ignored correction may
replace only these three unselected CC1 vias with one 0.50/0.30 mm F/B
through via at the same point, screened on all six copper layers and against
all other holes. Source copper remains untouched. Exact unchanged DRC and all
prior groups must still pass; a warning is not waived as a stackup assumption.

The same-point through-via proxy conflicts with retained F.Cu copper and is
rejected before saving a PCB. As a separate bounded ignored correction, the
new 0.50/0.30 mm In2/In3 via may instead be offset 0.50–1.50 mm from the
original point, with two 0.20 mm In2/In3 stubs back to the two original
0.30/0.10 mm adjacent captures. Retire only the unselected central via;
retain all accepted-source copper and the two adjacent captures. Screen
actual copper on both layers and all hole clearances; require native fills,
all prior groups and exact DRC before further use. No offset is selected by
this permission or by a shape-only pass.

The remaining battery split separates the original In4 filled region near
x≤72.50 mm from the right region beginning near x=79.08 mm. Direct In3
bridges and bottom-edge elbow templates are obstructed by retained ROW_14_A,
ROW_15_A and return/supply copper. Broaden only the ignored additive search
to ordinary In2.Cu tracks (normally disabled by the search heuristic), using
supported 0.50/0.30 mm centre transitions and actual native-witnessed filled
components within 45 mm of C53. Such a bridge remains CAD continuity only:
all original ground, battery, USB and APP groups must survive refill; return
and current-carrying qualification remains open. New mixed-drill captures
must be spatially separated, rather than relying on coincident-hole warnings.
This is no waiver of width, clearance, topology, DRC or source retention.

The ignored supported In2 battery bridge restores the battery group but splits
seven members of the original USB-supply group. It is rejected by the native
transaction guard. Permit additive restoration of this exact original USB
supply group as part of the coupled trial, using the same ordinary widths,
supported spans, individually witnessed plane components and full-group/DRC
checks. Preserve the previously isolated U39.5 as an independently counted
open unless its actual circuit connection is also completed. A partial USB
group restoration cannot satisfy acceptance, and the selected source stays
at 34 opens throughout these experiments.

## Recorded continuation

The [coupled review](../development/cc1-coupled-continuation-2026-11-12.md)
selects no successor. The offset trial retains exact 104 findings but loses
the original battery group. Its battery-restored descendant loses seven USB
members and has native/physical disagreement plus two dangling via findings.
No existing source copper is deleted to conceal these losses. The selected
34-open source remains immutable; complete coupled restoration remains open.
