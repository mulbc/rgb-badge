<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Panasonic ERJ2 order-code normalization

2026-09-30. The KiCad source previously inserted a hyphen after `ERJ` in the Panasonic resistor symbol name, Value, MPN property, and seven placed schematic sheets. That punctuation is absent from Panasonic's **Parts no** field: see the [511 kΩ](https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ2RKF5113X), [91 kΩ](https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ2RKF9102X), and [2.2 Ω](https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ2RCF2R20X) exact-part pages. The [ERJ series datasheet](https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf) defines the resistance-code format. The schematic/library/generator/checker identities are now normalized together; the `R_Panasonic_ERJ2_0402` footprint name is a **project-local** name and stays unchanged.

| Previously stored alias | Panasonic order-code target | Intended nominal resistance |
|---|---|---:|
| `ERJ-2RKF1001X` | `ERJ2RKF1001X` | 1 kΩ |
| `ERJ-2RKF1002X` | `ERJ2RKF1002X` | 10 kΩ |
| `ERJ-2RKF1003X` | `ERJ2RKF1003X` | 100 kΩ |
| `ERJ-2RKF2201X` | `ERJ2RKF2201X` | 2.2 kΩ |
| `ERJ-2RKF22R0X` | `ERJ2RKF22R0X` | 22 Ω |
| `ERJ-2RKF3922X` | `ERJ2RKF3922X` | 39.2 kΩ |
| `ERJ-2RKF4990X` | `ERJ2RKF4990X` | 499 Ω |
| `ERJ-2RKF6203X` | `ERJ2RKF6203X` | 620 kΩ |
| `ERJ-2RKF8873X` | `ERJ2RKF8873X` | 887 kΩ |
| `ERJ-2RCF2R20X` | `ERJ2RCF2R20X` | 2.2 Ω |

Two unplaced 3.3 V feedback symbols, `ERJ2RKF5113X` and `ERJ2RKF9102X`, were normalized in the preceding increment. The 2.2 Ω `2RC` family is distinct from the `2RK` family and has [−100 to +600 ppm/K](https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ2RCF2R20X), so a shared 100 ppm/K assumption would be wrong. This change does not select a different resistor or change connectivity, values, pads or coordinates. Historical native review SVGs and review records retain their original spelling as evidence of the earlier source state.

The host generator, source, and checker must agree; the next owner KiCad 10.0.6 export must confirm **zero ERC**, complete native XML and rendered symbol names after this migration. This is still a candidate BOM, not purchasing or manufacturing release. At assembly quoting, match every exact unhyphenated order code, packaging and traceable supplier; no aliases or substitutions in the fabrication BOM.
