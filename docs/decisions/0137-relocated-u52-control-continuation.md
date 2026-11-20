<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0137: Relocated U52 control continuation

Date: 2026-11-14
Status: Accepted for ignored bounded routing feasibility; no successor selected.

Continue from ADR 0136's immutable 32-open selected board, SHA-256
`1d34fd1e29c8f65d22e7626cc0d2f0307be26b8d5255a0f6e16eb0eac46ceb6b`.
Keep all poses, part identities, local pads, existing copper, rules/profiles and
board/zone structure fixed. Preserve every one of its 220 physical pad groups.

Read-only screen U52.2 DISPLAY_ENABLE and U52.4 DISPLAY_CLEAR_OK straight local
B.Cu necks on a 0.025 mm grid inside a 0.750 mm radius. Use their unchanged
existing package/net 0.12 mm rule only for each exact bounded neck, and test
0.30/0.10 mm B/In4 captures with native foreign/no-net/mechanical copper,
all holes and board/cutout edges. Keep both necks within the declared radius
and intersecting the actual U52 courtyard. Record exact successful geometry
before creating a routed prototype. No wider part search or source retirement.

Then permit ignored ordinary-width additive continuation from a frozen clear
capture, using supported adjacent 0.30/0.10 mm microvias and 0.50/0.30 mm centre
buried vias. Preserve all old groups after each refill. Do not count an
unfinished capture, source-group split or native/physical disagreement as a
selected reduction. Remove unused new captures before selection. Full exact
finding comparison under the already frozen U52 pose, complete addition ledger,
independent replay/refills, original-source/orphan proof, native faults, source
checks and visual review are mandatory for a successor. No new finding or
ignored check, rail/current/protection/default-off change, qualification or
fabrication release is authorized. Zero opens remains unfinished.

The straight-to-capture screen finds no clear capture: U52.2 has 24 clear
neck endpoints and U52.4 has 408, but every capture is blocked. Extend the
read-only screen to ordinary-width escape tips along those exact straight
necks, with the same 0.750 mm bound and existing courtyard rule. A clear tip
must accommodate an actual 0.20 mm B.Cu end cap with unchanged clearance;
ordinary continuation may then seek a supported capture farther away. Freeze
the tip/neck geometry before creating any prototype. This does not expand the
narrow-width exception or authorize a source retirement/part move.

The tip screen finds no ordinary-width tip for U52.2, but 306 for U52.4.
Prefer a direct ordinary-width contact at U52.4's actual left land edge,
(102.765,4.875) mm, where a 0.20 mm end cap overlaps the land; verify native
clearance before any route. The same actual-land endpoint algorithm may use
other clear edges of that identical land. No narrow neck is required if an
ordinary-width end cap contacts the land directly. Test full-board supported
additive DISPLAY_CLEAR_OK continuation first, with native per-refill retention
of all 220 selected groups. No part, existing copper, rule or safety boundary
changes; exact full DRC and successor gates remain mandatory.
