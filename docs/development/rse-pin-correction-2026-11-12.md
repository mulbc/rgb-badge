<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# RSE flip-flop correction and retained routing checkpoint

The exact `SN74LVC1G74RSER` pin map at U49/U50 was wrong. Canonical source
and the corrected routing successor now use its **RSE** assignment. This
corrects a material circuit error while retaining **35 native / 35 independently
counted physical opens**. Zero opens remains unfinished. This is CAD/source
validation of an unbuilt board, with no electrical or fabrication acceptance.
[ADR 0117](../decisions/0117-rse-flip-flop-package-pin-correction.md) records
scope before implementation; the [machine-readable evidence](../../mechanical/review/rse-pin-correction-2026-11-12.json)
identifies source files, checks and local raw evidence.

## Manufacturer evidence and source correction

TI SCES794G Figure 5-2, page 4, shows the RSE pinout, whereas its following
general table lists the other packages' numbering. The manufacturer-authored
SCES794F page 3 has separate RSE and other-package columns, confirming the
figure. TI notification 20200518000 identifies the 2020 documentation correction
and says the device itself did not change. The 2019 IBIS model predates this
correction and retains the old conflicting map. This conflict is recorded;
received-part orientation and independent engineering review remain open.

| Physical RSE pad | Function | U49 net | U50 net |
|---|---|---|---|
| 1 | Active-low PRE | +3V3_APP | +3V3_APP |
| 2 | Active-low CLR | DISPLAY_CLEAR_OK | DISPLAY_CLEAR_OK |
| 3 | Q | HEARTBEAT_SEEN | ARM_LATCH |
| 4 | GND | GND | GND |
| 5 | Inverted Q | No connect | No connect |
| 6 | D | +3V3_APP | HEARTBEAT_SEEN |
| 7 | CLK | HEARTBEAT_FALL_CLK | DISPLAY_ARM_CLK |
| 8 | VCC | +3V3_APP | +3V3_APP |

The symbol numbers change while the schematic's functional pin positions stay
fixed. The deterministic sheet, independent pin checker and fresh native XML
snapshot agree. The complete 497-component contract comparison proves that
only U49/U50 terminal identities changed, under the published permutation;
all other parts and logical connections remain identical. R108 remains the
exact 100 kΩ clear pull-down. Both candidate display outputs remain isolated
at test pads. Native ERC reports zero violations. Native schematic rendering
was inspected. The shared RSE footprint and USB-switch symbol are unchanged.

Sources: [TI current datasheet](https://www.ti.com/lit/ds/symlink/sn74lvc1g74.pdf),
[TI Rev F archived copy](https://static.datasheets.com/doc/10821154-texas-instruments-sn74lvc1g74dcut-ds.pdf),
[TI change notice archived copy](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/424/PCN20200518000.pdf).
Exact vendor bytes, hashes and rendered pages are cached locally in the ignored
vendor directory; no vendor document is committed.

## Physical migration and rejected intermediate counts

The previous 35-open board remains byte-identical as a historical wrong-pin-map
checkpoint. Historical comparisons require an explicit flag and return an
incorrect-RSE-wiring status. Ordinary source comparison rejects the old map.
The corrected successor has a distinct project, so older replay evidence is
not rewritten to appear correct.

The frozen plan retires eight obsolete directly contacting copper items and
adds 73 ordinary-width tracks/adjacent microvias. Every other source copper
item, all 244 previous accepted additions, all poses, part fields, footprint
geometry, zone definitions and profiles survive unchanged. No footprint pads
are renumbered to preserve the wrong physical wiring. No unsupported centre
microvia, protection, limit, firmware or output-enable change is introduced.

The first corrected trial has 38 opens, with three prior functional groups
lost: U49 clear, U50 clock and U50 Q output. Clear and Q routing restore two.
The clock route initially splits application-supply islands; restoring that
supply around the clock captures regains every original functional group.
A short B.Cu bridge and adjacent transitions preserve the existing supply
connections. These are geometric continuity results, not power integrity or
current-carrying qualification. The clear landing reaches the retained old
track centreline, and the preset landing reaches the actual pad centre.

A trial near the top edge fails the unchanged 0.5 mm edge constraint and is
rejected. Restoring all eight obsolete items also counts 35 opens but produces
128 findings, including ten shorting findings, demonstrating that an unchanged
open count cannot justify old copper. All such boards remain ignored.

## Acceptance evidence and remaining work

- The corrected board has 223 physical groups on 188 nets: 35 physical opens,
  matching KiCad's native count. Every one of the 223 original **functional**
  groups survives under the explicit old-to-corrected terminal permutation.
- Full native DRC retains the exact 104 original intrinsic findings, including
  item identities, descriptions, severity, coordinates and ignored-check list.
  Only the order of two implicated items is normalized; no finding is waived.
- Two independent exact-plan replays, each with three stable native refills,
  match the selected board byte-for-byte. The eight retirements and all 73
  additions retain exact signatures and UUIDs.
- Nine native faults reject the old map, Q/output inversion, low preset,
  unreviewed pose/copper removal, copper on inverted Q, narrow copper,
  unsupported centre microvia and actual clock disconnection.
- Portable source checks include all-terminal RSE faults, exact function marks,
  complete circuit equivalence and explicit rejection/reporting of historical
  pin maps. The local source workflow passes all 30 commands.
- Native B.Cu/In4.Cu/In3.Cu U50 views, B.Cu/In4.Cu U49 views and preceding B.Cu
  views were inspected. The unused inverted outputs remain free of copper.

The selected corrected project is
[led-rse-corrected-routing-trial-114mm.kicad_pro](../../hardware/coupon/rev-a/staging/led-rse-corrected-routing-trial-114mm.kicad_pro).
The source-only gate and `tools/check-rse-pin-migration.sh` reproduce its checks.
The prior PAIR01 34-open corridor is rejected by seven additional findings;
[ADR 0116](../decisions/0116-pair01-local-ground-corridor.md) records that outcome.
Further routing must begin with the corrected source. Remaining opens,
controlled stack, 557 historical centre microvias, electrical/process/fit
qualification and independent Gate A still prohibit fabrication.
