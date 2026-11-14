<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Provisional battery-header source review, 2026-10-11

[ADR 0029](../decisions/0029-provisional-battery-header-polarity.md) assigns exact JST `S2B-PH-SM4-TB` to J2 on the [root-linked charger sheet](../../hardware/coupon/rev-a/charger-core.kicad_sch). J2.1 joins BQ24074 BAT pins 2/3 and C53 on `+BAT_PROTECTED_DRAFT`; J2.2 joins ground. The local symbol has two numbered passive pins and maps to the previously audited local JST footprint's identically numbered contact pads. The BAT `PWR_FLAG` represents the external protected pack entering through J2 for ERC, with no BOM or board item. Its presence does not imply a pack is plugged in.

KiCad CLI 10.0.6 native ERC on the full 19-page root schematic reports **zero configured violations**. Full native XML has **461 PCB items / 1,695 logical pins**; the charger checker verifies all **9 items / 34 pins**, including both J2 connections. The focused ERC/XML are `/private/tmp/rgb-battery-j2-second.rpt` and `/private/tmp/rgb-battery-j2-second.xml`; full check output is `/private/tmp/rgb-battery-j2-full-check-20261011.log`. Page 16 of `/private/tmp/rgb-battery-j2-review-20261011.pdf` was rendered at `/private/tmp/rgb-battery-j2-page16.png` and visually reviewed after moving J2's labels clear of its contacts. These are schematic/source checks only.

The complete host suite passed **173 tests** on 2026-10-11, including a fault test that corrupts J2.1 in the exported netlist and requires the full-project checker to reject it.

The exact selected LP452845 assembly's as-shipped housing polarity is **unknown**. Before first mating, measure the delivered protected output at both keyed cavities, repin if required, then independently check the populated header's pad polarity and housing orientation. Record the results with pack lot and hardware revision. No battery or board has been physically tested; connector engagement, pack fit and independent Gate A review remain open.
