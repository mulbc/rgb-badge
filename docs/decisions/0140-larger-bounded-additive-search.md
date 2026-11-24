<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0140: Larger bounded ordinary additive search

Date: 2026-11-14
Status: Accepted for ignored native feasibility; no successor selected.

Continue from ADR 0139's selected immutable 31-open board, SHA-256
`4b14dd289f0f9908d9c9f2339a37bb29896bec00ba805e2c6742a52eb241cb2c`.
All 219 current groups, every source copper item/part/pose/pad/net and the exact
original 104 findings under the already frozen U52 transform must survive.

The preceding 120,000-node ordinary search leaves several directional attempts
at its bound. Test a larger 400,000-node bound with heuristic weight 6, without
claiming optimality or global impossibility. Scope only DISPLAY_CLEAR_OK,
ESP_EN, HEARTBEAT_SEEN, CHARGER_EN2, CHARGER_TS, LED_GCLK, LED_LAT, LED_SCLK,
ROW_GATE_00 and ROW_GATE_03. A search failure on one bounded/directional grid
is not proof against another valid route.

Retain ordinary 0.20 mm new tracks, supported adjacent 0.30/0.10 mm microvias
and 0.50/0.30 mm centre mechanical buried vias. No component move, source
retirement/change, wider narrow-rule exception, new centre microvia, board/
zone/rule/profile change or electrical/current/protection/NTC/timer/default-off
change. Check native copper/no-net/mechanical items, all holes and board/cutout
edges; preserve every live group after every refill. An ignored lower count
is not a selected result. Exact full finding payloads, complete additive ledger,
independent stable source replays, removal/orphan proof, native faults, source
checks and visual review remain required before selection. Zero opens and all
part/electrical/timing/return/thermal/stack/process/fit/Gate A holds remain;
fabrication remains prohibited.
