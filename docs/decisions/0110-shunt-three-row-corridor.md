<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0110: Three-row local corridor exploration

Date: 2026-11-09
Status: Accepted for ignored exploration; no successor selected.

ADR 0109's back-layer detours are bounded by the ROW_SEL_00 U-shaped
trace at x=77.85 mm. Explore moving that vertical section left while jointly
restoring ROW_SEL_01 and ROW_SEL_03 and joining U38's ground lands. Use
only ordinary 0.20 mm B.Cu tracks; no vias or part moves. The source remains
the selected 36-open board with SHA-256
`a24e9220226b77411ae8e8baea5cd629ce0fea8a97c377a708510d6791c2e439`.

Catalogue and freeze original tracks on these three nets intersecting the
centreline rectangle x=76.3–82.0, y=0.5–6.5 mm before trial. Preserve exact
outside fragments, all boundary ports and every original pad/via contact.
Changed metal must remain within that rectangle expanded by 0.10 mm for
track caps. Keep all other copper, poses, fields, zones, rules and safety
settings unchanged. Preserve all preceding pad groups and accepted additions.

Trials remain ignored. Selection requires a real native/physical reduction,
exact unchanged 104 native findings, independent original-interface proof,
deterministic replay, fault/source checks and visual review. Widths,
clearances and current limits remain fixed. Qualification and independent
Gate A still precede fabrication; no successor is selected by this ADR.

The fixed-pose three-row trial finds ROW_00_A's retained through-via at
(77.25,4.40) mm blocks the proposed leftward row-00 detour. Also permit a
single coupled U38 translation of (+0.250,0) mm, with its exact orientation,
MPN and local lands unchanged, under ADR 0107's contact-preservation bound.
This may create sufficient horizontal space for three ordinary-width row
traces. Independently retain U38.2's original track/via contacts, every
preceding group and all unrelated poses; no other footprint movement is
permitted. All selection gates above remain mandatory.

The coupled (+0.250,0) mm trial restores row traces and joins U38/U52 to
main ground, but its new ROW_SEL_01 B.Cu path separates PAIR03.1/PAIR04.1.
It stays at 36 opens and is rejected. Removing that signal in a diagnostic
copy restores all 196 ground pads, identifying the changed return barrier.
Permit an ignored adjacent-layer transfer of the row-01 horizontal section,
with at most two 0.30/0.10 mm In4.Cu–B.Cu microvias and ordinary 0.20 mm
tracks, inside the same bounds. Screen both via layers and the full refill;
no unsupported central via or reduced clearance is permitted. The original
36-open source and all full successor gates remain mandatory.

The local In4 transfer finds no usable left capture in the sampled corridor.
Also permit an ignored additive search from the disconnected PAIR02.2
land to actual retained ROW_SEL_01 copper, using the existing ordinary-width
routing policy on B.Cu/In4.Cu/In3.Cu. New adjacent transitions remain
0.30/0.10 mm; no In2.Cu transition or retirement outside the frozen local
cohort is allowed. Additions may extend beyond the local rectangle to
retained net copper. The search input must first restore all 196 ground
pads and preserve that group after each trial join. Dangling outside
fragments, if any, prevent adoption until separately resolved by a reviewed
exact-contact retirement policy. Native DRC and all original source groups
remain mandatory; a search result alone is not selection.

Use an explicit ordinary-width ground corridor to constrain further row-01
searches: the restored B.Cu filled component touches PAIR03.1, PAIR04.1
and PAIR02.1. A 0.20 mm ground path wholly contained within that existing
filled component may be added before signal exploration. Erode the native
filled polygon by 0.10 mm and check every path edge's swept copper for
containment/foreign clearance; preserve all groups after refill. This reserves
an actual return path as a routing obstacle rather than repeatedly accepting
signal candidates that cut it. It is CAD continuity evidence, not return-
impedance or electrical qualification. The full unchanged-DRC selection gate
still applies.

The reserved-corridor B.Cu/In4.Cu/In3.Cu restoration exhausts 18,962 nodes.
Permit a final ignored front/back variant with at most two ordinary
0.50/0.30 mm full-span vias for ROW_SEL_01, screened on every copper layer
under ADR 0092's existing through-via policy. ROW_SEL_03's replacement right
stem may shift 0.05 mm to x=81.90 mm, retaining its exact boundary port and
outside fragment. Keep the explicit ground corridor and every source pad
group protected. Any unresolved original stub still prevents adoption.

Outcome: neither the fixed three-row trial nor the (+0.250,0) mm coupled
variant is selected. The latter has exactly the unchanged 104 native findings,
but exchanges the U38/U52 ground island for a PAIR03/PAIR04 island and stays
at 36 opens. Keeping ROW_SEL_00 original does not repair that ground split.
Generic restoration recreates the split; the explicit ground reservation
makes the B.Cu/In4.Cu/In3.Cu search exhaust 18,962 nodes. The widened
front/back variant exhausts 322 nodes. No complete successor is selected.
The 196-pad ground return and ROW_SEL_01 must be restored together in any
future candidate; count or clearance alone is insufficient.
