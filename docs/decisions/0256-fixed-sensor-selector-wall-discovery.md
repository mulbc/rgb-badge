<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0256: Fixed sensor selector-wall discovery

Date: 2026-11-20
Status: Accepted for exact read-only gateway prerequisite discovery.

The fixed sensor's225 pad/global-grid B/In4 captures all fail source Cu.
Native witnesses identify In4 COL_00_B at15.250 and ROW_SEL_06 at15.750,
while B ROW_SEL_08 atx=56.200 and the retained TEMP_OK strap atx=57.550
enclose its source B component. Preserve those inner traces and TEMP_OK.

On immutable23-open source, catalogue exactly three prospective replacements:
B ROW_SEL_08 db361ff2-8ade-5ab0-bd15-6c1bbad753f9,
(56.200,10.600)→(56.200,16.250),0.20 mm;
B ROW_SEL_06 e734f33e-d79f-507d-97c2-bf4f468110e3,
(55.700,10.850)→(55.700,15.750),0.20 mm;
supported ROW_SEL_06 B/In4 microvia20ea7d57-fa47-5c6c-8ab6-3a5d113a3f67
at55.700,15.750,0.30/0.10 mm. Verify each signature/type and complete native
outside contacts before omission in RAM. Retain every other original item,
including any old In3/In4 access and the original In4 selector contacts.

Screen ordinary B ROW_SEL_06 through55.700,13.800;55.250,14.250;
55.250,15.700;55.325,15.700, with a supported B/In4 capture at the last
point and ordinary In4 connection back to actual old55.700,15.750 port.
Screen B ROW_SEL_08 through56.200,14.000;55.700,14.500;55.700,15.300;
56.200,15.800, retaining the exact original start/end contacts. All tracks
remain0.20 mm and every other original part/pin/net/profile/zone is fixed.

Require native source/new mutual Cu, original direct outside contacts and
all source/new drill rules before any supply discovery. No new centre,
through via, source omission or sensor/capacitor/NTC move is allowed. Write
no PCB. A clear template only opens a potential supply corridor. Any later
full22-open successor must restore both entire selector groups, all211 old
groups and retained attached Cu, main USB/GND/VLED groups, original contacts,
exact104, source/identity, replay/inverse/fault/visual gates and every existing
electrical/bypass/thermal/current/default-off/process/stack/fit/Gate A hold.
Fabrication remains prohibited.

The first fixed wall template preserves all nine original external contacts
and every proposed B segment clears source/mutual Cu. Reject its relocated
ROW_SEL_06 capture and In4 tail for original ROW_SEL_05 Cu and the old
In3/In4 drill at55.150,15.750. Keep that original selector entirely fixed.

Retain the qualified B wall paths through55.250,15.700, and discover only
the final ROW_SEL_06 B/In4 capture at0.025 mm points x=55.100–56.000 /
y=15.600–16.200. Connect from55.250,15.700 by ordinary B direct/either
one-bend tail≤1.5 mm and back to old In4 port55.700,15.750 by direct/either
one-bend tail≤1 mm. Screen full source/fixed/new Cu, holes and all original
contacts. No other source item, part, span, width or qualification changes.
