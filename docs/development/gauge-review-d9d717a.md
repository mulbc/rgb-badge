<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Native staged-gauge visual correction review: d9d717a

Reviewed 2026-09-27. Owner-generated KiCad 10.0.6 export for `coupon-power-rev-a` at `d9d717a2c2d98f662cbe13ff153925cdd2ab1ff5`, following the [first gauge review](gauge-review-20fdf48.md). This is first-author source review, not independent Gate A, battery qualification or fabrication release.

## Evidence and disposition

Owner attachment `gauge-review-d9d717a.zip`, SHA-256 `e903e9819d35b4a0d210df7c7a6fc5277687855ef7c5ee56a6064a34dd05f9ab`; terminal transcript `Pasted text(20260927-220819).txt`, SHA-256 `ea06917d6dc9012425501ad6f96be9fcd5a6c045238677122c0c6251e6789077`.

The native ERC report has **0 errors, 0 warnings** under the configured rules. The four pre-existing ignored categories remain: singleton global labels, four-way junctions, SPICE issues and footprint-filter mismatch. Independently rerunning `tools/check-coupon-controller.py --netlist` against the uploaded XML passed **400 on-board items / 1,507 logical pins**. The PDF has 12 pages.

Visual inspection of page 12 confirms the prior U35 ground-label overlap has been fixed: CTG, GND and exposed-pad leads end in three vertically separated, legible GND boxes. The two `+BAT_GAUGE_SW` labels on VDD/CELL, explicit NC on ALRT, QSTRT ground connection, two separate exact 2.2 kΩ pull-ups and bypass capacitor remain readable. The full XML mapping is documented in the first review and unchanged. Accept the **staged gauge sheet's native rendering and configured electrical checks**.

The `#FLG06` source marker still stands for a missing switch/battery path. No exact switch symbol/footprint or pack/charger connection is placed. The switch sequencing and potentially powered-off SDA/SCL, physical OFF leakage, NTC, source-qualified charging, runtime and SOC recovery remain unverified. The [switch/gauge boundary](../../hardware/coupon/rev-a/switch-gauge-boundary.md) and ADR 0015 govern future work.
