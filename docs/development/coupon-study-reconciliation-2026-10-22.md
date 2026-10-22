<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Canonical circuit versus routed study

Status: **source assignment checked with documented study exceptions**.
The routed board remains unbuilt, noncanonical and prohibited from fabrication.
The initial audit changed no PCB source. The subsequent [metadata projection](coupon-study-metadata-2026-10-22.md) adds exact shared identity fields without changing components, pads, nets, placements, copper or current settings.

The [checker](../../tools/check-coupon-study-contract.py) compares the saved
[native-control study](../../hardware/coupon/rev-a/staging/led-native-control-trial-114mm.kicad_pcb)
with a [canonical source snapshot](../../mechanical/review/coupon-canonical-net-contract.json).
A fresh KiCad 10.0.6 XML export passes the existing complete 497-component,
1,814-logical-pin circuit contract before snapshot creation. The snapshot
records exact canonical MPN/manufacturer/value/footprint properties, pin nets,
explicit no-connects and source-file hashes. It contains project-derived facts;
vendor PDFs and the temporary native XML are excluded from Git.

Each ordinary check verifies source hashes, compares canonical part properties
directly with placed schematic source, and checks snapshot nets against the
existing complete circuit model through a reconstructed XML representation.
That last step is model-side verification, not another native export. Local
`--netlist` verification compares a fresh checked native export with the same
snapshot. Refresh rejects XML older than the canonical source files. Neither
source hashes nor the circuit model replace native ERC, physical connectivity,
DRC or electrical review.

## Findings

The [retained report](../../mechanical/review/coupon-study-reconciliation.json)
accounts for the complete 497-versus-483 population difference:

- All **465 common components** match canonical values, footprint identifiers
  and every electrical pad assignment: **1,718 logical pins / 1,747 physical
  electrical pads**. Explicit no-connect pins must remain netless. The extra
  physical lands are not collapsed when checking pad nets.
- **69 unnumbered non-copper apertures** and **two netless J2 mounting pads**
  are accounted for separately. Unknown numbered copper pads, connected
  mounting pads and missing electrical pins are rejected.
- Canonical **Q1–Q32** remain absent. The sixteen `NTLJD3119CTBG_TRIAL_ONLY`
  pairs have the documented six-terminal/eight-land pin assignments mapped
  to the canonical P/N endpoint nets, including both physical drain lands.
  Logical agreement does not select that package or replace the canonical
  schematic/BOM, manufacturer land/process review or independent Gate A.
- `PROJ_U1_2` and `PROJ_U1_3` remain exact **netless projected driver geometry**.
  Adding nets or an orderable MPN annotation to these projections is rejected.
- All **465 common PCB footprints now contain explicit MPN and Manufacturer fields** copied from canonical source. Exact values and field presence are required by ordinary checks, including the 22 blank canonical MPN values and five blank manufacturer values. The blanks remain visible in the report; no missing identity is invented. Copying source metadata does not qualify a PCB BOM or select the trial row package.

The output always retains `fabrication_release_allowed: false`. Passing means
that the known study exceptions are accounted for; it does not mean the board
is canonical, fully routed, DRC-clean or electrically qualified.

## Repeat and verify

CI runs these standard-library checks without KiCad, native XML or vendor PDFs:

```sh
python3 tools/check-coupon-study-contract.py
python3 -m unittest discover -s tools/tests -p test_coupon_study_contract.py -v
```

A local fresh native export plus the same checks is available through:

```sh
./tools/check-coupon-study-contract.sh
```

Refresh the source snapshot only from a reviewed fresh export after an intended
canonical source change; `--refresh-contract` requires `--netlist`. An ordinary
check does not modify the snapshot, PCB or other project sources.

All **21 fault-test methods** pass, including controller net/NC changes,
value/footprint/MPN/manufacturer changes, missing identity fields, cleared or invented identity values, missing/extra components,
missing pins, trial gate swaps/duplicate-drain loss, connected projections or
mounting pads, unknown copper pads, forged snapshot net/MPN entries, source
hash drift, duplicate PCB references and stale native XML. A separate temporary
checkout containing only the declared CI inputs passes the same suite.
[Validation identities](../../mechanical/review/coupon-study-reconciliation-validation-2026-10-22.json).

The current routed PCB SHA-256 is `29d1f9cec25abc5ed199dd29b96c11338a646a2a95c4e6b49667e9a1b41bcf7e`. The
[gauge IC data continuation](led-gauge-ic-data-study-2026-10-22.md) lowers
native opens to 223 with exactly the same 104 intrinsic clearance findings,
without changing component metadata, pad assignments or canonical source.
The earlier metadata-only `20e56a77...` checkpoint differed from `0fd1f0df...`
only in hidden shared identity properties. Its
[validation record](../../mechanical/review/coupon-study-metadata-validation-2026-10-22.json)
is historical; the current native evidence is linked from the routing study.
An earlier UART-pad route merge added shorts, and a local isolated TP4 placement
search found no acceptable site within its bounded rear-side search. Both
remain rejected local probes; neither result proves routing impossible.
