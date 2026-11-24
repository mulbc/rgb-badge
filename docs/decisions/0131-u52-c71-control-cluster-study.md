<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0131: Read-only U52/C71 cluster placement study

Date: 2026-11-14
Status: Accepted for native geometry screening only; no PCB successor or copper retirement.

The selected source remains 33 opens. ADR 0129's ignored U51 interface-restored
prototype is the geometric input; it preserves all 221 original live groups
but still has an unfinished output capture. ADR 0130's 137 clear U52 poses and
short fans find no sampled escape. Study co-locating exact U52 with its own
exact C71 bypass near U51 rather than moving the gate alone away from its cap.

Keep SN74LVC1G08DSFR and GRM155R71C104KA88D, their local lands/pin numbers/nets
and board side. Screen U52 centres x=98.75..105.50, y=0.75..3.00 mm in 0.25 mm
steps, retaining 180-degree orientation. C71 centres are 1.85 mm left and
0.35 mm above U52, with 0/180-degree orientations considered and its power pad
facing the gate. Use actual project courtyard/copper geometry, all foreign
and mechanical/no-net copper and all nearby holes. Screen supported 0.30/0.10
mm B/In4 control/power/ground capture proxies and actual native board-edge
constraints. A proxy is not a new routed connection or source retention proof.

The owner's exact-byte Murata reference, SHA-256
`3174317e20e99e8568500d251f25a14163711b4c4ff40c5ee89fd20f1c57112c`,
is dated November 11, 2014. Both pages have been visually reviewed. It confirms
the exact D part family and body/terminal information, but is not a current
approval drawing and provides no recommended land pattern. Keep the existing
project-local 0402 land unchanged; current approval, combined-bias capacitance
and assembly qualification remain open. No instruction in the supplied PDF is
adopted as a task request or release authority.

Save only a machine-readable geometry report in the ignored build tree.
Do not save a relocated PCB from this screening decision. Before any routing
implementation, freeze the exact successful pair poses and full private-leaf
retirement/contact catalog in an additional decision paragraph. Every prior
live group, protection/current/default-off boundary and all other original
source items must survive a completed successor. Exact declared-pose finding
comparison, stable replay, native/fault/source and visual gates remain mandatory.
No fabrication or powered-operation qualification is authorized.

The first 560 templates are rejected by courtyard checks: the initial 1.85 mm
pair offset is smaller than the two actual project courtyard half-widths
combined. Use a 2.05 mm leftward C71 offset instead, retaining the same bounded
gate grid, vertical offset and orientations. This remains read-only screening;
no PCB, source retirement or acceptance gate changes.

The wider-offset templates are also rejected. A native witness at the nominal
pair identifies fixed SW1's courtyard (x=99.105..104.195,
y=0.304999..3.794999 mm), not an assumed empty upper-right region. Keep SW1
fixed. Extend only the read-only gate screen to x=100.75..105.50,
y=4.75..7.00 mm in 0.25 mm steps, retaining the 2.05 mm left/0.35 mm up C71
relation and the same unchanged footprints, orientations and capture proxies.
No routing implementation or source retirement is authorized by this extension.

The lower horizontal templates are also rejected; a native witness identifies
U11's actual courtyard extending to x=101.145 mm. A read-only vertical witness
at U52 (102.5,4.75) mm and C71 (102.5,6.60) mm clears all fixed courtyards.
Extend the same bounded lower gate grid only to a vertical pair: C71 1.85 mm
below U52, same x, 90/270-degree cap orientations with its power pad toward the
gate. Screen all original copper/holes and the five existing capture proxies.
This is still geometry screening only, with no relocated PCB or retirement.

The vertical 180-degree gate screen clears 40 pair courtyards but every such
pose hits retained B.Cu. Record a single additional read-only rotated-gate
witness: U52 (103.2,5.275) mm at 90 degrees and C71 (103.0,6.75) mm at 0/180
degrees. Identify every actual pad/copper obstruction without omitting source
items. This authorizes no PCB placement, source copper retirement or rule change.
