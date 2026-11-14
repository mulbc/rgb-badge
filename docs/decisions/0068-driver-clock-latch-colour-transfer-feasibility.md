<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0068: Exact driver clock/latch colour-transfer feasibility

Date: 2026-10-30
Status: Bounded screen completed without a selected transfer.

The accepted 59-edge board leaves U1 LED_SCLK/LED_LAT/LED_GCLK open. A native
0.05 mm endpoint screen identifies the exact original COL_05_B In4 track,
(84.75, 8.90) to (77.95, 8.90) mm, 0.20 mm wide, at otherwise clear B/In4
microvia sites for clock/latch. These are finite observations, not an exhaustive
impossibility result. TLC59581RTQT SCLK/LAT/GCLK pins remain 28/27/29 under the
already reviewed TI TLC59581/82 Rev. A drawing; no pin, part or setting changes.

Permit an ignored replacement of only that exact original. Keep original In4
endpoints and all independently derived direct source-layer contacts. Transfer
only a local interval within x = 82.10–84.60 mm using adjacent In4/In3 or In4/B
microvias and full-width copper; bound vertical displacement to 1 mm and total
replacement length to original plus 2 mm. Preserve all other original/accepted
59-edge copper, groups, poses, zones and earlier exceptions. Keep 0.20 mm
clearance, 0.30/0.10 mm adjacent microvias and 0.50 mm copper-edge clearance.
Only the existing ADR 0047 digital-net feasibility scope may use 0.12 mm tracks,
with the unchanged 120 mm aggregate bound per net. Never narrow colour/power.

Canonical adoption requires an exact source/replacement/interface catalog,
frozen 59-edge retention, lower native/physical counts, unchanged full 104
findings, stable fills/replay, native/fault/source and original-orphan proofs.
Source engineering, current/thermal/timing/return/process/assembly review and
independent Gate A remain open. No fabrication or source retirement is selected
merely by authorizing this ignored screen.

## Screen result

The 7,752 enumerated In3/B doglegs yield zero complete other-net-clear
candidates, so none advances to refill or canonical adoption. Native via-site
inspection identifies existing COL_12_G and MODE_BOOT_N copper on In3; B sites
meet SCLK/LAT/SIN pads and retained LED_SIN/ROW_SEL_03 copper. All existing
interfaces and 0.20 mm spacing remain required. These finite choices do not
prove impossibility. See the [follow-on record](../development/led-routing-progress-59-follow-on-2026-10-30.md).
