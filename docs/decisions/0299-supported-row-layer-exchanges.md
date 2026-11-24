<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0299: Bounded supported row layer exchanges

Date: 2026-11-24
Status: Accepted for bounded complete-cell RAM continuity discovery.

The monotone and outer-return graphs do not establish a row join. With
the frozen proved selector already present, permit supported bidirectional
layer exchanges on the same original/alternate three-part front cells:
F/In2 via an actual aligned F/In1 plus In1/In2 0.30/0.10 mm pair;
In2/In3 via one0.50/0.30 mm mechanically drilled buried via;
In3/In4 and In4/B each via one0.30/0.10 mm supported outer microvia.
Actual ordinary0.20 mm In4 traces may separate lower transitions.
At most eight new physical holes per completed row path, counted including
both members of an outer stack. No new hole type/span, centre microvia,
through hole, additional source retirement or rule/current/profile change.

Keep x72..90/y7..22 mm and18 mm new conductor. Search0.050 mm/300000
states, then0.025 mm/300000 if needed, at most16 full native candidate
rejections per pass. Repeated hole positions do not gain exemptions:
all source/mutual native drill policy applies, supported-disjoint and
exact adjacent-outer-stack alignment only. No mechanical alignment waiver.
Source/new Cu and actual original pad-group/contact proofs are unchanged.

Only a full20-open/all210-old-group RAM result with ROW18/selector3/gate4/
VLED40/GND197, all19256 retained attached source Cu and no orphans can
advance to separate exact PCB qualification. No partial selection or PCB
write. Original DRC/replay/inverse/fault/visual/part/timing/electrical/stack/
independent Gate A holds remain; fabrication is prohibited.
