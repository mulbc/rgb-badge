<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0266: Wider seeded sensor supply discovery

Date: 2026-11-20
Status: Accepted for bounded read-only route discovery.

ADR0265 exhausts6980 nodes/7019 Cu-blocked microvia candidates, reaching
the north and east study boundaries. Preserve its exact real seed and
complete gateway. Expand only the search region to x49..65/y9..21.5 mm,
with at most20 mm total real ordinary-width supply conductor and400000
expanded states; use a1.5 weighted heuristic. Keep at most one additional
supported B/In4 microvia with all native source Cu and hole checks.
This bound is geometry feasibility, not bypass/electrical acceptance.
Only actual main USB32 contact and filled USB33/22 opens preserving all
211 prior groups/retained Cu/no orphans can advance. Write no PCB.
All part/profile/current/return/bypass/thermal/process/stack/fit and Gate A
holds remain; fabrication is prohibited.
