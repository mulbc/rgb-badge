<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0097: Bounded temperature-cluster supply feasibility

Date: 2026-11-07
Status: Accepted for ignored feasibility only; no successor selected.

The selected 39-open CAD source leaves TMP390 U39.5 disconnected. Read-only
screening finds no direct two-microvia USB-plane capture near its current
position; the two clear sites within 3 mm collide with C50/C51 at all four
orthogonal sensor orientations. The narrow In4 corridor can also be used as
an intermediate route, so this finite screen is not an impossibility proof.

Permit an ignored coordinated study of U39, R89 and R90 with exact parts,
values, pin nets and local pad geometry unchanged. Keep TH1, C50/C51 and all
other parts fixed. The U39 courtyard must remain inside the existing
(49.5,12.25)–(59.5,20.25) mm battery-facing reservation; sensor movement is
bounded to 3 mm. Keep each programming resistor within 3 mm of its associated
sensor pin and the bypass distance no worse than the preceding source.

Before any routing trial, record an exact local copper cohort: only the
sensor's hot/cold/output leads and local ground returns may be replaced.
Retain every external signal endpoint and boundary contact, both existing
nearby ground vias, every other copper item and every preceding live pad
group. A ground-plane substitution requires one individually filled component
retaining every original outside ground contact. No arbitrary copper deletion,
width reduction, skipped microvia layer or clearance exception is allowed.
Existing ordinary-width and supported-span successor checks still apply.

Any selected successor requires a complete replacement ledger, original-layer
contact/endpoint evidence, local capacitor and programming paths, independent
native/physical open reduction, unchanged exact 104 findings, stable replay,
source and fault checks and visual review. An ignored trial is not adoption.
Thermal coupling, the 3.5 °C cell-to-board error allowance, insulation, swelling
clearance, charge thresholds, source/pack current ceilings, TS/timer/protection
and default-off logic remain unchanged and unqualified. Independent Gate A
and all fabrication holds remain mandatory.

The finite 0.10 mm / four-orientation sensor screen selects no candidate,
even before programming-resistor restoration is attempted. No source pose
or copper is changed. See the [screen record](../development/tmp390-supply-screen-2026-11-07.md).
