<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Manufacturer inquiry: protected thin 1S 900 mAh pack

Status: **request specification; do not order**. This is a requirements sheet for LiPol or another identified pack manufacturer, not a qualified battery or confirmed supplier offer. Based on [ADR 0016](../decisions/0016-runtime-and-fit-over-charge-speed.md) and the [pack shortlist](pack-shortlist-2026-09-27.md). The published `LP452845` two-wire pack is only a starting point; a three-wire version requires its own exact order code and revision-controlled drawing. A 700 mAh coupon battery may be procured separately once its documented charger configuration is reviewed.

## Product envelope and use

| Item | Request to manufacturer | Reason |
|---|---|---|
| Capacity and chemistry | Nominal ~900 mAh 1S Li-ion polymer; supply minimum guaranteed delivered capacity, test rate/temperature and cycle-life criteria | Six hours needs ~859 mAh nominal under the **provisional** 0.45 W / 85% usable model; 900 mAh gives only ~6.29 h mathematically |
| Installed geometry | Maximum dimensions **including cell, protection board, wrap, tabs and lead exit**, with tolerances and local peaks; trial ceiling 32.0 mm width, 6.1 mm thickness, length to be confirmed against placement | Trial case is 110 × 35 × 11 mm externally; a bare-cell 4.5 mm measurement does not qualify the pack; keep attachment and swelling clearance |
| Weight | Maximum assembled weight including leads/connector, aiming under 21 g battery allocation; provide real worst-case value | Finished badge must remain under 100 g |
| Discharge | State *continuous* discharge rating at low cell voltage and operating temperature, plus duration/conditions for any peak rating; provide protection trip values | Provisional full-white demand ~0.83 A at 3.0 V before transients; published 900 mA `LP452845` maximum lacks explicit continuous qualification |
| Charge | State maximum continuous CC current, CV voltage/tolerance, precharge profile and temperature derating; supply charge-time curve or test conditions if available | Published `LP452845` lists max 450 mA; 80% at that rate has an ideal **96 min minimum** before taper or system load. A slower safe charge is acceptable |
| Temperature sense | Integral **10 kΩ NTC**, its B value/tolerance, location, wiring and allowable charge-temperature window; confirm compatibility data for external charger TS threshold design | Hardware charge permission must work without firmware and with the actual cell temperature |
| Protection and OFF drain | Supply PCM overcharge/overdischarge/short-circuit/overcurrent thresholds, reset conditions and maximum protection quiescent current across voltage/temperature | Whole badge OFF goal <50 µA including protection and charger/switch leakage |
| Connector | Three-wire connector housing and mating header exact MPNs; cavity numbering, connector viewing orientation, BAT+/BAT−/NTC mapping, polarity and wire gauge/length | Avoid mating reversal or selecting a PCB footprint from a two-wire listing |
| Traceability | Exact *finished assembly* ordering code and dated, revision-controlled drawing, UN 38.3 test summary and available IEC/UL assembly evidence, lot marking and transport documentation | Gate A and PCBA source control |
| Purchasing | Sample and production MOQ, unit pricing at 5/25/100, quoted lead time, shipping into the US, reorder route and any tooling/NRE | Development quantity and follow-on reproducibility |

Ask explicitly whether a three-wire protected 900 mAh `LP452845` derivative is possible **within the entire finished-pack** width/thickness caps, and whether any alternate off-the-shelf exact assembly already meets these conditions. Request drawings before samples. If impossible, ask what dimension or current criterion is limiting; then reopen the case or runtime trade-off with the owner. Do not infer a new NTC variant's availability or ratings from the published two-wire listing.

## Design response when documents arrive

1. Cross-check manufacturer identifier, drawing revision, dimensions at PCM/lead exit and pack weight against the current mechanical section and full weight rollup; update trial CAD before freezing battery location.
2. Recompute six-hour reference runtime and full-white low-voltage current using documented minimum capacity and discharge limits, then use coupon measurements for final claims.
3. Choose a documented exact ISET resistor with a worst-case programmed maximum **below the pack's derated charge rating**. Verify charger TS network, safety timer, USB port budget and worst-case thermal dissipation; publish provisional pack-specific 80%/full timing before Gate A.
4. Confirm connector mating polarity from both manufacturer's pin view and the PCB footprint. Capture the exact pack and header in KiCad, run native ERC/netlist/DRC, then obtain independent Gate A review before any assembled-board/battery order.
