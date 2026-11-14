<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0069: Exact Murata six-capacitor land migration

Date: 2026-10-30
Status: Accepted for canonical source and the exact 59-edge routing migration; hardware qualification remains open.

Continue ADR 0066 using the owner's supplied GRM188R60J106ME47-61A-EN
reference sheet (14-Jun-2026), SHA-256
f51cff8dad7a6983263ab35b5705f4d1d4b9977b1f03739c653381ba03d94ea8.
Page 2 identifies GRM188R60J106ME47D and its ±0.1 mm body tolerances;
page 27 Table 2 specifies a = 0.6–0.8, b = 0.6–0.7, c = 0.6–0.8 mm.
Select the candidate's midpoint geometry for exactly C3/C32/C44/C45/C53/C54:
0.65 × 0.70 mm rectangular lands at ±0.675 mm, 1.6 × 0.8 mm fabrication
body, and a separately chosen 2.5 × 1.3 mm first-author courtyard.
The capacitor is nonpolar; numbered pins/nets remain unchanged.

Use a dedicated exact-part library assignment in canonical symbols, embedded
schematic symbols, placed properties and deterministic generators. Do not
change other MPNs using the shared GRM18 library. Historical PCB sources,
frozen routing plans and historical evidence remain byte-for-byte unchanged.
Map only these six explicitly checked corrected numbered pads back to the
legacy ±0.8 mm physical identities for comparison with historical witnesses;
verify exact new geometry before using that mapping. All unrelated pad data,
component fields/poses, copper, zones, rule exceptions and electrical settings
remain fixed. Freeze the complete accepted 59-edge plan and preserve every
completed physical group, not merely the aggregate open count.

Before selecting the corrected routing output, require canonical native XML
and ERC, exact library/board rendering, independent geometry/identity guards,
three stable fills, native and physical opens no worse than 59, no additional
full DRC findings, byte-identical replay, original-orphan restoration and
source/fault checks. If smaller lands lose existing contacts, report the exact
loss and design a separately bounded reconnection before selection. Do not
relax checks to admit it. Historical source reconciliation must explicitly
identify any retained legacy package assignments rather than implying migration.

This corrects source geometry only. Capacitance derating, C45/SYS envelope,
decoupling/return paths, stencil/assembly/process qualification and independent
Gate A remain open. The board is unbuilt; fabrication remains prohibited.

## Selection evidence

The [migration record](../development/murata-land-migration-2026-10-30.md) records all six corrected assignments, exact retention of all 247 accepted physical groups/copper/poses, 59 native/physical opens and 104 unchanged full DRC findings. Stable fills, byte-identical replay, native XML/ERC, rendering, original-orphan restoration, 62 native and 116 portable guards, 23 source faults and source-only CI layout pass. No routing or electrical exception is added; fabrication holds remain unchanged.
