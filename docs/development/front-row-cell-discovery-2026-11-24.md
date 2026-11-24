<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Remaining supply and front row-cell discovery

The selected board remains the fully qualified **22-open PAIR03 checkpoint**,
SHA-256 `03e74104c51811a18d558cdc7bd28513f9f1fcb5058ef8a7c7f62f612d8a252d`.
This record describes native CAD studies, not built hardware or electrical
qualification. No partial cell is selected and no successor PCB is written.
The zero-open objective remains unfinished.

The [discovery record](../../mechanical/review/front-row-cell-discovery.json)
contains frozen geometry, typed prospective retirements, original external
contacts, explicit incomplete-group counts and local evidence fingerprints.
ADRs0271–0291 and the corresponding requirements additions bound the studies.

## Fixed supplies and bottom-side routing pockets

Fixed PAIR05/09 searches exhaust166/145 states without a supported capture.
PAIR07 exhausts18831 states with1165 clear captures, without a complete join.
Its supported mechanical-centre extension exhausts18806 states, also without
a join. These are bounded searches, not global impossibility proofs.

Conservative native polygon subtraction identifies enclosed source routing
pockets at PAIR05 and PAIR09. Their source-point components have16/10 boundary
vertices and do not reach the5 mm study rectangle. Polygonization expands
actual foreign-net copper by the ordinary trace radius and clearance plus
a0.00025 mm numerical guard; that guard is not process qualification.
Actual source IDs identify the ground captures/selector traces forming the
walls. No width, clearance, hole, part or profile rule is relaxed.

All221 relocated-ground templates fail copper clearance. A shorter297-template
screen finds five copper-clear captures, but all five fail the original hole
policy against unsupported centre via `e3e4da23-135f-5153-8010-7c87988030c3`.
Those candidates remain rejected. The centre via is catalogued with its real
contacts; no ground-stack replacement or unsupported-hole exception is adopted.

## Coordinated front cell

The next study treats the actual row cell as a unit. Source component and
manufacturer evidence is rechecked before the placement work:

| Reference | Preserved identity/value | Source position, mm |
| --- | --- | --- |
| PAIR05 | Existing `NTLJD3119CTBG_TRIAL_ONLY` value/package | B75.750,11.250/180° |
| R10 | Panasonic ERJ2RKF1001X,1k1% | B47.250,4.250/180° |
| R26 | Panasonic ERJ2RKF1003X,100k1% | B37.250,7.250/180° |

Cached onsemi NTLJD3119C/D Rev6 April2024 pin/package pages and Panasonic
29-May-2025 ERJ coding/dimensions are re-read. The trial transistor value
does not become an approved MPN or footprint. Vendor PDFs/renders stay ignored.

The125244-pose front screen finds32 PAIR05 positions with actual courtyard,
pad/strap/access copper, source-plane and supported-hole clearance. Of these,
28 support short R10 power/gate connections;4058 resistor configurations pass
their bounded screen. Simple F-only row doglegs fail in140 module options.

The selector cut is checked against actual native groups. It separates
PAIR05.2/R26.1 together from U2.7; the initial hypothesis of a fixed R26/U2
driver pair is rejected. The complete cell therefore includes R26, preserving
its100k value, ground connection and default-off topology. Its first bounded
placement passes both real selector and ground leads and all three courtyards.

The frozen RAM study uses PAIR05 F83.4,13.1/270°, R10 F83.1,15.1/0° and
R26 F83.7,10.9/0°, each with the specified top-bottom flip. Exact independent
absolute pad transforms, every field/identity and all480 other placements
are checked. Exactly111 original items are prospectively omitted:106 selector
items, two package gate straps, two B row-leaf tracks and R10's direct B/In4
supply via. Original outside contacts are catalogued first. All19256 remaining
source copper items must stay attached; no additional item may retire.

Ten real conductors restore package straps, supply/ground access and both
resistors. The native refill has GND197/VLED40 and the full four-pad gate,
with no orphan copper. However, the original row and selector groups are
still split: **only208 of210 old groups survive**, despite22 matching opens.
This is an explicitly incomplete state and cannot be selected as progress.
The [repository replay](../../tools/check-front-row-cell-discovery.py)
reconstructs and verifies this exact state from the saved geometry, without
writing a PCB. Its frozen geometry hash is independent of later evidence notes.

## Restoring the row without losing supply connectivity

The first F/In1 row search reaches the actual retained ROW04 through-via
port after14521 expanded states. It restores the row but splits VLED into
34/6 pads after refill. The six-pad island is PAIR01/02/03/04,R6,R11.
That candidate and subsequent paths with the same loss are rejected.
The record retains its real conductor/path and exact separated memberships.

A two-microvia F hop around the rejected In1 path finds38 clear boundary
vertices but no pair inside the initial1–3 mm window. Clear vertices on
opposite sides are farther apart, while the early ones are near the first
proposed row access. No repeated same-span hole is allowed. The next bounded
search keeps more of the row conductor on F, either reaching a real original
F port or entering In1 once at a later clear vertex and carrying the full
real suffix to the retained source port. Every candidate must restore VLED40,
GND197 and all18 row pads; a net label or waypoint alone is never a join.

The later F-only row-entry search exhausts2778 states. A real power
bridge study then tests actual source-connected groups, rather than zone
labels: the wide native probe corridor finds223 six-pad and42934-pad
captures, but no clear direct/L F bridge. Ordinary In2/In3 routes exhaust
3563/1843 states; B/F/In4 routes exhaust30223/12143/2781 states.
A supported two-layer B/In4 graph exhausts33783 states without a join.
None of these bounded results proves global impossibility.

The fixed aligned F/In1/In2 row access fails actual In2 copper clearance.
The continuing row study instead permits a later supported In1/In2
transition, keeping the real F escape. It must restore ROW18 while
preserving VLED40, GND197 and every other existing group. A longer
single-layer path with the known power split is never accepted.

## Independently restored selector

The direct selector templates fail102060 bounded options. A joint F/In1
search finds a real join after310 states, using one supported0.30/0.10 mm
microvia at83.425,12.200 mm and3.405409754 mm of new ordinary track.
The retained destination is the original U2-side via at84.85,15.00 mm.
Full native Cu/hole/refill/group checks preserve VLED40/GND197/gate4,
all19256 retained source conductors and zero orphans. All three selector
pads join. Native and physical counts match21, with209 of210 old groups
preserved and **ROW04 explicitly still split**. This is a partial RAM
result, not a selectable21-open board.

The saved106 typed conductors are sealed by SHA-256
`a251ec65094ca128045753ce7b11c0d169ca0373406d8f54cc0e32930f02cc52`.
The repository checker accepts `--restore-selector` to reconstruct this
partial state from the public record and independently repeats the native
Cu/hole/refill/group checks. That replay passes; it never writes a PCB.
Its local result is `front-pair05/public-selector-replay.json` under the
ignored PAIR03 build directory.

Only a complete20-open cell with all210 original groups, retained source
copper, zero orphans and the full gate/row/selector memberships may proceed
to a separately frozen prototype. Exact original104 DRC comparison,
replay/inverse, deliberate faults, source checks and native visual review
remain mandatory before source selection.

The selected source still has554 unsupported historical centre microvias.
All current/protection/default-off, trial-part, electrical/power-copper/return,
thermal, controlled-stack/process/assembly/optical/fit and independent Gate A
holds remain. Fabrication is prohibited.
