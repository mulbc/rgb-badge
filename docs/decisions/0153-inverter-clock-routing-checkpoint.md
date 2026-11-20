<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0153: Select complete inverter clock routing checkpoint

Date: 2026-11-15
Status: Accepted for CAD continuity only; fabrication remains prohibited.

Select `led-inverter-routing-trial-114mm`, SHA-256
`a4d27c5babed5556002cf71b8fae3c3280f627edeb0ff673b9b787d21d4b91ab`,
from the immutable ADR 0142 30-open source. ADRs 0150–0152 define the exact
U48/C67 poses, supported local bypass/captures, ordinary clock/supply joins,
two obsolete original APP leaf retirements and removal of two unused new
input-capture items. This successor closes U48.4–U49.7 HEARTBEAT_FALL_CLK.
U48.2 DISPLAY_HEARTBEAT remains physically open and retains its net/function.

All 218 prior physical groups survive; native and independently counted
physical opens agree at 29 (217 groups on 188 nets). All 483 exact parts,
fields/local pads, other poses, 19,367 retained source copper items/native types,
original external branch/filled-plane contacts and profiles/rules/structure
are preserved. The exact plan contains 29 additions: 18 tracks and eleven vias.
Three existing-rule 0.12 mm U48 necks are each 0.100 mm; all other new tracks
are 0.20 mm. No width exception or native clearance rule changes.

The exact original 104 finding payloads match under an independent integer
U48 rigid transform and ADR 0136's prior frozen U52 transform. No C67 or extra
finding allowance. Two independent three-fill replays are byte-identical to
the selected source. Inverse reconstruction restores the 30-open parent byte
for byte, all 218 groups, all source items and exact original 104 findings.
Native external-contact, complete-ledger, inverse/orphan and visual gates,
18 native source/disconnection/finding faults, eight drill-policy controls
(three positive/five rejections) and all 36 source-workflow commands pass.
The checkpoint manifest records exact ignored raw evidence hashes.

The independent actual-hole audit records one close but disjoint supported
In2/In3 mechanical-buried versus In4/B microvia pair, plus one exactly aligned
In3/In4–In4/B stack. All other new pairs retain the conservative 0.25 mm hole
check. These are native CAD semantics, not fabrication qualification; the
controlled stack and fabrication spacing remain held. All 557 historical
centre microvias, electrical/part/timing/return/thermal/process/fit and
independent Gate A requirements remain unresolved. Current/protection/NTC/
timer/fail-safe/default-off boundaries are unchanged. Zero opens is unfinished.
