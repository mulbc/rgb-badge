<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# PAIR03 supply join: 23 to 22 open connections

The selected CAD source is
`hardware/coupon/rev-a/staging/led-pair03-supply-routing-trial-114mm.kicad_pcb`,
SHA-256 `03e74104c51811a18d558cdc7bd28513f9f1fcb5058ef8a7c7f62f612d8a252d`.
It has **22 matching native and independent physical opens**, down from 23.
Every previous connection and attached source conductor survives. This is
native CAD continuity evidence for an unbuilt board, not electrical acceptance.

ADRs0268–0270 authorize discovery, freeze the exact additive prototype and
select it after qualification. The immutable parent is the23-open PAIR01
checkpoint, SHA `9574949d6bd56caa6f79b9db78af3531b0150cfba1f110d727c829effcaf62b3`.
The [frozen plan](../../mechanical/review/pair03-supply-routing-plan.json),
[discovery](../../mechanical/review/pair03-supply-discovery.json) and
[qualification checkpoint](../../mechanical/review/pair03-supply-routing-checkpoint.json)
carry exact typed identities and evidence fingerprints.

The change adds 17 ordinary 0.20 mm VLED tracks and one supported 0.30/0.10 mm
B/In4 microvia at(77.800,10.075), with calculated total conductor length
5.235660172 mm. It joins actual PAIR03.4 through retained main-supply via
`85ad9ca5-5c6b-5aa4-a068-b51753571be9` and an intersecting retained supply
track on In4. The source witness belonged to the38-pad main supply group
before the join. All 483 parts, numbered pads, fields, poses, board/rule/zone
declarations and project profiles are unchanged; no original copper retires.

| Native qualification | Result |
| --- | --- |
| Previous physical pad groups preserved | All 211 |
| Previous attached copper preserved | All 19349 items |
| New physical groups / nets | 210 /188 |
| Main GND / VLED / USB supply pads | 197 /39 /32 |
| New copper / unattached copper | 18 /0 |
| Full CLI findings | Exact original 104; no new finding |
| New/source hole-policy audit | Pass |
| Initial stable fills | Four identical hashes |
| Independent replays | Two, each with three identical fills |
| Remove-additions inverse | Three byte-identical parent hashes |
| Inverse groups / zone geometry / DRC | All 211 equal /nine empty integer XORs /exact 104 |
| Deliberate faults / shared hole controls | 32 rejections /eight passing controls |
| Portable source checks | 43 pass |
| Native visual review | B/In4 before and after, complete changed region |
| Canonical source recheck | Same frozen bytes,22 matching opens and exact 104 |

The native policy checks the raw serialized additive ledger before loading,
then compares every fixed non-conductor declaration, including footprint/pad
net labels and identities. This catches labels the native importer might
otherwise repair. Native connectivity independently proves all previous pad
groups and their attached source copper remain joined. The original contact
catalogue and the retained main-supply witness are checked separately.

Faults cover exact MPN/value, numbered nets, source/fixed part poses and side,
pad geometry/field identity, source removal/change/via type, addition dimensions,
layer/net/identity/inventory, plan and original contact proof, and full DRC
payloads. Three physical controls move the actual source pad or remove the
actual supply track/microvia, then prove the intended pads are in separate
native groups before verifying rejection. Hole controls include unsupported
historical centre transitions and prohibited duplicate/shared-span holes.

Local raw evidence is under
`hardware/coupon/rev-a/build/pair03-supply-routing/`: prototype/current/canonical
audits, native DRC payloads, inverse PCB/DRC, two replay PCBs/logs,40 fault/hole
results,43 source-command results and the native SVG/PNG visual manifest.
Build outputs and unsigned fabrication artifacts remain ignored. The public
generator, native checker, portable checker and fault runner use the same
frozen plan. Hosted checks include the portable gate and exact selected files.

The remaining 22 opens,554 unsupported historical centre microvias, trial
NTLJD3119CTBG package/MPN acceptance, power-copper/electrical/return/thermal,
controlled-stack/process/assembly/fit qualification and independent Gate A
remain open. No current limit, protection, default-off behavior or fabrication
hold changes. Fabrication remains prohibited.
