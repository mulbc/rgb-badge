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
