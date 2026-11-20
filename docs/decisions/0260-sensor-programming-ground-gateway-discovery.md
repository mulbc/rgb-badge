<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0260: Sensor programming and ground gateway discovery

Date: 2026-11-20
Status: Accepted for exact read-only prerequisite discovery.

ADR0259 clears selector Cu/holes, all moved courtyards and thermal/C50/
programming bounds, but original TMP_COLD_SET and GND verticals conflict
with the moved U39/R90 pads. Preserve the23-open source; no partial
restoration is selected.

Use its exact U39(+0.375 mm x) and R90(+0.400 mm x) poses and selector/
TEMP_OK replacements. Also translate only exact R89 ERJ2RKF2151X by
+0.100 mm x to59.965,15.000 /B270°. Preserve all three part identities,
values, fields, local pads and numbered nets; all other480 parts stay fixed.
Independent pad transforms are x'=x+0.375/+0.400/+0.100 for U39/R90/R89,
y'=y. Keep actual thermal reservation, no-worse original C50 distance and
≤3 mm corresponding programming/GND distances. Thresholds do not change.

Catalogue two further exact original0.20 mm B items before omission:
TMP_COLD_SET2e37e68f-aaa0-57ec-87ec-9cbeec3eb43f,
59.000,15.500→59.000,16.750; GND
ebdefb60-8e25-59e1-b88a-9b7b1abf74cd,
60.250,16.000→60.250,17.750. Only these six total source items may omit.

Replace Cold by ordinary B conductor from old59.000,15.500 through
59.375,15.500;59.375,16.400 to old59.000,16.750. Preserve actual original
endpoints and all outside contacts, including the retained R90 source leaf.
Keep the proposed R90 SET extension59.500→59.900 at16.750.
Replace GND by ordinary B through60.900,16.000;60.900,17.750, connecting
its exact old60.250 endpoints and the actual moved R90.2 pad60.900,16.750.
Omit the earlier unselected R90 ground extension60.500→60.900; this new
GND path restores that pad directly. No original other Cu retires.

Require native source/new/own-pad Cu, all source/new holes, actual B
courtyards, retained original pin contacts and restored retired-item outside
contacts. For an interface whose old source item is explicitly retired,
require its entire replacement and every retained outside item; never require
a deleted UUID to remain or count a same-net label as restoration. Optional
in-memory refill must retain all211 old groups and attached retained Cu
without orphans. Write no PCB. Supply restoration and every complete22-open
source/identity/exact104/replay/inverse/fault/visual gate remain prerequisites
for selection. Electrical/bypass/thermal/return/current/default-off/protection/
NTC/timer/controlled-stack/process/fit/independent Gate A holds are unchanged;
fabrication is prohibited.
