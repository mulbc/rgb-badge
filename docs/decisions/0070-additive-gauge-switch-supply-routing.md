<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0070: Additive switched-gauge supply routing

Date: 2026-10-30
Status: Selected for the exact 58-edge source checkpoint; physical/electrical qualification remains open.

Following the ADR 0054 locality screen, an ignored ordinary-width supply search
joins legacy SW2.6 (printed SW2.7 under ADR 0071) to the existing C39.1/U46.1 switched-gauge group. Native preliminary
counts decrease from 59 to 58 without losing any preceding physical group.
The source circuit and provisional JS202011JCQN switch mapping remain unchanged
under ADRs 0015/0030; its actuator direction, mechanical fit, contact transitions
and manufacturing pin-map approval remain open. This is not a completed gauge
supply: U35 and the A-side pull-up/decoupling group still need their connections.

Permit only the exact additive transaction recorded in the gauge-supply join
catalog: thirteen 0.20 mm tracks and one 0.30/0.10 mm adjacent In4/B microvia,
on +BAT_GAUGE_SW. Extend the new SW2 lead 0.10 mm inside each adjacent pad edge
rather than terminating at the pad corner. Preserve every original and accepted
59-edge copper item, every prior physical group/pose/zone, all six corrected
Murata footprints and all earlier scoped exceptions. No source or accepted
copper may retire. Preserve current, protection, OFF/isolation and enable settings.

Replace only ADR 0069's temporary exact-plan equality check with frozen 59-edge
copper/group/catalog/pose retention that permits these additional items.
Independently require the SW2.7/C39.1/U46.1 physical join under ADR 0071 even if a catalog is
modified with the plan. Require lower independent/native counts, all original
interfaces, unchanged full intrinsic DRC findings, three stable fills,
byte-identical replay, native/source/fault checks and unchanged original-orphan
restoration before selection.

The wider supply searches and C39 ground-repair/lead-transfer trials remain
unselected whenever they split a previous ground/application-supply group or
fail clearance. A lower aggregate count cannot compensate for those losses.
The inductor screen selects no new pose. All power-path, bypass/return, switched
rail behavior, assembly/process/fit qualification and independent Gate A holds
remain open. No hardware measurements or fabrication release are implied.

## Selected source evidence

The [58-edge record](../development/led-routing-progress-58-study-2026-10-30.md) passes complete retention, source/native/ERC/rendering, stable fills/replay, orphan restoration, 65 native and 116 portable guards. Printed switch labels are checked without changing physical contacts. All engineering and fabrication holds remain open.
