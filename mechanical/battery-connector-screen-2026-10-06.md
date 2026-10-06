<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Battery connector and board-space screen

Status: **candidate and geometry screen, not a connector or pack selection**. The leading LiPol `LP503055` drawing specifies a protected, bare-wire pack with two AWG 28 leads, a 475 mA maximum charge current and a 950 mA maximum continuous discharge current. The wire insulation diameter, exact cable exit after termination, stocked assembly, connector polarity and crimp quality are not documented for a connectorized order. The pack remains unselected. [LiPol drawing](https://www.lipolbattery.com/LiPo-Battery-Datahseet/LiPo_Battery_LP503055_3.7V_950mAh.pdf).

## Candidate comparison

| Family | Manufacturer evidence | Disposition |
|---|---|---|
| JST GH, 1.25 mm pitch, locking `SM02B-GHS-TB` + `GHR-02V-S` + `SSHL-002T-P0.2` | 1.0 A rating **at AWG 26**; contact accepts AWG 30–26 and 0.76–1.0 mm insulation. [JST GH specification](https://www.jst-mfg.com/product/pdf/eng/eGH.pdf). | Compact, but its published 1.0 A test wire is not the pack's AWG 28. No #28 current margin has been established against the pack's 0.95 A continuous capability. Do not freeze it from the family rating alone. |
| JST PH, 2.0 mm pitch, side-entry SMT `S2B-PH-SM4-TB` + `PHR-2` + `SPH-002T-P0.5S` | 2 A family rating **at AWG 24**; the named crimp contact accepts AWG 30–24 with 0.8–1.5 mm insulation. The SMT side-entry header is listed by JST. [JST PH specification](https://www.jst-mfg.com/product/pdf/eng/ePH.pdf). | Better provisional electrical margin and compatible wire gauge range, subject to the actual AWG 28/insulation-specific current rating, mating orientation, polarity and supplier termination. Its mated package is substantially harder to fit. |

The connector must be ordered as an **exact matched assembly**, with pin 1/pin 2 polarity checked from the header mounting-side view through the mated housing to red/black pack wires. Neither this screen nor the common connector-family name establishes that polarity. The battery supplier or qualified cable assembler must confirm the crimp terminal, insulation diameter, pull test and protected pack assembly. No substitution of a generic “JST battery connector” is permitted.

## Existing rear-layout screen

The [fit-trial generator](../tools/screen-final-fit-trial.py) now tests a deliberately illustrative **8.0 × 9.6 mm** side-entry, mated-connector pocket in both orientations on a 0.25 mm grid. It excludes the battery body and currently anchored courtyards. The [machine-readable result](review/fit-trial.json) finds **zero free pocket positions in either orientation even before the remaining small parts are first-fit** on the current 106 × 32.5 mm trial board. This is a conditional collision result for that particular grouped arrangement, not a conclusion that a reworked KiCad placement cannot fit a connector. The pocket is not a transcribed JST land pattern; wire bend, strain relief, case wall, routing and mounting features would require more space.

The useful next placement change is to move the USB/driver/row-stage groups as a whole while reserving the connector and wire exit first, then pack the remaining small parts. Do this with an exact pack termination and a manufacturer-audited project-local connector footprint. The complete power netlist and case support are still absent, so this screen does not authorize a PCB or pack order.
