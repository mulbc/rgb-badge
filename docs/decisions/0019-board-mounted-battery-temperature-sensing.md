<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0019: Trial board-mounted battery temperature sensing

- Date: 2026-10-05
- Status: Accepted by owner as a provisional design direction; thermal validation pending
- Supersedes: the **pack-integrated NTC location** requirement in ADR 0016, CHG-003 and SAF-001
- Retains: protected and keyed connectorized pack, autonomous hardware charge qualification, charger safety timer, exact-pack limits and independent Gate A review

## Context

Requiring a three-wire pack-integrated NTC has restricted the stock-pack search. The owner accepts trialing a thermistor on the battery-facing PCB near a protected two-wire pack. The BQ24074 `TS` input can suspend charging without MCU assistance when its thermistor indicates an out-of-range temperature. A sensor on the PCB is a proxy for cell temperature; charger and LED heat, ambient changes and any air gap can bias or delay it. The charger's own junction-temperature control does not measure the cell.

## Decision

For the next design pass, allow a protected **two-wire** pack and a board-mounted NTC connected directly to the charger's `TS` network. Keep the charger safety timer and hardware charge permission. Place the NTC in the battery-facing area, electrically insulated from the pouch, mechanically clear of it, and away from charger and LED heat where practicable. Do not use a fixed resistor or firmware-only temperature decision to bypass `TS` qualification. Choose the exact NTC and threshold network only after selecting the battery's documented charge-temperature range.

This direction broadens sourcing; it does **not** approve an exact pack, PCB location or temperature accuracy. Keep a keyed battery connector and verify its actual polarity. Do not place the pouch against components or consume the reserved swelling clearance to improve thermal contact.

## Verification before battery/board freeze

1. In the coupon, temporarily measure actual pack-surface temperature independently while logging board NTC temperature. Compare both through cold/warm starts, display OFF and ON charging, and representative warm enclosure operation at the selected pack's allowed ambient limits. Record hardware revision, pack MPN, setup and raw logs.
2. Set conservative hardware `TS` trip points using the **observed worst-case** cell-to-board difference and component tolerances, then inject hot, cold, open and short sensor faults. Charging must stop without MCU assistance; the safety timer remains active.
3. Include sensor placement, insulation, pack fit and those results in Gate A/B review. If the PCB sensor cannot bound cell temperature, return to a pack-mounted NTC or another independently qualified sensing arrangement.

Sources: [TI BQ24074 datasheet, battery-pack temperature monitoring](https://www.ti.com/lit/ds/symlink/bq24074.pdf); [Microchip charger-board example with a thermistor under an attached battery](https://onlinedocs.microchip.com/oxy/GUID-1CE2657F-0A40-47B3-AA7D-5FB057E6EF7C-en-US-5/GUID-2A9AE32E-553A-476D-A8C5-0BCF90F784F8.html); [TI cell-surface sensor placement guidance](https://www.ti.com/tw/lit/pdf/sluubc9). These are design references, not badge measurements.
