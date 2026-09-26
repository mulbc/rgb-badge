<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# BQ24074 OFF-charge thermal screen

2026-09-26. Calculated **no-system-load** sensitivity screen for exact `BQ24074RGTR`, not an actual board temperature, charge-rate qualification, pack selection or authorization to assemble a battery-powered board. The BQ24074 PowerPath, protection and pack NTC circuits are not captured yet. This screen is independent of the unresolved EN1/EN2/input-protection topology.

## Datasheet basis and assumptions

TI's [BQ24074 family datasheet SLUS810N](https://www.ti.com/lit/ds/symlink/bq24074.pdf), sections 8.4, 8.5 and 12.3, gives `RθJA = 44.5 °C/W` for the RGT 16-pin package and a **125 °C junction thermal-regulation point**. TI's equation (11) is `P = (VIN − VOUT) × (IOUT + IBAT) + (VOUT − VBAT) × IBAT`. Setting `IOUT = 0` reduces it to **`P ≈ (VIN − VBAT) × IBAT`**, neglecting quiescent and auxiliary consumption. This simplification does not model ON charge-through operation. TI says the fast-charge cell voltage usually rises to approximately 3.4 V within two minutes and suggests using that for thermal design; 3.0 V is retained as a short early/edge example, not a sustained fast-charge assumption.

Use **5.5 V at charger IN as an illustrative upper-voltage case** because normal USB VBUS can reach 5.5 V under [ADR 0014](../../../docs/decisions/0014-usb-voltage-envelope-and-logic-ldo.md). Cable and protection drops usually lower IN; they are not assumed as guaranteed savings. Use **40 °C local ambient** solely as a sensitivity point for a worn/small enclosure, not a product environmental limit or a measurement. Assume a steady 44.5 °C/W *only as the datasheet reference*: TI explicitly says board copper, orientation, airflow and neighbouring surfaces change thermal impedance. The finished PCB/case may have a materially different effective value.

| ISET case and source of calculated **maximum** | BAT voltage | Idealized dissipation at 5.5 V IN | Open-loop junction at 40 °C using 44.5 °C/W | Maximum effective θJA for open-loop junction below 125 °C at 40 °C |
|---|---:|---:|---:|---:|
| Existing 1.13 kΩ draft: 0.872 A, **not compatible with the screened packs** | 3.0 V | 2.180 W | **137.0 °C** | 39.0 °C/W |
| Existing 1.13 kΩ draft: 0.872 A, **not compatible with the screened packs** | 3.4 V | 1.831 W | 121.5 °C | 46.4 °C/W |
| 1.50 kΩ *numerical* proposal for 700 mAh coupon pack: 0.657 A | 3.0 V | 1.643 W | 113.1 °C | 51.8 °C/W |
| 1.50 kΩ *numerical* proposal for 700 mAh coupon pack: 0.657 A | 3.4 V | 1.380 W | 101.4 °C | 61.6 °C/W |
| 2.49 kΩ *numerical* proposal for 400 mA-rated 800 mAh pack: 0.396 A | 3.0 V | 0.990 W | 84.1 °C | 85.9 °C/W |
| 2.49 kΩ *numerical* proposal for 400 mA-rated 800 mAh pack: 0.396 A | 3.4 V | 0.832 W | 77.0 °C | 102.2 °C/W |

Inputs 0.872/0.657/0.396 A are the existing worst-corner ISET arithmetic from [pack screening](../../../docs/sourcing/pack-screen-2026-09-25.md), not proposed delivered current or a promise that input-current limiting/thermal control leaves the current unchanged. Figures rounded only for display; sample calculation: `(5.5 − 3.4) V × 0.872 A = 1.8312 W`, `40 + 44.5×1.8312 = 121.49 °C`. The 3.0 V / 0.872 A row predicts a junction above thermal regulation **if current were held constant**; the actual IC reduces charge current when its die reaches 125 °C. This row does not claim the device will operate at 137 °C. At 3.4 V the same draft current has only ~3.5 °C between that illustrative open-loop result and regulation on TI's reference board, before other losses and packaging.

The numerical 1.50 kΩ/700 mAh case is less demanding thermally, but the documented pack's 700 mA charging ceiling and **700 mA continuous discharge ceiling** still apply. Its full-badge runtime and peak-power model are inadequate; it remains a coupon-only candidate. The 400 mA-rated pack/case is cooler in this simplified calculation but its ideal minimum time to 80% is about **96 minutes**, conflicting with the present 60-minute upper charge target. Do not raise charge current to offset either a thermal or time shortfall.

## Implications for board and bench work

- This is a **real thermal design risk**, particularly if the final enclosure insulates the charger or allows charge-through display load. It is not proof that the actual charger or case gets hot; junction temperature, pouch temperature and touch surface temperature are distinct.
- Keep the RGT exposed thermal pad tied to the documented ground network and reserve real copper/thermal-via area consistent with TI's layout guidance and assembler capability. The [trial rear placement](../../../mechanical/preliminary-placement-screen-2026-09-26.md) does not reserve that copper. Do not place the pouch against the board solder/charger region merely to save thickness.
- In the coupon charge test after schematic/layout review, log USB voltage and current, pack voltage and charge current, charger-pad board temperature, case exterior temperature and ambient over a depleted-to-full cycle with the display OFF. Repeat ON charge-through and warmer ambient as defined in the Gate A plan. Thermal regulation slows the charge timer and battery charge current; the application cannot claim 45–60-minute 80% charging from a nominal resistor alone.
- Finish exact pack ISET/NTC/timer limits and independent Gate A review **before** assembly or an order. No charger resistor, pack, board stack-up or circuit changed in this screen.
