<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Native actuator-library review: 2b7a468

Reviewed 2026-09-18. The candidate library rendering passes first-author review. This does not select the actuator, validate its circuit or authorize assembly.

The owner supplied `actuator-library-review-2b7a468.zip` and its KiCad 10.0.6 terminal transcript. This is the library-only source checkpoint `2b7a468b25b08fe40ad3fdfe2ccae62f4dab3cf3`.

| Evidence | SHA-256 |
|---|---|
| ZIP | `206d892bdd73200a4093501ebbd45ec4894aca46dbf3d41a008caf4db033ea47` |
| ERC | `ae2053c4ad7bc03479ccb8c8a6a313817b12d46d16b2d6d45e01e482edba7331` |
| XML | `8a46c8a29fcd8514a7202fc86b8cc2ba2c586c8993db762b90a5c69a2fb778e3` |
| PDF | `708d6c30333bb241edd98a762f9e63df50257bf538928f2f9f27c7b999a838cb` |

Independent rechecks of the supplied reports pass: zero ERC messages and all 443 PCB items / 1,636 logical pins. The archive contains 46 symbol SVGs, 27 footprints in each of four raw views, and an eleven-page schematic PDF. AppleDouble metadata was excluded. The ERC report retains the project's existing disabled check categories; zero reported violations is not a claim that every possible ERC rule was enabled.

The ADG4612BCPZ-REEL7 symbol and all four candidate footprint views were rasterized on a white background and visually inspected. The symbol labels, exact MPN, VDD and separate VSS/GND/EP pins are readable and separated. EP is correctly numbered 0. Copper shows sixteen distinct perimeter lands and a separate central pad; paste shows sixteen perimeter apertures and four separated central windows. The fabrication outline crosses some small pad labels, so copper separation was assessed in the copper-only view rather than inferred from fabrication strokes. Mechanical view shows the intended body outline. No new rendering defect was found. Numerical geometry remains controlled by the [source audit](../../hardware/coupon/rev-a/charger-actuator-library-audit.md).

No schematic connectivity changed in this increment, and this review does not claim a fresh visual review of all eleven unchanged schematic pages. No repeat native run is needed for this documentation-only acceptance.

The proposed lands still require assembler/process qualification. The candidate remains unselected and uncaptured: intermediate-supply behavior, control-current budget, ILIM leakage and startup/brownout inhibition remain open in [actuator screening](../../hardware/coupon/rev-a/charger-actuator-screening.md). Independent Gate A remains required before fabrication.
