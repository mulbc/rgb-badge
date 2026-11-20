<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Remaining Murata capacitor footprint source audit

2026-11-05. First-author library/source review under
[ADR 0084](../../../docs/decisions/0084-remaining-murata-source-migration.md).
This records CAD geometry, not assembly or hardware qualification.

The owner-supplied June 10, 2026 manufacturer reference sheets, exact-byte
hashes and full page-27 diagram/Table 2 review are recorded in the
[drawing study](../../../docs/development/remaining-murata-lands-2026-11-04.md).
The ±0.20 mm dimensional-tolerance rows apply to both parts. In that diagram,
a is the inner copper gap, b one land length and c transverse land width.

| Source part stem | References | Selected a / b / c, mm | Pad centres, mm |
| --- | --- | --- | --- |
| GRM187R61A226ME15 | C40/C41/C46/C47/C48/C49/C56/C61 | 0.80 / 0.75 / 0.90 | ±0.775 |
| GRM219R60J476ME44 | C42/C43 | 1.20 / 0.70 / 1.30 | ±0.950 |

Dedicated project-local footprints use two rectangular SMD lands with matching
copper/paste/mask layers. The nonpolar capacitor symbol retains passive pins
1/2 and all assigned nets. Native footprint copper and paste exports show two
separate rectangles. Fabrication bodies remain 1.6 × 0.8 and 2.0 × 1.25 mm;
conservative project courtyards remain 3.0 × 1.3 and 3.6 × 2.0 mm. Courtyards
are project choices, not manufacturer-specified assembly lands. Native body/
courtyard exports were reviewed separately from copper and paste.

Canonical embedded/placed/library symbols and deterministic generators share
these assignments. Legacy GRM18/GRM21 footprints remain unchanged for historical
studies; their descriptions must not be treated as verified current geometry.
No source MPN suffix is selected here. D/J packaging choices, separate approval
consultation, actual-board land/stencil/process evaluation and electrical
capacitance under bias/temperature/aging remain open. Independent Gate A and
fabrication holds remain unchanged.
