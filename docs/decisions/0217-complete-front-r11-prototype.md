<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0217: Complete front-side R11 prototype

Date: 2026-11-19
Status: Accepted and fully qualified for the exact 26-open CAD successor;
electrical/assembly/fit/fabrication qualification remains open.

ADR0216 finds sixteen mutually clear front-side poses. Freeze exact Panasonic
ERJ2RKF1001X R11 at (78.850,9.100) mm / 180 degrees on F, using the native
top-bottom side flip. Pad 1 VLED becomes (79.350,9.100); pad 2 ROW_GATE_05
becomes (78.350,9.100). Preserve exact part/field/pad identities, net mapping,
package geometry and every other part pose. Exact source ledger is
`mechanical/review/r11-front-routing-plan.json`.

Retire only the graph-proven 25-item original private gate prefix, including
its five obsolete vias (one historical unsupported centre microvia). Preserve
all four native retained F endpoint-cluster contacts and every other source
item, including the remaining complete PAIR06 gate network and original GND
routes/planes. Add one ordinary 0.20 mm F gate track from (78.350,9.100) to
(78.300,10.800) mm, directly touching each original outside gate wire.

R11.1 directly touches original main VLED F wire
`9e97b5ce-a21b-5767-80bb-e30b1564a12d`; the discovery supply neck is
redundant and must not be added. Add no supply track or new via. Independently
check the exact global pad transform x'=x+6.100 mm, y'=13.350 mm-y and
exact native mirrored local package geometry. A side change is not an
assembly/enclosure/LED optical-access qualification.

Before selection require every preceding 215 group (including all 196 main
GND pads), all retained attached copper and source interfaces, matching 26
native/physical opens, exact104 and all serialized/part/rule/net/zone/setup,
independent replay/stable fill, byte-identical inverse/integer fill XOR,
hole/orphan/fault/native visual gates. Otherwise retain the selected 27-open
source. No current/value/protection/default-off, electrical/return/thermal/
bypass/part/assembly/fit/stack/process/Gate A or fabrication hold changes.

All required CAD gates pass; see `docs/development/r11-front-routing-2026-11-19.md`
and `mechanical/review/r11-front-routing-checkpoint.json`. The 27-open parent
remains immutable. No fabrication release is authorized.

Validation correction adds an explicit F.CrtYd gate against all 257 original
front footprints and two direct overlap/missing-courtyard rejection controls.
Corrected preliminary discovery preserves the selected pose and all sixteen
complete pose results. Native exact104, inverse/replays, all original groups
and source/plan bytes remain unchanged. This does not relax any release hold.
