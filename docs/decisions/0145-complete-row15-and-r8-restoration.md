<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0145: Complete selector and anchored pull-up restoration

Date: 2026-11-14
Status: Accepted for ignored complete-circuit feasibility; no successor selected.

Continue from the immutable 30-open source, SHA-256
`90db778d8e44b2c71ab5e1f5d8a1c586ee71c25d46892b1406c4792ac7720abd`.
The bounded complete R8 relocation screen finds no clear pose. Revisit the
anchored flip from ADRs 0095/0103 with a full-board supported-layer restoration
of its obstructing selector, rather than another bounded two-capture transfer.

Freeze R8 ERJ2RKF1001X / 1 kΩ / 1% on B side at (72.575,8.0) mm / +90 degrees,
from (72.575,9.0) mm / −90 degrees. Pad 1 remains VLED at exactly
(72.575,8.5) mm and retains every original direct copper contact. Pad 2 remains
ROW_GATE_02 and moves to (72.575,7.5) mm. Independently validate the integer
180-degree pad transform about the fixed supply-pad centre. Retain PAIR03
NTLJD3119CTBG and every other part/pose/local land/field/net unchanged.

Retire only original 0.20 mm B.Cu ROW_SEL_15 segment
`8f141701-3e53-50fe-a1fe-bc2869d6daab`, from (68.9,7.85) to (73.35,7.85) mm.
Its complete current native contact catalog SHA-256 is
`549c816fad7a3de082757682a7f1ad3d022b519005fb5d8ac97638d7df02bbb6`.
Preserve all six original external B.Cu track contacts and both exact boundary
interfaces, all other source copper/native via types and its complete original
PAIR16.2/R37.1/U2.15 terminal group. Do not retire the adjoining vertical,
ROW_SEL_00/01/14, COL_06_R or R8's VLED supply leaf.

Test new 0.30/0.10 mm adjacent B/In4 gate captures at actual pad centres
(72.575,7.5) and (74.825,7.5) mm and an ordinary 0.20 mm In4.Cu gate lead.
Screen actual native foreign/no-net/mechanical copper, every hole and the
board/cutout edges, including interaction with the selector repair. If needed,
ordinary supported adjacent transitions may extend that gate lead; no new
centre microvia or narrow-width rule. Gate copper remains bounded to 5 mm.

Restore ROW_SEL_15 through ordinary 0.20 mm full-board copper, supported
adjacent 0.30/0.10 mm microvias and centre mechanical 0.50/0.30 mm buried vias,
with up to 120 mm new selector track length. Use actual live same-net copper
endpoints and preserve every original external branch, including branches
without pads. Do not count a temporary selector cut or partial gate join as
progress. Final selection requires all 218 original live groups, the original
35-pad VLED group and original selector group to survive together with the real
new gate join, no extra finding under the existing frozen U52 comparison,
native/physical count below 30, a complete exact ledger and independent stable
replay/inverse/orphan/native-fault/source/visual gates.

No current limit, VLED voltage/domain, resistor value, protection/NTC/timer,
fail-safe input control or default-off boundary changes. All gate/supply/return/
timing/thermal/part/HDI/stack/process/fit and independent Gate A qualifications
remain unresolved; zero opens is unfinished and fabrication prohibited.
