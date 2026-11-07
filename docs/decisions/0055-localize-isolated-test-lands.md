<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0055: Localize isolated test lands

Date: 2026-10-28
Status: Accepted for exactly four isolated test-land moves in the unqualified 65-edge continuation.

The 69-edge study has seven isolated 1.0 mm PCB test lands: TP1/LED_SOUT, TP2/ESP_EN, TP4/UART0_TX, TP11/SYS_I2C_SDA, TP13/VLED_ENABLE_CANDIDATE, TP14/ROW_ENABLE_N_CANDIDATE and TP20/USB_RAW_OUT1. They are PCB copper features, with their existing exact field values retained; no manufacturer component substitution is involved. Their remote draft placement can force unnecessary signal routing.

Permit ignored placement trials only for these exact references/nets. This is a narrow experimental exception to ADR 0045's fixed-test-pad rule. Retain each existing 1.0 mm circular land, footprint, mask/paste/layer attributes, pin number, component fields and orientation. Keep the back side and existing courtyard/board-edge/other-net clearance. Prefer an accessible location beside existing same-net copper, with at most 3 mm of new original-width lead. Do not move other components or change any value, current/protection/enable setting, firmware or net boundary. No feedback, current-setting or supply test pad is included.

Before selection, independently prove that each selected pad was physically isolated and touched no nonzero accepted 69-edge copper. Preserve all accepted 69-edge copper, prior pad groups, zones, parcels, five source replacements and exact DSF necks. Require lower native/independent opens, three stable fills, unchanged full 104 intrinsic findings, exact integer pose/net/geometry policy, deterministic replay, original-source metadata and negative guards. Only a completed physical join may be selected. Record exact original/selected poses and separate test-land counts from resistor/capacitor moves.

The existing canonical fixed-test-pad contract remains in force until these guards and selected evidence are recorded. Relocated probe access, enclosure exposure, assembly/fixture access, stub loading and signal quality remain unqualified engineering review items. The board remains unbuilt; independent Gate A precedes fabrication. No fabrication release is authorized.

## Selected result

Select TP1, TP2, TP11 and TP20 only, under [the exact catalog](../../mechanical/review/routing-progress-testpad-placements.json), SHA-256 `e7d5b933844d6b19843c2dfdae954f47dcbd68a328b793bd9c595ee5ad977dfc`. Original/selected integer poses and original 180° orientation are pinned with numbered nets and joined source witnesses. Their 0.20 mm B.Cu leads calculate to 2.095, 1.545, 1.44638 and 1.545 mm, respectively. All four prior isolation/no-copper-contact proofs pass independently. TP4, TP13 and TP14 remain fixed.

The [65-edge evidence](../development/led-routing-progress-65-study-2026-10-28.md) records three stable fills, identical replays, independent counts, unchanged 104 full DRC findings, 37 native/69 portable guards, canonical/LED checks and separate orphan restoration. Every accepted 69-edge copper item, previous physical group and R/C pose survives. New native fault cases independently inject prior copper contact or suppress the lead while bypassing catalog matching; both are rejected. This selects only the four enumerated poses and leads, without broad test-pad movement, geometry relaxation or fabrication approval.

## Follow-on coupled UART feasibility experiment, 2026-10-28

TP4's UART0_TX net terminates at isolated R47.2. Standalone test-land moves cannot find a short joined pose around the crowded resistor location. Permit ignored joint R47/TP4 placement trials, combining ADR 0045's connected-R/C policy with this decision's isolated-land policy. This is an explicit exception to the preceding experiment's no-other-component-move restriction, for R47 only. Retain exact Panasonic `ERJ2RKF4990X` (499 Ω ±1%), both pin/net assignments and the existing footprint; TP4 retains its entire 1.0 mm land/fields/net/orientation. R47's centre may move at most 5 mm; connect its input to the exact old UART0_TX_RAW copper endpoint with at most 8 mm of added original-width routing, and keep the TP4 output lead at most 3 mm. Preserve all 65-edge copper, physical groups and the four already selected test-land poses. No IC, other test land, current/protection/enable setting or firmware changes are included.

Panasonic's exact-part page, ERJ datasheet and recommended lands were rechecked: https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ2RKF4990X , https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf and https://industrial.panasonic.com/cdbs/www-data/pdf/RDM0000/DMM0000COL17.pdf . The unchanged local footprint uses two 0.50 × 0.50 mm lands at ±0.50 mm, within the published 0402 land ranges. No substitution or geometry change is proposed. Vendor PDFs remain outside Git.

Any selection still requires exact poses/leads, prior test-land isolation, stable lower independent counts, unchanged full DRC, replay and fault evidence; the canonical selection above remains four lands until that gate passes. UART loading/return/timing and probe/fixture/mechanical access remain engineering holds, and independent Gate A precedes fabrication.

The joint screen found 584 geometrically valid trial poses and no complete input/output reconnection. A diagonal six-layer follow-up found 62 valid trial poses and no completed reconnection. No R47/TP4 move is selected; all four accepted test-land poses remain unchanged. These finite screens do not prove that placement is impossible.
