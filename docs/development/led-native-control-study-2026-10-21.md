<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Native-clearance gate and control continuation

Status: **unbuilt, noncanonical routing study**. No board measurement,
electrical/process qualification or fabrication approval.

The [saved derivative](../../hardware/coupon/rev-a/staging/led-native-control-trial-114mm.kicad_pcb)
continues the [row-13 checkpoint](led-row13-bias-study-2026-10-21.md) without
moving any footprint. The initial four joins reduced full native opens 234 → 230.
A supply-preserving clock detour added a fifth join (229 opens). The 2026-10-22
gauge-data continuation added a sixth (228 opens). A joint gauge-clock and
supply-continuity increment added a seventh (227 opens). The subsequent UART
receive/device-transmit joins left 225 opens. The [application-data continuation](led-application-data-study-2026-10-22.md) joins U46.6 to R79.2/U3.10, leaving 224 opens. The [gauge IC data continuation](led-gauge-ic-data-study-2026-10-22.md) completes SDA to U35.8, leaving 223 opens. The [clock/control continuation](led-clock-controls-study-2026-10-22.md) completes gauge SCL, ROW_ARM and USB_CHARGE_REQ, leaving 220 opens. The [reserved ground escape](led-reserved-ground-escape-2026-10-23.md) replaces one ROW_SEL_04 source segment and joins R28.2 to ground, leaving 219 opens. The subsequent R29 extension retains R28 and leaves 218 opens. The R2 driver-control ground escape leaves **217 opens**, seventeen joins in total.

| Net | Opens before | Opens after | Newly joined terminals |
|---|---:|---:|---|
| ROW_GATE_05 | 1 | 0 | R11.2 to PAIR06's gate group |
| SYS_I2C_SDA | 2 | 1 | U46.6 to the existing R79.2/U3.10 group; TP11 remains open |
| SYS_I2C_SCL | 3 | 0 | TP12.1, U46.7 and U3.11 to the existing R80.2 group |
| VLED_WINDOW_OK | 1 | 0 | U55.6 to the existing R104.2 group |
| GAUGE_I2C_SDA | 2 | 0 | U46.3 and U35.8 to the existing R101.2 group |
| GAUGE_I2C_SCL | 2 | 0 | U46.2 and U35.7 to the existing R102.2 group |
| ROW_ARM | 1 | 0 | U55.3 to U54.5 |
| USB_CHARGE_REQ | 1 | 0 | U23.2 to TP30.1/U17.4/U42.1 |
| UART0_RX | 1 | 0 | U3.36 to TP5.1 |
| UART0_TX_RAW | 1 | 0 | U3.37 to R47.1 |
| GND | 27 | 24 | R28.2, R29.2 and R2.2 to the main group through reserved escapes |

Ten of sixteen gate-side pullup terminals now connect. Rows **0, 2, 3, 4, 6
and 7** remain open. R11's VLED terminal is still isolated, the application
clock bus now forms one physical pad group, and the interlock's candidate outputs still do
not join actual display enables. These source connections establish no gate,
I²C or interlock operation; application SDA test-pad routing remains incomplete. GND and VLED are now at 24 and 14 opens.

## Method and retained source

The previous coarse via mask conservatively expands track/pad obstacles. Some
adjacent-layer 0.30/0.10 mm microvia positions fail that approximation while
passing KiCad's exact native shape-distance check at the same 0.20 mm clearance.
Allowing those checked transitions found the row-5 path without relocating R11.
The gate search expanded 152,684 nodes within a 250,000-node bound. A follow-on
control search used exact short native-checked leads to existing copper and a
150,000-node bound per attempt. These searches retain the 0.05 mm grid, 0.20 mm
track width/clearance and six-layer study; no rule or current limit is relaxed.

After each tentative join, zones refill and every existing physical pad group
must survive. Proposed joins from U3.11 on SYS_I2C_SCL and U46.3/U46.2 on the
gauge SDA/SCL nets originally split old groups and were rejected. The clock
detour, gauge-data bridge and joint gauge-clock repair below now resolve
those three rejections. The [search record](../../mechanical/review/native-control-search.json)
retains accepted/rejected attempts and local raw evidence identities. Search
success and native shape screens are preliminary; final acceptance uses full
native DRC and a separately loaded board.

The fifth join resolves the application-clock rejection. Its first candidate
ran a long In4.Cu column and cut U3.2 off its existing +3V3_APP group, even
though clearance checks passed. Moving the three inner clock segments to
In3.Cu, with adjacent-layer transitions at both ends, joins U3.11 while
preserving U3.2's connection to C74.1 and the rest of the old supply group.
This increment adds four 0.20 mm tracks and three 0.30/0.10 mm microvias to
the 230-open checkpoint; it changes no source power track, pad, part or limit.
[Detour and rejected-gauge evidence](../../mechanical/review/native-control-clock-detour.json).

The sixth join adds 23 gauge-data tracks and four adjacent-layer microvias,
joining exact TCA9517ADGKR U46 SDAA pin 3 to R101.2. U35 (MAX17048G+T10)
SDA pin 8 remains disconnected; neither gauge-bus line is complete. The first
SDA route disconnected C38.1 from its old USB-logic group after zone refill.
Three additional 0.20 mm B.Cu tracks retain that group by joining C38.1 at
(57.65, 2.75) mm to C36.1 at (52.65, 2.75) mm through y = 1.75 mm. The checker
at that checkpoint allowed only those three supply tracks, checked the
preserved group and permitted no supply-group merge. This seven-millimetre bridge is source geometry;
its impedance, decoupling locality, current and return paths are unqualified.
No current limit, source supply copper, device, pad or circuit net changes.
[Gauge continuation and rejected combined routes](../../mechanical/review/native-control-gauge-continuation-2026-10-22.json).

Combined gauge-clock/data candidates retained pad groups and reduced opens to
227 but added clearance/shorting findings (108 and 107 full native findings).
Those earlier variants are rejected, remain local, and are not included in
this saved study. The following joint repair resolves their blocking condition.

The seventh join retains 45 gauge-clock tracks and two adjacent-layer
microvias from U46 SCLA pin 2 to R102.2. The first In4 clock path split the
old application-supply group, isolating C1/C2 and C37/R104. A short rear
C1-to-C3 connection and a routed C37-to-main-group repair restore that group;
the latter initially split USB-logic bypass groups in turn. Six rear tracks
then reconnect C23/C24/C25 and the retained C36/C38 bridge to C17's group.
These clock and supply additions form **one accepted transaction**. Partial
repairs are rejected; both power groups must survive the final zone refill.
The increment adds 75 tracks and four adjacent-layer microvias: 45 clock
tracks/two vias, 24 application-supply tracks/two vias and six USB-logic
tracks. No original source copper, pad, placement, part, current setting or
supply-group membership changes. The checker pins exact integer signatures
for both sets of added power copper as well as checking every old pad group.
Its fault cases leave gauge clock joined while withdrawing each supply repair
in turn, and require a physical-group-split rejection. Supply impedance,
decoupling/return locality, current capacity and bus electrical behavior remain
unqualified. At that clock checkpoint U35 SCL pin 7 and SDA pin 8 still needed their respective joins. The later gauge IC data continuation joins SDA pin 8 and the subsequent clock continuation joins SCL pin 7.
[Joint clock/power evidence](../../mechanical/review/native-control-gauge-clock-2026-10-22.json).

The eighth/ninth joins connect UART receive from U3.36 to TP5.1 and device
transmit from U3.37 to R47.1. They add 16 receive tracks/two microvias and
52 transmit tracks/four microvias. The first transmit candidate disconnected
C58/C59 from the old USB-logic group; one 1.5 mm B.Cu supply track from
C59.1 (35.15, 4.25) mm to C11.1 (35.15, 2.75) mm retains that group without
merging a new power group. Its exact signature is pinned with the other power
repairs. The transmit fault regression keeps U3.37/R47.1 joined while moving
that bridge away and requires the old supply-group split to be rejected.
UART0_TX between R47.2 and TP4.1 is still open; 600,000-node follow-up searches
found no accepted route. The series resistor and canonical pin nets are
unchanged. This establishes source connectivity only, not UART/programming,
ROM recovery, signal integrity or target firmware operation.
[UART and rejected-transmit evidence](../../mechanical/review/native-control-uart-continuation-2026-10-22.json).

The cumulative addition comprises **934 tracks and 77 adjacent-layer microvias**, with exactly two original ROW_SEL_04/COL_07_R segments replaced,
bringing the board to **15,503 tracks/vias**. All 483 placements, exact parts,
pad assignments and 14,492 unaffected source tracks/vias survive; the two reviewed ROW_SEL_04/COL_07_R segments are replaced. The selected added
copper is captured in an integer-coordinate [replay plan](../../mechanical/review/native-control-routing-plan.json)
(1,000,000 KiCad internal units/mm). The [generator](../../tools/generate-native-control-trial.py)
pins the source hash, applies the exact two-removal contract and added plan, refills zones and normalizes saved
ordering/UUIDs. It does not depend on exploratory local scripts. KiCad source
remains canonical; this replay does not authorize a package/BOM substitution.

Manufacturer pin recheck on 2026-10-22: TI SCPS245E Rev E (October 2025),
page 4, retains SDAA 3 / SDAB 6 and separate A/B domains; page 23 retains the
DGK 1.4 × 0.45 mm, 0.65 mm-pitch example lands. Analog Devices MAX17048/49
Rev 7 (November 2016), page 6, retains TDFN SDA 8 / SCL 7 and grounded EP.
The selected pin maps, footprints and all component placements are unchanged.
Sources: [TI datasheet](https://www.ti.com/lit/ds/symlink/tca9517a.pdf),
[Analog Devices datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX17048-MAX17049.pdf).
Vendor PDFs are excluded from Git.

## Validation

- Full KiCad 10.0.6 DRC retains the **exact same complete multiset of 104
  intrinsic footprint-clearance findings**, with no additions. This is not
  clean DRC. [Raw report](led-native-control-drc-2026-10-21.json).
- The [saved-board checker](../../tools/check-native-control-trial.py) verifies
  unchanged physical pad geometry, all unaffected source copper, the two exact replacements, every old pad group, all
  seventeen claimed joins, actual via dimensions/layer adjacency and all eighteen
  physical anode pads per row. [Result](../../mechanical/review/native-control-check.json).
- [Per-net native counts](../../mechanical/review/native-control-open-nets.json)
  reconcile all 217 opens. Only the ten listed signal nets and the reviewed GND group change;
  the USB-logic and application supply groups are preserved.
- All 256 exact LED placements/rotations/pad maps/nets pass. Twenty-eight isolated
  native guard cases cover detached gate/I²C copper without item-count changes,
  removed source copper, altered duplicate drain geometry, moved footprints,
  pad-net changes and nonadjacent microvias. The new regression deliberately
  puts the clock column back on In4, proves that the clock remains connected
  but U3.2 loses its supply group, and requires the checker to reject it.
  Gauge-data guards detach signal copper without changing counts, and
  reproduce a connected data line with C38
  disconnected when USB bridge tracks move away. Gauge-clock guards detach
  clock copper or leave it joined while withdrawing application/USB supply
  repairs, proving the rejected power split in each domain. UART cases detach
  receive/device-transmit copper or keep transmit joined while disconnecting
  C58/C59 from their old supply group. These are checker fault tests,
  not powered-board fault response or independent Gate A review. The application-data case detaches its added copper without changing counts and requires rejection.
- Two generations are byte-identical. [Manifest](../../mechanical/review/native-control-trial.json),
  [reproduction](../../mechanical/review/native-control-reproduction.json) and
  [validation record](../../mechanical/review/native-control-validation.json)
  retain exact source/raw-evidence identities.

```sh
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/generate-native-control-trial.py
./tools/check-native-control.sh
```

Saved-board SHA-256 after the reserved ground escape: `a1f742cd395079eb8360483a912c69890bd4f5f2ebbf17201bbd5ddf74f23f98`. The preceding clock/control checkpoint was `b513c152...`; its increment record remains historical. All old physical pad groups survive; source-copper retention now has two explicitly pinned replacements.

Remaining work includes six gate terminals and missing pullup supplies,
ground/power/control/clock/USB completion, timing/dead-time and bus signal
qualification, return/capacitor locality, fine-pitch/HDI/via-in-pad process,
canonical row-package synchronization, RF, battery/enclosure fit and independent
Gate A before fabrication. Firmware, current settings, libraries and canonical
schematic/BOM are unchanged.
