<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0279: Frozen front-cell in-memory restoration

Date: 2026-11-24
Status: Accepted for exact RAM-only complete restoration discovery.

Freeze three-part-cell.json SHAab22766a5f0a756ae65b29b8a1c7008b4a2379f31dd05ab6fd11ff101070dd0b
and private-leaf-catalog.json SHAc6177b1a9bab4cb3b691f880c482c361cc36af4ea887c863be285914c6138936
under the ignored front-pair05 study. The actual cut proves a two-pad
PAIR05.2/R26.1 private component105 Cu and retained U2.7 singleton197 Cu.
The exact111-item cohort is106 selector items including its In1 bridge,
two gate straps, two B row-leaf tracks and R10's one B/In4 supply via.
All other19256 source Cu stay byte-for-byte geometrically fixed.

In RAM only, omit that exact typed catalogue and flip only PAIR05 to
F83.4,13.1/270, R10 to F83.1,15.1/0 and R26 to F83.7,10.9/0, preserving
identities/values/fields/numbered nets and local package geometry.
Independent absolute transforms (mm) are PAIR05:(94.65-y,88.85-x),
R10:(130.35-x,10.85+y),R26:(120.95-x,3.65+y). Add only the frozen ten
real package/access/resistor conductors before the bounded row/selector
restoration searches authorized by ADR0278. No other source item retires.

Require initial source-hole/courtyard/Cu validity, actual GND197/VLED40
and complete four-pad gate. Temporary row/selector splits must be named
and counted; a matching or lower open count alone is not progress.
Every other original group and all retained attached source Cu must
survive, with no unattached new copper. Row completion must restore
all18 pads; selector completion all3. Only the final20-open/208-group/
188-net state preserving every210 original group can advance to a
separate frozen PCB prototype. Ground stubs may stay only if still
attached and full native CLI DRC later adds no finding; no waiver.

Write no PCB. Full exact104/replay/inverse/fault/source/visual,
trial-package/part/electrical/return/thermal/stack/process/fit and
independent Gate A holds remain. Fabrication is prohibited.
