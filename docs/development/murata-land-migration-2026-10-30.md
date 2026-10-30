<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Exact Murata six-capacitor land migration

Date: 2026-10-30. Coupon Rev A is unbuilt. This record describes first-author
source, drawing and native geometry checks, not hardware measurements.
Firmware logic is unchanged; the provisional board inventory is regenerated
only to track changed canonical-source/checker hashes. Independent Gate A and
fabrication approval remain open.

[ADR 0069](../decisions/0069-exact-murata-six-capacitor-migration.md) adopts a
dedicated `C_Murata_GRM188R60J106ME47_0603` footprint for exact
GRM188R60J106ME47D at C3, C32, C44, C45, C53 and C54. The supplied reference
sheet, GRM188R60J106ME47-61A-EN (1).pdf, is dated 14-Jun-2026 and has SHA-256
`f51cff8dad7a6983263ab35b5705f4d1d4b9977b1f03739c653381ba03d94ea8`.
Page 2 identifies the 10 µF ±20%, 6.3 V X5R part with a 1.6 × 0.8 mm body
and ±0.1 mm dimensional tolerances. Page 27 Table 2 was rendered and visually
checked: **a is the inner gap, b is ONE land's length, c is its width**.
The applicable row specifies a = 0.6–0.8, b = 0.6–0.7, c = 0.6–0.8 mm.

Selected midpoints give two 0.65 × 0.70 mm rectangular copper/paste/mask lands
at x = ±0.675 mm, with a 0.70 mm inner gap. The fabrication body remains
1.6 × 0.8 mm; the 2.5 × 1.3 mm courtyard is a separate first-author choice.
This capacitor is nonpolar. Pads 1/2 retain their original supply/GND nets:

| References | Pad 1 | Pad 2 |
|---|---|---|
| C3 | +3V3_APP | GND |
| C32 | +3V3_USB | GND |
| C44, C45, C54 | +SYS_APP_IN_DRAFT | GND |
| C53 | +BAT_PROTECTED_DRAFT | GND |

The exact library symbol, all affected placed and embedded schematic symbols,
controller/charger/VLED generators, source checkers and fresh native XML contract
now use the dedicated footprint. The unlinked VLED fixture follows its generator.
Other MPNs retain the shared GRM18 footprint and still need their own drawing
reviews; their historical dimension claims are not qualified by this work.
Native copper, paste, fabrication/courtyard and schematic exports were inspected.

The active routing PCB SHA-256 is
`95d7b7679319cdd64f8e22d428bd2a78454b91298ca17432d34ede0c824ab214`.
Its preceding accepted 59-edge board has SHA-256
`a28258edac032d3dd047f2d7404c0752b25c472af4236b4618b3854717ddfc62`.
The [complete frozen plan](../../mechanical/review/routing-progress-59-checkpoint.json)
is unchanged. No track, via, component pose, value, MPN, numbered net, zone,
current setting, protection or enable boundary changes. The migration preserves
all 18,324 copper items and all **247 existing physical pad groups exactly**.
All six old/new pad identities are checked explicitly before their corrected
positions map back to historical witness coordinates. Other pad properties
remain subject to the complete native signature comparison.

[Direct retention evidence](../../mechanical/review/murata-land-retention-2026-10-30.json)
checks the exact preceding board, every component pose/field, all copper/zones
and all physical groups through three stable fills at 59 opens. Native and
independent physical-pad counts remain **59**, with exactly **104 unchanged
intrinsic findings**. The complete routing acceptance checks also retain all
original source interfaces and previous routing exceptions. Two deterministic
generations produce identical PCB bytes; project and custom rules are unchanged.
Restoring the three original retired orphan vias preserves all selected groups
and 59 opens, with only the same three extra dangling-via warnings.

The historical 215-edge board and earlier native-control manifest remain
unchanged. Their [original canonical snapshot](../../mechanical/review/coupon-canonical-net-contract-before-murata.json)
is preserved for historical fingerprint checks. Current-source comparison of a
legacy board requires explicit `--legacy-land-study` (or historical generator
mode), checks its original land dimensions and reports all six uncorrected
assignments. Ordinary comparison requires corrected assignments and geometry.
The earlier C32-only trial remains historical; its review command now requires
an explicit historical `--source`.

Validation also exercises oversized lands, incorrect old/new labels/positions,
wrong numbered nets and layer sets. The shell-wrapper fixture now represents
the existing isolated onsemi row XML/JSON stage. Isolated native fault processes
retain their KiCad/SWIG objects until test results are reported, then exit with
the result status before interpreter teardown; this avoids post-test native
crashes without suppressing failed assertions. These fixtures are not native
ERC or hardware evidence. Full suite counts and fingerprints are recorded in
the [validation manifest](../../mechanical/review/murata-land-validation-2026-10-30.json).

Reproduce canonical checks with `./tools/check-kicad.sh`, the current source/XML
comparison with `./tools/check-coupon-study-contract.sh`, and routing acceptance
with `./tools/check-routing-progress.sh`. For the direct historical comparison,
extract the pre-migration board from commit `d88599a` to an ignored build path,
then run KiCad Python on `tools/check-murata-land-retention.py --before PATH`.
Local raw outputs are under `hardware/coupon/rev-a/build/murata-*` and
`hardware/coupon/rev-a/build/routing-progress-review/`; their hashes are recorded.
Vendor PDFs, rendered vendor pages, local build output and manufacturing files
are excluded from Git.

Remaining holds include the 50-edge routing target, 104 intrinsic DRC findings,
C45/SYS voltage and effective-capacitance review, decoupling/return/current/
thermal/timing qualification, other exact MPN land reviews, stencil/assembly/HDI,
RF/enclosure work and independent Gate A. This source correction is not a
fabrication release or evidence of electrical operation.
