<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0222: R71 supported edge-route discovery

Date: 2026-11-19
Status: Accepted for exact read-only native discovery only.

Continue from qualified 26-open front-R11 source SHA-256
fb862c0a548599b7acf328ad8bb5006ce5f78d8b98ceec12bb4af9ace21f1d0f.
Keep exact Panasonic ERJ2RKF8873X R71, every other part, all source copper
and all current/protection/circuit settings fixed. R71.1 VBUS_CONNECTOR at
(32.750,10.250) mm is isolated; original main VBUS has an actual retained
F/In1 via at (107.250,18.650) mm, UUID
`622180b7-a70d-5112-979d-d4aa69df0189`. This is the existing sense branch;
no resistor or input-current-limit value is changed.

Read-only screen an ordinary 0.20 mm B neck to (32.750,10.750), supported
B/In4 + In3/In4 0.30/0.10 mm microvias there, a 0.20 mm In3 lead to
(33.250,10.750), one supported mechanical buried In2/In3 0.50/0.30 mm
transition there, a 0.20 mm In2 lead to (33.750,10.750), and supported
In1/In2 + F/In1 0.30/0.10 mm microvias there. Stagger the centre transition
by 0.500 mm from each outer stack; add no centre microvia or through via.
The new B endpoint drill is outside the original resistor pad.

Screen the F ordinary lead from (33.750,10.750) through
(33.750,31.900) and (107.250,31.900) to the actual retained F supply via.
This investigates the legal lower-edge lane outside older search bounds,
not any reduced edge clearance. Require actual source 0.500 mm copper-edge
clearance, full foreign/no-net copper and source/mutual hole rules. Bound
new total ordinary conductor length to 112 mm. No source retirement, smaller
feature, part/value/current change or inferred supply plane is allowed.

Write no PCB. A clear result needs a separate exact full prototype scope;
all 214 current groups, complete supply/ground contacts, matching reduced
native/physical opens, exact104 and every source/serialized/replay/inverse/
hole/orphan/fault/visual gate precede selection. Electrical/return/sense-noise,
assembly/fit, controlled stack/process, Gate A and fabrication qualification
remain open; this is not a fabrication release or current-capacity approval.
