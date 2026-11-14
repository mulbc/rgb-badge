<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0134: Local ROW_SEL_14 transfer feasibility

Date: 2026-11-14
Status: Accepted for ignored copper feasibility only; no part move or successor selected.

ADR 0131's exact rotated U52/C71 witness clears all fixed courtyards and all
six U52 lands. Only original ROW_SEL_14 B.Cu track
`cd082b6f-a457-51b2-9175-398e50ffe1c0` obstructs the two C71 lands.
Continue from ADR 0129's interface-restored prototype, preserving its exact
three-item MODE_BOOT_N cohort and unfinished output capture.

Permit replacing only this additional 0.20 mm B.Cu track,
(101.2,6.75)–(104.3,6.75) mm. Its complete frozen native contact catalog has
seven external ROW_SEL_14 tracks; preserve every contact and the original
complete terminal group, including both exact old ends. No source row net,
pin, assignment, latch/default-off function or current limit may change.

Test supported 0.30/0.10 mm B/In4 captures at the two original ends and ordinary
0.20 mm In4 replacement copper within x=100.5..105.0, y=6.25..8.0 mm.
Reserve the prospective bypass area by first testing the detour through
y=7.4 mm, retaining actual capture positions, all copper/hole/board-edge checks
and every one of the selected source's 221 live groups after refill.
Do not introduce a centre microvia or narrower copper. No U52/C71 pose or
private-leaf retirement is authorized by this transfer decision.

A transfer is not a new circuit join. It remains ignored unless all source
contacts/groups and exact finding payloads survive, apart from the already
declared unfinished U51 capture. A complete successor still needs a real new
terminal join, native/physical count below 33, no additional finding, frozen
full ledger, stable independent replay/refills, fault/source and visual checks.
All electrical/stack/process/fit and independent Gate A holds remain; no
fabrication or powered-operation qualification is authorized.

The direct original-end capture is rejected before saving by retained
ROW_SEL_15 In4 track `e17575b0-ae78-5697-bd24-e5a76d1bcb8c` at y=6.9 mm.
Test an exact alternative: B.Cu stubs from each original end to y=6.25 mm;
supported B/In4 and In3/In4 0.30/0.10 mm stacked adjacent captures at
(101.2,6.25) and (104.3,6.25) mm; and the ordinary 0.20 mm In3 connection
between those two points. Expand only the new-copper bounding box's lower y
limit to 6.0 mm to include full capture/trace extents. No centre microvia,
additional source retirement, source ROW_SEL_15 change or component move.
The same exact source-group/contact/finding and final successor gates apply.

The direct In3 segment hits an original GND stem; the bounded In3-only search
exhausts both sampled components (1,115 / 765 nodes). Permit an ignored local
B/In4/In3 search, expanding the lower y limit to 5.0 mm, using only supported
adjacent 0.30/0.10 mm captures and ordinary 0.20 mm tracks. Preserve every
original track outside the one ROW_SEL_14 cohort and existing MODE_BOOT_N cohort.
Reserve the exact prospective rotated U52/C71 B.Cu lands and two prospective
C71 B/In4 capture disks at (102.6,6.4) and (103.4,6.4) mm only in the search
occupancy. Never add these proxy parts/captures to the PCB or count them as
connections. Actual part migration remains separately unauthorized until its
private-leaf/contact ledger is frozen. All original-group/contact/DRC and
successor gates remain unchanged.

The reserved-space search restores the terminal group with a B.Cu detour; the
four preparatory layer captures are unused and must not remain as dangling
artifacts. Freeze the actual two-track source cohort: also replace original
`8ac4e8e2-39d6-5d3b-998e-590f576d8edf`, the 0.20 mm B.Cu stub
(101.2,7.5)–(101.2,6.75) mm. Its complete contact catalog is recorded before
implementation. Remove only the four newly added unused captures and two
new preparatory B.Cu stubs. Extend the actual detour's boundary contacts to
exact original (101.2,7.5) and (104.3,6.75) mm, instead of relying on 5 µm
end-cap overlaps. Retain every external contact and all 221 original groups.
No other original source retirement, part move, width or rule change.
