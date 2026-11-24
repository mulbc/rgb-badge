<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0218: Freed R11 corridor discovery

Date: 2026-11-19
Status: Accepted for read-only native discovery only.

Continue from the qualified 26-open front-R11 source, SHA-256
fb862c0a548599b7acf328ad8bb5006ce5f78d8b98ceec12bb4af9ace21f1d0f.
Its exact obsolete gate prefix retirement frees the former R11 B/In4 area;
old blocked-capture results on the 27-open parent do not decide this source.

Sample supported 0.30/0.10 mm B/In4 captures at 0.050 mm centres within
x=70.750–76.750 / y=2.250–5.750 mm, for ROW_GATE_00 and VLED. Recheck all
actual retained foreign/no-net copper, pads, edges and full-board hole policy.
For the row gate require an ordinary 0.20 mm B straight/one-elbow neck of
at most 3.5 mm from actual PAIR01.5, mutually clear with the capture.
If those simple necks fail, refine with native-screened eight-neighbour
0.050 mm polylines under the same region and total-length bounds.
Use all actual B pad centres and retained trace endpoints already connected
to PAIR01.5 as alternative zero-length seeds; traversing existing intrinsic
package copper must not require adding a new track through that package.
A path must start at an actual witnessed member of this exact three-pad group.
Record optional aligned In3/In4 access only after native/hole checks. Direct
main VLED targets must be actual retained connected copper; do not infer a
power plane or count an isolated same-net pad as a main supply contact.

Record exact layer-specific source blockers at otherwise B-clear reachable
capture points, including sole-blocker witnesses; this is diagnosis only.
Keep every selected part/field/pose/pad and source copper item fixed. Add no
PCB, unsupported centre/through via, smaller feature or source retirement.
A gateway is incomplete: a complete R6 or supply restoration requires a
separate exact scope and every original group/contact/source/serialized/
replay/inverse/hole/orphan/fault/visual gate with reduced matching counts
and exact104 before selection. All safety/current/electrical/assembly/fit/
stack/process/Gate A and fabrication holds remain unchanged.
