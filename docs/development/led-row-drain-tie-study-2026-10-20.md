<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Both physical row-drain lands joined

Status: **unbuilt geometry study with full native DRC evidence**. This is the latest checked combined routing board. Sixteen short local drain ties reduce native opens from **262 to 246**, retaining exactly the same **104 intrinsic footprint-clearance findings**. No additional DRC finding is introduced; the existing findings still require disposition before fabrication.

## Finding and source change

Each onsemi candidate `NTLJD3119CTBG` footprint has two physical P-drain lands numbered `3`: a perimeter terminal and the exposed drain island. The supplied manufacturer top view identifies both as D2; [the source audit](../../hardware/coupon/rev-a/dual-row-package-library-audit.md#owner-supplied-source-recheck-2026-10-20) records the exact source identity. Both already have the same schematic net. This work does not select the package or change any pin map.

In the [supply-distribution source](led-supply-distribution-study-2026-10-20.md), each complete LED row reaches the perimeter drain land, while its exposed drain island is a separate native PCB cluster. For example, PAIR01's perimeter pad 3 belongs to a **17-physical-pad** cluster (sixteen LEDs plus that land), and its other pad 3 is a **one-pad** cluster. These account for the sixteen remaining `ROW_00_A`…`ROW_15_A` opens; they are not extra test pads. Earlier ref/pin-pair row assertions could not distinguish the two lands because both share the same reference and pad number.

The [generator](../../tools/generate-row-drain-tie-trial.py) preserves every footprint/pad assignment and all existing tracks/vias, adding one 0.20 mm B.Cu track between the two pad-3 centres on each pair. It then refills the existing ground/supply zones. The [saved board](../../hardware/coupon/rev-a/staging/led-row-drain-tie-trial-114mm.kicad_pcb) has 14,195 tracks/vias and 483 unchanged footprints. No current setting, source enable, firmware, library or canonical schematic/BOM changes.

## Checks and evidence

The [new checker](../../tools/check-row-drain-tie-trial.py) uses reference, pad number **and physical position**, requiring both physical drains and all sixteen LED anodes to form exactly one **18-pad** cluster per row. Every other pad cluster, including all colour channels, gate/select/control nets, ground returns and the three supply stages, must remain exactly unchanged. All source tracks/vias are retained; the sixteen additions are limited to the intended row nets.

A negative regression check removes the row-00 tie from an in-memory copy and rebuilds native connectivity. The physical-row guard rejects it as required; no saved source file is modified by this test. This prevents an isolated duplicate-numbered land from passing as a complete row again.

Evidence:

- [Manifest](../../mechanical/review/row-drain-tie-trial.json): exact source/output hashes, native version and all sixteen route endpoints.
- [Acceptance result](../../mechanical/review/row-drain-tie-check.json): sixteen joined rows, eighteen physical anode pads per row, preserved prior clusters and successful missing-tie rejection.
- [Full native DRC](led-row-drain-tie-drc-2026-10-20.json): KiCad 10.0.6, the same full normalized 104-finding set as the input.
- [Per-net report](../../mechanical/review/row-drain-tie-open-nets.json): full native and pad-cluster counts both 246; no row-anode open remains. GND remains at 27 opens, VLED 15, +3V3_APP 7 and +3V3_USB 4.
- All 256 exact LED placements/rotations/pad maps/nets pass. A second full generation is byte-identical: `c668d3e58ba2f66549c0378ee541acb6622769c686b04d2d9bb9b030dab12efe`.

Run `./tools/check-row-drain-tie.sh` from the repository root for full acceptance, including native DRC, the physical-pad mutation check and LED placement checks. Generate with KiCad's bundled Python and `tools/generate-row-drain-tie-trial.py`. Native DRC may require desktop access on macOS.

## Remaining work

The leading unresolved net is GND at 27 opens. Supply distribution is incomplete; eight gate pullups and many controls remain open. A separate bounded probe using native 0.20 mm via-shape clearance rather than only the conservative raster screen found no added join for those eight gates at the current placements within 200,000 expanded nodes per attempt. It is not adopted and does not prove those gates impossible. Coordinate placement, local escapes and select routing rather than assuming that a smaller search guard alone resolves them.

These are native file/connectivity checks, not bench measurements. The 0.20 mm drain ties have no assigned current rating. Hot-row/overlap/fault current, heat flow, converter capacitor locality and loops, return quality, default-blanking/interlock behavior, fine-pitch mask/paste, HDI manufacturing, canonical package/net synchronization, sensor/pack/case/RF fit and independent Gate A remain open. No hardware revision, firmware revision, bench setup or measured result exists. This board is never fabrication source.
