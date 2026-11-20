<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Ground and row-selector continuation, 2026-11-09

No successor is selected. The canonical board remains at **36 native and
physical opens**, SHA-256
`a24e9220226b77411ae8e8baea5cd629ce0fea8a97c377a708510d6791c2e439`.
Its prior validation remains applicable; the unchanged source/plan fingerprint
check passes after these experiments. The zero-open objective remains open.

[Machine-readable evidence](../../mechanical/review/shunt-ground-study-2026-11-09.json)
records inputs, search outcomes and SHA-256 references to ignored local raw
outputs/scripts. The two original-interface catalogues are
[ADR 0109's two-row interface](../../mechanical/review/shunt-ground-reroute-interface-2026-11-09.json)
and [ADR 0110's three-row interface](../../mechanical/review/shunt-three-row-interface-2026-11-09.json).
All candidate boards, native reports, vendor pages and PDFs remain ignored.

## Bounded results

- **U38 placement (ADR 0107):** 81 sampled translations within 0.25 mm.
  Seventy-nine fail foreign-copper clearance, one loses an original direct
  contact, and the original pose alone passes geometry without a join.
  TI LM4040 Rev Q's pin table and DBZ0003A land example were visually
  rechecked. Exact LM4040A25IDBZT identity, numbered nets and lands remain.
- **Ground-layer search (ADR 0108):** enabling ordinary GND movement on
  In2.Cu produces no join. A bounded 0.025 mm grid with denser filled-plane
  targets also produces no join, both on In2 alone and across six layers.
  These experiments change sampling restrictions only; no production tool
  or selected profile changes.
- **Two-row reroute (ADR 0109):** two routing orders cannot restore both
  ROW_SEL_01/03 around a short shunt-ground path. The third row's U-shaped
  trace is a concrete obstruction. Sampled full-span captures find no usable
  left or right endpoint.
- **Coupled local trial (ADR 0110):** moving U38 right by 0.250 mm and
  reshaping the rows joins U38.3/U52.3 to main ground. Full native DRC has
  exactly the unchanged 104 findings; the independent baseline comparator
  passes. However, PAIR03.1/PAIR04.1 leave main ground. The group-size
  inventory remains `[1,2,194]`, with different membership, and the count
  remains 36. This is rejected. Retaining ROW_SEL_00 original has the same
  ground loss.
- **Return restoration:** removing the new ROW_SEL_01 section in an ignored
  diagnostic restores all 196 ground pads. Its native filled B.Cu component
  touches PAIR03.1, PAIR04.1 and PAIR02.1. An ordinary-width explicit ground
  corridor is derived inside that filled region and foreign-copper screened.
  The constrained B.Cu/In4.Cu/In3.Cu row-01 search exhausts 18,962 nodes;
  the widened front/back alternative exhausts 322. Neither selects a join.
- **Broader additive searches:** front/back through-via and six-layer reverse
  searches each test 37 endpoint cases on the original 36-open board without
  a complete join. Several cases hit node bounds; this is not proof of
  impossibility. Two already-authorized DSF neck seeds clear foreign copper
  but do not yield complete connections; no dangling seed is adopted.

The coupled result is useful evidence that count and clearance checks alone
would miss a lost return group. Further work must preserve the 196-pad return
while completing the row-selector interface, potentially through a broader
coordinated placement/layer change. Repeating the same bounded ordinary-width
searches has no supporting evidence of benefit.

These are CAD calculations/searches on an unbuilt revision, not hardware
measurements. Electrical return impedance, power/thermal qualification,
controlled stack and via process, mechanical fit and independent Gate A remain
unresolved. No fabrication release is authorized.
