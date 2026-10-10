<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Coupon project-local footprints

Only footprints checked against a controlled manufacturer package drawing belong here. Each footprint review must record pad numbering, dimensions, polarity/orientation marks, courtyard, paste/mask treatment and the source drawing revision.

The LED footprints are traced in the adjacent [LED audit](../led-audit.md). Charger and converter footprints are traced in the [power-library audit](../../power-library-audit.md). The GCT connector draft is traced separately in the [USB4505 audit](../../usb-connector-audit.md); its `Dwgs.User` lines are review datums rather than a qualified board cutout. Their presence records a first-author dimensional transcription, not the independent pin/pad/polarity review required before fabrication.

The unpopulated `U-DFN2020-6_TypeB_Diodes_DMC1229UFDB` candidate follows [proposed ADR 0020](../../../../../docs/decisions/0020-dual-row-mosfet-package-proposal.md) and the separate [land-pattern record](../../dual-row-package-library-audit.md). It is not assigned to the canonical row schematic.

The `SOT563_TI_DRL0006A` temperature-switch footprint follows [ADR 0024](../../../../../docs/decisions/0024-lp452845-pack-and-temperature-window.md) and its [pin/pad audit](../../tmp390-library-audit.md). The exact `TMP390A2DRLR` is root-linked on the temperature sheet; its gate output is still a named boundary. The `NTC_Murata_NCU15_0402` first-author land is traced in the [temperature capture review](../../../../../docs/development/charger-temperature-capture-review-2026-10-10.md).

The staged `JST_PH_S2B-PH-SM4-TB` footprint follows the [battery-header audit](../../jst-ph-header-library-audit.md). Its two electrical pads and two retention lands are source-checked and natively rendered; cable polarity and physical mating are not yet qualified.
