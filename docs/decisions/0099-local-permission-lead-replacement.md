<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0099: Local permission-lead replacement beside U54

Date: 2026-11-07
Status: Selected as a validated 38-open CAD successor; fabrication prohibited.

The fixed U54 ROW_ENABLE_N_CANDIDATE output is enclosed by existing signal
copper. Test replacing only this exact USB_RAW_LOGIC_READY B.Cu cohort,
all at the unchanged 0.20 mm width:

- (93.500,18.950)–(92.900,18.350) mm
- (93.500,19.600)–(93.500,18.950) mm
- (92.500,20.600)–(93.500,19.600) mm

The trial may use the shorter left-side path from (92.900,18.350) through
(92.900,20.350) to (92.500,20.600) mm, or an explicitly recorded nearby
ordinary-width detour. Preserve both outer endpoints and every actual
original external boundary contact on B.Cu, all prior live pad groups and
every other copper item. Do not silently retire additional leads or vias.
A clear pad-group count alone is insufficient boundary evidence.

Only a completed TP14 join under ADR 0098 may justify selection of this
replacement. TP14 keeps its existing 1.0 mm land/fields/net/orientation;
its lead remains at most 5 mm. No other part moves. The rerouted permission
signal retains its source/sink and hardware inhibit function; no current
limit, source/cell boundary, protection, default-disabled setting or firmware
changes. This is not USB data-pair routing.

Require exact old/new contact and copper ledgers, unchanged full native 104
findings, independent native/physical reduction, stable replay/fills, source
contracts, isolated faults and native visual review before selection. Signal
loading/return, probe access, stack/process/fit and independent Gate A remain
unqualified; fabrication is prohibited. Reject any failed boundary or group.

The selected successor replaces the three tracks with two, moves only TP14
beyond the already selected R90 pose, and retains all 227 preceding groups
and all 219 additions. Native/physical counts are 38 with exact unchanged 104
findings. Both outer endpoints and all four rederived external contacts pass;
three stable fills, identical replays, 25 fault guards, 27 source commands
and native visual review pass. See the
[implementation record](../development/permission-output-locality-2026-11-07.md).
