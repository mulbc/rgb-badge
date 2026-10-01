<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADG4612 candidate library audit

**Superseded for active design by [ADR 0013](../../../docs/decisions/0013-type-c-only-fixed-current-charging.md):** no switched ILIM branch or ADG4612 actuator is planned. Retained as investigation/library history; its unresolved switch-leakage questions are not active design blockers. Physical charger standby control still requires qualification.

2026-09-18. Library preparation only: not a selected BOM part, captured circuit or fabrication approval. [Native KiCad rendering at 2b7a468](../../../docs/development/actuator-library-review-2b7a468.md) passed first-author review. Electrical selection remains governed by [actuator screening](charger-actuator-screening.md).

## Source and package identity

Owner-supplied `ADG4612_4613.pdf`, Analog Devices Rev. 0, ©2010, 24 pages. SHA-256: `da7e5b537396e1b53eb5e8b1cd45fcb3076b3991978a98ecf381bdaee038ba9d`.
[Manufacturer source](https://www.analog.com/media/en/technical-documentation/data-sheets/ADG4612_4613.pdf).
Pages 10, 17, 18 and 21 were rendered and visually inspected: pinout/truth table, operating modes and CP-16-22 package drawing. Exact candidate: **ADG4612BCPZ-REEL7**, 3 mm LFCSP. Neither the TSSOP pin map nor ADG4613 control polarity is interchangeable.

## Symbol mapping

| Pin | Function | Pin | Function |
|---|---|---|---|
| 0 | Exposed pad, GND | 9 | S3 |
| 1 | S1 | 10 | NC |
| 2 | VSS | 11 | VDD |
| 3 | GND | 12 | S2 |
| 4 | S4 | 13 | D2 |
| 5 | D4 | 14 | IN2 |
| 6 | IN4 | 15 | IN1 |
| 7 | IN3 | 16 | D1 |
| 8 | D3 | — | — |

The manufacturer explicitly numbers the exposed pad **0**; do not rename it 17. It connects to GND. All four controls are active high. VSS would also connect to GND in the proposed single-supply use. NC is retained for an explicit schematic no-connect when captured.

## Package versus proposed lands

The drawing supplies package dimensions, **not a recommended PCB land pattern**. The following lands are project-derived candidates requiring assembler approval, registration/tolerance review and stencil qualification.

| Feature | Package drawing | Candidate PCB geometry |
|---|---|---|
| Body | 2.90–3.10 mm square, nominal 3.00 | F.Fab 3.00 mm square |
| Pitch | 0.50 mm | 0.50 mm |
| Terminals | Width 0.18–0.30; length 0.30–0.50 mm | 0.30 × 0.70 mm, centers 1.45 mm from origin |
| Exposed pad | 1.45–1.75 mm square | Pad 0, 1.75 mm square |
| Courtyard | Not prescribed | 4.10 mm square |
| Paste at EP | Not prescribed | Four 0.70 mm square rounded windows at (±0.425, ±0.425) mm |

Board top-view numbering runs down the left edge 1–4, across the bottom 5–8, up the right 9–12 and across the top right-to-left 13–16. The mechanical bottom view must be mirrored when comparing board-top geometry.

Nominal bounding-box copper gaps are 0.20 mm between adjacent terminals and 0.225 mm to the EP. Mask expansion is 0.05 mm, giving 0.10 mm minimum nominal mask web. Rounded corners use a 0.05 mm radius. EP paste has a 0.15 mm cross-web and 0.10 mm edge inset, with 64% rectangular bounding-box coverage (approximately 63.8% with rounded areas). These are design choices, not manufacturer process guarantees. The proposed lands do not claim full maximum-terminal heel coverage or IPC qualification. No thermal vias or board layout are supplied.

## Remaining electrical limits

Table 11 characterizes isolation at VDD = 0–0.8 V; prose discusses isolation up to 1 V. Normal operation starts at 2.7 V. Do not infer defined isolation across the whole 0.8–2.7 V interval. Independent supply qualification and startup/brownout timing remain necessary before capture. Normal off leakage and power-off isolation leakage are separate specifications. Actual control-level supply current and the effect of leakage at the BQ24074 ILIM pin are still unresolved; this library does not close those budgets.

## Verification boundary

`check-power-libraries.py` checks the exact pin map, active-high controls, pad numbering/geometry, stencil, mask, courtyard and marker. Fault-injection tests cover EP renumbering, pin-map corruption, inverted controls, mirrored placement and EP/stencil faults. The native wrapper requires the candidate symbol and all four raw footprint views.

Expected native output: 46 symbols, 27 footprints per raw view, eleven schematic pages, 443 PCB items / 1,636 logical pins, zero ERC violations. The circuit is unchanged. Review the native candidate symbol and fabrication/copper/paste/mechanical views before accepting this library checkpoint. Independent Gate A and assembly qualification remain pending.

Host validation on 2026-09-18: all 140 tests passed; the targeted 27 power-library tests also passed after removing a redundant constant-only assertion. `git diff --check` passed. The strict USB-closure command still exits 1 for the documented unfinished circuitry. The subsequent owner-supplied native bundle passed the review linked above.
