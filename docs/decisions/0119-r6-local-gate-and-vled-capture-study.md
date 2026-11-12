<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0119: Localize R6's isolated gate with an explicit supply capture

Date: 2026-11-12
Status: Accepted for ignored feasibility; no successor selected.

Use the immutable corrected-RSE 35-open board, SHA-256
`3967bb66e89e0005f6859ce78a766b4536d06883b76fce130e75a6fdeefaf96e`.
Exact R6 `ERJ2RKF1001X` is the unchanged 1 kΩ VLED pull-up for ROW_GATE_00.
Its gate pad is isolated; its supply pad joins main VLED through an old leaf.
Test local poses near PAIR01's existing gate lands, with an ordinary-width
B.Cu gate lead no longer than 3 mm. Preserve R6's association, value, local
footprint, pad nets and disabled-row default. PAIR01 is not moved or modified.

Only the following six obsolete source items may be retired in this trial:

- `430f9728-db9a-55c3-bc3a-c15f77000cfa`: VLED In4/B microvia at (57.75,8.75).
- `37dd7533-43cb-5304-82c1-189a29f31d7b`: VLED In3/In4 microvia there.
- `2538e05f-0e95-52a5-813a-3f61b41300a2`: In3 leaf (57.75,8.75)→(58.45,8.75).
- `750bfacf-ba86-5c75-9580-95e8142b8407`: old In2/In3 microvia at (58.45,8.75).
- `42fd1a41-569a-505d-a7f3-ff8a9a5bd1b8`: In2 leaf (58.45,8.75)→(58.75,8.75).
- `b0d25ba3-c6d5-5224-8d60-741e3760ff1a`: In2 stem (58.75,8.75)→(58.75,14.05).

Replace the last stem by its unchanged-width remainder from
(58.75,9.713636) to (58.75,14.05) mm, retaining its actual first junction
with `607bd79b-bb37-5fc4-8a76-ed1e127f247c` and every other original
same-net contact. Re-derive those contacts from source rather than relying
only on these labels. Never retire a shared branch beyond this reviewed leaf.

Restore R6's VLED supply through an explicit local B/In4/In3/In2/In1 capture
to the existing connected VLED plane. Adjacent transitions retain 0.30/0.10 mm
geometry; the central transition must use provisional 0.50/0.30 mm **buried**
geometry, screened across its complete span. Do not copy or retype the retired
unsupported central microvia. A new source connection must have an actual
same-group filled-plane witness after refill, not just a zone name. If a
coincident stack is used, record its unqualified fabrication requirement;
native clearance cannot establish assembler/fabricator capability.

Keep all other copper, all ADR 0117 additions, part poses, fields, nets,
source circuit, current/protection/permission limits, converter geometry and
rule profiles unchanged. Preserve every previous live physical group,
including the source VLED group and gate lands. Reject any new short,
clearance, dangling fragment, plane split or unconnected inverse output.

Outputs remain ignored. A successor requires exact original-contact and
retirement proof, native/physical reduction, unchanged full 104-finding DRC,
stable refills and independent replay, source/fault and visual checks before
selection. This does not qualify VLED copper, gate timing or a manufacturing
stack. Electrical/process/fit qualification and independent Gate A still
prohibit fabrication.

## Negative preliminary screen

The [62,468-pose native screen](../development/r6-locality-2026-11-12.md)
selects no pose or capture. None of the 4,920 pad-clear samples has the proposed
coincident supply stack, and the direct/single-corner ≤3 mm gate templates
also select none without capture. The source stays byte-identical at 35 opens;
no authorized retirement is executed. A more coordinated placement requires
an explicit later scope rather than removing unrelated blocking copper.
