<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# First native staged-gauge review: 20fdf48

Owner-generated KiCad 10.0.6 evidence uploaded 2026-09-27 for `coupon-power-rev-a` at `20fdf48f58cd6cfc943217cdc7e763b65bdbeb4c`. This is first-author review of the staged gauge, not independent Gate A or a fabrication release.

## Evidence

The attached `gauge-review-20fdf48.zip` has SHA-256 `635e1bcabe6998dec9c243eadb40fcf20a73e40356eb8c06b19be9092d6d8102`. The terminal transcript `Pasted text(20260927-185507).txt` has SHA-256 `7f7f46c535d123b16514f2cc06cf1c2a3aebff125e9a441b22a6c7edf9462771`. The zip contains the native KiCad schematic PDF, ERC report, full XML netlist and library SVGs; the transcript identifies the source commit and its successful run.

The ERC report has **zero errors and zero warnings** under the configured rules. The project ignores singleton global labels, four-way junctions, SPICE issues and footprint-filter mismatch, as before. Independently running `python3 tools/check-coupon-controller.py --netlist` against the supplied XML passed **400 PCB items and 1,507 logical pins**. The PDF has 12 pages.

The actual XML maps U35 VDD/CELL (pins 3/2) and C39.1 to the **assumed** `+BAT_GAUGE_SW` source, U35.1/.4/.6/.9 and C39.2 to GND, U35.8/R79.2 to SDA, U35.7/R80.2 to SCL, and both R79.1/R80.1 to `+3V3_APP`. U35.5 ALRT has the expected one-pin unconnected net. The XML cannot prove a physical switch is present; `#FLG06` is only a draft source assertion.

## Visual inspection and correction

PDF page 12 confirms the gauge is shown on the left, two separately labeled I²C pull-ups are on the right and the hypothetical switched battery input is clearly called out. VDD/CELL and ALRT/QSTRT pins are legible. **Finding:** the three GND global-label boxes below U35 overlap each other, making their text unreadable even though the XML shows all three pins on GND. Corrected the generator and canonical sheet to stagger these three GND labels vertically; this changes only wire and label coordinates. The corrected source passes host source/connectivity checks, but its **native PDF/ERC/XML are pending**. Do not reuse the original page 12 image as proof of readable labels at the corrected revision.

Accept the `20fdf48` **electrical XML/ERC checkpoint**, subject to a new native visual review of the revised page 12. No BLE, switch, charger, protected pack, OFF current, I²C waveform or post-OFF-charge SOC measurement follows from this review. The [capture boundary](../../hardware/coupon/rev-a/switch-gauge-boundary.md) and ADR 0015 remain in force.
