<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0004: Standalone charging and hard application-off state

- Status: Partially superseded by ADR 0009 and ADR 0010; hard-OFF principle retained
- Date: 2026-09-05

## Context

The latching switch must make the application visibly and electrically off, while USB charging must continue without firmware. The badge also needs a compliant conservative USB input state and faster charging from a capable Type-C source.

## Decision

The original decision selected a BQ25616J-class standalone switching charger/NVDC power path. The slide switch controls the enables of the 3.3 V and LED converters; it does not carry matrix current. Charging, the fuel gauge and hardware charge indication remain upstream.

ADR 0009 rejected that charger's provisional direct `ILIM` implementation. ADR 0010 replaces it with a BQ24074/BQ24392/TUSB320/TS3USB31E source-qualified topology while retaining the standalone charger, physical OFF switch, hardware current ceilings and no-firmware high-current grant principles.

## Consequences

- USB data is available only with the slide switch ON.
- Charge current is fixed by hardware and bounded by the exact cell specification.
- The selected BC1.2/data-switch circuit, USB default-current behavior, priority logic and every attach/detach/suspend transition require explicit schematic review and bench validation.
