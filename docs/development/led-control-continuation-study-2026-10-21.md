<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Guarded control-routing continuation, 2026-10-21

Status: native source geometry/connectivity evidence on an unbuilt, noncanonical mixed-source study. No powered-board measurement or fabrication approval.

The [control continuation board](../../hardware/coupon/rev-a/staging/led-control-continuation-trial-114mm.kicad_pcb) follows the checked [physical drain-tie checkpoint](led-row-drain-tie-study-2026-10-20.md). Ten new joins reduce full native open edges from **246 to 236**, without moving any footprint, changing a pad assignment, removing source copper or splitting an existing physical pad group. The 483 footprints and all eighteen connected physical anode pads per row remain present.

| Control net | Before opens | After opens |
|---|---:|---:|
| CHARGER_GATE_EN | 6 | 3 |
| ROW_A2 | 2 | 1 |
| ROW_A3 | 2 | 1 |
| SYS_I2C_SDA | 3 | 2 |
| USB_CC_HIGH | 1 | 0 |
| USB_CHARGE_REQ | 2 | 1 |
| USB_LOGIC_SENSE | 2 | 0 |

These are connected pad-cluster counts from KiCad, not signal-integrity, sequencing or fault-response tests. All other nets' physical pad groups remain exactly as in the source. GND still has 27 opens; VLED, +3V3_APP and +3V3_USB retain 15, 7 and 4 respectively. Eight gate pullups remain unjoined. The isolated display-interlock outputs remain isolated from the actual converter/decoder enable nets.

## Routing method and rejected candidates

`generate-local-control-trial.py --continuation` uses the physical-drain source and supplements pad-centre targets with the exact endpoints of tracks/vias in the native connected group. A connector between each grid point and its exact native endpoint ensures physical contact. Filled-zone anchors are excluded because an arbitrary outline point does not establish membership in the connected copper region.

Search retains the 0.05 mm grid, 0.20 mm trace width/clearance, adjacent-layer 0.30/0.10 mm microvias and 200,000-expanded-node budget. It adds 288 tracks/vias, bringing the saved total to 14,483. These dimensions do not qualify the stack-up, microvia process or current capacity. A failed bounded search does not establish that routing is impossible.

An initial candidate retained the 104 clearance findings but lost three ground connections when zones refilled. It was rejected. The generator now snapshots physical pad groups before each proposed join, refills zones, and accepts the join only if every prior group survives and the intended source/anchor actually joins. Otherwise it removes the tentative copper, restores the routing occupancy and refills again. This rejects the attempted U46.3 GAUGE_I2C_SDA and U46.2 GAUGE_I2C_SCL routes; the [manifest](../../mechanical/review/control-continuation-trial.json) records both rejections. Clearance equivalence alone is insufficient acceptance evidence.

## Validation and reproducibility

- KiCad 10.0.6 full native DRC: exactly the same complete multiset of 104 intrinsic footprint-clearance findings as the physical-drain source, with no additions. This is **not clean DRC**. [Raw report](led-control-continuation-drc-2026-10-21.json).
- The [independent saved-board check](../../mechanical/review/control-continuation-check.json) verifies all source tracks/vias, footprints/pad signatures, physical cluster preservation, all ten claimed joins, actual microvia dimensions/layer adjacency and eighteen connected anode pads per row.
- [Per-net native connectivity](../../mechanical/review/control-continuation-open-nets.json) reconciles the full 236-edge native count to physical pad clusters.
- Exact 256-LED placement/net check passes. Repeated generation must be byte-identical; the retained [reproduction record](../../mechanical/review/control-continuation-reproduction.json) records both hashes. The generator's default mode also reproduces the preceding 354-open board byte-for-byte.

Run with KiCad's bundled Python from the repository root:

```sh
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/generate-local-control-trial.py --continuation
./tools/check-control-continuation.sh
```

Saved board SHA-256: `f945becb2b685e14bc08a3402e07bf1c2fc56af6b940e12b3470f6fad3e16851`.

Remaining work includes coordinated placement/escape changes for the blocked ground, power and gate-bias terminals; completion and electrical review of control/clock/USB paths; converter capacitor/return locality; exact source/package synchronization; RF, case and HDI/process qualification. No current limit, MPN or canonical circuit changes here. Independent Gate A precedes fabrication.

A follow-on exploratory ground-only pass used this board, the same endpoint search/cluster guard and a 100,000-expanded-node budget. It attempted 31 outstanding pad-to-anchor connections and accepted none; the saved probe still had 236 opens. Probe files remain local under `hardware/coupon/rev-a/build/control-ground-probe.*`. This bounded result supports changing the placement/escape strategy next, and does not prove ground routing impossible.
