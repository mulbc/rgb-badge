<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# First-author 3.3 V candidate review at c929711

2026-10-05. Owner-generated KiCad 10.0.6 evidence:

- ZIP SHA-256: `c676d959616e436b291750d92fb25e3e4633ad9fa85188f7fbeb64eb645c1fb3`.
- Console log SHA-256: `bae8dff4f41c0ed1e721a233d21065d510fb708695db4c9cb4570154d9166547`.
- Candidate PDF SHA-256: `6aa88d82971d7a6b4c626cadc0891664396580d60367524da5d80de2d6d42dcc`.
- Candidate XML SHA-256: `2ac1cfd5d736398fb483ed50479f041f43973ecf7b412cae08ea2fc80594f91a`.

## Electrical evidence

The main project reports zero configured ERC violations and its native XML passes the complete 400-item / 1,507-pin checker after the Panasonic naming migration. The separate candidate XML contains all nine exact-part components and 24 pins: U36 VIN connects to both input capacitors; VOUT to both output capacitors and R81; FB to R81/R82; EN to R83; MODE/GND and all returns to GND. Each local LX net connects only its U36 pin and its corresponding L1 terminal. No switched source or physical ON contact is present. **No candidate ERC report was requested or supplied**; main-project ERC does not validate the unlinked sheet.

## Visual findings and repair

The candidate PDF has readable component values and local LX wiring, but C40/C41 input labels touch the left drawing frame. Move C40/C41 and R83 from x=50.80 to x=76.20 mm, including their labels/wires. This is a presentation change; the source checker and deterministic generator tests pass after the repair.

The native inductor copper and paste exports show two separated rectangular lands. The fabrication export's nominal body/courtyard is consistent with the source audit; raw pad numerals intersect fabrication outlines and the long value extends beyond the export viewport. Use the separate copper view for connectivity; assembler documentation still needs a readable annotated view. The standalone inductor symbol's Reference/Value headings touch: increase reference Y from 5.08 to 7.62 mm. Its two passive terminals and footprint association are unchanged. The source library checker passes. **Both rendering repairs await the next combined native export**; no separate immediate owner rerun is required.

The [capture contract](../../hardware/coupon/rev-a/3v3-converter-capture-contract.md) still controls capacitor, thermal, load, protected SYS and ON-input qualification. Do not link this candidate before removing the superseded application-rail source flag and auditing its real source/enable. Independent Gate A remains required before fabrication.
