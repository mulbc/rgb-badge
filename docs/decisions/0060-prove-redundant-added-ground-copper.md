<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0060: Prove redundant added ground copper

Date: 2026-10-28
Status: Authorized for ignored feasibility only; no canonical retirement selected.

A native geometric audit of the accepted 64-edge board (`5b67c6618d8bbf1c945492c2c2ab96cf722edf7475799f2689d14be317c769ae`, commit 9493793) identifies 87 added GND tracks whose complete copper shape is already covered by retained ground copper: 85 on B and two on In2. The proof unions the actual native filled GND zones, original-source GND tracks, retained vias and pads; it excludes all candidate added tracks from the covering set. Each candidate's conservative outer polygon is subtracted from that retained inner coverage with 100-IU approximation error. Empty difference proves geometric redundancy at that resolution; any residual fails this category. No original 215-edge copper or any via is eligible for retirement.

Permit an ignored experiment removing only that exact 87-signature inventory, plus the separately enumerated eleven-track ADR 0059 local branch (eight overlap the geometric set, yielding 90 unique tracks). Keep the three local signatures that fail strict polygon coverage classified as ADR 0059 rework, not geometric redundancies. Their calculated native-geometry uncovered outer-envelope areas are 0.00004707725, 0.0000233729775 and 0.000047077 mm²; do not inflate the covering polygon or discard these residuals to claim neutrality.

Record the exact union before any removal. Refill three times, preserve every 64-edge physical group, every remaining copper signature, original/selected zone definition, all component poses and the unchanged full 104 native findings. Check original-source non-retirement independently. Then investigate new joins at the original 0.20 mm clearance, 0.20 mm ordinary width and existing exact DSF neck/microvia policy. Do not combine this with ADR 0058's smaller-spacing experiment. Plane copper can reflow around a signal only if all prior groups and retained-layer interfaces still survive; deleting route objects is not evidence that an electrical connection exists.

Any canonical selection requires a frozen 64-edge reference, exact independently checked retirement categories and native polygon proof, original-layer retained-interface witnesses, guards against unlisted/original/via retirement or a false coverage claim, lower independent/native opens, unchanged complete DRC and orphan restoration, stable replay and source/LED checks. Existing checkpoint retention must allow only this reviewed inventory and continue rejecting all other coordinated plan/candidate deletion. Ground-return, bypass/noise, thermal/process and assembly effects remain engineering review items. Current/voltage/protection/enable settings are unchanged; no hardware claim or fabrication release follows, and independent Gate A remains mandatory.

## Recorded feasibility result

The exact 90-track union preserves all accepted 64-edge physical groups and the full 104 findings through three native refills. Subsequent original-width searches make no selected lower-count join. A narrow USB status trial reaches 63, but transferring only its new signal copper to the untouched 64-edge board also reaches 63 and passes the complete acceptance gate. The canonical selection therefore retains all 90 ground tracks. No new retirement policy is implemented or selected; inventories, geometric audit and failed probes remain ignored build evidence.
