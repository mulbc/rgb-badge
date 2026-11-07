<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0029: Provisional battery-header polarity and harness acceptance

- Date: 2026-10-11
- Status: Accepted for schematic capture only; physical polarity remains unverified
- Relates to: ADR 0024, BAT-001, CHG-001 and Gate A

## Decision

Capture exact JST `S2B-PH-SM4-TB` as J2 with numbered pad 1 on `+BAT_PROTECTED_DRAFT` and pad 2 on GND. The connector pin numbers and board land follow the JST PH drawing and the project-local footprint audit. This assignment is a board-side design choice, **not** a claim that the selected LiPol `LP452845` assembly's as-supplied `PHR-2` wire order matches it. The owner permits repinning the harness if necessary.

Before mating a delivered pack to any board, inspect the keyed mating view and measure protected-output polarity at its housing cavities with a meter. Record the pack lot/drawing revision, cavity-to-wire map and measurement; repin the housing with the correct contact tooling if its order is opposite. Then check the completed board header's pad 1/2 polarity against the schematic and confirm correct mating orientation. Do not connect a reversed pack, and do not treat wire colour as sufficient evidence.

## Limits

This lets the schematic gain a real protected-pack entry. ERC's `PWR_FLAG` on the BAT net now marks the external pack supply through J2; it is not a board component or substitute battery. The capture does not qualify stock, discharge duty, charge temperature, connector retention, battery protection, or the physical assembly. The inaccessible assembly PDF leaves as-supplied lead polarity unresolved until receipt or a readable manufacturer confirmation. No board or battery has been tested. Gate A remains required before fabrication.

Source: [JST PH series drawing](https://www.jst-mfg.com/product/pdf/eng/ePH.pdf), pages 2 and 4; [existing header land audit](../../hardware/coupon/rev-a/jst-ph-header-library-audit.md).
