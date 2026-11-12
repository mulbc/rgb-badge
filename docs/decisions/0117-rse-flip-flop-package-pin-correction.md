<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0117: Correct the RSE flip-flop pin assignment before further routing

Date: 2026-11-12
Status: Corrected canonical source and separate 35-open PCB successor selected;
electrical/process qualification and independent Gate A remain open.

The exact SN74LVC1G74RSER uses RSE-specific numbering: PRE-bar 1, CLR-bar 2,
Q 3, GND 4, Q-bar 5, D 6, CLK 7, VCC 8. TI SCES794G Figure 5-2 (page 4)
shows this assignment, although its following general pin table incorrectly
lists the other packages' numbering. TI SCES794F page 3 explicitly separates
RSE and other packages in its table and agrees with the RSE figure.
TI notification 20200518000 (June 8, 2020) identifies the Rev E-to-F pinout
documentation correction and says the physical device did not change.
The July 2019 SCEM591 IBIS model predates that correction and retains the
conflicting general numbering; it cannot establish the RSE assignment.

Sources: [current TI drawing](https://www.ti.com/lit/ds/symlink/sn74lvc1g74.pdf),
[archived TI Rev F](https://static.datasheets.com/doc/10821154-texas-instruments-sn74lvc1g74dcut-ds.pdf),
[TI notification archived by DigiKey](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/424/PCN20200518000.pdf).
Local exact bytes and hashes belong in the source review; vendor documents
and rendered pages remain ignored. This is manufacturer-authored evidence,
not a distributor inference. Received-part orientation and independent review
remain acceptance work.

Correct only U49/U50's symbol numbering and associated physical pin nets.
Preserve the logical heartbeat-then-arm circuit, active-low clear, defined
PRE high, all resistor values, exact part numbers and isolated candidate
outputs. Old functional pin numbers map to corrected numbers as
1→7, 2→6, 3→5, 4→4, 5→3, 6→2, 7→1, 8→8. The RSE footprint geometry
and physical pad numbers remain unchanged; TS3USB31ERSER is unaffected.
Do not renumber the footprint to conceal wiring to the wrong physical pads.

Update the local symbol, embedded canonical sheet, deterministic generator,
independent numbered-pin checks and native-exported source contract. Retain
the preceding contract as an explicitly historical snapshot. Historical PCB
checks must opt into and report the old RSE map; ordinary checks must reject
it. Never call a historical source comparison current pin-map acceptance.

Freeze the 35-open routing source (SHA-256
da3764ddf5c8c615529340c33c92974cff3fd036b937b5e4a53c408e0b141637)
and its replay evidence. Its count measures historical CAD connectivity,
not correctness of the flip-flop wiring. Explore a separate ignored successor
with exact corrected pad nets. Inventory each affected old copper contact
and every functional connection lost by that correction. Retire only an
explicit reviewed obsolete cohort; preserve or restore all functional pad
groups under the published terminal permutation, all other copper/additions,
converter geometry and safety boundaries. No new unsupported central vias,
clearance waiver or current increase is permitted.

Select a corrected PCB only after independent semantic group retention,
complete native/physical connectivity, exact DRC comparison, contact and
retirement proof, stable replay/fills, meaningful injected faults and visual
review. A larger honest intermediate open count is preferable to falsely
counting wrong-pad connections. Zero opens remains the goal; the controlled
stack, electrical/process/fit qualification and independent Gate A still
prohibit fabrication.

## Bounded first migration trial

Retire exactly the eight directly contacting obsolete copper items below.
The three old supply vias may be replaced at the corrected supply pads;
restore the clear, arm-clock and arm-output leaves to their retained actual
network endpoints using ordinary tracks and supported adjacent transitions.
No other retirement or pose change is authorized by this first trial.

- `288b2d15-1433-5042-87a6-7f1436e992e4`
- `2e514485-4464-59f2-a6ba-1397d4fad179`
- `6be521a2-c717-5172-96b7-f2f9e6bc46f8`
- `6fced5d8-797a-56fa-a82b-87a9a87056ff`
- `a19a5928-5dec-5a62-a738-6b2f7769e217`
- `cff72e1e-b062-5a84-bfc3-b45fb76a7d69`
- `d27e9101-48d6-553e-9b60-c2bb73866a79`
- `e0ee2639-b200-5dbf-9c43-57813a69e234`

## Selected corrected source

The [implementation review](../development/rse-pin-correction-2026-11-12.md)
records the exact eight retirements and 73 additions, including short supply
restoration around the clock captures. All 223 preceding functional groups
and 244 accepted additions survive under the explicit terminal permutation.
Full native DRC retains the exact 104 findings; the corrected successor has
35 native/physical opens, stable independent replays, nine native rejection
cases and current canonical source/ERC/visual checks. The earlier wrong-map
board stays immutable. This selects corrected routing source, not fabrication.
