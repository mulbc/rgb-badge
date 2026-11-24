<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0143: Exact outer-capture transition screen

Date: 2026-11-14
Status: Accepted for read-only native discovery; no successor selected.

Continue from ADR 0142's immutable 30-open selected source, SHA-256
`90db778d8e44b2c71ab5e1f5d8a1c586ee71c25d46892b1406c4792ac7720abd`.
Its exact non-grid adjacent transition enabled a group-preserving route.
Screen whether other disconnected control/row/clock groups have similar actual
retained captures that a 0.05 mm routing grid cannot transition at directly.

Read-only scope: DISPLAY_CLEAR_OK, ESP_EN, HEARTBEAT_SEEN, CHARGER_EN2,
CHARGER_TS, LED_GCLK, LED_LAT, LED_SCLK, ROW_GATE_00/02/03/04/06/07,
DISPLAY_HEARTBEAT and HEARTBEAT_FALL_CLK. Use only actual source group copper,
part identities/numbers/nets and existing 0.30/0.10 mm microvia positions.
Report whether each non-grid actual B/In4 capture permits an exact In3/In4
0.30/0.10 mm transition, or the reverse; similarly test the two supported outer
F/In1 and In1/In2 spans. Never propose a new In2/In3 microvia. Do not alter,
retire or reinterpret any historical via type or source item.

Every prospective transition must share exactly the existing 0.10 mm hole;
all other hole spacing, native foreign/no-net/mechanical copper on both actual
layers and native board/cutout edge checks remain unchanged. Exclude duplicate
existing captures and record exact source UUID/group/geometry/blockers.
This screen writes no PCB and makes no circuit join. Before implementation,
freeze the exact clear prospective cohort and refill-preservation scope in an
additional decision paragraph. Every one of the selected source's 218 groups,
all original items/poses/rules/profiles, exact old findings, full successor
replay/orphan/fault/source/visual gates and all existing safety/qualification/
Gate A/fabrication holds remain mandatory. Zero opens remains unfinished.

The retained-capture discovery finds no eligible missing non-grid outer capture
on the sixteen scoped open nets. The row-gate source inventory shows that the
disconnected PAIR groups have no retained vias. Test a bounded fine-grid ordinary
route for ROW_GATE_02 between its actual R8/PAIR03 groups, using 0.025 mm grid
centres only within x=70..78, y=5..12 mm. Keep explicit native board-edge checks
and prevent endpoint leads from leaving that region. Permit only ignored new
0.20 mm tracks and supported adjacent 0.30/0.10 mm or centre mechanical buried
0.50/0.30 mm vias. No source part/item/pose, rule or net changes. Preserve every
one of the selected 218 groups after every refill. A sampled lower count remains
unselected until exact findings and all full successor gates pass. No new
narrow-width exception, centre microvia or fabrication authority is introduced.
