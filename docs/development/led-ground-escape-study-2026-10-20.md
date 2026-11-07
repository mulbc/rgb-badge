<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Routed ground escapes on the combined row-control board

Status: **unqualified geometry study with full native DRC evidence**. KiCad 10.0.6 reports exactly the original 104 intrinsic footprint-clearance findings, with no added finding. No fabrication release or canonical schematic/BOM change follows from this study.

The [generator](../../tools/generate-ground-escape-trial.py) starts from the [combined row-control derivative](led-row-combined-partial-study-2026-10-20.md), preserves every existing track, pad, footprint placement and non-ground pad cluster, and adds 900 GND tracks/vias plus a solid In2.Cu GND pour. It searches routed escapes from the rear ground pads through B.Cu, In4.Cu and In3.Cu to In2.Cu, rather than forcing a direct via stack through occupied inner copper. The 0.05 mm search grid, 0.20 mm traces/clearance and provisional adjacent-layer 0.30/0.10 mm microvias retain the earlier study assumptions. Via cost and planar-step cost are equal in this short-path breadth-first search; the result is not optimized for HDI cost or current return quality.

KiCad 10.0.6 native connectivity reports **383 open edges**, down from 527. GND falls from **188 to 44** open edges; the other nets retain their original pad clusters. Of 195 rear ground pads searched, 158 get an escape; 37 do not. Some pads were already connected locally, so routed-pad count is not the open-edge reduction. The pour has **six copper polygons**, totalling **2886.218 mm²**. It is not a single completed ground network. All sixteen anode rows, 48 complete colour channels, sixteen gate ties, sixteen decoder selects, sixteen select-pulldown signal pads and the seven previously joined gate pullups retain their source connectivity.

Evidence:

- [Generation manifest](../../mechanical/review/ground-escape-trial.json): source/output SHA-256, KiCad version, all pad attempts and search counts, copper counts and fill area.
- [Saved-board check](../../tools/check-ground-escape-trial.py) and [recorded result](../../mechanical/review/ground-escape-check.json): 483 unchanged footprint placements/pad assignments, all source copper retained, unchanged non-ground pad clusters, 900 ground-only additions and zero added-copper versus foreign-pad/track/via conflicts in a native effective-shape screen at 0.20 mm clearance (0.00001 mm equality tolerance).
- [Native per-net report](../../mechanical/review/ground-escape-open-nets.json): disconnected pad clusters reconcile with all 383 native open edges. Leading unresolved nets are +3V3_APP (46), GND (44), VLED (41), +3V3_USB (32) and +SYS_APP_IN_DRAFT (12).
- The existing LED-placement checker passes all 256 exact placements, rotations, pad maps and nets. A second full generation yields the identical board SHA-256 `7331ede6842cc438dc01e813948966b9a9e0ee0e414cfdc879fe7cfabbe48f30`.

## Full DRC acceptance and host execution requirement

The initial sandboxed KiCad CLI run exited 134 without JSON for both source and derivative; the Python DRC path also failed. The [historical crash summary](../../mechanical/review/ground-escape-drc-blocker.json) records a macOS desktop registration failure. Running the existing acceptance script with desktop access on 2026-10-20 completed successfully: **104 unchanged intrinsic findings and 383 open edges**. This resolves the execution blocker; it does not clear the existing footprint findings or qualify fabrication. The [retained native DRC JSON](led-ground-escape-drc-2026-10-20.json) has SHA-256 `9b7d95add7ddf6fb4e27dc9ce6f5549683b06a0f7403d1cfb16ae92daa9f16d9`. The saved-board, native shape and all 256 LED checks passed in the same acceptance run. No board source changed during acceptance.

Run the complete acceptance check from a normal desktop terminal at the repository root:

```sh
./tools/check-ground-escape.sh
```

This writes raw JSON/check evidence under the ignored coupon build directory and requires exactly the original 104 intrinsic findings, together with the saved-board and LED checks. In a sandbox that prevents macOS desktop registration, run the same command with desktop access; do not reinterpret a host crash as a DRC result. This run establishes a DRC-checked study baseline, with the 104 existing findings still unresolved; it is not a release acceptance. The structural/shape-only check can be repeated separately with KiCad's bundled Python and `tools/check-ground-escape-trial.py`.

## Remaining work

Join the six ground regions and remaining 44 GND edges with explicit return-current/thermal review, coordinate the nine blocked gate pullups, and route the remaining supplies/controls. The manifest identifies the blocked pads and coordinates, including eight row-pair source pads and several select-pulldown grounds.

The broad pour has no antenna/return-current, converter loop, EMI, thermal or current-capacity qualification. The stacked microvia process, row-pair selection and mask/paste, canonical net synchronization, enclosure/battery/RF fit, interlock qualification and independent Gate A remain open. This is an unbuilt source study with no firmware, bench setup or measured hardware result.
