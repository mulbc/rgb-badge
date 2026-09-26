<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Staged gauge/switch boundary, 2026-09-26

The canonical KiCad `gauge.kicad_sch` contains `U35` MAX17048, `C39` 100 nF local bypass, and `R79/R80` exact Panasonic `ERJ-2RKF2201X` I²C pull-ups (2.2 kΩ each). `ALRT` has an explicit no-connect; `QSTRT`, CTG, GND and the thermal pad are grounded. VDD and CELL share the named **`+BAT_GAUGE_SW`** net, which is **not** yet connected to a real battery or switch. `#FLG06` tells draft ERC to accept this as an assumed source. It does not prove charging, isolation or OFF current. Pull-ups connect only to `+3V3_APP`; an absent MCU/rail must not source SDA/SCL while the gauge is OFF. The dedicated source and full KiCad-exported XML checks reject an accidental raw-BAT connection or replacement with the existing 10 kΩ resistor.

The [Littelfuse/C&K JS series Rev. January 14, 2026 drawing](https://www.littelfuse.com/assetdocs/littelfuse-c-k-slide-js-series-datasheet?assetguid=aba42b08-0d2c-423b-813d-a2faa5a3bb14) identifies exact candidate `JS202011JAQN` as a right-angle, J-bend SMT **DPDT non-momentary, non-shorting** slide switch, with silver contacts, 2 mm travel, 0.3 A at 6 VDC (or 0.1 A at 30 VDC), 70 mΩ maximum contact resistance and 5,000 make/break cycles. The drawing on printed page 8 gives six contact positions with two commons (2 and 5); check the terminal-1 chamfer, pad dimensions, top/bottom viewing orientation and selected ON throw against a native rendered footprint before any symbol/land-pattern freeze. The switch will carry the microamp-scale gauge branch and an enable/control branch, **not** the LED rail or pack charge current. The separate poles' transition skew, OFF leakage and physical case clearance have no established guarantee from this drawing.

On the eventual switch/charger sheet, connect one pole from the **protected pack positive** to `+BAT_GAUGE_SW` in the mechanically identified ON position. The other pole controls the application regulator enables with hardware OFF defaults. Leave both unused throws genuinely unconnected. Keep charger BAT and hardware charge status on the protected pack side, so qualified-source OFF charging does not depend on MCU firmware. Verify switch contact order and bounce, including the interval when one pole is ON and the other is OFF. Reconcile the switch footprint against the actual 110 × 35 × 11 mm case and 3D-printed actuator opening. Do not replace the PWR_FLAG with a new label until a **physical circuit** drives the rail.

## Outstanding native and hardware evidence

1. Native KiCad 10.0.x ERC, project-local symbol exports and full XML check for this staged sheet. Its flag is explicitly a boundary assumption.
2. Pin/pad/courtyard/actuator drawing audit for the exact switch, native visual inspection and independent Gate A engineer review. The switch is **not yet** a selected production MPN or a placed schematic component.
3. Whole-bus rise/LOW timing and off-state back-power tests, then USB-absent OFF current under 50 µA on an unprogrammed coupon. Confirm charge status and source-limited charging while OFF.
4. Chosen protected pack/NTC/connector, current-limit and post-OFF-charge SOC recovery qualification. No pack has been selected.

The [ADR 0015](../../../docs/decisions/0015-switch-fuel-gauge-with-application.md) decision and [gauge contract](fuel-gauge-capture-contract.md) govern the intended final design; this sheet provides a reviewable electrical fragment, not a power-subsystem release.
