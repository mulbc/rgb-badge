<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0013: Type-C-only charging with one fixed input limit

- Status: Accepted by owner; capture and qualification pending
- Date: 2026-09-18
- Supersedes: ADRs 0010/0011 source policy and switched ILIM topology
- Retains: battery safeguards, current ceilings, OFF charging, operation while charging and independent Gate A

## Decision

Charge only when the Type-C source advertises 1.5 A or 3 A. USB-A connections and default-current Type-C connections do not power the system through the charger or charge the battery. Native USB data remains available while ON, with the application battery-powered when charging permission is absent. A depleted or missing battery is therefore not guaranteed to support USB recovery on an unsupported source.

Use one permanent resistor-programmed input-current limit, no switched parallel branch and no firmware charging grant. Keep BQ24074, TUSB320LAI, the USB-only logic supply and application-powered TS3USB31E isolation. Remove BQ24392 BC1.2 detection, its support parts and all BC/SDP/application-grant gates. ADG4612 is no longer needed for ILIM switching; its library remains historical candidate evidence only.

The current ceilings are not increased. Initially retain the already audited 3.65 kohm and 3.48 kohm precision resistors **permanently in parallel** as a single fixed setting: ideal calculated input range 0.834–0.975 A with the retained ±1% total resistance envelope. Two passive resistors avoid a new library/MPN review; there is no analog switch or intermediate node. A later single-resistor replacement requires its own value/tolerance check. ISET and battery prerequisites remain unchanged. The total-resistance qualification remains applicable, but switch leakage no longer contributes programming error.

## Stable policy

`CHARGE_REQUEST = VBUS_VALID AND LOGIC_READY AND NOT OUT1`

TUSB320LAI GPIO Table 3 maps OUT1/OUT2 to 11 unattached, 10 default, 01 1.5 A and 00 3 A. OUT2 is retained for diagnostics, not an additional grant. No application GPIO, USB configuration/suspend grant, or BC1.2 status feeds this request. Advertisement reduction to default removes charging permission. Firmware does not control input-current selection.

| Source | OFF | ON |
|---|---|---|
| No USB | No charge | Battery playback |
| USB-A or default-current Type-C | Charger standby | Battery operation; USB data if a host is present |
| Type-C advertising 1.5 A/3 A | Autonomous fixed-limit charge | Fixed-limit charge/PowerPath; USB data if a host is present |

The charger EN1/EN2 physical defaults must still enforce standby when permission is absent. A logic truth table is not a power-up/brownout proof. Protection, supply qualification, whole-port standby/current budget, input transients, exact pack/NTC and thermal analysis remain required. No circuitry is cleared for fabrication by this decision.

## Consequences

Eliminates dual-current selection, precision actuator leakage, BC1.2 classification/timer concerns and firmware-to-charger permission sequencing. Charging speed remains conditional on the pack and thermal results. The preserved data isolator prevents an OFF application's USB path from being treated as automatically safe merely because BC detection was removed.

Previous native reviews remain evidence for unchanged libraries and circuit sections, not acceptance of the revised three USB sheets. Historical calculations/tests must be labelled as such. Request one combined native checkpoint after the functional migration, not one per removed component.

Sources: [TUSB320LAI SLLSEQ8D](https://www.ti.com/lit/ds/symlink/tusb320lai.pdf), GPIO Table 3; [BQ24074 SLUS810N](https://www.ti.com/lit/ds/symlink/bq24074.pdf), EN mode table and external ILIM factors; previous source audits remain applicable.
