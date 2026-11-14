<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0031: Separate the controller row request from decoder enable

Date: 2026-10-11. Status: accepted for provisional source capture; hardware display interlock remains absent.

Rename ESP32-S3 U3 pad 12 (GPIO8) and its observation pad TP7 to `ROW_ENABLE_REQ_N`. Retain `ROW_ENABLE_N` only at U2 pin 23 (active-low E) and its R42 100 kΩ pull-up to `+3V3_APP`. The two nets remain intentionally disconnected until an independently reviewed hardware gate is captured. With the application rail valid and the gate absent, R42 holds decoder E high and no row is selected. The VLED converter EN also remains tied only to its 100 kΩ pull-down under ADR 0028.

This source step removes the present direct GPIO-to-decoder path that would let a firmware glitch select a row or create contention with a future hardware inhibit. It establishes the two sides of the proposed `ROW_ENABLE_N = ROW_ENABLE_REQ_N OR NOT ROW_ARM` interface, without choosing or claiming a working implementation of `ROW_ARM`. The requested functional behavior in PWR-004 and DSP-006 is unchanged. No LED operation is possible from this capture alone.

Validate exact source equivalence, pin-net separation in native XML, zero configured full-project ERC violations and review of both changed schematic pages. Before enabling display operation, select the exact reset-dominant arm, application-rail supervision, programming inhibit, watchdog/fault handling and VLED readiness/decay behavior. Check all pin/land identities and transitions, then perform independent Gate A review and hardware measurements. Native continuity and a pull-up are not evidence of safe power ramps or a finished board.

References: [display interlock interface](../design/display-interlock-interface-2026-10-05.md), [ADR 0028](0028-root-link-dark-vled-converter.md), [row capture](../../hardware/coupon/rev-a/row-capture.md).
