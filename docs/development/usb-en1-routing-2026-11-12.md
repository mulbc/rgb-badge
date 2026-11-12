<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# USB EN1 continuity checkpoint: 34 opens

The selected corrected-source successor joins U23.4, R70.2 and TP31.1 on
`USB_EN1_RAW_N`, reducing **35 → 34 native and independently counted physical
opens**. Every previous live group survives. Full native DRC retains the exact
104 intrinsic findings. This is CAD/source evidence for an unbuilt board;
zero opens, electrical/process qualification and independent Gate A remain open.

[ADR 0121](../decisions/0121-local-usb-en1-pullup-and-test-land.md) records the
scope before implementation. The [exact plan](../../mechanical/review/usb-en1-routing-plan.json)
and [validation record](../../mechanical/review/usb-en1-routing-checkpoint.json)
identify the source, poses, original contacts, copper and raw evidence.

## Exact circuit and physical change

Exact Panasonic R70 `ERJ2RKF1002X` stays 10 kΩ. Its supply and output pins,
U23 `SN74LVC1G06DBVR`, test-land size/name and all other component identities
and nets remain unchanged. TI SCES295AB, October 2025, Figure 4-1/Table 4-1
confirm DBV Y on 4 and VCC on 5; no package/symbol change is made. The current
manufacturer PDF is cached and hashed locally, with no vendor material committed.

R70 translates to (10.55,6.50) mm. Its physical orientation remains −90°,
equivalent to the specified 270°. TP31 moves to (11.90,7.75) mm, retaining
180° and its original 1 mm circular land. Their new courtyards clear the fixed
switch, logic, comparator and controller-module courtyards. Probe/enclosure
access remains unqualified.

Exactly three obsolete items are retired: the old R70–TP31 B.Cu leaf and
two old adjacent supply microvias. The source contact catalog independently
re-derives their actual pad/copper/filled-polygon interfaces. All other copper,
including every ADR 0117 addition, all other parts, zones, outline, setup and
rule profiles remain identical.

Eleven new ordinary 0.20 mm B.Cu tracks restore the complete 32-pad USB-supply
group through actual U23.5 and join the actual U23.4 output and test pad. There
are **no new vias**. Calculated branch lengths are 11.525 mm for supply,
13.525 mm for output and 2.100 mm for the test branch, each below the unchanged
16 mm bound. Every branch reaches real native pad centres; no arbitrary zone
anchor, net reassignment, current-limit change or firmware control is introduced.

## Validation

- All 223 preceding physical groups are retained; the joined target yields
  222 groups on 188 nets, hence 34 physical opens, matching native connectivity.
- Exact full DRC comparison retains every original finding's item IDs,
  description, severity, coordinates and check lists. Only implicated-item
  order is normalized; no finding or clearance is waived.
- Two independent replays, each with three stable refills and group checks,
  match the canonical board byte-for-byte. The complete check script repeats
  both replays and verifies the exact three-retirement/eleven-addition ledger.
- Twelve native faults reject wrong parts/nets, altered land/pose, unreviewed
  retirement, restored obsolete copper, narrowing, a new via, missing source
  contacts, false endpoint evidence, and actual supply/output disconnection.
- Restoring all obsolete items leaves physical continuity unchanged but raises
  the native count to 35 and produces 106 findings, including a dangling track
  and via. That counterfactual is rejected; retiring pad-free copper is not
  counted as the circuit join.
- The current canonical source contract and all 31 local source-workflow
  commands pass. The firmware pin inventory passes without a fingerprint or
  GPIO change because canonical schematic/library source is unchanged.
- Native old/new B.Cu views of the local circuit and old remote copper were
  inspected. Earlier unsaved/ignored placements and the 106/108-finding
  candidates are rejected; their lower count alone was not accepted.

The selected project is
[led-usb-en1-routing-trial-114mm.kicad_pro](../../hardware/coupon/rev-a/staging/led-usb-en1-routing-trial-114mm.kicad_pro).
Reproduce with `tools/check-usb-en1-routing.sh`. The corrected 35-open RSE
parent remains immutable. All remaining opens, supply/return/timing, controlled
stack, 557 historical centre microvias, effective capacitance, thermal/process/
fit qualification and independent Gate A still prohibit fabrication.
