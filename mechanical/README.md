<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Mechanical design

The enclosure will be parameterized in CadQuery and released as source plus reviewed STEP/STL exports. It must enforce the finished envelope, protect the pouch cell, reserve the RF zone and support a replaceable development diffuser.

Do not freeze the 900 mAh cell or final enclosure until a complete PCB STEP assembly proves the thickness stack without pouch compression.

The [2026-09-26 envelope screen](envelope-screen-2026-09-26.md) quantifies display width and a trial 11 mm thickness stack. It flags conflicting manufacturer length figures for the 900 mAh *bare* cell. Under [ADR 0019](../docs/decisions/0019-board-mounted-battery-temperature-sensing.md), a protected two-wire pack with a battery-facing PCB NTC is now allowed for testing; no final pack or physical fit is selected.

The [USB/LED edge screen](usb-led-edge-screen-2026-09-26.md) finds a nominal 0.025 mm copper intrusion into the USB cutout guide with the centred final LED grid and 106 mm board, and flags the connector's 0.80 mm board recommendation against the historical 1.0 mm plan. Actual placement and stack-up remain to be qualified.

The [preliminary front/rear placement study](preliminary-placement-screen-2026-09-26.md) additionally checks exact LED/USB courtyards. A centred grid conflicts with the USB courtyard; an illustrative 1.775 mm left shift avoids *bounding-box* intersections but does not establish manufacturability. The trial rear placement omits many components and the final battery.

The [2026-10-06 board/battery fit trial](fit-trial-2026-10-06.md) adds a grouped rear footprint plan and an 11 mm section with a separate LP503055 pack that still needs support above the board. All 32 row switches and 77 conditional under-pack 0402 candidates have nonoverlapping XY trial positions, but eight captured coupon parts and all remaining power/connector/RF/mounting needs are unplaced. A 0.55 mm 0402 height example leaves only 0.25 mm nominal case margin before assembly tolerances. No physical mount, complete PCB or DRC has been validated.
