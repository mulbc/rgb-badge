<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# R36 ground escape and exact obsolete colour-branch retirement

Status: **unbuilt noncanonical routing study; fabrication prohibited**.

The saved derivative connects R36.2 (`ERJ2RKF1003X`, 100 kΩ ±1%,
ROW_SEL_14 pull-down) at (64.25, 7.25) mm to the existing In2 ground group.
A 0.15 mm rear lead reaches (64.10, 7.25) mm; three adjacent B–In4–In3–In2
microvias complete the escape. Native and physical-pad opens decrease
**217 → 216**, GND **24 → 23**. Every previous physical pad group, all colour
columns, R28/R29/R2 grounds, 483 placements and exact part/pad metadata survive.

## Replace the obstruction and retire only obsolete copper

The original In4 COL_06_G segment from (82.6, 7.25) to (61.9, 7.25) mm
blocks the ground stack. Local detours are blocked by anode/gate copper.
The preceding bounded global search reaches U1 OUTG6 pin 31 in 381,583
expansions, but leaves the old source escape dangling, producing 105 native
findings. Removing its via exposes the next obsolete track rather than curing
the entire branch. These intermediate candidates remain rejected.

This continuation follows full native DRC one step at a time, removing only
original COL_06_G items identified as dangling. Each removal preserves all
previous physical pad groups and 216 opens. Eighteen isolated cleanup steps
retire **seventeen In3 tracks and one In3/In4 via**; the final DRC returns to
the exact original 104-finding multiset. Together with the obstructing In4
segment, the increment retires **eighteen original tracks and one via**.
No component, pad or other original copper is removed. The retained per-step
inventory records each exact signature, DRC finding and report hash.

The new 72-track colour route is simplified using complete native straight-line
clearance tests, retaining every via and layer transition. Nine tracks remain;
new colour length decreases from **47.278 to 45.577 mm**. This is 1.701 mm less
than the unsimplified candidate, not a claim that it is shorter than the retired
source path. It includes one exact 0.826 mm In2 endpoint lead; the grid search
has no planar In2 steps. Zone refill preserves the previous ground/supply groups.
The longer replacement, return locality, inductance, settling and colour timing
remain unqualified and require engineering review.

Including its short ground lead, this increment adds **ten tracks / eleven
adjacent-layer microvias**. The cumulative plan has **944 tracks / 88 microvias**,
**15,505 total items**, eighteen joins and exactly **14,473 retained original
items** out of 14,494. Its three replaced original routes comprise **twenty
retired track segments / one retired via** in total. Track width/clearance
remain 0.20 mm; microvias remain 0.30/0.10 mm with adjacent layers only.

## Independent acceptance and limits

The replay pins the earlier two segment exceptions, the new integer retirement
list by digest and the exact obsolete via separately. The checker independently
pins every missing native signature and all added COL_06_G/GND/supply geometry.
Unexpected source removal or restoration is rejected. Thirty-one isolated native
guard methods include withdrawing R36 ground while proving prior escapes remain
connected, withdrawing the green replacement, and restoring each of the nineteen
newly retired original items individually. The other two original restoration
cases remain covered. All 256 LED checks, fresh 21-case schematic comparison and
source-only CI pass; two native generations are byte-identical.

Full KiCad 10.0.6 DRC retains exactly **104 intrinsic findings**, with no added
finding. GND/VLED/application-3.3-V/USB-3.3-V retain **23/14/7/4 opens**.
TP11, the transmit test-pad leg, six gate terminals and remaining power/control/
USB routing remain incomplete. No board was measured, no firmware or current
setting changed, and the actual VLED/decoder enable boundaries remain isolated.
R36.1 remains on ROW_SEL_14, and the driver/LED pad maps and manufacturer package
contracts are unchanged. No material circuit or component decision is introduced.
Canonical package/BOM reconciliation, current/return/decoupling, HDI/process,
fit/RF/thermal and independent Gate A remain open before any fabrication release.

[Increment and branch inventory](../../mechanical/review/native-control-r36-ground-escape-2026-10-23.json),
[current native checks](../../mechanical/review/native-control-check.json),
[current validation](../../mechanical/review/native-control-validation.json).
Repeat with `./tools/check-native-control.sh` and `./tools/check-coupon-study-contract.sh`.
Current PCB SHA-256: `6a2f61c07b647e727e1ed08daf87b3964365da2dca73504078d763aed88b72fa`.
