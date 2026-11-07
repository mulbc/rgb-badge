<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# TMP390 supply escape: bounded screen, no placement selected

The selected source remains the **39-open** checkpoint in commit `772c83a`,
SHA `aab8f44a9ec3ae65aed4ee2500d52d57d4d3872c8428b8f50c765bfedd205a1e`.
U39.5 remains disconnected. This is a finite CAD screen, with no built board,
powered hardware, firmware revision or bench measurement.

[ADR 0097](../decisions/0097-bounded-temperature-cluster-supply-study.md)
bounds the study. The [native screen](../../tools/screen-tmp390-supply.py)
and [machine-readable result](../../mechanical/review/tmp390-supply-screen.json)
bind the exact source, script, seventeen-item unselected local copper cohort,
parameters and rejection counts. The script changes only an in-memory board;
it never saves a modified PCB.

The sensor centre is sampled every 0.10 mm over x=54–59 mm / y=13–19 mm,
with 0/90/180/270° orientations and movement no greater than 3 mm. The entire
courtyard must remain inside the existing x=49.5–59.5 mm / y=12.25–20.25 mm
battery-facing reservation. TH1, C50/C51 and all other parts remain fixed;
only U39/R89/R90 are excluded from external component checks. The C50 supply
pad distance cannot exceed the original calculated 3.816022 mm. This distance
is a geometric screen, not a qualified bypass-loop length.

Even after excluding the exact local study cohort, no sampled sensor pose
passes courtyard, foreign-pad/copper and ordinary adjacent 0.30/0.10 mm
B.Cu–In4.Cu capture screening. Among positions within the movement bound,
first-failure counts are:

| Condition | Count |
|---|---:|
| Outside sensor reservation | 2,386 |
| Bypass pad distance increased | 3,020 |
| Fixed component courtyard | 2,219 |
| Sensor pad copper | 871 |
| Adjacent-via copper | 56 |
| Clear candidate | 0 |

Programming-resistor restoration is therefore not attempted. Zero candidates
does not prove impossibility between grid samples, with an off-pad escape,
or with coordinated bus/bypass rework. It authorizes no actual retirement.
The earlier read-only direct In3/In4 plane-capture screen found only two
nearby sites, both at y=18.3 mm, and all four orientations hit fixed C50/C51;
those preliminary raw logs remain ignored in `build/zero-open-routing/`.

The current sensor position, exact temperature programming, NTC, timers,
source/pack current ceilings and hardware inhibits stay unchanged. Cell
coupling and the 3.5 °C cell-to-board error allowance still need physical
qualification. Wider rework requires its own exact contact-preserving scope;
all electrical/thermal/stack/process/fit and independent Gate A holds remain.
