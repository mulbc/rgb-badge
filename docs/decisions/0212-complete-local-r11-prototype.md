<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0212: Complete local R11 routing prototype

Date: 2026-11-19
Status: Accepted for exact ignored prototype; successor qualification pending.

ADR0211 finds nine mutually clear short-lead poses. Freeze exact Panasonic
ERJ2RKF1001X R11 at (77.750,13.750) mm / 90 degrees on B. Its VLED pad 1
is (77.750,14.250), gate pad 2 (77.750,13.250). The exact frozen prototype
ledger is `mechanical/review/r11-local-routing-plan.json`.

Replace only the graph-proven 65-item original ROW_GATE_05 private cohort.
Its sole outside interfaces are R11.2, PAIR06.5 and the retained ordinary
PAIR06 B bridge `adce34ac-69c2-58a6-9d2a-b49f25dca8e7`. Keep both original
local PAIR06 gate bridges and all other source items. The cohort has no zone
contact; no other pad or retained copper branch is removed. Retire its ten
obsolete vias, including two unsupported historical centre microvias; add no
via. Every retained attached copper item must remain attached to its original
live group.

Add only two ordinary 0.20 mm B tracks: VLED from (77.750,14.250) to the
retained main supply endpoint (78.800,13.750), and ROW_GATE_05 from
(77.750,13.250) to PAIR06.5 at (78.825,13.000). Preserve all fields, exact
pad geometry and all other part poses; current, values and circuit functions
are unchanged. This shortens the complete gate connection rather than adding
a branch to an obsolete route.

Before selection require all 215 preceding groups, matching 26 native and
physical opens, all retained source copper attached, exact original104,
unchanged raw retained copper/part/profile/net/zone/setup identities,
independent pad transforms, actual original supply/gate contacts, stable
independent replay, byte-identical inverse restoration with integer fill XOR,
hole/source/orphan/fault and native visual gates. Failure leaves the 27-open
source selected. No electrical/thermal/bypass/part/assembly/fit/stack/process
qualification, Gate A or fabrication hold is relaxed.
