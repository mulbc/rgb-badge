<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0282: Real supply bridge across the proposed row cut

Date: 2026-11-24
Status: Accepted for bounded RAM-only complete-cell discovery.

The rejected real row path restores ROW04 but divides VLED into actual
34/6-pad groups. ADR0281's F-only/later-entry graph exhausts2778 states
without a join. Keep the exact ADR0279 cell/cohort and the real rejected
row conductors. Test a physical VLED bridge rather than accepting the
split or changing source/group checks. Source22 remains immutable.

Probe supported0.30/0.10 mm F/In1 VLED microvias on0.10 mm grid
x79.5..82.5/y13.6..15.8 mm. Each must pass source/new Cu and hole checks
and have actual native pad connectivity to the identified six- or34-pad
supply component. A label/plane name alone is insufficient. A single
via may qualify only if it actually joins both through real existing F
and In1 copper. Otherwise test at most64 closest eligible cross-group
pairs with direct/L ordinary0.20 mm F conductor, at most4 mm and two
new microvias. Check all new mutual holes and Cu before refill.

Require refill at21 matching opens with actual VLED40/GND197, all18
row/four gate pads, every original group except the explicitly pending
selector, all19256 retained attached source Cu and zero orphans. The
selector's full restoration and final20-open/all210-group state still
precede any frozen PCB prototype. No further source retirement, no new
centre/through via, no current-limit or protection change, no PCB write.
This is CAD feasibility only: power-copper/current-sharing/electrical/
return/thermal/trial-package/stack/process/assembly/fit and independent
Gate A qualification remain unresolved; fabrication is prohibited.
