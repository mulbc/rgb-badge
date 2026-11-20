<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0185: Read-only sensor and correctly associated bypass floorplan

Date: 2026-11-16
Status: Accepted for read-only geometry discovery only.

Local routes at the previously fixed poses remain incomplete. The two verified
USB In3 access sites are near (55.900,18.300)/(56.000,18.300) mm, where previous
sensor courtyards overlapped fixed C50/C51. Source schematic review identifies
C50 as U39's bypass and C51 as fixed U40 SN74AUP1G125DBVR's bypass; C51 is not
a second U39 capacitor. TI SCES595N pages 3/18 confirms DBV VCC 5/GND 3 and
recommends local 0.1 µF bypassing. Both existing capacitors remain exact Murata
GRM155R71C104KA88D with unchanged manufacturer local lands and pin nets.
[TI source](https://www.ti.com/lit/ds/symlink/sn74aup1g125.pdf).

Read-only screen U39/R89/R90/C50/C51 as a coordinated cohort. Keep U40, TH1
and all other parts fixed. The actual U39 courtyard must remain wholly inside
the original (49.5,12.25)–(59.5,20.25) mm battery-facing reservation. Extend
only the sensor discovery movement radius from 3 to 4 mm; this does not change
the reservation, 3.5 °C thermal-error allowance, thresholds or qualification.
Use cardinal sensor orientations and ordinary straight 0.20 mm B supply necks
≤0.750 mm from VDD to a physically witnessed USB-plane site, supported aligned
0.30/0.10 mm B/In4 and In3/In4 microvias, exact foreign/no-net/mutual copper,
hole and 0.500 mm edge rules. No centre microvia or width/clearance exception.
R89/R90 pad distances to their corresponding SET/GND pins remain ≤3 mm.
C50's VDD-pad distance must not exceed the original 3.816022 mm; full supply/
return loops remain unresolved. C51 discovery must place its USB pad within
3 mm of U40.5, with a clear ordinary local supply lead ≤4 mm and original
connected-ground contact. Do not merely preserve its original remote distance.

Before any in-memory omission, freeze the exact source signature/type/native
contact catalog for the prior 34-item sensor/GND cohort and the complete six-
item C50/C51 supply-port leaf: B track UUID 311027e9-3797-5f1d-bf17-703362aedca5,
In4 track 7770d5b2-8202-57fe-b134-45b147cf4215, and via UUIDs
a8ec3311-126a-52e1-8771-9bbd3853a4af, ac0abf2e-78dc-5712-836e-65a09064a65f,
c5efc353-4d11-5564-b651-3ed76b0a74f9, a2fa9f1d-15df-5f56-946d-a635812ab51a.
The leaf includes two historical duplicate B/In4 vias at (54.485,18.350).
Its only outside pad contacts are moving C50.1/C51.1; all original plane-unit
contacts remain restoration obligations with retained main-group witnesses.
No arbitrary other original track/via may be omitted. The exact forty-item
union is a prospective discovery cohort, not an adopted retirement.

Write no PCB. A clear sensor site or local capacitor pose is incomplete until
all five exact poses, programming/output/local supply/quiet returns, original
plane contacts and all 216 source groups are restored together. Any later
prototype needs a separate exact complete-circuit decision and full matching
reduced native/physical, exact104, source/contact/hole/replay/inverse/orphan/
fault/visual gates. No exact part, current/threshold/protection/NTC/timer/
default-off, thermal-error, HDI/stack/process/fit/Gate A or fabrication hold is
changed; zero opens remains unfinished.

Also test the two actual original capacitor supply-port coordinates
(54.485,18.350)/(57.285,19.295) mm, requiring the same retained main-group
filled-unit witness and all native checks. They are already source copper
interfaces, not invented power anchors. Fewer prospective omissions are
permitted: read-only test C50's 180° flip about its fixed USB pad at
(57.285,19.295) mm (new centre (57.685,19.295) mm / 0°), leaving its entire
original supply copper/interface as an obstacle. This does not authorize any
extra omission, actual pose or saved PCB. C51's exact buffer association and
local-bypass bounds remain unchanged.

The initial 2 mm C51 screen rejects all 5,012 samples on actual U40/J2/U34
courtyards. Extend only its discovery pad-distance bound to 3 mm and local
supply-lead bound to 4 mm, with centre samples x=22–31/y=8–17 mm. These are
engineering search bounds, not manufacturer numeric limits or qualification.
Keep exact native courtyard/pad/ground-contact checks and seek the closest
actual successful site.
