<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Native-clearance gate and control continuation

Status: **unbuilt, noncanonical routing study**. No board measurement,
electrical/process qualification or fabrication approval.

The [saved derivative](../../hardware/coupon/rev-a/staging/led-native-control-trial-114mm.kicad_pcb)
continues the [row-13 checkpoint](led-row13-bias-study-2026-10-21.md) without
moving any footprint. The initial four joins reduced full native opens 234 → 230.
A supply-preserving clock detour added a fifth join (229 opens). The 2026-10-22
gauge-data continuation adds a sixth, leaving **228 opens**.

| Net | Opens before | Opens after | Newly joined terminals |
|---|---:|---:|---|
| ROW_GATE_05 | 1 | 0 | R11.2 to PAIR06's gate group |
| SYS_I2C_SCL | 3 | 0 | TP12.1, U46.7 and U3.11 to the existing R80.2 group |
| VLED_WINDOW_OK | 1 | 0 | U55.6 to the existing R104.2 group |
| GAUGE_I2C_SDA | 2 | 1 | U46.3 to the existing R101.2 group |

Ten of sixteen gate-side pullup terminals now connect. Rows **0, 2, 3, 4, 6
and 7** remain open. R11's VLED terminal is still isolated, the application
clock bus now forms one physical pad group, and the interlock's candidate outputs still do
not join actual display enables. These source connections establish no gate,
I²C or interlock operation; SDA and gauge routing remain incomplete. GND and VLED remain at 27 and 14 opens.

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
detour and the gauge-data bridge below resolve two of those rejections; gauge
clock remains rejected. The [search record](../../mechanical/review/native-control-search.json)
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
allows only those exact three supply tracks, checks the preserved group, and
permits no supply-group merge. This seven-millimetre bridge is source geometry;
its impedance, decoupling locality, current and return paths are unqualified.
No current limit, source supply copper, device, pad or circuit net changes.
[Gauge continuation and rejected combined routes](../../mechanical/review/native-control-gauge-continuation-2026-10-22.json).

Combined gauge-clock/data candidates retained pad groups and reduced opens to
227 but added clearance/shorting findings (108 and 107 full native findings).
They are rejected, remain local, and are not included in this saved study.

The cumulative addition comprises **134 tracks and 24 adjacent-layer microvias**,
bringing the board to **14,652 tracks/vias**. All 483 placements, exact parts,
pad assignments and 14,494 source tracks/vias survive. The selected added
copper is captured in an integer-coordinate [replay plan](../../mechanical/review/native-control-routing-plan.json)
(1,000,000 KiCad internal units/mm). The [generator](../../tools/generate-native-control-trial.py)
pins the source hash, adds only that plan, refills zones and normalizes saved
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
  unchanged physical pad geometry, source copper, every old pad group, all
  six claimed joins, actual via dimensions/layer adjacency and all eighteen
  physical anode pads per row. [Result](../../mechanical/review/native-control-check.json).
- [Per-net native counts](../../mechanical/review/native-control-open-nets.json)
  reconcile all 228 opens. Only the four listed signal nets' pad groups change;
  the USB-logic and application supply groups are preserved.
- All 256 exact LED placements/rotations/pad maps/nets pass. Eleven isolated
  native guard cases cover detached gate/I²C copper without item-count changes,
  removed source copper, altered duplicate drain geometry, moved footprints,
  pad-net changes and nonadjacent microvias. The new regression deliberately
  puts the clock column back on In4, proves that the clock remains connected
  but U3.2 loses its supply group, and requires the checker to reject it.
  Gauge-data guards detach signal copper without changing counts, and
  reproduce a connected data line with C38
  disconnected when the three bridge tracks move away. These are checker fault tests,
  not powered-board fault response or independent Gate A review.
- Two generations are byte-identical. [Manifest](../../mechanical/review/native-control-trial.json),
  [reproduction](../../mechanical/review/native-control-reproduction.json) and
  [validation record](../../mechanical/review/native-control-validation.json)
  retain exact source/raw-evidence identities.

```sh
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/generate-native-control-trial.py
./tools/check-native-control.sh
```

Saved-board SHA-256: `8789452903b0f34641bdd9889cffa5dd9031f370f399ff537d2eb88bc95d4d86`.

Remaining work includes six gate terminals and missing pullup supplies,
ground/power/control/clock/USB completion, timing/dead-time and bus signal
qualification, return/capacitor locality, fine-pitch/HDI/via-in-pad process,
canonical row-package synchronization, RF, battery/enclosure fit and independent
Gate A before fabrication. Firmware, current settings, libraries and canonical
schematic/BOM are unchanged.
