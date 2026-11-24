<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Row-14 local pullup and VLED bias connection

Status: **unbuilt geometry study with full native DRC evidence**. The [saved board](../../hardware/coupon/rev-a/staging/led-row14-bias-trial-114mm.kicad_pcb) moves only `R20`, the existing exact 1 kΩ row-14 pullup, next to `PAIR15` and joins both local terminals. Full native opens fall from **366 to 364**, while GND remains at **27**. Gate pullups now connected are rows **1, 8, 9, 10, 11, 12, 14 and 15**: eight of sixteen. VLED is still globally incomplete.

The [generator](../../tools/generate-row14-bias-trial.py) starts from the [ground-return derivative](led-ground-return-study-2026-10-20.md). Both R20 pads are isolated in that source. It relocates R20 from (64.75, 5.75) mm / 180° to (73.5, 30.0) mm / 90°, preserves all source tracks/vias and other footprints, and adds two rear-side 0.20 mm tracks: R20.2 to PAIR15.5 (`ROW_GATE_14`) and R20.1 to PAIR15.4 (`VLED`). The ground zones are refilled around the moved pads and new routes; their existing connected pad clusters remain intact. The resistor value, library lands, candidate pair pin map, current settings and canonical schematic/BOM are unchanged.

Evidence:

- [Generation manifest](../../mechanical/review/row14-bias-trial.json) and [saved-board result](../../mechanical/review/row14-bias-check.json): 482 unchanged footprints, independently transformed R20 pad geometry, all source tracks/vias retained, exactly the two intended cluster merges, and unchanged remaining pad clusters including all ground returns.
- [Native DRC JSON](led-row14-bias-drc-2026-10-20.json): KiCad 10.0.6, exactly the same 104 intrinsic footprint-clearance findings as the source; no added courtyard, edge, short or clearance finding. These existing findings remain unresolved and preclude a clean fabrication DRC claim.
- [Native per-net report](../../mechanical/review/row14-bias-open-nets.json): 364 full native and pad-cluster opens, GND 27, VLED 40, and no remaining `ROW_GATE_14` open.
- All 256 exact LED placements/rotations/pad maps/nets pass. Second generation is byte-identical: `5d4b9c9a67b9b78d221ac25f7be84ed8469d053a25aef0935e6895cfbe587a2a`.

A temporary placement/path search found this direct local route, while straight/orthogonal B.Cu paths for the other eight blocked gate resistors did not succeed even with candidate centres up to ±12 mm from their row pair. This bounded probe does not prove those rows impossible; coordinate placement with inner-layer escapes and the existing selects. Its unsaved candidate sites are not adopted.

Repeat generation with KiCad's bundled Python and `tools/generate-row14-bias-trial.py`; run native DRC and `tools/check-row14-bias-trial.py --drc PATH --report PATH`, followed by `tools/check-coupon-led-placement.py` on the saved board. Desktop access may be required for native DRC on macOS. The full normalized finding set must equal the recorded source baseline.

All sixteen anode rows, 48 complete colour channels, gate ties, decoder selects and select-pulldown signal pads survive. Eight gate pullups, 27 ground edges, global supplies and other controls still need routing. Row-package adoption, fine-pitch process/mask/paste, stacked microvias, current/return/thermal/RF review, battery/enclosure fit, interlock qualification and independent Gate A remain open. No board or firmware has been tested and no fabrication file is released.
