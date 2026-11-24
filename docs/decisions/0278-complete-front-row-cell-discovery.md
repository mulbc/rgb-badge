<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0278: Complete three-part front row-cell discovery

Date: 2026-11-24
Status: Accepted for bounded read-only complete-cell discovery.

ADR0277's F-only row doglegs fail. Its native selector bridge cut gives
PAIR05.2/R26.1 together (two pads), with U2.7 on the other side, not the
hypothesized retained R26/U2 pair. Preserve this result; do not omit a
branch containing a fixed pull-down. Source R26 is exact Panasonic
ERJ2RKF1003X,100k1%,B37.250,7.250/180 degrees; its pin2 is main GND.
Its family coding/package evidence is the already re-read29-May-2025 ERJ
sheet. Keep that value, exact identity and default-off topology unchanged.

Extend only the coordinated F-side cell to PAIR05,R10,R26, all other480
parts fixed. Screen R26 cardinal0.10 mm poses within3 mm of actual new
PAIR05.2, with real ordinary0.20 mm selector and ground connections to
new PAIR05.2/.1. Require actual native source/mutual courtyards and Cu.
The selector's driver access may start at either genuinely connected
new selector pad. Recheck every proposed path against all three parts.

Allow bounded F/In1 ROW04 access to the same original actual ROW04
through-via port, up to three additional supported0.30/0.10 mm F/In1
microvias and12 mm total row conductor including package strap. Use
x76..85/y10..16 mm,0.025 mm grid/100000 states. Require every source
hole and every mutual new-hole check; same-span repeated/aligned holes
are not an exception. Selector access remains at most12 mm conductor
and one F/In1 capture on the original In1 bridge with its actual retained
U2-side port; no new centre/through transition.

For source cataloguing, explicitly require the bridge cut to yield the
PAIR05.2/R26.1 pair and the U2.7 singleton. Only then catalogue that entire
two-pad private component plus the cut bridge and original outside
contacts. Catalogue the separate exact two gate straps, two B row-leaf
tracks and R10's single direct B/In4 supply access. No full cohort omits
before a separate bounded replacement decision. No PCB is written.

Only a complete20-open cell with every210 original group and all retained
attached source Cu, GND197/VLED40 and full gate/row/selector groups can
advance. Full exact104/replay/inverse/fault/source/visual qualification,
unchanged currents/protection and all electrical/return/trial-package/
thermal/stack/process/fit/independent Gate A holds persist. Fabrication
is prohibited.
