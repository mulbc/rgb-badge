<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0259: Small sensor and resistor gateway discovery

Date: 2026-11-20
Status: Accepted for exact read-only prerequisite discovery.

All three ADR0258 offsets fail the fixed R90 courtyard and their last
selector B segment/capture proximity. Do not adopt them. Keep source23
immutable and retain the same exact four source replacements.

Test U39 at58.000,15.500 /B180° (+0.375 mm x) and exact existing R90
ERJ2RKF1402X at60.400,16.750 /B0° (+0.400 mm x). Preserve both parts'
identities/fields/local pads/numbered nets. Independent pad transforms are
x'=x+0.375 and x'=x+0.400 respectively, y'=y. All other481 parts remain
fixed. Require all actual B courtyards, unchanged thermal reservation and
no-worse original C50 distance. Both programming and resistor-ground pad
distances to corresponding U39 SET/GND pins remain≤3 mm. No threshold,
resistance, bypass role, current or default-off change is permitted.

Translate only the prospectively replaced TEMP_OK vertical tox=57.925,
with ordinary0.20 mm connections to its old57.550 ends. Preserve every
other original sensor track/via. Restore R90's original SET and GND copper
interfaces using ordinary0.20 mm B bridges from its old59.500/60.500,
16.750 pad coordinates to its new59.900/60.900,16.750 pads. Each original
contact must remain physically restored; no source R90 item may retire.

Use ROW_SEL_06's previous B detour ending55.250,15.700, a supported
0.30/0.10 B/In4 capture55.850,15.800 and its ordinary In4 tail to the
original55.700,15.750 port. ROW_SEL_08 keeps its upper56.200,14.000 /
55.700,14.500 detour, then uses55.700,15.100;56.350,15.600;
56.350,16.000;56.200,16.250. Preserve all original outside contacts.
No additional original Cu may omit and no centre/through via is permitted.

Require full source/new/own-pad Cu, unrelaxed source/new hole rules,
original U39 pin contacts and restored R90 interfaces, actual B courtyards
and all thermal/C50/programming bounds. An in-memory fill may prove all211
old groups and retained attached Cu with no orphans; write no PCB. A clear
gateway still needs complete supply restoration and separately frozen22-open
prototype/source/DRC/replay/inverse/fault/visual gates. All electrical/thermal/
bypass/return/process/stack/fit/independent Gate A holds remain open and
fabrication is prohibited.

For each retained R90 interface, record whether a single new bridge directly
touches both old Cu and new pad. If that direct test is false, it may not be
reported restored before refill. Require actual post-refill connected-item
UUID membership from that exact moved pad to every original contacted item,
plus all211 original-group and retained-attached-Cu checks. Net labels alone
cannot establish restoration. No failed Cu/hole/courtyard prerequisite may
be bypassed by the connectivity check; no extra source item is retired.
