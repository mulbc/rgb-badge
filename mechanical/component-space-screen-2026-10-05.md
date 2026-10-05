<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Preliminary component-space screen

The [rear packing trial](review/component-space.svg) and [machine-readable inventory](review/component-space.json) answer whether the current 106 × 32.5 mm **final-badge trial board** has obvious room for the parts already captured in the **16 × 16 coupon** schematic. Regenerate them from the current native KiCad netlist and project-local footprint courtyards with:

```sh
python3 tools/screen-final-component-space.py --output mechanical/review
```

This is a two-dimensional screen, not a KiCad PCB, routed design, DRC, complete final-badge netlist or pack fit. It replaces the coupon's 256 mixed LEDs with a trial 768 front QBLP1515 array and its one TLC59581 body with three on the rear; the final LED remains a Gate B choice. It carries the other 151 captured footprint instances over as a **provisional trial inventory**; some coupon test pads may be omitted on a final board, while extra support parts for the two added drivers are absent. The 20 test pads have 1.0 mm physical pads but no courtyard, so the trial assigns each a 1.5 × 1.5 mm reservation. All small captured components are tried on the rear, outside the centred `LP503055` maximum finished-body rectangle. The board-facing battery NTC is still an XY target, not an exact footprint.

| Area accounting | mm² |
|---|---:|
| Trial board | 3445.00 |
| `LP503055` finished body (56 × 30.5 mm) | 1708.00 |
| MCU, three driver courtyards and on-board portion of USB courtyard | 736.71 |
| Area outside those large reservations | **1000.29** |
| Other captured courtyards plus trial test-pad reservations | **901.60** |
| Nominal remainder before any part-to-part clearance, routing or missing parts | **98.69** |

The largest remaining groups are 16 row P-MOSFETs (207.2 mm²), 16 row N-MOSFETs (190.4 mm²), 62 resistors (124.0 mm²), and the row decoder (63.9 mm²). A deterministic first-fit trial on a 0.25 mm grid, with just 0.25 mm around each small reservation, puts **55 of 151** on the rear and leaves **96** unplaced. First-fit failure does not prove that an expert manual layout is impossible, and the area sum does not model routing channels. Together they show that the current arrangement cannot be called spatially feasible.

The absent circuit is substantial: input protection, charger, battery connector and strain relief, VLED converter, temperature-sensor footprint and network, final gauge isolation, display interlock, two additional LED-driver support networks, antenna/cable zone, mounting features and all copper/routing. Even omitting all 20 coupon test-pad reservations would increase the nominal remainder only to **143.69 mm²**. The `LP503055` drawing omits wire exit, connector and possible protection-board protrusion beyond its body. The [trial section stack](envelope-screen-2026-09-26.md) totals 4.9 mm outside the cell; with this pack's 5.3 mm maximum body thickness it reaches 10.2 mm within an 11 mm case. Placing components under the cell would require an insulating mechanical barrier, explicit standoff and a new height-stack check; the trial does not silently allow that space. The rightward driver move removes one body/courtyard overlap but does not make room for these items.

**Disposition:** Do not advance this 106 × 32.5 mm arrangement as a complete final-board placement. The next layout decision is to make room for the row-switch bank and power circuitry in a revised mechanical stack or electrical architecture, then run a genuine KiCad PCB placement and DRC with the complete netlist. Slightly moving the three drivers farther right cannot close the missing-area and routing problem. The independent Gate A review and the exact protected pack remain required before fabrication.
