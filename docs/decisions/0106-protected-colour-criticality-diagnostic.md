<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0106: Protected colour-segment criticality diagnostic

Date: 2026-11-09
Status: Read-only diagnostic scope; no source retirement authorized.

Inspect the exact two In4.Cu conductors obstructing PAIR01's first capture:
COL_09_R (60.900,3.250)–(78.600,3.250) mm and COL_09_G
(82.600,2.750)–(62.100,2.750) mm, both 0.20 mm. Test their removal independently
and together only in memory, reporting actual named-pad group losses both
before and after refill. This is a topology diagnostic, not a proposed route
or permission to retire either original or accepted copper in staging.

Keep the canonical source bytes unchanged. Do not change components, fields,
pads, net assignments, settings, profiles or any other copper. Do not count a
colour disconnection as progress toward zero opens. Even a redundant segment
would still require an exact original-contact/current-path review and a separate
retirement policy before adoption. The prior source remains the validated
36-open checkpoint; all qualification and fabrication holds remain.

Both conductors are essential. Removing either splits its 17-pad colour
group into components of one and sixteen pads, giving 37 native/physical
opens; removing both gives 38 and loses both groups. Results agree before
and after refill, with all other copper/net identities unchanged. The
36-open source bytes remain intact. The
[machine-readable result](../../mechanical/review/colour-criticality-2026-11-09.json)
also records the subsequent ordinary ground search, which finds no new join.
