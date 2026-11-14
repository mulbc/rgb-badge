<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0142: Select the complete enable routing checkpoint

Date: 2026-11-14
Status: Accepted for CAD continuity only; fabrication prohibited.

Select `led-enable-routing-trial-114mm`, SHA-256
`90db778d8e44b2c71ab5e1f5d8a1c586ee71c25d46892b1406c4792ac7720abd`,
as successor to the immutable 31-open source. Native and independently counted
physical opens agree at 30. All 219 predecessor groups survive; R105.1, TP10.1,
U3.17, U52.2 and U55.2 form the complete DISPLAY_ENABLE group.

Adopt ADR 0141's one exact C71 −0.500 mm x translation, two private-leaf
retirements and the complete 88-item [addition ledger](../../mechanical/review/enable-routing-plan.json).
Keep the exact GRM155R71C104KA88D identity/local pads, all other parts/poses,
19,281 retained source copper items/native via types and every board/net/zone/
rule/profile setting unchanged. Two new U52 B.Cu neck segments use its existing
0.12 mm package rule, with combined calculated length 0.736340601 mm. Other
new tracks use 0.20 mm. New adjacent microvias are 0.30/0.10 mm; centre
transitions are mechanical buried 0.50/0.30 mm vias.

One exact non-grid In3/In4 transition shares the enable B/In4 capture's
0.10 mm hole. Other hole checks remain unchanged. Two routes that split supply
net groups are rejected. The selected ordinary continuation favors In2.Cu
and preserves every predecessor group. DRC retains exactly the original 104
finding payloads under the unchanged existing U52 coordinate transform, with
no additional transformation, finding or ignored check.

Two independent complete source reconstructions, each with three stable fills,
match selected bytes. Inverse reconstruction restores the two original items,
old C71 pose, all 219 groups, 31 opens and exact old findings. Integer polygon
XOR is empty for all nine zones; cached collinear vertex serialization differs.
Eighteen native/DRC faults, all 35 source checks and native old/new layer review
pass. `tools/check-enable-routing.sh` reproduces the acceptance gates. Exact
[evidence](../../mechanical/review/enable-routing-checkpoint.json) and the
[implementation record](../development/enable-routing-2026-11-14.md) retain
outcomes and the corrected predecessor contact-omission fixture.

Zero opens, signal/return/timing/thermal/power/part qualification, controlled
stack/HDI/process/assembly/fit acceptance, the 557 historical centre microvias
and independent Gate A remain unresolved. No current limit, protection, NTC,
timer, fail-safe USB or default-off boundary changes. No fabrication release
or hardware measurement is implied or authorized.
