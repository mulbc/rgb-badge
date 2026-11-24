<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0139: Select the full-width clear-output join

Date: 2026-11-14
Status: Accepted for CAD continuity only; fabrication prohibited.

Select `led-ordinary-routing-trial-114mm`, SHA-256
`4b14dd289f0f9908d9c9f2339a37bb29896bec00ba805e2c6742a52eb241cb2c`,
as successor to ADR 0136's immutable 32-open source. Native and independently
counted physical opens agree at 31, with all 220 predecessor groups retained.
U52.4 joins the existing R108.1/U49.2 DISPLAY_CLEAR_OK group; U50.2 remains
separate. No part, pose, existing copper, rule or circuit setting changes.

Freeze the complete 57-item additive [plan](../../mechanical/review/ordinary-routing-plan.json).
Its 51 tracks use 0.20 mm width; six supported vias use adjacent 0.30/0.10 mm
microvias or centre mechanical buried 0.50/0.30 mm vias. Preserve all 19,226
source copper items and native via types, all 483 parts/fields/local pads/poses,
all existing joins and full board/net/zone/rule/profile structure.

The actual original land contact permits ordinary-width copper without a new
narrow neck. Full DRC retains the exact original 104 finding payloads under
ADR 0136's unchanged frozen U52 coordinate transform; no other transformation,
new finding or ignored check is allowed. Two independent exact-ledger replays,
each with three stable fills, match selected bytes. Removing all 57 additions
restores the selected 32-open source byte for byte, including all 220 groups,
original copper, filled geometry and exact findings. Eleven native faults,
all 34 source checks and native old/new visual review pass.

The first search snapshot has different cached fill geometry and is not the
selected board; only the independently rebuilt, fully checked stable source
above is selected. The [implementation record](../development/clear-output-routing-2026-11-14.md)
and [checkpoint](../../mechanical/review/ordinary-routing-checkpoint.json)
retain exact evidence. Reproduce with `tools/check-ordinary-routing.sh`.

Zero opens remains unfinished. Signal timing/return, power/effective-capacitance,
thermal/part/process/stack/fit qualification, 557 historical centre microvias
and independent Gate A remain unresolved. No current/protection/NTC/timer/
fail-safe USB/default-off boundary or fabrication authorization changes.
