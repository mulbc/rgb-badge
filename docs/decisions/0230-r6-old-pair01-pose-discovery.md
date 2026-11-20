<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0230: R6 discovery in the old PAIR01 space

Date: 2026-11-20
Status: Accepted for exact read-only combined geometry screen only.

Use the immutable selected 25-open board. ADR0229's reversed R6 B pose has
clear pads/courtyards and both supported lower accesses, but its bounded
supply search ends after 635 nodes / 170 possible transitions, none clear.
It writes no PCB and is not selected.

Independently screen R6 ERJ2RKF1001X B at (75.750,3.750) mm / 0 degrees,
in the space vacated by PAIR01. Keep all other parts, fields, pin nets and
source Cu unchanged except the same exact six prospective R6 supply items
from ADR0119; include its mandatory shortened shared In2 stem. No schematic,
BOM, current/protection/default-off or package change is authorized.

Power: ordinary 0.20 mm B lead R6.1 (75.250,3.750) to supported B/In4 access
(75.250,4.250), In4 through (76.650,4.250) to (76.650,4.550), supported
In3/In4 access there and ordinary In3 lead to the actual retained main VLED
In2/In3 via (78.850,6.800), uuid 525924a2-aff1-59a0-85f5-25c3625c5124.
The historical destination centre remains unsupported/held; do not create or
retype a centre microvia. This is only the resistor pull-up supply; PAIR01.4
remains open, with no row-power claim. Complete pull-up conductor ≤8 mm.

Gate: ordinary B R6.2 (76.250,3.750) to (77.650,4.250), aligned supported
B/In4 and In3/In4 accesses there, In3 to mechanical buried In2/In3 centre
(78.150,4.150), 0.50/0.30 mm, In2 to (76.600,4.300), and aligned supported
In1/In2 plus F/In1 accesses there on the existing PAIR01 gate body. Gate
conductor ≤12 mm. Every ordinary conductor is 0.20 mm; every supported
microvia is 0.30/0.10 mm. No co-located mechanical/micro stack or new through
via is authorized.

Require actual B courtyard and pad screening, all retained/mutual source Cu,
actual original main-supply endpoint witness and full new/source drill audit.
Write no PCB. If clear, a separate frozen prototype must prove all original
213 groups / attached Cu, matching reduced counts, exact104, replay/inverse,
fault and visual gates before selection. All electrical/timing/return/thermal,
trial-package, assembly/optical/fit, via/process/controlled-stack and independent
Gate A/fabrication holds remain open.
