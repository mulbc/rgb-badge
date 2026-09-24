<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Input-protection candidate library audit

2026-09-20. Library-only preparation; neither candidate is selected or placed. No input connection, procurement approval or fabrication release.

## Controlled source

TI TPS25947 SLVSFC9C, May 2026, downloaded PDF SHA-256 `8f96de389903091650d4f462dcfad3210071c3ae7093623a7978f34baf8a65b4`. [Manufacturer PDF](https://www.ti.com/lit/ds/symlink/tps25947.pdf). Pin tables on PDF pages 5–6; electrical tables pages 8–11; PG behavior pages 39–41. RPW0010A drawing 4225183/A, August 2019, pages 72–74. Board and stencil drawings were visually inspected separately. A source-derived copper/paste preview was also inspected; it is not a native KiCad render.

## Exact candidates

| MPN | Pin 2 | Overvoltage response | Sustained overcurrent response |
|---|---|---|---|
| TPS259472ARPWR | OVCSEL | Pin-selected clamp | Active current limiting |
| TPS259474ARPWR | OVLO | Divider-selected disconnect | Circuit breaker |

Both are the auto-retry variants, not the L latch-off variants. Both provide PG on pin 3, PGTH on 4 and the same physical package. Their different pin-2 function is checked independently to prevent a silent variant substitution.

Pin map: 1 EN/UVLO, 2 as above, 3 PG (open drain, active high), 4 PGTH, 5 IN, 6 OUT, 7 DVDT, 8 GND, 9 ILM, 10 ITIMER. The symbol uses analog output electrical types for DVDT/ILM/ITIMER per TI's table. **The two central copper strips are pins 5 and 6, not exposed ground pads.** There is no pin 11 or additional EP.

## Land pattern and stencil

`VQFN_TI_RPW0010A_2x2mm_HotRod` uses the manufacturer's example geometry. Coordinates are top-view KiCad millimetres, y increasing downward.

- Central IN/OUT lands: centres x = -0.25/+0.25, y = 0; size 0.30 × 2.40.
- Inner side lands 2/3/8/9: x = ±0.90, y = ±0.225; size 0.60 × 0.25.
- Corner lands 1/4/7/10 are unions of two overlapping same-number rounded rectangles: horizontal arm at (±0.90, ±0.70), 0.60 × 0.30; vertical arm at (±0.725, ±0.875), 0.25 × 0.65. Preserve the L shape rather than filling its bounding rectangle.
- Minimum separation between distinct copper lands is 0.20 mm in the transcription. This is a component-library property, not board DRC.
- Nominal corner radius 0.05 mm. Project NSMD mask expansion is 0.05 mm; assembler capability must be checked.
- Body outline 2 × 2 mm; project courtyard 2.90 × 2.90 mm. Pin 1 marker is upper left.

The separate stencil follows TI's **0.100 mm thick** example. Central lands each have two apertures 0.28 × 1.06 mm at y = ±0.63. Corner horizontal apertures are 0.60 × 0.275 at (±0.90, ±0.6875); vertical apertures are 0.225 × 0.65 at (±0.7125, ±0.875). Inner side lands retain their copper-sized apertures. All aperture corners use 0.05 mm radius. TI reports approximately 93% corner and 82% central-rail coverage. Overlapping corner aperture primitives must merge into single L-shaped openings in the eventual manufacturing output; native/Gerber and assembler review remain necessary. Do not apply an additional blanket paste reduction.

The source contains 14 numbered copper primitives for 10 electrical pads and 12 unnumbered paste-only primitives. Same-number overlap is intentional; distinct-pad overlap is rejected. This representation does not add logical device pins.

## Electrical findings that guide the next capture

The updated `check-input-protection.py` keeps three findings explicit:

1. A screening 27.4k/10k PGTH divider with ±1% total resistor error gives calculated 4.3575–4.6501 V rising and 3.9631–4.2440 V falling thresholds. PGTH leakage is -0.1 to +0.3 µA, unlike OVLO's symmetric ±0.1 µA. These values are not selected resistor MPNs or a guaranteed charging envelope.
2. PG may reach 1 V while deasserted under the specified unpowered/pull-up conditions. The existing SN74LVC2G17 has a minimum falling threshold of 0.8 V at its 3 V test point. Thus a direct connection is not universally proved low; do not interpolate a guaranteed 3.3 V threshold. Startup, stored output charge and LOGIC_READY sequencing require joint review. TI's PG fault table also conditions some fault indications on PGTH; it is not an unconditional fault flag.
3. The 3.32k ILM table test point spans 0.850–1.150 A before external resistor error. Since 0.850 A is below the charger's 0.9753 A ceiling even before auxiliary loads, this point cannot guarantee full available charger current without limiting/tripping. Repeated circuit-breaker retries are a potential issue for the 474 variant; the 472 variant limits instead. The eFuse must not replace the charger's Type-C-qualified current control.

The wider-input TPS709 makes the 472 fixed-clamp alternative worth evaluating again: an open OVCSEL removes two overvoltage-divider resistors. Clamp threshold is 5.25–6.2 V; the separate output-clamping specification is 5.0–6.12 V at **10 mA**. Comparing 6.2 V to U34's 6.5 V recommended maximum yields only 0.3 V static headroom, not a transient guarantee or an all-load clamp bound. Normal sources near 5.5 V may cause early clamping without disconnecting. Higher-voltage faults can cause dissipation and thermal cycling; TI's operating-range note and actual fault waveform must be respected. No switch from 474 to 472 is approved by this library addition.

## Validation and next gate

Two exact symbols and one footprint added: **49 symbols / 28 footprints per raw view**. Schematic unchanged: 396 PCB items / 1,492 logical pins, eleven pages. Host checks independently audit pin identity, central-rail identity, compound lands, aperture geometry and separation. Fault tests reject rail renumbering, widened/shifted copper, unsplit central paste and wrong variant pin names. The wrapper's synthetic exporter includes both candidate symbols and the shared footprint; it remains synthetic evidence.

All **150 host tests passed** on 2026-09-20; whitespace checks passed. No native KiCad evidence is claimed for the new library.

Native review of these libraries and U29 is pending and will be batched with a functional input-stage checkpoint. Remaining design work is selection of the protection response and exact divider/current/slew components, PG/startup conditioning, physical charger standby, complete-port inrush and transient/thermal verification. Gate A remains mandatory.

## Native follow-up

Owner KiCad 10.0.6 exports at bad43fa passed the [native review](../../../docs/development/input-review-bad43fa.md): configured zero ERC violations, complete connectivity and U29/candidate symbol/copper/paste inspection. Compound corner numerals overlap in the combined fabrication view; clear final assembly numbering remains open. Neither protection candidate is selected or placed. Earlier pending statements describe the source-only checkpoint.
