<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Switched-gauge supply join, 2026-11-12

The selected successor reduces **34 → 33 native and independently counted
physical opens**, retaining all 222 preceding pad groups and the exact original
104 DRC findings. Coupon Rev A remains unbuilt; this is CAD continuity
validation, not a measurement or electrical/fabrication qualification.

[ADR 0124](../decisions/0124-supported-inner-layer-supply-bridge-study.md) and
the [frozen plan](../../mechanical/review/gauge-supply-routing-plan.json)
add exactly **105 ordinary 0.20 mm tracks and nine supported vias**. No source
copper is retired, no part or pad moves, and no pin, net, profile, zone outline,
rule, board edge, current limit, firmware or protection/permission boundary
changes. All 19,064 preceding copper items retain their UUIDs, geometry and
native via types, including every corrected RSE and USB EN1 addition.

The new route joins SW2.7/U46.1/C39.1 with C64.1/R101.1/R102.1: the switched
repeater supply now reaches its A-side pull-ups and decoupling. **U35.2/3 is
still disconnected**; this does not complete gauge-device power or qualify
powered operation. Cached TI TCA9517A SCPS245E, October 2025, page 4 visually
confirms DGK pin 1 VCCA and pins 2/3 SCLA/SDAA. Existing exact parts, lands and
printed switch numbering remain unchanged.

Calculated new track length is **39.560971250 mm**. Vias comprise three In4/B
and four In3/In4 0.30/0.10 mm adjacent captures, plus two In2/In3 0.50/0.30 mm
buried transitions. No new unsupported centre microvia is introduced. Current
capacity, voltage drop, return paths, bus behaviour, via assembly and controlled
stack remain unqualified.

## Validation

- Native and physical opens agree at 33: 221 live groups on 188 nets. All 222
  source groups survive. The six joined terminals are one exact group, while
  U35's original two-pad supply group remains separate.
- Native comparison proves all parts/fields/local pads/poses, original copper,
  profiles, board/net/setup/zone/outline structure and exact five original-layer
  contact witnesses. New copper must equal the frozen complete 114-item ledger.
- Full native DRC preserves all original 104 findings, including item UUIDs,
  positions, descriptions, severities and check lists. No warning is waived.
- Two independent replays, each with three stable refills and group checks,
  match the canonical board byte for byte.
- Removing all additions restores the exact original 222 pad groups, 34 native
  opens and exact 104 findings. Refill serializes two collinear cached vertices
  differently near the old EN1 circuit. Exact integer polygon XOR is empty for
  all nine filled zones; source geometry is identical. The parent file remains
  byte-identical. Child replay still requires exact bytes.
- Eleven native faults reject wrong parts/nets/poses, source retirement,
  narrowing, extra copper, wrong via type/drill and missing contact evidence.
  Actual longest-track and complete-join removals exercise native connectivity
  independently of ledger rejection.
- All 32 current source-workflow commands pass. The canonical pin inventory
  passes with no GPIO or schematic/library fingerprint changes.
- Old/new native B.Cu, In2.Cu, In3.Cu and In4.Cu views were inspected. New
  copper is highlighted from the frozen ledger in the ignored review images.

The [checkpoint](../../mechanical/review/gauge-supply-routing-checkpoint.json)
records exact tracked/raw hashes, replays, faults, source checks, manufacturer
reference and inspected views. Reproduce with `tools/check-gauge-supply-routing.sh`.
Open [the selected project](../../hardware/coupon/rev-a/staging/led-gauge-routing-trial-114mm.kicad_pro).
The immutable 34-open parent remains available. Zero opens, 557 historical
centre vias, electrical/thermal/process/fit/stack qualification and independent
Gate A remain unresolved; fabrication remains prohibited.
