<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0003: ESP32-S3 module and external antenna

- Status: Accepted
- Date: 2026-09-05

## Context

The badge needs BLE, native USB, substantial flash and simple firmware development. The dense front matrix prevents the multilayer copper keepout required by a module PCB antenna.

## Decision

Use ESP32-S3-WROOM-1U-N16R8 with 16 MB flash, 8 MB PSRAM and an approved external 2.4 GHz FPC antenna positioned in a non-metallic case-edge zone away from the battery, body and magnets.

## Consequences

- RF validation must be performed in the worn orientation.
- Antenna part, cable routing and placement are release-controlled items.
- The existing classic ESP32-WROOM-32 board is useful only for portable software experiments; it is not representative of final USB, RF or peripheral behaviour.
