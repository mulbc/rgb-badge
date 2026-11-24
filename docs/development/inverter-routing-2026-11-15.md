<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Inverter clock routing checkpoint, 2026-11-15

The selected CAD study has **29 native and independently counted physical
opens**, down from 30. U48.4 and corrected U49.7 now share HEARTBEAT_FALL_CLK.
Every one of the 218 prior physical groups survives. There are 217 current
groups on 188 nets. The zero-open goal remains unfinished.

[ADR 0153](../decisions/0153-inverter-clock-routing-checkpoint.md) selects
[the project](../../hardware/coupon/rev-a/staging/led-inverter-routing-trial-114mm.kicad_pro).
The [exact plan](../../mechanical/review/inverter-routing-plan.json) and
[checkpoint evidence](../../mechanical/review/inverter-routing-checkpoint.json)
freeze all changes and validation. The accepted 30-open parent remains immutable.

Exact U48 SN74LVC1G04DSFR moves from (64.250,1.000) mm / 180 degrees to
(110.000,28.150) mm / 270 degrees on B. Exact C67 GRM155R71C104KA88D moves to
(109.450,29.950) mm / 180 degrees on B. The manufacturer DSF pin map remains
2 A, 3 GND, 4 Y, 6 VCC, 1/5 NC. No local land, net, field or other pose changes.
TI SCES214AF October 2025 and the owner-supplied Murata family reference
printed 2014-11-11 remain ignored source references; no current capacitor
approval, capacitance/process qualification or land-pattern change is inferred.

The original fixed-pose neck screen found no capture. The coordinated native
screen finds 3,424 clear sampled placements among 45,880. Its first eight
checked placements have four-pin capture cohorts; four local bypass templates
are found. The exact selected cohort is independently checked against original
integer pad transforms. Its first prototype loses APP continuity, carries an
unfinished input capture and leaves an obsolete supply stub. It is unselected.
Ordinary native routing restores APP and joins the clock. Both input searches
reach 500,001-node bounds. Remove that unused new input neck/capture and only
the two recorded obsolete original APP leaf items. DISPLAY_HEARTBEAT stays
open with its original function and assignment; it is never marked NC.

The final source retains 19,367 original copper items/native types, adds 29
items (18 tracks, eleven vias), and has 19,396 total copper items. Only three
new U48 necks use the unchanged 0.12 mm local rule, each 0.100 mm long and
intersecting the actual courtyard. Remaining new tracks are ordinary 0.20 mm.
All new outer adjacent microvias use 0.30/0.10 mm and two centre mechanical
buried vias use 0.50/0.30 mm. No centre microvia or general narrowing is added.

The original APP external In4 branches and their actual filled source-zone
contact survive independently, as do the main APP and GND groups and all prior
accepted joins. The full 104 original finding payloads match under only the
exact U48 pose change and the earlier frozen U52 transform. Two independent
three-fill replays match source bytes. Removing additions and restoring the
two old items and old poses reconstructs the 30-open source byte for byte,
including every group and exact original findings; all nine integer zone
symmetric differences are empty.

Native strict-ledger/contact/hole and inverse-source checks, 18 native faults,
eight hole-policy controls and all 36 source-workflow commands pass. Native
visual review covers B/In4/In3/In2 at the new site and B/In4 at the old site.
The actual hole audit records one close pair with disjoint supported drilling
spans and one aligned adjacent stack. The native 0.25 mm rule is unchanged;
overlapping/unsupported/through-hole controls remain rejected by the search
policy even where native microvia exemptions would otherwise be permissive.
Those CAD results do not qualify the physical drilling process or stack.

Reproduce the complete gate on the configured native KiCad host with
`bash tools/check-inverter-routing.sh`. The public checkpoint stores hashes;
raw boards, native output and vendor material stay ignored. The 30-open supply
continuation separately made no join and retained identical source bytes.

No board has been built or measured. Current limits, protections, NTC, timers,
hardware fail-safe and default-off behavior remain unchanged. Electrical,
part/capacitance, timing, return, thermal, HDI/controlled-stack, process and fit
qualification, 557 historical centre vias and independent Gate A remain open.
Fabrication remains prohibited.
