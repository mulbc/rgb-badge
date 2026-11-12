<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0123: Restore supply groups during USB CC1 routing

Date: 2026-11-12
Status: Accepted for ignored feasibility; no successor selected.

The ADR 0091/0092 additive search from the selected 34-open source
`92f942e46281475cbdadf6e9a0ad7a0d531e38c3032f85a4206bbf9e9bc1fccd`
finds a provisional USB_CC1 path from J1.A5 to U31.1, but rejects it after
native zone fills split existing +3V3_APP and +BAT_PROTECTED_DRAFT groups.
The rejected snapshot hash is
`ccc636909faeca02a8f29096945cb6670eb6db361278811751947b107326d345`.
No lower open count or isolated CC1 join authorizes adoption.

Permit additive restoration feasibility on an ignored copy of that exact
snapshot. Restore the former +3V3_APP members R106.1/U32.8 and the former
battery group C53.1/U41.2/U41.3 to their complete original source groups.
Retain every source part, pose, net, copper item and accepted addition,
including the corrected RSE mapping and ADR 0121 USB join. Preserve the full
original supply groups, rather than reconnecting only these listed members.
No current, charge, protection, permission or firmware boundary may change.

Use ordinary 0.20 mm copper and the existing supported adjacent microvia,
0.50/0.30 mm central buried-via or full-span via rules. No skipped-layer or
new centre microvia, arbitrary plane anchor, narrowing or DRC waiver is
allowed. Any native-filled plane destination must identify its actual
connected component. Restoration alone is not evidence of power-path current,
return, signal-integrity or thermal qualification.

Selection requires a frozen full copper/endpoint ledger, all 222 preceding
live groups, matching native/physical count below 34, exact unchanged 104
findings, stable independent replays/refills, source/fault checks and visual
review. Any remaining group loss rejects the candidate. The immutable source
remains at 34 opens until every acceptance gate passes. All controlled-stack,
557 centre-via, electrical/process/fit and independent Gate A holds remain;
fabrication is prohibited.
