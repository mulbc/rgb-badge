<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Clear-output routing checkpoint, 2026-11-14

The selected CAD study now has **31 native and independently counted physical
opens**, down from 32. U52.4, U49.2 and R108.1 are one DISPLAY_CLEAR_OK group;
U50.2 remains separate. All 220 predecessor groups survive, with 219 current
groups on 188 nets. The zero-open goal is still unfinished.

[ADR 0139](../decisions/0139-clear-output-routing-checkpoint.md) selects
[the project](../../hardware/coupon/rev-a/staging/led-ordinary-routing-trial-114mm.kicad_pro).
The [complete plan](../../mechanical/review/ordinary-routing-plan.json) freezes
57 additions and every native original-layer contact witness. All 19,226 prior
copper items and their native via types, 483 parts/fields/local pads/poses and
board/net/zone/rule/profile structure remain unchanged. No original copper is
retired, and no new narrow-width exception is needed.

The actual U52 land edge admits 0.20 mm copper. Fifty-one ordinary-width tracks
and six supported vias connect to the existing clear-output leaf. Calculated
new track length is 25.273080 mm; this is a layout calculation, with no delay,
impedance, return-path or powered-operation qualification implied. Adjacent
microvias use 0.30/0.10 mm diameter/drill and centre mechanical buried vias use
0.50/0.30 mm. No centre microvia or electrical setting is added or changed.

## Validation

- Native and physical counts agree at 31. Every one of the selected source's
  220 live groups and its completed CLEAR3 connection survive. Exact native
  source/part/structure/profile and original contact checks pass.
- DRC retains exactly the original 104 full finding payloads. Only the already
  frozen U52 coordinates follow ADR 0136's independently checked transform.
  UUIDs/pairs/descriptions/actual clearances/severities and ignored checks stay
  unchanged; no warning is waived.
- Two independent source-ledger replays, each with three stable refills, match
  selected SHA-256 `4b14dd289f0f9908d9c9f2339a37bb29896bec00ba805e2c6742a52eb241cb2c`.
  The preliminary search snapshot has different cached fill geometry and is
  not selected; no geometry equivalence to it is claimed.
- Removing every new item restores the exact 32-open source bytes across three
  stable fills, all 220 source groups and the exact original findings. All
  nine filled-zone integer XORs are empty. Both selected source files remain
  immutable.
- Eleven native faults reject changed part/net/pose/source copper, narrowed or
  extra tracks, wrong via type/drill, omitted original contacts, removal of the
  actual longest connection track and removal of the whole join. The actual
  disconnection cases exercise connectivity independently of ledger rejection.
- All 34 source-workflow commands pass. Native old/new B.Cu, In4.Cu, In3.Cu,
  In2.Cu and In1.Cu views were rendered; the five new layer views and old B.Cu/
  In2.Cu were inspected with the added copper highlighted.

## Continuation findings

ADR 0137's straight 0.750 mm local neck screens find no clear capture for
U52.2 or U52.4. An ordinary-width tip exists for U52.4 and enables this join;
U52.2 has no sampled clear straight full-width tip. The unchanged existing
0.12 mm package rule is not expanded.

The remaining U50.2 clear-output join reaches the 300,001-node bound from each
group. ADR 0138's sixteen-net ordinary-width continuation makes no further join
in 32 directional attempts: fifteen sampled components exhaust, eleven reach
the 120,001-node bound and six have no usable grid endpoint. These are bounded
search outcomes, not a proof that no other route or floorplan can work.

Reproduce the selected acceptance gates with `tools/check-ordinary-routing.sh`.
The [checkpoint](../../mechanical/review/ordinary-routing-checkpoint.json) records
all raw hashes, search outcomes, checks, replays, faults and inspected views.
Zero opens, electrical/timing/return/thermal/part/process/fit/controlled-stack
qualification, the 557 historical centre microvias and independent Gate A
remain open. No fabrication or hardware measurement is claimed or authorized.
