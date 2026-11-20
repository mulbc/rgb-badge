<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0062: Exact local colour-layer transfer feasibility

Date: 2026-10-29
Status: Exact 61-edge candidate selected only after its complete acceptance gate.

The preceding accepted board has 62 opens. A 0.025 mm native local search from the
authorized U52.3 ground neck reaches 26,824 B.Cu cells but no legal adjacent
microvia or existing main-ground contact. Nearby via sites have one obstruction:
the original COL_10_R track from (83.75, 1.10) to (70.25, 1.10) mm on In4.Cu,
width 0.20 mm. This finite search is not an impossibility proof.

Permit an ignored trial that replaces only this exact original signature with
two retained In4 portions and one local, full-width layer excursion using adjacent-layer microvia stacks.
Keep both original endpoints and every original same-layer external contact.
Bound the transferred interval to 2 mm and aggregate replacement length to
the original plus 2 mm. Use only 0.20 mm tracks/clearance and 0.30/0.10 mm
adjacent microvias, with at most four adjacent pairs per transfer endpoint. Ground may use only the existing ADR 0051 U52.3 neck and
original-width routing. Preserve every other original and accepted copper item,
component pose, zone and completed physical pad group after refill.

Rechecked [TI TLC59581/82 Rev. A](https://www.ti.com/lit/ds/symlink/tlc59581.pdf)
and [SN74LVC1G08 Rev. AA](https://www.ti.com/lit/ds/symlink/sn74lvc1g08.pdf).
The unchanged TLC59581RTQT U1 pin 44 is OUTR10; COL_10_R carries a constant-current LED sink output.
Its width and all driver/LED settings remain fixed. U52 DSF pin 3 is ground;
the package and pin map stay fixed. This trial does not establish finished-copper
or microvia ampacity, return quality, transient behavior or manufacturability.

Canonical selection requires an exact independent retirement/interface/length
catalog, preservation of the entire 62-edge checkpoint, lower native and physical
counts, the unchanged full 104 findings, stable refills/replay, fault/source checks
and unchanged original-orphan restoration. Do not relax a prior freeze merely
because the replacement is connected end to end. Independent Gate A and all
electrical/process/fit and fabrication holds remain open.

## Exact selected candidate

The [61-edge continuation](../development/led-routing-progress-61-study-2026-10-29.md)
selects only the 1 mm original interval x = 70.30–71.30 mm, with a full-width
In3 dogleg through y = 1.60 mm and two In3/In4 microvias. Its aggregate
replacement is 14.5 mm versus 13.5 mm original. Both original In4 contacts
survive. U52.3 uses the exact 0.70 mm ADR 0051 ground neck, 0.65 mm of full-width
B.Cu routing and three adjacent microvias at (70.80, 1.15) mm to In2 ground.
The catalog, source-derived contacts, independent hard length/extent guards,
frozen 62-edge preservation, native/physical counts, unchanged full DRC,
refill/replay/source/fault and original-orphan checks record this selection.
No other transfer, stack experiment, component move or electrical setting is selected.
