<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Preliminary component-space screen

The [rear packing trial](review/component-space.svg) and [machine-readable inventory](review/component-space.json) answer whether the current 106 × 32.5 mm **final-badge trial board** has obvious room for the parts already captured in the **16 × 16 coupon** schematic. Regenerate them from the current native KiCad netlist and project-local footprint courtyards with:

```sh
python3 tools/screen-final-component-space.py --output mechanical/review
```

This is a two-dimensional screen, not a KiCad PCB, routed design, DRC, complete final-badge netlist or pack fit. It replaces the coupon's 256 mixed LEDs with a trial 768 front QBLP1515 array and its one TLC59581 body with three on the rear; the final LED remains a Gate B choice. It carries the other 151 captured footprint instances over as a **provisional trial inventory**; some coupon test pads may be omitted on a final board, while extra support parts for the two added drivers are absent. The 20 test pads have 1.0 mm physical pads but no courtyard, so the trial assigns each a 1.5 × 1.5 mm reservation. The initial screen puts all small captured components on the rear **outside** the centred `LP503055` finished-body outline. This is deliberately restrictive: the pack is a separate wired assembly held by the enclosure, and insulated PCB components may be possible beneath it. The board-facing battery NTC is still an XY target, not an exact footprint.

| Area accounting | mm² |
|---|---:|
| Trial board | 3445.00 |
| `LP503055` finished body (56 × 30.5 mm) | 1708.00 |
| MCU, three driver courtyards and on-board portion of USB courtyard | 736.71 |
| Area outside those large reservations | **1000.29** |
| Other captured courtyards plus trial test-pad reservations | **901.60** |
| Nominal remainder before any part-to-part clearance, routing or missing parts | **98.69** |

The largest remaining groups are 16 row P-MOSFETs (207.2 mm²), 16 row N-MOSFETs (190.4 mm²), 62 resistors (124.0 mm²), and the row decoder (63.9 mm²). A deterministic first-fit trial on a 0.25 mm grid, with just 0.25 mm around each small reservation, puts **55 of 151** outside the pack outline and leaves **96** unplaced. This failure reflects the restrictive placement rule and the simple packing algorithm; it does **not** prove that the board lacks room.

## Correction: conditional under-pack placement

The owner correctly pointed out that the battery is not soldered to the PCB. A second, deliberately optimistic XY screen treats the 62 captured 0402 resistors and 15 captured 0402 capacitors as *candidates* for placement beneath a supported, insulated pack. Their 77 courtyards total **154.0 mm²**. Moving those reservations into the battery-facing region raises the nominal outside-area remainder from 98.69 to **252.69 mm²**; the first-fit pass then leaves **22 of 74** outside components unplaced. That is an improved screening result, not a final component assignment: decouplers and row-gate parts may need to remain beside the devices they serve, and the pack centre is reserved for the provisional NTC target.

The 11 mm section stack currently has only **0.8 mm nominal headroom** above the `LP503055` maximum body thickness. Component assembled height, solder, insulating cover, pouch support, swelling, tolerance and temperature coupling must all be checked before any footprint is actually placed under the pack. The case thickness may ultimately need to increase, but the first outside-only area screen did not establish that. Equally, it does not establish that reducing resolution or component count is necessary.

The absent circuit is substantial: input protection, charger, battery connector and strain relief, VLED converter, temperature-sensor footprint and network, final gauge isolation, display interlock, two additional LED-driver support networks, antenna/cable zone, mounting features and all copper/routing. In the outside-only baseline, omitting all 20 coupon test-pad reservations would increase the nominal remainder to **143.69 mm²**. The `LP503055` drawing omits wire exit, connector and possible protection-board protrusion beyond its body. The [trial section stack](envelope-screen-2026-09-26.md) totals 4.9 mm outside the cell; with this pack's 5.3 mm maximum body thickness it reaches 10.2 mm within an 11 mm case. The rightward driver move removes one body/courtyard overlap but does not settle the rest of the placement.

**Disposition:** The existing screens do not establish either a fit or a no-fit result. Keep the 106 × 32.5 × 11 mm target for a more realistic trial: model the supported battery above the board, place low-profile candidate parts beneath it only with a verified height/insulation stack, keep warm/tall parts and required local decouplers in appropriate zones, then place the complete netlist in KiCad and run DRC. Do not relax the product requirements based solely on the original outside-only packing result. Independent Gate A review and the exact protected pack remain required before fabrication.
