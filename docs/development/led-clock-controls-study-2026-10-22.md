<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Gauge clock and existing control-net continuation

Status: **unbuilt noncanonical geometry study; fabrication prohibited**.

The [saved derivative](../../hardware/coupon/rev-a/staging/led-native-control-trial-114mm.kicad_pcb)
adds three existing-net joins after the gauge SDA checkpoint:

| Net | Newly completed physical pad group | Opens before → after |
|---|---|---:|
| GAUGE_I2C_SCL | R102.2 / MAX17048 U35.7 / TCA9517A U46.2 | 1 → 0 |
| ROW_ARM | SN74LVC2G08 U55.3 / SN74LVC2G00 U54.5 | 1 → 0 |
| USB_CHARGE_REQ | TP30.1 / SN74LVC1G11 U17.4 / SN74LVC1G06 U23.2 / SN74AUP1G125 U42.1 | 1 → 0 |

Native and physical-pad open counts decrease **223 → 220**. Both gauge bus
nets now form single pad groups. This establishes source connectivity, with no
physical bus, interlock or charging operation qualified. Actual VLED and decoder
enables retain their isolated/default-disabled source boundaries. The fixed
hardware USB current limit is unchanged and has no firmware permission path.

## Search and joint acceptance

Reversed empty-grid gauge clock search first reaches the 800,000-node bound;
a 2,400,000-node attempt finds a route after **922,941 expansions**. Full DRC
finds one additional dangling-track warning: a redundant newly generated
0.4959 mm lead on In4 at (39.65, 2.35) mm. Removing only that lead preserves
all old pad groups, the completed clock group and 222 opens; full DRC then
matches exactly the baseline 104 findings.

A separate reverse control search on the original 223-open source joins ROW_ARM
in 308,275 expansions and USB_CHARGE_REQ in 300,719. Other bounded attempts
remain local/rejected. Combining those independent routes with the clock yields
**180 findings**, so that combination is rejected. Rerouting the controls against
the pruned clock candidate joins ROW_ARM in **357,512 expansions** and
USB_CHARGE_REQ in **300,719**. This joint candidate preserves every old physical
pad group and retains exactly **104 intrinsic findings**. Native shape/group
screens do not replace the full DRC comparison.

The selected increment adds **449 tracks and 16 adjacent-layer microvias** with
0.20 mm track width/clearance and 0.30/0.10 mm adjacent-layer vias. It adds no
supply copper; pinned application/USB supply-repair signatures are unchanged.
The cumulative integer replay plan adds **920 tracks / 64 microvias**, giving
**15,478 total items and fourteen claimed joins** over the row-13 source.
All 483 placements, prior tracks/vias, physical pad groups and exact shared
component metadata survive. Two sequential generations are byte-identical.

## Source review and validation

The existing ADR 0030 gauge boundary, ADRs 0031/0032 isolated display interlock
and ADR 0013 fixed-current Type-C policy apply without circuit changes. No part,
symbol, footprint, pad assignment, current limit, firmware or canonical
schematic/BOM is changed. Manufacturer pin tables rechecked on 2026-10-22 confirm
U55 pin 3 is 2Y, U54 pin 5 is 2A, U17 pin 4 is Y, U23 pin 2 is A and U42 pin 1
is active-low OE. Package geometry remains unchanged and covered by the existing
library audits and complete physical-pad/source comparison:
[dual AND, SCES198N](https://www.ti.com/lit/ds/symlink/sn74lvc2g08.pdf),
[dual NAND, SCES193N](https://www.ti.com/lit/ds/symlink/sn74lvc2g00.pdf),
[AND3, SCES487I](https://www.ti.com/lit/ds/symlink/sn74lvc1g11.pdf),
[inverter, SCES295AB](https://www.ti.com/lit/ds/symlink/sn74lvc1g06.pdf),
[buffer, SCES595N](https://www.ti.com/lit/ds/symlink/sn74aup1g125.pdf).

Full KiCad 10.0.6 DRC retains the exact normalized multiset of **104 intrinsic
findings**, native/physical-pad counts agree at **220**, and all **256 LED
checks**, **21 isolated native guards** and **21 circuit/metadata fault tests**
pass. A fresh complete native canonical XML comparison and source-only CI layout
(21 circuit, fourteen distance, six path/CLI methods) pass. New fault cases detach
ROW_ARM and USB_CHARGE_REQ copper without changing item counts and require
rejection; the existing clock-detach and supply-cut cases remain effective.
No hardware was measured and independent Gate A remains open.

GND/VLED/application 3.3 V/USB logic remain at **27/14/7/4 opens**. TP11,
R47.2/TP4.1, six gate terminals and remaining power/control/USB routes are
incomplete. Bus/return/decoupling, current capacity, sequencing and faults,
intrinsic footprint findings, HDI/mask/paste process, mechanical fit, canonical
row-package adoption and independent review remain unqualified/open.

[Increment evidence](../../mechanical/review/native-control-clock-controls-2026-10-22.json),
[current validation](../../mechanical/review/native-control-validation.json),
[native checker](../../mechanical/review/native-control-check.json),
[per-net opens](../../mechanical/review/native-control-open-nets.json),
[full DRC](led-native-control-drc-2026-10-21.json),
[reproduction](../../mechanical/review/native-control-reproduction.json).

Repeat with `./tools/check-native-control.sh` and
`./tools/check-coupon-study-contract.sh`.
Board SHA-256: `b513c1522e56bbf791cb6e069ab2d6ef081802605327b7f4d50750fffddb98e1`.
