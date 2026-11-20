<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# DMC1229UFDB-7 row-stage decision screen, 2026-10-11

The [current LP452845 XY screen](../../mechanical/current-lp452845-xy-screen-2026-10-11.md) makes the exact Diodes `DMC1229UFDB-7` complementary pair the leading area-saving row-stage candidate. The manufacturer's [DS36128 Rev. 7-2 datasheet](https://www.diodes.com/datasheet/download/DMC1229UFDB.pdf) still lists the `-7` Type B tape-and-reel order code. This is a **calculation and source review**, not a measured or approved substitution. The canonical coupon still has 32 separate row transistors.

| Screen condition | Calculated result | Basis and limit |
|---|---:|---|
| Final 48-pixel white row at the current nominal TLC59581 setting | 0.699 A | 144 channels × 4.8545 mA; the driver setting is not a guaranteed current ceiling. |
| P-device drop and conduction loss at that current | 56.6 mV; 39.6 mW while ON | 81 mΩ maximum at −2.5 V gate drive and 25 °C short-pulse test. Hot compact-board resistance and transient/fault current are not bounded. |
| Illustrative 1.0 A row-current stress point | 81 mV; 81 mW while ON | Sensitivity calculation only; this does not raise the designed LED or regulator current. |
| N-device sink for the existing P-gate pull-up | 3.944 mA nominal | 3.944 V / 1 kΩ. Its datasheet gives at most 65 mΩ RDS(on) with only 1.5 V gate drive at 25 °C, so the proposed 3.3 V decoder drive is well above a characterized test voltage. This does not bound the decoder's edge timing. |
| Gate-source voltages in the proposed row topology | about +3.3 V N; −3.944 V P | Both are below the datasheet's ±8 V absolute limit at nominal rails; transients still need a real-circuit review. |

The transistor's P-channel test-board current rating of −3.0 A at 70 °C uses a 1 × 1 inch high-copper PCB; it must **not** be applied as the badge's thermal rating. The 39.6 mW calculation is encouraging for a single selected row but does not close the LED-driver tolerance, simultaneous-row fault, hot-resistance, small-copper or switching-loss cases. Its typical 10.7 nC P-gate charge at −4.5 V also does not establish turn-off time with the present 1 kΩ pull-up. Row overlap, ghosting and dead time require waveform measurement on the chosen coupon stage.

The physical-pole drawing identifies S1/G1/D1 and S2/G2/D2 and pin 1, but the [first-author footprint audit](../../hardware/coupon/rev-a/dual-row-package-library-audit.md) still needs independent confirmation of the **numeric 2–6 pad sequence** before a symbol can be connected. Its 0.15 mm edge-to-center copper gap and full-size paste also need assembler review. These two concrete items, together with the unbounded real row current/heat, prevent accepting the substitution now. Next, obtain a manufacturer-confirmed numbered pin drawing or directly verify the package terminals, then connect one exact-part coupon row for native pin/net review and bench switching tests before replacing all sixteen stages. Independent Gate A remains required before fabrication.
