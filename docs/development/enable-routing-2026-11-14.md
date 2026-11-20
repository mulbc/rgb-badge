<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Complete enable routing checkpoint, 2026-11-14

The selected CAD study now has **30 native and independently counted physical
opens**, down from 31. R105.1, TP10.1, U3.17, U52.2 and U55.2 form the complete
DISPLAY_ENABLE group. All 219 prior groups survive, with 218 current groups on
188 nets. The zero-open goal remains unfinished.

[ADR 0142](../decisions/0142-enable-routing-checkpoint.md) selects
[the project](../../hardware/coupon/rev-a/staging/led-enable-routing-trial-114mm.kicad_pro).
The complete [plan](../../mechanical/review/enable-routing-plan.json) freezes
one exact C71 translation, two source retirements, all original native contact
witnesses and 88 additions. The 31-open predecessor remains immutable.

## Exact geometry and routing

C71 GRM155R71C104KA88D moves left by 0.500 mm to (102.5,6.75) mm, retaining
B side, 180-degree orientation, local lands, fields and nets. Replace only its
private APP capture and one GND return head; retain the original GND return
tail. Replacement APP and GND contacts preserve both original supply groups.
No other part/pose, source copper or rule/profile setting changes.

The new U52.2 neck follows (103.2,5.675) → (103.2,6.075) → (103.425,6.325) mm.
Its two 0.12 mm segments total a calculated 0.736340601 mm and intersect the
actual U52 courtyard under its unchanged package/net rule. All other new tracks
are 0.20 mm. An exact B/In4 capture and one In3/In4 microvia share the same
0.10 mm hole at the final non-grid point. This clear native transition was not
available at the routing grid's ordinary sampled positions.

The first stacked-capture routes split VBUS/APP/USB supply groups and are
rejected. Favoring In2.Cu finds the group-preserving continuation. Calculated
new DISPLAY_ENABLE track length, including its neck, is 42.431497 mm; the
replacement GND head is 0.460977 mm. These are layout calculations, not measured
delay/current-capacity or electrical qualification. There are 78 new tracks
and ten vias; adjacent microvias use 0.30/0.10 mm and centre mechanical buried
vias use 0.50/0.30 mm. No centre microvia, new current limit or protection change.

## Validation

- Native and physical counts agree at 30. All 219 source groups, both preceding
  control joins and complete bypass supply/ground connectivity survive.
  All 483 part identities/fields/local pads, unchanged poses, 19,281 retained
  source copper items/native via types, exact retired contacts and complete
  board/net/zone/rule/profile structure pass. Every C71 pad position follows
  an independent integer translation of its original position.
- Native DRC retains all original 104 full finding payloads. Only the unchanged
  prior U52 transform applies; C71 needs no finding-coordinate allowance.
  No UUID/pair/description/actual clearance/severity or ignored check changes.
- Two independent exact-source replays, each with three stable refills, match
  SHA-256 `90db778d8e44b2c71ab5e1f5d8a1c586ee71c25d46892b1406c4792ac7720abd`.
- Inverse reconstruction removes all additions, restores the two source items
  and old C71 pose, and restores all 219 source groups, 31 opens and the exact
  old findings. Three inverse fills are stable; integer polygon XOR is empty
  for all nine zones. Serialized cached collinear vertices differ; the source
  file remains byte-identical and is not overwritten.
- Eighteen native/DRC faults reject changed parts/nets/poses/source copper,
  narrowing, extra copper, via type/drill/span changes, actual omitted contact
  evidence, real connection removals and altered/omitted finding payloads or
  ignored-check changes. Actual longest-route and whole-join removals exercise
  connectivity independently of exact-ledger rejection.
- All 35 source-workflow commands pass. Five native new B.Cu/In4.Cu/In3.Cu/
  In2.Cu/In1.Cu views and old B.Cu/In2.Cu views were inspected with actual
  additions highlighted and component outlines visible.

The predecessor's original `omit-contacts` fixture inserted an empty field
with the wrong name, exercising an extra-field rejection rather than actual
contact-evidence omission. It now clears `source_retirement_contacts`; the
corrected native predecessor case also rejects. The frozen-plan guard already
rejects actual omission. The predecessor PCB is unchanged; its old raw evidence
hashes are retained with an explicit follow-up record.

ADR 0140's larger ordinary search made no additional join in twenty directional
attempts: thirteen reached 400,001 nodes and seven sampled components exhausted.
These finite outcomes do not prove global routing impossibility.

Reproduce with `tools/check-enable-routing.sh`. The
[checkpoint](../../mechanical/review/enable-routing-checkpoint.json) records all
hashes, replays, inverse/source/fault checks, rejected routes and inspected views.
Zero opens, electrical/part/effective-capacitance/timing/return/thermal/stack/
HDI/process/fit qualification and independent Gate A remain open. The owner
Murata reference remains historical, with no current approval inferred. The
557 historical centre microvias remain unresolved. No fabricated or measured
hardware or fabrication authorization is claimed.
