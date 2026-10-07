<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Unlinked charger EN2 candidate

This two-part [KiCad schematic](charger-en2-candidate.kicad_sch) is the isolated ADR 0023 mode-source candidate. Run `tools/generate-coupon-charger-en2.py` from the repository root to regenerate its schematic and combined local symbol library. It does not include or control E1 or BQ24074, and does not make the coupon charger functional.

`LM4040A30IDBZT` is TI's active A-grade 3.0 V, industrial-temperature DBZ SOT-23-3 orderable. [TI Rev Q](https://www.ti.com/lit/ds/symlink/lm4040.pdf) Table 5-1 maps cathode pin 1, anode pin 2 and optional pin 3. Pin 3 is grounded here, as TI permits and recommends near switching noise. The candidate footprint transcribes TI DBZ0003A's 3 × 0.6 × 1.3 mm lands, paired pads at ±0.95 mm from the centerline and 2.1 mm row separation. Board-top pads 1/2 are the pair; pad 3 is opposite. The 0.05 mm rounded corners and marker are candidate geometry. Exact land/polarity orientation must receive independent visual review before it moves to the canonical library or a board.

`ERJ2RKF1002X` is Panasonic's exact 10 kΩ ±1%, 0402, 0.1 W part; its existing project-local symbol and land were copied into this isolated library. [Panasonic model page](https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ2RKF1002X). No new accepted BOM population follows from the copy.

On 2026-10-07, KiCad CLI 10.0.6 exported an XML netlist: R88.1 = `CHARGER_IN`; R88.2 = U38.1 = `CHARGER_EN2`; U38.2 and U38.3 = ground. ERC reported zero errors and one expected isolated-input-label warning. That check establishes source connectivity only, not EN2 current, startup timing, resistor temperature, input protection or hardware behavior. Independent Gate A remains required before fabrication.
