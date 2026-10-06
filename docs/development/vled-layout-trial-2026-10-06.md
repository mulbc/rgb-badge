<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Unrouted VLED local placement check, 2026-10-06

The source is the [unlinked converter schematic](../../hardware/coupon/rev-a/staging/vled-converter.kicad_sch) and its [separate local KiCad placement](../../hardware/coupon/rev-a/staging/vled-layout-trial.kicad_pcb). This is **not** the coupon or final-board PCB. No board exists and no hardware measurement or firmware revision applies.

KiCad's bundled Python 3.9 regenerated the placement deterministically from the current 13-part / 39-logical-pin native XML netlist, exact project-local footprints and the [fit-screen coordinates](../../mechanical/review/fit-trial.json). A saved-board round trip checked all thirteen references, footprint library IDs, orientations, centres and numbered pad nets. Two consecutive generations had the same SHA-256, `5396a23ecd8321d44ec5a78d6362348a95c6895f1506655683edb55a4edfa1fa`. KiCad CLI 10.0.6 loaded and plotted the actual copper pads and courtyards; the output was visually inspected. The local board has no tracks, vias or copper zones.

Standalone `kicad-cli pcb drc` aborted with exit 134 before creating a report. The same command also aborted on a separate one-footprint control board generated with pcbnew, so this check is unavailable in the current Mac environment; it is **not** a DRC pass or evidence of a clean board. The root coupon schematic still has zero configured ERC violations and 410 components / 1,537 logical pins. Those are different checks.

Open findings: place and route the switching/input/output loops and control-ground feedback according to [TI's TPS63020 layout guidance](https://www.ti.com/lit/ds/symlink/tps63020.pdf); check copper clearance, return paths, heat and component height; include the other final-board circuits; resolve the baseline INA232 fit conflict; then run a working full-board DRC and independent Gate A review before fabrication.
