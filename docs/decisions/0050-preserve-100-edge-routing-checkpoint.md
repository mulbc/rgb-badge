<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0050: Preserve the accepted 100-edge routing checkpoint

Date: 2026-10-26
Status: Accepted for an unqualified routing continuation toward 50 opens.

The 100-edge checkpoint at commit 91090c8 passes independent physical-pad counts, exact source-copper retention, unchanged 104 intrinsic DRC findings and the three orphan-via restoration proof. Freeze its integer plan and protect every selected copper item, all four added power-zone definitions and every completed physical pad group, in addition to the earlier 150/215-edge contracts. No new orphan-via retirement is selected by this decision.

Further original-width additive routing and exact R/C localization may proceed under ADR 0045, with R45/R46 and other component classes fixed. Preserve exact parts, numbered nets, metadata and relative pad geometry, the 0.20 mm track/clearance floor, 0.30/0.10 mm adjacent microvias, 0.10 mm annular floor, five original zones and sensitive-setting 5 mm limit. Reject native net propagation or any route that splits a completed group. Require actual lower native and independent physical-pad counts after refill and exactly the original 104 DRC findings. Pin accepted additions/poses and replay the full selected plan independently.

This does not approve new widths, display-track retirement, current limits, enable connections, hardware behavior or fabrication. Supply/bypass/return, current/thermal/voltage-drop/SI/process/RF/fit qualification and independent Gate A remain open. Record actual progress without claiming the 50-edge target until it is independently verified.
