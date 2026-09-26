<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Badge envelope and battery thickness screen

2026-09-26. Calculated feasibility screen for the **final 48 × 16 badge**, not a CAD fit, selected pack, protection design or permission to make a case mold. The physical limits are 110 × 35 × 11 mm including the case. This screen is independent of the unfinished charger actuator and can inform the preliminary PCB placement and eventual CadQuery model.

## Display geometry and usable width

At 1.95 mm pitch, the 48 × 16 centres span 91.65 × 29.25 mm. A 1.55 × 1.50 mm QBLP1515 package extends the envelope to approximately **93.20 × 30.75 mm** (assuming each package is centred on its pixel). That leaves only **16.80 mm total along length** and **4.25 mm total across width** between the package envelope and the maximum case outline. These are differences of outer dimensions, **not PCB-edge or component placement clearance**. With a centred display, width allocation is 2.125 mm per side for wall, optical lip and tolerances. The alternative 1010 LED may shrink its own package envelope, but cannot justify a reduced pixel pitch or a smaller nominal luminous aperture without Gate B selection.

For a *trial* 1.0 mm wall on both long sides and 0.5 mm cell side clearance on each side, the rectangular internal battery-width ceiling is `35 - 2×1.0 - 2×0.5 = 32.0 mm`. This is a provisional geometry budget; structural strength, print error, fasteners, USB/antenna placement and pack swelling may require more clearance. A nominal 34.8 mm-wide Jauch cell cannot fit that illustrative envelope. A 30.5 mm-wide *terminated* pack would leave 1.5 mm spare in this width budget **only if 30.5 mm is its guaranteed maximum including wrap and tabs**. It cannot overlap M2 bosses, magnets or the FPC antenna zone.

## Illustrative section through LED, PCB and cell

The following single-stack assumption deliberately includes a local swelling allowance. The assumptions are **not selected wall/PCB/pack specifications**. Battery protection circuitry, leads and connectors may form a separate local maximum, so a pack thickness alone is insufficient.

| Layer, front to rear | Trial allowance (mm) | Basis or uncertainty |
|---|---:|---|
| Replaceable diffuser | 0.6 | Inside the plan's 0.5–0.8 mm trial range |
| LED-to-diffuser optical gap | 0.5 | Trial value; optics and physical stops unmeasured |
| QBLP1515 above front PCB surface | 1.2 | QT Brightek drawing says 1 mm height with ±0.2 mm general dimension tolerance; confirm drawing stack/assembly height |
| PCB | 0.8 | Trial stack-up, not an assembler commitment |
| Electrical/mechanical isolation behind PCB | 0.3 | Trial film/barrier allowance; validate where solder and vias face cell |
| Cell swelling/installation allowance | 0.5 | Trial reserve; pack vendor must define required clearance |
| Rear shell under cell | 1.0 | Trial printed shell wall |
| **Non-cell subtotal** | **4.9** | Leaves **6.1 mm** of the 11 mm maximum for the **entire pack** in this section |

| Candidate battery envelope | Calculated total using above stack (mm) | Status |
|---|---:|---|
| 5.3 mm protected GlobTek 700 mAh pack thickness | 10.2 | 0.8 mm apparent margin; poor six-hour and peak-current fit for full badge; protection PCB/wires may create thicker local zones |
| 6.0 mm protected GlobTek 800 mAh pack thickness | 10.9 | 0.1 mm apparent margin before board/solder/print/pack tolerances; five-pin integrated-gauge pack and 400 mA charge limit remain unresolved |
| 6.3 mm EEMB 900 mAh **bare cell** page thickness | 11.2 | Exceeds this trial stack by 0.2 mm **before** pack protection, NTC, wrap or connector |

The last two results are **layout risks**, not proof that thinner alternatives fit. Local staggering of tall circuitry and the cell may change the true section, but a cavity touching a pouch or pushing on components is forbidden. A lower LED height applies only if the selected LED and optical design support it; mixed-height coupon results do not authorize a final LED change. Do not shrink swelling clearance merely to force the arithmetic under 11 mm.

## 900 mAh source discrepancy and runtime

The [EEMB LP603048 product page](https://www.eemb.com/product-146) lists a **900 mAh bare cell** measuring 30.5 × 32.0 × 6.3 mm. [EEMB's part-number explanation](https://www.eemb.com/faq-6) decodes `603048` as *nominal* 6 × 30 × 48 mm (thickness × width × length) and explicitly excludes PCM and assembly. Those manufacturer statements conflict on the cell length; the source's 32.0 mm is therefore **unverified** for fit planning. The cited bare-cell page also does not specify a protected NTC-equipped terminated pack or its maximum charge/discharge currents. Obtain the exact manufacturer cell drawing and terminated-pack drawing before freezing a pouch outline. The earlier project plan repeats the page's 32 mm value as a candidate and should not be used as a final fit dimension.

With the project's provisional **0.45 W reference load**, 3.7 V nominal and 85% usable-energy assumption, a nominal 900 mAh cell gives `(0.900 Ah × 3.7 V × 0.85) / 0.45 W ≈ 6.29 h`. This is a **calculated model**, only about 0.29 h beyond the rough six-hour goal, before cell aging or measured variation. A drawing that resolves the cell size would still leave charge rating, peak discharge, NTC curve, connector polarity and heat to qualify.

## Next independent work

1. Make a parametric preliminary PCB footprint/antenna/USB outline and import the exact selected *terminated-pack* STEP or maximum drawing, with protection and lead exit included. The PCB STEP is not available yet.
2. Print a section gauge with the trial 5.3/6.0/6.3 mm cavity blocks and 0.5 mm nominal swelling allowance; use inert mockups, **not a compressed LiPo**, for this fit experiment.
3. Revise the trial wall, diffuser, gap, board and battery allowances from real parts and process limits. Then check magnet/screw separation, connector insertion, strain relief, antenna clearance and mass.

See the [pack rating screen](../docs/sourcing/pack-screen-2026-09-25.md) for electrical exclusions. No full badge or case model is claimed to fit yet.

## Source evidence

- [QT Brightek QBLP1515A-RGB2A datasheet, version 1.0](https://www.qt-brightek.com/datasheet/QBLP1515A-RGB2A.pdf), pages 3 and 4: package width/height and general dimension tolerance.
- [EEMB LP603048 bare-cell listing](https://www.eemb.com/product-146) and [EEMB part-number explanation](https://www.eemb.com/faq-6), checked 2026-09-26: contradictory 32 mm listing versus nominal 48 mm model code.
- [Protected-pack screening](../docs/sourcing/pack-screen-2026-09-25.md): exact GlobTek pack drawings and candidate electrical ratings.
