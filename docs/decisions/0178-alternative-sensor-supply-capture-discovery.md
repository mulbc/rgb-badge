<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0178: Alternative supply capture at the exact sensor cohort

Date: 2026-11-16
Status: Accepted for read-only geometry discovery only.

The exact ADR0177 prototype restores hot/output paths in its first bounded
route order but leaves cold and USB supply unresolved. Route order refinement
is allowed within that same scope. Read-only also enumerate alternative VDD
neck/capture sites at the exact ADR0176 three-part poses, rather than retaining
only the first clear capture found by ADR0172. No part pose/cohort changes.

Test a 0.050 mm offset grid within 0.750 mm of actual U39 VDD pad 5. A straight
ordinary 0.20 mm B neck must pass all moved own foreign pads, retained foreign/
no-net copper and source edges. Screen supported 0.30/0.10 mm B/In4 captures,
full-board ADR0147 hole policy and optional aligned In3/In4 continuation.
Record whether higher access is clear. The previously sampled VDD neck and
capture are alternatives, not simultaneous additions; do not excuse any
original source copper or existing drill. Retain exact local thermal/bypass/
programming bounds and exact source profiles.

Write no PCB for this discovery. A new exact VDD alternative needs a separate
complete prototype decision before implementation; all hot/cold/output/ground/
supply and original 216 groups/interfaces must still be restored together.
Full native/physical/exact104/source/contact/hole/replay/inverse/orphan/fault/
visual gates precede adoption. All electrical/current/threshold/protection/NTC/
timer/default-off/part/HDI/stack/process/fit/Gate A and fabrication holds remain.
