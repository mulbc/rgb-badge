<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0287: Supported two-layer lower supply bridge

Date: 2026-11-24
Status: Accepted for bounded RAM-only additive continuity discovery.

Single-layer B/F/In4 searches exhaust30223/12143/2781 states without
joining the actual supply groups. Keep the exact ADR0279 cell/cohort
and real row path. Search B/In4 together, x72..83/y7..16 mm,
0.025 mm/100000 states/6 mm conductor, with at most two new supported
0.30/0.10 mm B/In4 microvias and ordinary0.20 mm tracks. Starts/goals
are actual retained six-/34-pad Cu or pads. No new centre/through via,
source retirement, component, width, clearance, profile or current change.

Source-hole spatial screening must implement the unchanged native
policy exactly:0.25 mm physical drill clearance, projected disjoint
closeness only for supported spans, exact same-net adjacent outer-stack
alignment only, and no unsupported-source exception. All new same-span
holes need mutual clearance. The complete proposed route must then pass
the existing full native hole auditor independently of the search cache.

Require actual VLED40/GND197/row18/gate4 and21 matching opens, every
original group except explicitly pending selector, all19256 retained
attached source Cu and zero orphans. A full20-open/all210-group cell is
still required before any separately frozen PCB prototype. Write no PCB.
Power-current-sharing/electrical/return/trial-package/thermal/stack/process/
assembly/fit/independent Gate A holds remain; fabrication is prohibited.
