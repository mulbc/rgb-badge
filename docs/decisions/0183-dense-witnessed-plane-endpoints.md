<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0183: Dense actual filled-component endpoint discovery

Date: 2026-11-16
Status: Accepted for ignored routing endpoint refinement only.

The local sensor searches retain all original groups after accepted joins but
miss USB supply. Historical native contact screening identifies narrow actual
USB-plane capture sites at y=18.300 mm. The existing zone-target sampler uses
every fourth 0.050 mm grid cell, which can omit that row. Its centre-inside-only
criterion can also miss a track endcap's real physical overlap with a filled
component. These finite search misses do not prove geometric infeasibility.

In a separate ignored successor of the local search tool, sample every actual
0.050 mm grid cell within the unchanged local window/radius. Target only an
individual original filled polygon returned with an actual same-group retained
copper witness. Permit a grid point when its ordinary 0.20 mm track endcap
physically overlaps that exact filled unit, rather than requiring its centre
inside the unit. Keep exact native foreign/no-net copper, hole/span, edge,
width/via/type and every length/node bound unchanged. No fabricated zone anchor,
shared-net shortcut, rule waiver or public historical tool modification.

The endpoint is only a discovery candidate. Commit a join only after native
refill proves actual terminal-group connection and preserves every current
original group; otherwise undo it. Full final original 216 groups/interfaces,
matching native/physical reduction below 28, exact original 104 findings and
all source/contact/hole/replay/inverse/orphan/fault/visual gates still precede
selection. Use only the exact already scoped ADR0177/0179/0182 prototypes.
No new part/retirement/profile/current/thermal/threshold/protection/NTC/timer/
default-off/HDI/stack/process/fit/Gate A or fabrication change is authorized.
