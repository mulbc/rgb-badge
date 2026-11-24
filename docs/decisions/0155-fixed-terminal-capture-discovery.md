<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0155: Read-only exact terminal capture discovery

Date: 2026-11-15
Status: Accepted for read-only native geometry discovery only.

Continue from ADR 0153's immutable selected 29-open source. Inventory actual
native disconnected pad groups and screen terminal-local supported captures
on groups with at most six physical pads. Keep every part/pose/source item,
net/pin mapping, profile/native rule and all safety boundaries fixed. Use only
actual B.Cu live pad copper as anchors; require the prospective 0.30/0.10 mm
B/In4 microvia disk to touch that exact pad shape, with centres sampled at
0.025 mm offsets within ±0.400 mm of its actual centre. Check actual foreign,
no-net/mechanical copper on both layers and the board/cutout edges. Record
possible exact In3/In4 transitions at the same hole when separately clear.
Skip already-present same-position/span captures; do not alter native types.

Use ADR 0147's bounded supported-disjoint-span prefilter while retaining all
other 0.25 mm hole checks and aligned supported same-net stack handling. Do
not add any track or use any width exception in this discovery. A native clear
sample proves neither a join nor filled-plane membership/current capacity.
Write no PCB, retire no item and select no successor. Before implementation,
freeze the exact capture cohort and source-preservation scope in a follow-up
record; any successor still needs all 217 original groups, actual native and
physical reduction, exact original 104 findings under the existing two pose
transforms, independent hole/contact/replay/inverse/fault/source/visual gates.
No current/protection/NTC/timer/fail-safe/default-off boundary changes. All
part/electrical/return/timing/thermal/HDI/stack/process/fit and independent
Gate A holds remain; zero opens is unfinished and fabrication prohibited.
