<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Native-clearance gate and control continuation

Status: **unbuilt, noncanonical routing study**. No board measurement,
electrical/process qualification or fabrication approval.

The [saved derivative](../../hardware/coupon/rev-a/staging/led-native-control-trial-114mm.kicad_pcb)
continues the [row-13 checkpoint](led-row13-bias-study-2026-10-21.md) without
moving any footprint. Four joins reduce full native opens **234 → 230**.

| Net | Opens before | Opens after | Newly joined terminals |
|---|---:|---:|---|
| ROW_GATE_05 | 1 | 0 | R11.2 to PAIR06's gate group |
| SYS_I2C_SCL | 3 | 1 | TP12.1 and U46.7 to the existing R80.2 group |
| VLED_WINDOW_OK | 1 | 0 | U55.6 to the existing R104.2 group |

Ten of sixteen gate-side pullup terminals now connect. Rows **0, 2, 3, 4, 6
and 7** remain open. R11's VLED terminal is still isolated, the application
clock bus still has one open, and the interlock's candidate outputs still do
not join actual display enables. These source connections establish no gate,
I²C or interlock operation. GND and VLED remain at 27 and 14 opens.

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
gauge SDA/SCL nets split old groups and are rejected. The [search record](../../mechanical/review/native-control-search.json)
retains accepted/rejected attempts and local raw evidence identities. Search
success and native shape screens are preliminary; final acceptance uses full
native DRC and a separately loaded board.

The final addition comprises **104 tracks and 17 adjacent-layer microvias**,
bringing the board to **14,615 tracks/vias**. All 483 placements, exact parts,
pad assignments and 14,494 source tracks/vias survive. The selected added
copper is captured in an integer-coordinate [replay plan](../../mechanical/review/native-control-routing-plan.json)
(1,000,000 KiCad internal units/mm). The [generator](../../tools/generate-native-control-trial.py)
pins the source hash, adds only that plan, refills zones and normalizes saved
ordering/UUIDs. It does not depend on exploratory local scripts. KiCad source
remains canonical; this replay does not authorize a package/BOM substitution.

## Validation

- Full KiCad 10.0.6 DRC retains the **exact same complete multiset of 104
  intrinsic footprint-clearance findings**, with no additions. This is not
  clean DRC. [Raw report](led-native-control-drc-2026-10-21.json).
- The [saved-board checker](../../tools/check-native-control-trial.py) verifies
  unchanged physical pad geometry, source copper, every old pad group, all
  four claimed joins, actual via dimensions/layer adjacency and all eighteen
  physical anode pads per row. [Result](../../mechanical/review/native-control-check.json).
- [Per-net native counts](../../mechanical/review/native-control-open-nets.json)
  reconcile all 230 opens. Only the three listed nets' pad groups change.
- All 256 exact LED placements/rotations/pad maps/nets pass. Eight isolated
  native guard cases cover detached gate/I²C copper without item-count changes,
  removed source copper, altered duplicate drain geometry, moved footprints,
  pad-net changes and nonadjacent microvias. These are checker fault tests,
  not powered-board fault response or independent Gate A review.
- Two generations are byte-identical. [Manifest](../../mechanical/review/native-control-trial.json),
  [reproduction](../../mechanical/review/native-control-reproduction.json) and
  [validation record](../../mechanical/review/native-control-validation.json)
  retain exact source/raw-evidence identities.

```sh
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/generate-native-control-trial.py
./tools/check-native-control.sh
```

Saved-board SHA-256: `7d439c8072e4c2943ce5960db80c21d706c713059a8e51c8e290e3bf831ff1ec`.

Remaining work includes six gate terminals and missing pullup supplies,
ground/power/control/clock/USB completion, timing/dead-time and bus signal
qualification, return/capacitor locality, fine-pitch/HDI/via-in-pad process,
canonical row-package synchronization, RF, battery/enclosure fit and independent
Gate A before fabrication. Firmware, current settings, libraries and canonical
schematic/BOM are unchanged.
