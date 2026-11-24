<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0138: Ordinary additive continuation screen

Date: 2026-11-14
Status: Accepted for ignored routing feasibility; no new source selected.

The selected source remains ADR 0136's immutable 32-open checkpoint. ADR 0137's
ignored clear-output candidate has 31 native/physical opens, exact original
104 findings under the frozen U52 pose transform and all 220 selected source
groups retained. Its SHA-256 is
`ad729d4fcdba406c6b2db4aa10b8288035fa194c5059d7ecc3c4e0be5fbbdc2d`.
It joins U52.4 to the R108.1/U49.2 group; U50.2 is still separate.
This preliminary candidate has not passed the full successor gates.

Permit ignored ordinary 0.20 mm additive searches from that exact candidate for
LED_SCLK, LED_GCLK, LED_LAT, ROW_GATE_00/02/03/04/06/07, ESP_EN, CHARGER_EN2,
CHARGER_TS, DISPLAY_HEARTBEAT, HEARTBEAT_FALL_CLK, HEARTBEAT_SEEN and DISPLAY_ENABLE.
Do not move any part, retire or change existing copper, narrow any track,
change rules/profiles/board/zone geometry or alter any current/protection/NTC/
timer/default-off setting. This is physical continuity feasibility only, with
no electrical qualification of charger sense, clocks or control circuits.

Use only supported adjacent 0.30/0.10 mm microvias and 0.50/0.30 mm centre
mechanical buried vias. Check native copper including foreign/no-net/mechanical
items, all holes and board/cutout edges. Retain every current pad group after
each native refill, including the new clear-output group. Record bounded
search outcomes rather than claiming global impossibility from sampled failures.

No lower count is selected until native and physical counts agree, all 220
selected source groups and preliminary joins survive, full original 104 finding
payloads match under the already frozen U52 pose, the complete addition ledger
is frozen, independent source replays/refills and removal/orphan/native-fault/
source/visual gates pass. No extra finding, ignored check, unsupported centre
microvia, changed component or fabrication release is authorized. All existing
part/electrical/stack/process/fit and independent Gate A holds remain.
