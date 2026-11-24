<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0272: Native boundary discovery for fixed pair supplies

Date: 2026-11-20
Status: Accepted for bounded read-only geometry discovery.

ADR0271 fixed PAIR05/09 graphs exhaust166/145 states with no supported
capture; PAIR07 exhausts18831 states without a full join. Keep selected
source22 immutable. Inspect continuous conservative B routing space for
PAIR05/09 using native source pad/track/via polygons expanded by0.30025 mm
(new0.10 mm trace radius+unchanged0.20 mm clearance+0.00025 numerical
guard), native ERROR_OUTSIDE polygonization with0.00025 mm maximum error.
Within x72.5..77.5 and actual supply-pad y+/-2.5 mm, subtract all foreign-
net B conductors from the rectangle. Identify the actual source-point
component, its boundaries and source-backed blockers. This is bounded
geometry, not an exact global no-path proof or process qualification.
Any later boundary-derived conductor must be real ordinary0.20 mm Cu,
individually native-screened and source/group/Cu preserved after fill.
Waypoints are not electrical witnesses. No PCB is written or selected.
All physical/part/current/protection/qualification/Gate A holds remain;
fabrication is prohibited.
