<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Complete converter power-stage review — 2026-11-05

The next useful work is a complete U36 power-stage correction, followed by
U37 return/thermal and voltage-window reconciliation. Arbitrary open-count
reduction would leave critical power-circuit defects unresolved.
[ADR 0089](../decisions/0089-complete-power-stage-review-before-routing.md)
records the bounded plan. This completes the review/planning goal; layout
implementation and electrical qualification remain open.

This is a **CAD review and calculation**, not a measurement of built hardware.
Coupon Rev A is unbuilt. No firmware revision, bench setup or measured electrical
result applies. The selected board remains at **50 native/physical opens and
104 unchanged intrinsic clearance findings**, SHA-256
`5e07fb866cc059de670e34102045d9dfd88c88f101355fcdbb27253c0ae26e43`.
The [machine-readable evidence](converter-power-layout-review-2026-11-05.json)
contains native pad UUIDs, nets, positions, connectivity, all 104 findings,
source hashes and calculation inputs/results. No board, circuit, rules, current
limit or permission boundary changed.

## Native findings

Distances below are straight pad-centre distances in CAD, **not routed length,
loop inductance or a manufacturer spacing limit**. Returns use U36.7 and the
largest U37.15 exposed-ground land, rather than an arbitrary same-number wing.

| Stage | Supply pin to capacitor pad / return pad to IC ground (mm) | Disposition |
|---|---|---|
| U36 C40 / C41, input | 69.583 / 69.526; 69.552 / 69.452 | Connected globally; unacceptable evidence of local converter bypass |
| U36 C42 / C43, output | 18.937 / 19.000; 86.929 / 87.281 | Connected globally; relocate as a complete stage |
| U37 C44 / C45, input | 1.599 / 3.232; 1.835 / 4.120 | Supply locality improved; complete return loop needs review |
| U37 C46 / C47, output | 1.452 / 3.281; 2.104 / 4.193 | Preserve joins while reviewing local power return |
| U37 C48 / C49, output | 6.392 / 8.281; 6.275 / 7.949 | Cannot assume equal high-frequency contribution to nearest caps |
| U37 C63, VINA bypass | 2.761 to VINA1; 2.750 to control GND2 | Connected; optimize quiet supply/return placement |

**U36 functional blockers:** FB pin 8 is isolated from the joined R81.2/R82.1
divider group, whose pads are 56.280/52.781 mm away. EN pin 5, R83.1 pull-down
and SW2.3 are three separate physical groups. A symbol-level pull-down therefore
does not yet establish the routed default. Never energize this candidate to
evaluate regulation. Ground pin 7 does join main ground, but that does not repair
the absent FB/EN connections or remote bypass.

**U37:** R85.2/R86.1 join FB3 and the R84/R85 midpoint is joined.
R84.2 is intentionally a different midpoint net, not a missing direct FB join.
EN12 joins R87.1 and remains held low; the separate interlock candidate permission
is not bridged. Control GND2 and power ground share a net, but connectivity alone
does not demonstrate quiet divider/VINA returns.

No ground vias lie under either IC's selected ground-pad bounding box.
No GND via lies within 3 mm of U37's main exposed-pad centre. Its nine pad-15
copper shapes and paste apertures are **surface lands, not thermal vias**.
The C47 ground repair outside that radius is not an under-package thermal array.
TI's U37 layout example includes exposed-pad vias and short power returns.
A process-compatible heat-spreading/via plan is required; copying a reference
thermal resistance or adding arbitrary holes would not qualify this board.

Both inductors retain short, via-free switching paths from the earlier review:
U36 2.453/2.238 mm, U37 3.216 mm per switching net. This useful result does not
establish complete input/output loops. Existing 0.20 mm routing is a geometric
study parameter. The source specifies six copper layers and 1.0 mm total board
thickness, with no defined finished-copper/dielectric stackup.

## Electrical sensitivity calculations

All calculations are in the linked JSON and reproduced by
`tools/calculate-converter-review.py`. Inputs distinguish source specifications
from assumed scenarios. No operating/current limit is approved here.

**Feedback and mode.** With nominal 0.5 V FB, U36's 511 kΩ / 91 kΩ gives
3.30769 V. Opposing 1% resistor errors and 0.495–0.505 V FB give
3.21957–3.39806 V. An illustrative 60 K resistor excursion with opposing
100 ppm/K TCR, multiplied with initial tolerance, widens this to
3.18707–3.43298 V. Dynamics/ripple/aging are excluded.

U37's 1.24 MΩ / 180 kΩ gives 3.94444 V nominal in PWM. PS/SYNC is grounded.
TI specifies power-save regulation 0.6–5% higher than PWM; including that effect
gives 3.86050–4.25688 V with initial errors, or
3.82039–4.30187 V in the same 60 K sensitivity.
The [existing interlock arithmetic](../design/display-interlock-circuit-proposal-2026-10-12.md)
has an upper rising trip of 4.200–4.443 V **before** resistor TCR and other
effects. These ranges overlap: nuisance inhibition/availability is a credible
risk, not proof of an observed fault. Reconcile both full envelopes, hysteresis
and transitions before joining enable. Do not raise the window, change mode or
alter LED current without a separately reviewed design change.

**Capacitance.** Owner-supplied independent-axis Murata characteristic curves are
at 25°C, AC 0.5 Vrms. They are not guaranteed combined lower bounds.

| Bank and assumed DC bias | Curve sum (µF) | Hypothetical ×0.80 ×0.85 ×0.90 (µF) |
|---|---:|---:|
| U36 2×GRM187, SYS 4.5 V | 12.924 | 7.909 |
| U36 2×GRM187, 5.5 V sensitivity | 10.263 | 6.281 |
| U36 2×GRM219, output 3.43298 V | 32.266 | 19.747 |
| U37 4×GRM187, 3.94444 V | 30.094 | 18.418 |
| U37 4×GRM187, 4.30187 V sensitivity | 27.229 | 16.664 |

The factors model initial tolerance, temperature and an assumed 10% aging loss;
multiplying them with a characteristic curve is **not manufacturer qualification**.
Correlated variation and combined voltage/temperature/age remain unresolved.
U36's explicit effective minima are 4.2 µF input and 10.4 µF output at this
output range. Numerically exceeding those in a sensitivity does not establish
a local bypass requirement with capacitors tens of millimetres away.

U37's table lists 1.5 µH with nominal 2×22 through ≥100 µF combinations,
anticipating 20% capacitor tolerance and 50% bias loss. The derived
`2×22×0.8×0.5=17.6 µF` endpoint is **not a published guaranteed minimum**.
The selected GRM187 curves lose more than 50% at this rail. Four nominal parts
therefore do not automatically establish stability/startup/transient margin.
Exact GRM188R60J106ME47D input combined-bias data is missing; C63's combined
behavior also needs confirmation. No capacitor substitution is selected.

**Inductors.** Exact parts remain DFE252012P-1R0M=P2 / -1R5M=P2.
Initial ±20% gives 0.8 / 1.2 µH. U36's specified L range is 0.7–1.3 µH;
U37 guidance says at least 1 µH. A hypothetical further 30% reduction from the
initial minimum would give 0.56 / 0.84 µH, outside those respective guides.
This is a stress scenario, not an inferred current-dependent curve.
Obtain actual L(I,T), including startup/fault conditions.

At assumed VIN 2.8 V, efficiency 80%, initial-minimum L and electrical-table
minimum frequencies 1.8 / 2.2 MHz, the fixed-frequency boost approximation gives
L1 peak 0.888 A at a **hypothetical** 0.5 A application load; L2 peak 0.633 A at
nominal coupon 0.23302 A VLED load and the 4.30187 V high scenario.
The JSON marks CCM applicability; the 0.1 A L1 case crosses zero and its CCM
result is not an appropriate PFM/DCM operating prediction. DCR-loss arithmetic
excludes core/AC loss and temperature rise. Murata's 4.3/3.5 A inductance-drop
and 3.2/2.6 A temperature-rise entries have separate 20°C conditions; neither
is the pack limit or an enclosure rating. IC current-limit entries likewise
are not permitted output/battery currents.

**Power copper and source budget.** Use uniform-copper
`R=ρL/(w t)`, ρ=1.72×10⁻⁸ Ωm at 20°C. Explicit assumed
18/35 µm thickness and 80°C conductor scenarios are tabulated, with
0.00393/K temperature coefficient as a model assumption. At 35 µm, a 3.216 mm,
0.20 mm track calculates about 7.90 mΩ at 20°C / 9.76 mΩ at 80°C;
0.9 A gives about 8.79 mV and 7.91 mW at 80°C.
This is one segment, not total loop loss or thermal ampacity. Wider
0.40/0.60/0.80 mm candidates reduce resistance; pin necks, vias, planes,
contacts and return paths still require a complete budget. An example 10 mV
local-loop allocation would need review against the full rail/load envelope;
it is not adopted as a requirement here.
Ideal barrel calculations assume 0.10 mm finished holes, 0.05/0.10 mm height
and 10/20 µm plating. No such HDI process is specified or qualified.

At assumed 2.8 V and 80% efficiency, 0.5 A on nominal 3.30769 V plus the
coupon's calculated nominal 0.23302 A on 3.94444 V requires **1.149 A input**
before other loads. The project-recorded LP452845 discharge statement is
900 mA and is not explicitly continuous. This example proves the need for a
complete load/source budget; it does not establish the actual workload,
battery current, pack capability or permission to increase any limit.
Final-display 0.69906 A is a three-times-coupon nominal sensitivity, not an
approved driver accuracy bound. Retain reference-workload and full-content/
fault cases separately; current sinks do not automatically double their total
current when two rows are accidentally enabled.

## Disposition of all 104 intrinsic findings

The native extractor resolves every DRC item UUID to a physical pad.
All are **same-footprint pad/pad** findings; none of these 104 is a track/via
or inter-component clearance error.

| Exact trial part / footprint | References | Count | Actual gap versus global 0.20 mm |
|---|---|---:|---|
| NTLJD3119CTBG / WDFN6_2x2_onsemi_NTLJD3119C | PAIR01–PAIR16 | 96 | 80 at 0.15 mm, 16 at 0.18 mm |
| SN74LVC1G04DSFR / X2SON_TI_DSF0006A_1x1mm_P0.35mm | U48 | 4 | 0.18 mm |
| SN74LVC1G08DSFR / same DSF footprint | U52 | 4 | 0.18 mm |

The onsemi April 2024 Rev 6, CASE 506AN issue H mounting drawing uses these
nominal land dimensions and identifies a solder-mask-defined pattern.
Current zero explicit mask margin/equal copper-paste-mask dimensions do
**not** establish a qualified mask-defined process. Resolve copper/mask
registration, exposed-pad paste and assembler process before any rule relief.
The combined row-pair part remains a PCB-study candidate; this does not silently
replace the canonical separate P/N schematic parts.

TI's DSF land example has 0.60×0.17 mm copper at 0.35 mm pitch:
0.18 mm nominal adjacent copper gap. The stencil example uses 0.60×0.15 mm.
Current 0.05 mm mask expansion implies approximately 0.08 mm mask web;
fabricator/assembler capability is unconfirmed.

Disposition for **every** listed pair is pending process/engineering review,
not accepted-for-fabrication. Preserve manufacturer lands rather than shrinking
them to satisfy a generic rule. Retain global 0.20 mm and forbid broad whole-net
waivers. Future exact physical-pair exceptions must bind footprint/library
identity, geometry and local position (duplicate pad numbers alone are
insufficient), reject pad-to-track/via/foreign-pad relief and fail on new pairs.
If the qualified process cannot build the package, return to explicit part/
footprint selection with an ADR. This review implements no exception.

## Bounded correction queue and acceptance

1. **U36 complete stage first:** jointly place U36/L1/C40–C43/R81–R83.
   Preserve numbered LX joins and exact parts/values; physically join FB and
   R83/EN with correct switch interfaces. Aim initially for nearest input/output
   capacitor edge separation ≤1 mm, supply and return paths of a few mm, and
   divider within about 2 mm of FB. These are proposed floorplan screens,
   not TI hard limits. Reject a pose if short LX paths require remote bypass.
   Include courtyard, front LED, enclosure, ground access and routing blockage.
2. **U37 complete returns/thermal:** preserve the restored supply/FB joins,
   review nearest-cap loop area and C63/control-ground Kelvin return away from
   switching current; join returns near the intended ground interface without
   arbitrarily splitting ground planes. Define exposed-pad heat spreading and
   compatible ground vias with actual stack/process. Treat C48/C49 as distributed
   bulk unless their impedance contribution is demonstrated.
3. **Electrical/process inputs:** establish real SYS and rail/load envelopes,
   pack permission, combined C and L(I,T), finished copper/dielectrics, microvia
   specifications and mask/paste process. Size short power necks and wider
   local copper from drop/loss/thermal calculations. Reconcile VLED voltage
   window without bypassing hardware protection.
4. **Remaining connections by function:** ground/power/FB/default pull-downs;
   then reset/blanking/watchdog/interlock and protection interfaces; then
   USB/clock/serial routes with return paths; finally ordinary control/status
   signals. Each candidate must preserve previous physical groups and bounded
   copper. The numerical open count remains a diagnostic, not acceptance.
5. **Before selecting geometry:** new bounded ADR/requirements/contact ledger;
   exact retirement/addition/pose replay; source-contract/native ERC and pin
   audit; complete DRC with only independently justified package dispositions;
   stable fills, no old-group losses and meaningful contact/rule rejection tests.
   Do not claim the original 104 exact findings after changing rules: report
   the explicit old/new disposition instead.
6. **Before hardware qualification:** independently reviewed calculations and
   Gate A, then controlled coupon startup, OFF/reset/programming, charge/source
   transitions, low/high battery, load-step/rail-pad ripple, retained-VLED decay,
   stuck-row/permission faults and thermal tests. Record hardware/firmware
   revisions, setup and raw evidence. Fabrication remains prohibited until its
   required independent review is recorded.

## Source identity and reproduction

Vendor material remains byte-preserved in ignored
`hardware/coupon/rev-a/reference/vendor-datasheets/`; none is redistributed.
The JSON records exact SHA-256 for each cited cached PDF and owner CSV.

- [TI TPS631000](https://www.ti.com/lit/ds/symlink/tps631000.pdf),
  cached SLVSFH3C, August 2026: §§5.3/5.5, 7.2 and 7.4.
- [TI TPS63020](https://www.ti.com/lit/ds/symlink/tps63020.pdf),
  cached SLVS916I, October 2019: electrical table, pp.13–15 and 23.
- Owner-supplied Murata DFE252012P sheet p.1; exact GRM187/219 June 10, 2026
  reference sheets; GRM188 June 14, 2026 sheet; owner SimSurfing CSV dated
  October 1, 2026. [Murata aging explanation](https://www.murata.com/en-eu/support/faqs/capacitor/ceramiccapacitor/char/0013)
  explains why aging cannot simply be omitted.
- Owner-supplied onsemi NTLJD3119C Rev 6, p.10 mounting drawing;
  [TI SN74LVC1G04](https://www.ti.com/lit/ds/symlink/sn74lvc1g04.pdf)
  DSF land/stencil PDF pp.31–32 and
  [TI SN74LVC1G08](https://www.ti.com/lit/ds/symlink/sn74lvc1g08.pdf)
  PDF p.35 land drawing. Relevant full pages were visually inspected.
- [TI hardware design guide](https://www.ti.com/lit/an/sprabi2d/sprabi2d.pdf),
  §10.1, supplies the copper resistance relation/resistivity. This board's
  finished copper is unknown.

Source discrepancies are retained explicitly: TPS631000 electrical table
lists 1.8/2.0/2.2 MHz whereas application prose calls 2.2 MHz typical;
use table minimum for ripple. Its recommended table caps output capacitance
at 330 µF whereas application prose says no upper limit. Follow the explicit
table pending clarification; the existing nominal 94 µF is below it.
Its input example mislabels exact GRM187 as 6.3 V; Murata specifies 10 V.
TPS63020 electrical minimum is 2.2 MHz despite the 2.5 MHz application example.
These corrections supersede the older unqualified prose assumptions in the
capture records, without changing parts or operating limits.

Reproduce from the repository root:

```sh
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/review-converter-power-layout.py --output hardware/coupon/rev-a/build/power-layout-review-2026-11-05/native.json
python3 tools/calculate-converter-review.py --native hardware/coupon/rev-a/build/power-layout-review-2026-11-05/native.json --output hardware/coupon/rev-a/build/power-layout-review-2026-11-05/reproduced.json
cmp docs/development/converter-power-layout-review-2026-11-05.json hardware/coupon/rev-a/build/power-layout-review-2026-11-05/reproduced.json
python3 tools/test-converter-review-calculations.py
python3 tools/check-converter-checkpoint-plan.py
```

Validation: six independent synthetic unit/axis/corner checks pass; repeated
native inventories and combined reports are byte-identical; selected
checkpoint fingerprints pass. Native child geometry/DRC recheck confirms
50 opens and exact unchanged 104 findings. Full earlier routing/fault/orphan
evidence is linked in the [checkpoint closure](dual-converter-goal-closure-2026-11-05.md);
it is not newly claimed as electrical validation.
