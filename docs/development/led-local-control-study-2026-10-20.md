<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Local control routing on the combined coupon study

Status: **unbuilt source geometry with full native DRC evidence**. This is the latest checked derivative of the combined row-control/ground-return board. It joins ten additional connections across eight control nets and reduces full native open edges from **364 to 354**. Full KiCad 10.0.6 DRC retains **exactly the same 104 intrinsic footprint-clearance findings**, with no added finding. Those existing findings remain unresolved; this is not a clean fabrication DRC result.

## Changes

The [generator](../../tools/generate-local-control-trial.py) starts from the [row-14 local-bias derivative](led-row14-bias-study-2026-10-20.md). It preserves all 483 footprints, their exact pad assignments and every source track/via. A deterministic six-layer search considers 23 named low-speed control nets, with 0.05 mm cells, 0.20 mm tracks/clearance and the existing provisional 0.30/0.10 mm adjacent-layer microvias. Shorter physical net spans are attempted first; each search is capped at 200,000 expanded nodes. New copper comprises **383 segments and 14 microvias**, all on the eight nets below.

| Net | Source opens | Derivative opens |
|---|---:|---:|
| ROW_REQUEST | 1 | 0 |
| USB_LOGIC_READY | 1 | 0 |
| USB_VBUS_VALID | 1 | 0 |
| USB_OUT2 | 1 | 0 |
| TEMP_OK | 3 | 2 |
| ARM_LATCH | 2 | 0 |
| VLED_WINDOW_OK | 3 | 1 |
| USB_CHARGE_REQ | 3 | 2 |

The search does not select supply, analog feedback, current-setting, USB differential or display-clock nets. These physical joins preserve the existing source topology; they do not qualify the USB or display-interlock state machines. The candidate display outputs remain on their existing isolated nets; no real converter-enable or decoder-enable net is substituted.

Ground zones are refilled around the new routes. Their filled polygons can change; the acceptance check requires every existing connected pad cluster, including GND, to remain intact. It therefore checks actual return connectivity rather than assuming that unchanged track objects imply unchanged poured returns.

## Evidence and reproduction

- [Generation manifest](../../mechanical/review/local-control-trial.json): source/output SHA-256, allowed nets, per-pad success/search counts, copper count and native version.
- [Saved-board checker](../../tools/check-local-control-trial.py) and [recorded result](../../mechanical/review/local-control-check.json): all placements/pad maps and original tracks/vias retained; no existing pad cluster split; only the eight intended nets acquire merged pad clusters; every one of ten claimed joins reaches its actual native anchor cluster. GND remains at 27 opens.
- [Full native DRC JSON](led-local-control-drc-2026-10-20.json): exactly the source's full normalized 104-finding set, not just an equal count. The native unconnected total is 354.
- [Per-net report](../../mechanical/review/local-control-open-nets.json): pad-cluster and native totals both reconcile to 354. All 256 LED placements, rotations, pad maps and nets pass the separate native checker.
- A second complete generation is byte-identical: board SHA-256 `7def02820ad488304c6a83479d233b45d1fd738f6b0239af4bff524c76caf5c6`.

Run `./tools/check-local-control.sh` from the repository root for the complete saved-board acceptance check. It runs native DRC, structural/connectivity checks and LED checks, writing raw output under the ignored coupon build directory. Use desktop access if macOS registration fails in a sandbox. Generate with KiCad's bundled Python and `tools/generate-local-control-trial.py`; compare hashes before accepting a changed output.

The source chain is combined row-control → ground escapes → ground returns → row-14 bias → local controls. The resulting board retains all 48 complete colour channels, sixteen anode rows, sixteen local gate ties, sixteen complete decoder selects and select-pulldown signal pads, eight connected gate pullups, and all prior ground pad clusters.

## Remaining work

Leading unresolved nets are +3V3_APP (46), VLED (40), +3V3_USB (32), GND (27) and +SYS_APP_IN_DRAFT (12): **157 of 354** opens. Eight gate pullups also remain incomplete. The per-pad manifest identifies blocked local controls; exhausting this bounded search does not prove a path impossible. Coordinate placement and escape reservations rather than repeatedly extending the same search limit.

This geometry has no timing, startup/brownout, return-current, EMI/RF, copper-current or thermal qualification. It uses an unselected row-pair package and provisional HDI process; mask/paste, canonical schematic/BOM synchronization, sensor/pack/case fit and independent Gate A remain open. The new control routes clear parts of the ground pours; connectivity preservation does not establish their electrical return quality. No hardware revision, firmware revision, bench setup or measured result exists for this study. It is never fabrication source.

Manufacturer-source access note: reopening the onsemi `NTLJD3119C/D` manufacturer PDF URL returned HTTP 403 in this session. No retrieval workaround or alternate source was attempted. Existing audited study pins/lands were retained without library edits. The owner subsequently supplied the Rev. 6 PDF on 2026-10-20. The [owner-source recheck](../../hardware/coupon/rev-a/dual-row-package-library-audit.md#owner-supplied-source-recheck-2026-10-20) records its separate SHA-256 and confirms the relevant pin/package drawings. Source access is now resolved; package/process adoption and independent review remain open.
