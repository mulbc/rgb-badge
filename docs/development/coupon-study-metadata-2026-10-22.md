<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Canonical part metadata on the routed study

Status: **source metadata transferred; unbuilt noncanonical study, fabrication prohibited**.

This records the metadata-only 225-open checkpoint. The later [application-data route](led-application-data-study-2026-10-22.md) changes copper and reduces opens to 224 while preserving this metadata. Rolling reports below describe the latest board; this checkpoint's exact file identities remain in its validation record.

The [native generator](../../tools/generate-native-control-trial.py) now adds hidden
`MPN` and `Manufacturer` properties to the 465 components shared with the canonical
schematic. It validates canonical source fingerprints, exact placed identities and
the complete circuit model before copying anything. The historical replay input
is checked with the explicit `--historical-generator-input` mode, which permits
absent metadata and reports that it is not final-study acceptance. The generated
board must then pass the ordinary strict check. Host Python runs the source
checker because KiCad's bundled Python 3.9 does not support its typing imports.

All 930 properties copy canonical values verbatim. There are **443 nonempty MPN
values and 22 explicit blanks**, and **460 nonempty manufacturer values and five
explicit blanks**. The blank MPNs are PCB test features. Manufacturer blanks are
J1, TP13, TP14, TP34 and TP35; these source gaps are not filled by inference.
Nonempty source metadata also does not establish availability, part qualification
or an approved purchasing BOM. Canonical schematic, libraries and current settings
are unchanged. This is metadata reconciliation, not a material circuit decision.

The sixteen candidate row pairs and both netless driver projections receive no
new identity fields. They remain the exact documented exceptions to canonical
source; no package adoption follows. The checker now rejects absent shared
identity fields, cleared populated identities and invented values where canonical
source is blank. Its **21 test methods** include those regressions; the declared
source-only CI layout passes without native KiCad, XML or vendor PDFs.

## Native verification

Two sequential KiCad 10.0.6 generations produce identical bytes. New metadata
UUIDs derive from reference/property names without renumbering existing objects.
A complete parsed-source comparison with the pre-change PCB removes only the
MPN/Manufacturer properties on shared references: every remaining node, including
all existing UUIDs, pad properties, copper, zone fills, placements and all trial/
projected footprint content, is identical. The PCB diff consists solely of the
930 added properties.

The full native runner passes all **17 isolated routing guards**, exact checks for
all **256 LED placements**, all old physical pad groups and source copper. Full
DRC retains the exact normalized multiset of **104 intrinsic findings**; native
and physical-pad-cluster counts agree at **225 opens**. A fresh complete native
schematic XML export also matches the unchanged source contract and annotated
board. These are source/native checks, not bench measurements.

Repeat the checks with:

```sh
./tools/check-native-control.sh
./tools/check-coupon-study-contract.sh
```

[Retained validation and exact identities](../../mechanical/review/coupon-study-metadata-validation-2026-10-22.json),
[current circuit comparison](../../mechanical/review/coupon-study-reconciliation.json),
[native routing check](../../mechanical/review/native-control-check.json),
[full native DRC](led-native-control-drc-2026-10-21.json) and
[reproduction](../../mechanical/review/native-control-reproduction.json).
Earlier audit/routing validation files describe their recorded historical hashes.

Board SHA-256: `20e56a776dc6e27a6bfab389753d8acba29998926dba10272f32f4e9034785c9`.

Remaining routing, intrinsic footprint/process findings, canonical row-package
adoption, exact battery/part qualification, physical/electrical review and
independent Gate A remain open. No hardware was measured or fabrication output
released; vendor PDFs and local probe/build outputs are excluded from Git.
