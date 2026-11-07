<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0095: Anchored R8 row-gate pull-up locality

Date: 2026-11-07
Status: Accepted for ignored feasibility; successor not selected.

Screen an R8 rotation about its existing VLED pad to close ROW_GATE_02 locally.
R8 remains Panasonic ERJ2RKF1001X, 1 kΩ, 1%, with identical local lands and
source nets. Preserve its supply-pad centre (72.575,8.500) mm and every direct
accepted copper contact. The first pose tested flips −90° to +90°, moving the
body centre from (72.575,9.000) to (72.575,8.000) mm and placing R8.2 at
(72.575,7.500) mm. Target PAIR03.5 is at (74.825,7.500) mm. Keep the exact
paired-device trial identity/lands and all other component poses unchanged.

Require native courtyard/foreign-copper clearance including no-net pads,
ordinary 0.20 mm B.Cu routing, all preceding live groups and copper, native/
physical count agreement, exact unchanged 104 findings, stable replay and
source/fault validation. No additional retirement or via is authorized by
this bounded test. Gate-pad separation must remain below 3 mm. All values,
current limits, protection/NTC and disabled-at-boot LED/row permission circuits
stay unchanged. This connects the existing designed pull-up; it does not
qualify switching speed, gate transients, currents, thermal or production use.

The cached onsemi NTLJD3119C Rev 6 (April 2024), page 1 top-view diagram,
identifies G2 as pin 5, S2 as pin 4 and D1 as pin 6, matching the existing
trial's ROW_GATE_02 / VLED mapping. Panasonic's 29-May-2025 ERJ2R package
reference was visually rechecked in ADR 0094. Neither source is redistributed.
All trial-package, stack, electrical/process/fit and independent Gate A holds
remain open; fabrication is prohibited.

The first +90° flip passes courtyard checks but its gate land conflicts with
the existing B.Cu ROW_SEL_15 track at y=7.850 mm. Test a 0° alternative about
the same fixed supply pad: body centre (73.075,8.500) mm, R8.2 at
(73.575,8.500) mm, with an ordinary B.Cu dogleg around that retained selector
track. No selector copper is retired. All original constraints still apply.

Both tested anchor-preserving poses are rejected: the 0° gate land also
intersects retained ROW_SEL_15/ROW_SEL_01 B.Cu segments. No R8 pose or copper
change is selected; the 40-open source remains unchanged by this study.
