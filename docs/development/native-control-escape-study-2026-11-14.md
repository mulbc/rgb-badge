<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Native control escape continuation, 2026-11-14

**No successor is selected.** The validated source remains 33 native/physical
opens, SHA-256 `14f0c49582063bab84ea685a8cec798011eb4cd66389b085a3a47777180a13ce`.
The [machine record](../../mechanical/review/native-control-escape-study-2026-11-14.json)
freezes native results, source/prototype hashes, exact retirement/addition and
contact ledgers, temporary-tool fingerprints and manufacturer-reference hashes.
These are CAD studies; no operation or fabrication qualification is claimed.

[ADR 0126](../decisions/0126-complete-gauge-supply-group-restoration-study.md)'s
broad USB-plane reservation exhausts the sampled battery graph from both
sides (1,939,995 / 944,718 expansions). A native 0.101 mm inward-offset corridor
reaches the existing USB capture through its actual left filled polygon;
its separate right polygon is reached by retained In2 copper, not overlapping
bounding boxes. Reserving only that corridor also exhausts the sampled graph
(1,936,137 / 944,985 expansions). Neither trial is a selected join or a proof
of general infeasibility.

[ADR 0127](../decisions/0127-native-board-edge-routing-study.md) widens the
ordinary-width search grid and adds explicit actual board/cutout edge checks.
U52.1 gains 108 native endpoints, versus zero in the old grid. Its sampled
component exhausts after 5,884 expansions; U51.4's fixed component exhausts
after eleven. The broader control study rejects an ESP_EN route for GND,
USB-supply and APP group losses. Other bounded control and heartbeat searches
select no connection. A preliminary nominal-pad-layer cap screen is invalid
and excluded; the corrected screen uses actual copper membership and all
foreign/mechanical/no-net copper. No board was generated from the invalid screen.

[ADR 0128](../decisions/0128-u51-contact-preserving-locality-study.md)'s 441
U51 translations yield seven geometrically clear poses. None produces a
supported capture directly on its output or through the sampled short B.Cu
fan. Those proxies are not full placement/group validation and are not adopted.

[ADR 0129](../decisions/0129-u51-mode-loop-layer-transfer-study.md) identifies
three MODE_BOOT_N tracks enclosing U51's output. The first replacement rejoins
the original terminal group but leaves two old ends dangling and chooses an
out-of-bounds lead; it is rejected. Exact interface branches repair both old
ends and replace that lead. The resulting ignored prototype:

- Retains all 221 original live groups and all 483 original part/field/land/pose
  inventories, every profile and board/net/zone structure.
- Retires exactly the three recorded MODE_BOOT_N tracks, retaining the other
  19,175 original copper items and native via types, with eleven exact additions.
- Has 33 matching native/physical opens and stable repeated fills.
- Retains the exact original 104 findings plus **only one declared unfinished
  output-capture dangling finding**. It therefore fails successor acceptance.

The actual U51 output capture now reaches the wider sampled routing graph,
but the full control join is not established: the 2.6-million-node source
search reaches its bound, while the U52 side still exhausts after 5,884 nodes.
No full successor replay/fault/visual acceptance is claimed for this prototype.

[ADR 0130](../decisions/0130-u52-local-control-capture-study.md)'s two proposed
leftward U52 poses fail native clearance to the retained ROW_SEL_01 track
before saving. The bounded 1,281-pose screen finds 137 geometrically clear
poses, but none yields a supported overlapping capture across its full sampled
contact range. A finer fixed-pose B.Cu fan screen finds no capture; its 137-pose
continuation also finds none. These finite screens do not establish global
infeasibility, do not adopt a U52 pose or finding-coordinate transform, and
leave the selected source's exact DRC gate untouched.

A larger gate/bypass cluster placement can be studied read-only next. C71 is
exact GRM155R71C104KA88D; its referenced current manufacturer sheet returns
HTTP 403 and no corresponding local PDF was found. Its current drawing is
needed before implementing a new C71 placement. No capacitor footprint,
substitution, source limit or protection/default-off setting has changed.

The original four owner ground-probe files, vendor PDFs and all trial boards
remain excluded from this work's commits. Power/return/current, logic timing,
local bypass, controlled stack, historical centre vias, process/thermal/fit
and independent Gate A remain open. The zero-open goal is unfinished and
fabrication remains prohibited.
