<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0004: Standalone charging and hard application-off state

- Status: Accepted baseline; implementation requires Gate A review
- Date: 2026-09-05

## Context

The latching switch must make the application visibly and electrically off, while USB charging must continue without firmware. The badge also needs a compliant conservative USB input state and faster charging from a capable Type-C source.

## Decision

Use a BQ25616J-class standalone switching charger/NVDC power path. The slide switch controls the enables of the 3.3 V and LED converters; it does not carry matrix current. Charging, the fuel gauge and hardware charge indication remain upstream.

Use TUSB320LAI Type-C sink detection and a fail-safe hardware `ILIM` network. The passive/default/unattached state is 500 mA. A higher approximately 1.2 A input limit is allowed only for a valid 1.5 A or 3 A advertisement. Application firmware is not in this safety loop.

## Consequences

- USB data is available only with the slide switch ON.
- Charge current is fixed by hardware and bounded by the exact cell specification.
- The charger's isolated BC1.2 D+/D− behaviour, the TUSB320 truth table and every attach/detach transient require explicit schematic review and bench validation.
