<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Native input-library and U29 review: bad43fa

Reviewed 2026-09-24. Owner-generated KiCad 10.0.6 evidence for commit `bad43fa49164e640dec592ac665a81c1b4147b9e`. First-author staged review, not independent Gate A or a fabrication release.

## Evidence and electrical checks

Owner attachment `input-review-bad43fa.zip`, SHA-256 `542c3135163872d7cd20f4fce588235f610f58c11c289385fe34335c8e4d6668`, with terminal transcript `Pasted text(20260924-180904).txt`. The transcript identifies the expected commit and contains no tracked changes after the run.

The native ERC report has zero errors and zero warnings. It lists the existing ignored check categories: singleton global labels, four-way junctions, SPICE model issues, and footprint-filter mismatch. Zero violations means the configured project ERC passed, not that every possible check is enabled. No new exclusion was added for this review.

The uploaded `coupon-matrix.xml` was independently rerun through `tools/check-coupon-controller.py --netlist`: **396 PCB items / 1,492 logical pins pass** across the full captured coupon. The historically named XML contains the entire coupon; the matrix-only checker is not the appropriate validator. Exports contain **49 symbols**, **28 footprints in each of fabrication/copper/paste/mechanical**, and two derived numbered LED views. The PDF has eleven sheets.

## Visual disposition

- PDF page 11: TPS70933DBVR U29 has IN on the staged +5V_USB boundary, OUT on +3V3_USB, GND connected, EN and NC intentionally open. Heading, labels and enable annotation are readable. Input protection remains explicitly uncaptured; the connector supply and draft boundary are not bridged.
- TPS70933DBVR symbol: the five pin identities and drawing agree with the previously audited source.
- TPS259472ARPWR and TPS259474ARPWR symbol exports: readable headings and pin labels, distinct OVCSEL/OVLO pin 2, PG pin 3, IN/OUT pins 5/6 and GND pin 8. Neither candidate is placed in the schematic.
- RPW copper export: two separate central strips, separated inner side pads and the four L-shaped corner pads appear as intended; no visible accidental bridging.
- RPW paste export: central strips are divided into two apertures each; reduced corner openings remain L-shaped. This closes native-render uncertainty for the source representation, not final Gerber/stencil manufacturing acceptance.
- RPW mechanical/fabrication exports: body, courtyard and upper-left polarity marker are present. The combined fabrication view has overlapping/repeated pad numerals at compound corner pads. Do not use that raw combined view as the final assembly numbering drawing. Clear numbered assembly output remains an explicit release-documentation item; no copper change is indicated by this finding.

Native SVGs were rasterized on a white background for inspection; the original SVGs remain the evidence. Earlier black-looking raster previews resulted from transparency against a dark background, not empty exports.

## Result and remaining work

Accept the U29 native capture and candidate symbol/copper/paste rendering checkpoint. No additional owner run is needed for this documentation-only acceptance. The candidate package still needs clear final assembly numbering and assembler stencil/process review. Protection-variant selection, PG/startup behavior, physical charger standby, remaining power capture and independent Gate A remain open. PR #8 stays draft.
