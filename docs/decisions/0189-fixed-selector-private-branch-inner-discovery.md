<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0189: Fixed selector private branch inner discovery

Date: 2026-11-16
Status: Accepted for read-only complete-interface discovery only.

All 59 ADR0188 upper captures meet retained foreign copper. Keep every part,
pose and power-stage/bypass path fixed. Screen replacement of the exact private
ROW_SEL_08 B component catalogued in `selector8-private-bridge-topology.json`:
78 B tracks and its two supported outer microvias at (56.900,17.650) mm.
Freeze signatures and full native source contacts before in-memory omission.
Its only outside B pad is R30.1 at (50.250,7.250) mm; its only outside inner
wire is In3 UUID 401b8b44-9f6a-5db2-9684-00f87af760dd. Preserve both interfaces.

Read-only sample ordinary 0.20 mm B escapes from R30.1 to supported aligned
0.30/0.10 mm B/In4 and In3/In4 captures within 1.000 mm, on a 0.050 mm grid.
Screen direct and orthogonal two-segment necks no longer than 1.500 mm.
Also sample captures at 0.050 mm intervals along the original B branch above
y=14 mm, preserving an exact original-route prefix from R30.1 no longer than
12 mm. This permits reuse of its existing escape without assuming a near-pad
capture is possible. Native geometry and hole checks still apply to every
proposed capture and retained prefix.
Also screen the exact fixed U39 VDD escapes bounded in ADR0188, mutually
against proposed selector copper. Preserve original edge, foreign/no-net
copper, full-board hole and ordinary width rules. Write no PCB.

Any clear capture remains incomplete until selector continuity and the full
USB supply join preserve all 216 original groups, every outside contact,
matching reduced native/physical opens, exact104 and complete successor
source/replay/inverse/contact/hole/orphan/fault/visual gates. A separate exact
prototype decision is required. No electrical, threshold, current, protection,
thermal, C51/U40 locality, stack/process/fit/Gate A or fabrication hold changes.
