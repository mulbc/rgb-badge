<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0172: TMP390 off-pad escape discovery

Date: 2026-11-15
Status: Accepted for read-only geometry discovery only.

On immutable selected 28-open row-two source, refine the historical ADR 0097
sensor screen using ordinary off-pad escape rather than requiring a capture
at the pad centre. Reuse only the exact seventeen-item local study cohort
recorded in `tools/screen-tmp390-supply.py`; require every signature exactly
once before any in-memory omission. No PCB or actual retirement is authorized.
Keep the historical thermal reservation, ≤3 mm sensor movement, C50 pad-distance
bound, fixed TH1/C50/C51 and all external part/copper obstacles. U39 remains
exact TMP390A2DRLR with unchanged TI Rev A pin mapping, local pad geometry and
both open-drain outputs on TEMP_OK. R89/R90 restoration remains unresolved.

At existing 0.100 mm/cardinal sensor samples passing pad/courtyard checks,
screen 0.30/0.10 mm B/In4 captures on a 0.050 mm offset grid within 0.750 mm of
actual VDD pad 5. Permit only a straight ordinary 0.20 mm B.Cu neck ≤0.750 mm
from that pad to the capture. Check all retained foreign/no-net copper, moved
own foreign pads, source edge requirement and supported-span hole policy. An
optional aligned In3/In4 continuation is discovery only and must pass the same
checks. Native holes are never waived; no centre microvia may be added.

A successful escape is incomplete: exact programming-resistor poses, hot/cold
and output restoration, ground interfaces, bypass/return locality and actual
USB supply group still require a separate complete-circuit decision. Preserve
all 216 current groups and every other source item/type/part/rule; matching
native/physical reduction and exact original 104 findings, full contact/
replay/inverse/orphan/fault/source/visual gates precede any selection. No
threshold/current/thermal-error/protection/NTC/timer/default-off or fabrication
change. All electrical/thermal/part/HDI/stack/process/fit/Gate A holds remain.
