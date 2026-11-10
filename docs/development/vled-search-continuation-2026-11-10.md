<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# VLED and group-target routing continuation, 2026-11-10

The board remains at **36 native/physical opens**, SHA-256
`a24e9220226b77411ae8e8baea5cd629ce0fea8a97c377a708510d6791c2e439`.
No pose, copper, rule, zone or part change is selected.

The useful implemented change is an opt-in search for bridges between any
actual disconnected groups on a net. Previously, every target was the
largest group. That can miss a shorter bridge between two smaller groups.
`--all-group-targets` deduplicates live groups, tries small source groups first,
and retains exact native endpoint and post-refill group-preservation gates.
`--source-reference` restricts exploration to an actual selected reference.
The default search mode remains unchanged. Every search still writes only
ignored build outputs; it does not update the selected board.

The [evidence record](../../mechanical/review/vled-search-continuation-2026-11-10.json)
and ADRs [0111](../decisions/0111-all-group-additive-routing.md) /
[0112](../decisions/0112-anchored-vled-pullup-placement.md) distinguish native
regression results from the unsuccessful real-board experiments:

- A native synthetic fixture blocks access to the largest group. The default
  search stays at two opens; all-group targeting joins the other two groups
  and reaches one. The largest group and every prior group remain intact.
- Portable checks verify source-group exclusion, target deduplication and
  re-evaluation after live group membership changes. The portable test is now
  included in the host workflow. All **28 source-workflow commands pass**.
- Forty-six close pad pairs on different groups have no clear sampled direct
  or orthogonal back-layer bridge. The broader all-group three-net search
  also selects no join; node bounds remain explicit in the evidence.
  An ignored eight-neighbour variant with exact diagonal edge screening and
  a zero heuristic likewise adds no copper across VLED, ground, gauge supply
  and display-clear groups. Diagonal routing is not enabled in production.
- R11/R21 retain their exact 1 kΩ ERJ2RKF1001X identities and original gate
  contacts during ignored angular exploration. Their 144 sampled orientations
  leave thirteen geometry-clear poses, including each original orientation.
  None yields a complete ordinary-width B.Cu/In4.Cu/In3.Cu VLED connection.
  No rotated resistor or dangling seed is adopted.

The checkpoint records the updated search-tool fingerprints and separate
native regression evidence. Existing full board validation remains evidence
for the unchanged board, profiles and acceptance policy; no new successor
replay/fault/visual acceptance is claimed. Candidate boards, raw native reports
and vendor documents remain ignored. The four pre-existing probe files are
untouched.

These are CAD calculations and searches, not hardware measurements or proof
of electrical functionality. The zero-open objective, controlled stack/process,
electrical/thermal/fit qualification and independent Gate A remain unresolved.
