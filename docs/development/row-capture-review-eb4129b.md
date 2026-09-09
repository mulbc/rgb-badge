<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Row-selector circuit review at eb4129b

Status: native first-author ERC, connectivity and drawing review complete; independent Gate A review pending

## Evidence

The owner ran KiCad 10.0.6 on macOS arm64 from branch `coupon-row-capture-rev-a` at source commit `eb4129b117142f8979adb8be44264a0ec82050ff` and uploaded `row-capture-review-eb4129b.zip` on 2026-09-08. The transcript reports successful controlled-library and source checks, all symbol and footprint exports, zero ERC violations, complete native XML validation, a seven-page schematic PDF export and no output from `git status --short`.

| Evidence | SHA-256 |
|---|---|
| Uploaded ZIP | `d26eb62500418cf9943e62b46b09fd9e2967e0bcf9f6146d06823499746c6512` |
| `coupon-erc.rpt` | `8f6438f43c8466c301944764039066eff10a9b353b583876e0c921ca5c6dde0b` |
| `coupon-matrix.xml` | `068e699611d807e421af758c25803a664275dd9218e35fe2de850f1bbd6f9c12` |
| `coupon-schematic.pdf` | `2011cd03d250b295ef12950e7e0947d02254d0032ed028f6ca22be411b577c87` |

The archive contains macOS AppleDouble `._` metadata entries. Those packaging artefacts were ignored; the corresponding KiCad outputs above were extracted and checked directly.

## Electrical and visual findings

The ERC report contains **0 errors, 0 warnings and 0 ERC messages**. Its four ignored categories are unchanged: global-label uniqueness, four-way junctions, SPICE models and footprint filters. The complete checker was rerun against the uploaded XML and passed exactly 335 PCB items and 1,290 physical pins across the matrix, TLC59581 support and row selectors.

All seven PDF pages were rendered with Poppler and inspected:

- The root page contains six child sheets, current scope text and filenames without border or title-block collisions.
- The four matrix pages retain all 64 LEDs each, orderly reference/net labels and current `driver/rows captured; controller and power pending` title-block notes.
- The TLC59581 page remains readable and retains its previously accepted output, current-reference, default, test-point and draft-supply connections.
- The row page shows U2 with C2, R38-R42 and all 16 decoded outputs. All sixteen P/N-MOSFET stages are present in rows 00-15 with a consistent one-to-one reference pattern.
- Each visible stage maps the P-MOSFET source to VLED, drain to the matching `ROW_nn_A`, and gate to the matching `ROW_GATE_nn`; the 1 kOhm pull-up and N-MOSF drain share that gate net. Each N-MOSF source returns to GND and its gate uses the matching `ROW_SEL_nn` plus 100 kOhm pull-down.
- Notes, fields and title blocks do not obscure a required connection. Page 7 is dense but unambiguous at full resolution.

## Disposition and limits

This run closes the first-author native gate for the row-selector circuit and makes the increment eligible to merge. The acceptance update changes documentation only; it does not alter the KiCad sources, project libraries or validation tools checked at `eb4129b`, so no additional owner rerun is required for this record.

This is not a fabrication release. The draft VLED flag is not a power source or startup interlock. Independent Gate A must still review the complete schematic and preliminary layout, the IPC-derived decoder land pattern and the bounded 3.3 V use of `2N7002K-7`. Gate B must measure row overlap, edge timing, anode discharge, ghosting and the actual N-MOSF drain-low voltage. The controller and real power circuits remain to be captured.
