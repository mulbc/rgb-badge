<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Controller circuit review at d56e1aa

Status: native first-author ERC, connectivity, footprint and drawing review complete; independent Gate A review pending

## Evidence

The owner ran KiCad 10.0.6 on macOS arm64 from branch `coupon-controller-rev-a` at source commit `d56e1aa4456b11ac83e9887665534cce7ad7c430` and uploaded `controller-review-d56e1aa.zip` on 2026-09-09. The transcript reports successful controlled-library and source checks, all symbol and footprint exports, the strictly accepted temporary USB-boundary warning pair, complete native XML validation, an eight-page schematic PDF export and no output from `git status --short`.

| Evidence | SHA-256 |
|---|---|
| Uploaded ZIP | `d16f0f1faf0c998873659eed2e2d93efb62e292e115ec841c7d1479863584f39` |
| Terminal transcript | `e84a33bb8fb201796b3549bbd353e9375d4248da0bdef861266f61de3fef4a43` |
| `coupon-erc.rpt` | `8cb135c017079f332a347738728ce1035eb38ea4aa7c7647acc8438e6f953d62` |
| `coupon-matrix.xml` | `b1a3b3e8fabd4b05cea8dfaab13c8bf3eee4ec515ee855e667b4fe3f5d32cdd7` |
| `coupon-schematic.pdf` | `ee95e156599eb3a4c219a4ec703e9d67e1da73d7dc2e7d6a4b27f5d31bc8a1a8` |

The archive contains macOS AppleDouble `._` metadata entries. Those packaging artefacts were ignored; the corresponding KiCad outputs above were extracted and checked directly.

## Electrical and visual findings

The ERC report contains **0 errors and 2 warnings**. Both warnings are the exact temporary `USB_D-` and `USB_D+` isolated global-label boundary pair documented by the controller capture; the strict report checker accepted that complete pair and would reject a partial pair or any other message. The complete checker was rerun against the uploaded XML and passed exactly 356 PCB items and 1,360 logical pins across the matrix, TLC59581 support, row selectors and controller. KiCad's 18 one-node `unconnected-(...)` nets correspond exactly to U3's 18 explicit no-connect markers.

All eight PDF pages were rendered with Poppler and inspected:

- The root page contains seven child sheets, current scope text and filenames without border or title-block collisions.
- The four matrix pages retain all 64 LEDs each, orderly references and readable row/colour labels.
- The TLC59581 and row-selector pages retain the previously reviewed circuits without visible connection or legibility regressions.
- Controller page 8 is legible at full resolution. U3 is the exact `ESP32-S3-WROOM-1U-N16R8`; GPIO35–37 and every other unused pad have visible no-connect marks.
- GPIO0 reaches `MODE_BOOT_N`, R44, SW1 and TP3. `ESP_EN` reaches R43, C5 and TP2. No capacitor is present on GPIO0.
- GPIO19/20 reach `USB_DN_MCU` / `USB_DP_MCU`; R45/R46 independently bridge those nets to `USB_D-` / `USB_D+`. R47 independently bridges `UART0_TX_RAW` to `UART0_TX`.
- TP2–TP12 are present and readable for EN, mode/boot, UART, GCLK, row enable, 3.3 V, ground, display enable and system I2C.
- The fabrication/copper/paste views show 40 distinct module perimeter lands, nine separate same-numbered pad-41 lands, two pad-1 and two pad-2 switch contacts, and the two 0603 capacitor lands.

The visual pass also found stale pre-controller annotations on older pages: matrix title blocks say controller is pending, the driver page says its GPIO assignment is open, and the row title block says controller is pending. These notes do not change electrical interpretation and are non-blocking for this isolated increment. They must be corrected by the power/input increment and verified in that increment's native PDF before its merge.

## Disposition and limits

This run closes the first-author native gate for the controller circuit and makes the increment eligible to merge. The acceptance update changes documentation only; it does not alter the KiCad sources, project libraries or validation tools checked at `d56e1aa`, so no additional owner rerun is required for this record.

This is not a fabrication release. USB-C, ESD, charging, gauging, switched regulators and the hardware VLED interlock are still absent. The two USB labels remain intentional boundaries, not completed data paths. Independent Gate A must review the complete schematic and preliminary layout; Gate B must measure reset timing, USB enumeration, BLE range/current, row timing and display-safe startup behaviour.
