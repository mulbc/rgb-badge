<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0257: Small sensor and selector gateway discovery

Date: 2026-11-20
Status: Accepted for exact read-only gateway prerequisite discovery.

The925-point ADR0256 replacement capture screen has no native-Cu-clear
capture with its exact B wall geometry. Preserve that bounded miss. Study
one smaller coordinated change on immutable23-open source, keeping C50,
C51, R89/R90, TH1 and all other parts fixed.

Translate only exact TMP390A2DRLR U39 by+0.150 mm in x, from57.625,15.500
to57.775,15.500 mm, unchanged B/180°. Preserve its UUID/fields/local pads/
numbered nets. Independent absolute pad transform x'=x+0.150,y'=y. Require
actual B courtyards inside the original49.5,12.25–59.5,20.25 thermal
reservation, all new-pad/source Cu and retained original pad-contact checks.
R89/R90 programming/GND distances remain≤3 mm and C50's actual VDD-pad
distance must not exceed original3.816022 mm. No threshold or part change.

Retire prospectively exactly ADR0256's three original selector items plus
TEMP_OK B vertical2a6ffeb0-e209-5116-a8b2-31bbae1c9fe7,
57.550,16.000→57.550,15.000,0.20 mm. Catalogue all native outside contacts
before omission. Replace that TEMP_OK vertical atx=57.700 with ordinary
0.20 mm connections to its unchanged original57.550,15.000/16.000 ends.
Keep every other original sensor track/via and source item.

Use ADR0256's B ROW_SEL_06 wall through55.700,13.800;55.250,14.250;
55.250,15.700, then a B tail to supported0.30/0.10 B/In4 access55.650,
15.800 and ordinary In4 tail to old55.700,15.750 port. Use ROW_SEL_08 B
through56.200,14.000;55.700,14.500;55.700,15.200;56.200,15.700 to its
unchanged original16.250 end. All original external contacts must survive.

Screen exact source/new/own-pad Cu, actual B courtyards, all source/new
holes and all retained original U39 pad contacts. An optional in-memory
refill may report full original-group/retained-copper preservation; write no
PCB. No supply join or22-open source follows from a clear fixed gateway.
A later full supply restoration needs a separate frozen complete plan and
all211 original groups/attached retained Cu, exact104, source/identity,
replay/inverse/fault/visual checks. Bypass/return/thermal, current/protection/
NTC/timer/default-off, controlled-stack/process/fit and independent Gate A
holds remain unchanged; fabrication is prohibited.
