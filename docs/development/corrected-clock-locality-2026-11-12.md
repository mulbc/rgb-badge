<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Corrected-source routing and heartbeat-clock locality

The corrected 35-open source remains unchanged. A finite additive pass makes
39 group attempts across 19 control/row/timing nets and selects no join.
Sixteen attempts reach the 60,000-node bound, thirteen exhaust their permitted
grid, nine have no usable sampled endpoint, and one proposed join splits
existing VBUS/application/battery connections after refill and is rejected.
These are search observations, not proof that routing is impossible.

[ADR 0118](../decisions/0118-corrected-heartbeat-clock-locality-study.md) then
permits a read-only U49 placement screen near U48. Among 80,324 poses on a
0.1 mm grid at four right-angle orientations within 8 mm, 41,120 put the
courtyard outside the board, 29,972 collide with fixed courtyards, and all
9,232 remaining poses fail actual pad/copper or edge screening. No PCB is
saved and no pose is selected. The saved native witnesses include original
ground and ROW_GATE_15 copper; clearing courtyards alone would not clear pads.

The [machine-readable review](../../mechanical/review/corrected-clock-locality-2026-11-12.json)
records the exact source/tool hashes, counts, bounded witness sample and ignored
raw evidence. Only the first 512 copper-failure witnesses are retained; their
frequencies are sample observations, not the full blocker distribution. Zones,
contact reconnection, support/bypass placement and route qualification are
outside this preliminary screen. Different floorplans or unsampled poses may
still work. Zero opens and electrical/process/fit/stack/Gate A acceptance
remain open; fabrication remains prohibited.
