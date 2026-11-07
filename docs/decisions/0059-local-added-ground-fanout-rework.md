<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0059: Local added-ground fanout rework

Date: 2026-10-28
Status: Authorized for ignored feasibility only; no accepted added copper is retired in canonical source.

A native audit finds a previously added 0.20 mm GND branch across U48's DISPLAY_HEARTBEAT escape. Its B.Cu wall at x = 65.30 mm, y = 0.85–1.40 mm blocks the otherwise approved straight 0.12 mm input neck. The branch belongs to accepted additions, not the original 215-edge source. Repeated fixed-copper and scoped-spacing screens do not make another join.

Permit ignored rework only of the eleven 0.20 mm B.Cu GND tracks in the chain from (64.45, 1.40) through (65.30, 1.40)/(65.30, 0.85) and the staircase to (65.80, 0.65) mm. Enumerate each exact retired signature before removal and prove each belongs to the frozen 64-edge additions, with none in the original source. Preserve the retained C67-side track, lower return, U48.3 and every other external pad/via/retained-copper interface on B.Cu, using actual filled original ground copper or an exact replacement. Do not move any source/added via, other track, component or zone. Retain all original source copper subject only to the six existing catalog replacements and three orphan proofs.

Use the original 0.20 mm clearance and ordinary width, existing 0.30/0.10 mm adjacent microvias and the exact ADR 0051 neck policy. Do not combine this experiment with ADR 0058's smaller-spacing profile. Additional replacement ground trace length may be at most the retired length plus 2 mm. Every old 64-edge physical group and contact must survive refill before a new signal join can be considered. A redundant ground trace is not declared neutral merely because an airwire count stays unchanged; actual native filled connectivity, all external interfaces, no new dangling finding and the exact retirement inventory require independent proof.

TI's current SN74LVC1G04 Rev. AF and SN74LVC1G08 Rev. AA were rechecked: https://www.ti.com/lit/ds/symlink/sn74lvc1g04.pdf and https://www.ti.com/lit/ds/symlink/sn74lvc1g08.pdf . Exact parts, pins, DSF lands, supply and current/protection/enable boundaries remain unchanged. Illustrative calculation only: 2 mm extra 0.20 mm copper, assuming 18 µm thickness and 1.724e-8 ohm metre at 20 °C, adds 9.58 milliohms; at the listed 24 mA drive magnitude that is 0.230 mV / 5.52 µW. This is not an ampacity, transient-return or finished-process qualification and raises no current setting.

Canonical selection requires a new exact added-copper-retirement/replacement/interface policy with a frozen 64-edge plan, independent source/non-retirement proof and fault guards; lower native/physical-pad opens; unchanged full 104 intrinsic findings and three-orphan restoration; stable replay; all source/LED checks; and recorded ground-return/bypass/timing/process consequences. No general added-copper deletion is authorized. The board remains unbuilt; independent Gate A precedes fabrication.

## Recorded feasibility result

Removing the eleven exact additions alone preserves 64 opens, every prior physical group and all 104 native findings. The combined ADR 0060 screen also preserves those counts, but seeded heartbeat escapes can isolate C67 ground and remain excluded. The subsequent 63-edge USB status connection is transferred additively to all accepted 64-edge copper, so it selects no local ground retirement. Raw trial inventories remain in ignored build output; no broader neutrality or engineering qualification is claimed.
