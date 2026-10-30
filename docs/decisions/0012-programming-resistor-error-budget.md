<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0012: Include temperature and drift in programming-resistor limits

- Status: Accepted for part selection and capture; assembly/service qualification pending
- Date: 2026-09-17
- Amends: ADR 0011 resistor specification; nominal values and permission policy unchanged

## Finding

The [supervisor-stage assessment](../../hardware/coupon/rev-a/usb-supervision-capture.md) found that an ordinary 1%, 100 ppm/K candidate does not preserve the configured-SDP margin at temperature. Initial tolerance cannot consume the complete resistance-error budget before temperature, assembly shifts or aging are included.

## Decision

Keep 3.65 kohm base ILIM, 3.48 kohm switched boost and 1.13 kohm ISET. Select these exact Panasonic thin-film parts for capture:

| Role | Manufacturer MPN | Initial tolerance | TCR |
|---|---|---|---|
| Base ILIM | [ERA2AEB3651X](https://industrial.panasonic.com/ww/products/pt/high-precision-chip-resistors/models/ERA2AEB3651X) | ±0.1% | ±25 ppm/K |
| Boost ILIM | [ERA2AEB3481X](https://industrial.panasonic.com/ww/products/pt/high-precision-chip-resistors/models/ERA2AEB3481X) | ±0.1% | ±25 ppm/K |
| ISET | [ERA2AEB1131X](https://industrial.panasonic.com/ww/products/pt/high-precision-chip-resistors/models/ERA2AEB1131X) | ±0.1% | ±25 ppm/K |

The existing current-limit calculations retain a **±1% total resistance envelope**, now an explicit qualification requirement covering initial tolerance, temperature, assembly shift and service drift. It is not the new parts' initial-tolerance rating. The exact parts were previously unspecified; this is a documented selection, not a silent BOM substitution. Do not use generic 1% ERJ parts in these three positions.

For design evaluation, allow ±0.5% combined additional assembly/service drift after initial tolerance and temperature. Across the assumed -40..85 C resistor-body range, use 65 K maximum displacement from the resistance reference temperature. The multiplicative interval is:

`Rmin/Rnom = 0.999 × 0.998375 × 0.995 = 0.992389741875`

`Rmax/Rnom = 1.001 × 1.001625 × 1.005 = 1.007639758125`

Both fit inside the retained 0.99–1.01 envelope. The ±0.5% drift term is a **project allocation requiring qualification**, not a manufacturer lifetime guarantee. The individual catalog stress-test limits do not establish an arbitrary service life or a sequential combination of stresses. Verify actual assembly shifts and the intended environmental/service profile before Gate A closes this allocation. Resistor body temperature, not just room temperature, must stay within the modeled range; otherwise recalculate.

Keeping the larger ±1% envelope preserves all previous ceilings: configured-SDP resistor-limited charger input remains at most 0.475993 A before auxiliary/switch allowances, high input at most approximately 0.9753 A with an ideal switch, and charge at most approximately 0.8716 A. No input or charge limit is raised. The exact pack must still permit the full charge ceiling; a lower-rated pack forces a larger ISET resistor.

## Implementation and limits

Add exact project-local symbols and an ERA2-specific 0402 footprint controlled by the manufacturer body/land drawings. Their current role is library preparation; no charger or boost switch is populated by this decision. Library rendering is reviewed with the next native checkpoint.

The whole-port current proof remains incomplete: 20 mA auxiliary and 2 mA programming-network allocations need actual upper bounds, and unconfigured/suspend states have separate budgets. The temperature-only counterexample stays as a regression test. `check-power-design.py --require-usb-closure` must keep failing until the entire input path is closed.

## Source provenance

Manufacturer exact-part pages and [ERA-A datasheet, 24-Apr-2024](https://industrial.panasonic.com/cdbs/www-data/pdf/RDM0000/AOA0000C307.pdf), checked 2026-09-17. The [library audit](../../hardware/coupon/rev-a/programming-resistor-audit.md) records controlled dimensions, hashes and calculation assumptions. These selections authorize design work, not procurement or fabrication.
