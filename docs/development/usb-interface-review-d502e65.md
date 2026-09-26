<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Native USB-interface review: d502e65

Reviewed 2026-09-17. Result: **native ERC and complete XML connectivity passed; two drawing findings require correction**. This is not USB compliance, a complete power-system review, bench evidence or Gate A approval.

The owner supplied `usb-interface-review-d502e65.zip` and its terminal transcript after KiCad 10.0.6 ran on the clean `d502e652b234c658f98c1ac678e7e02680df07f8` checkout. The archive contains an eleven-page schematic PDF, ERC, XML, 41 symbol exports and 25 footprints in each raw view. AppleDouble metadata is excluded.

| Artifact | SHA-256 |
|---|---|
| ZIP | `36a24b7570836e9cabbe58421d2d34f3ec0dbc5d782e3ce8fadfe5118efb5f7b` |
| ERC | `74c7ac17606af3b795ed8ed4a5d22b07055ad64d19f6269e1a94a0331e640cf1` |
| XML | `0f8626a83b0f1994f5b6b8de37ed416a1ef849ccf25ce972bd3b7f35ef197fa7` |
| PDF | `700b07f93bcc6c56a01eb4464c1f416a5cfc143948b16d867cd563d2e6aaa4f7` |

The supplied ERC and XML were independently rerun through the repository checkers before the next circuit edit: **zero violations; 437 PCB items / 1,620 logical pin entries**. The earlier isolated USB data-net warnings are gone. Source flags still represent unfinished supply boundaries; zero ERC does not turn them into physical power sources.

The PDF was rendered. Inspection focused on the changed conditioning page, permission page and new USB-interface page, with enlarged connector, ESD and BC-detector views. Both new resistor-symbol SVGs were inspected. No new footprint was introduced. Earlier footprint audits remain applicable; no new independent dimensional audit is claimed here.

| Finding | Cause | Source correction |
|---|---|---|
| J1 value crosses its top body outline | Generator measured highest pin, ignoring the taller body | Include both rectangle corners in header clearance; raise reference/value 2.54 mm |
| U33 value crosses its top body outline | Same generator defect | Raise reference/value 2.54 mm |

The shared fix also increases U30's existing clearance by 1.27 mm. No pin, wire or label position changes on the USB-interface page. A geometry regression checks J1/U33 value baselines against their independently stated body dimensions. These are **source corrections awaiting the next native PDF**, not claimed native visual passes.

The next checkpoint combines those drawing corrections with the [logic-rail supervisor capture](../../hardware/coupon/rev-a/usb-supervision-capture.md). Input protection, charger actuation, complete current/transition budgets, remaining power circuits and independent review stay open.

## Follow-up native disposition

The [2bb0e08 evidence record](logic-supervisor-review-2bb0e08.md) accepts the supervisor-stage native ERC/XML and visual review and closes the USB symbol-heading findings. This does not close the remaining power-design or independent Gate A requirements.
