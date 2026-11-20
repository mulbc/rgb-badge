<!-- SPDX-License-Identifier: Apache-2.0 -->

# Provisional board inventory

[ADR 0041](../../docs/decisions/0041-derived-coupon-pin-map.md) adds [Coupon Rev A's machine-readable U3 inventory](coupon-rev-a.json). It is **provisional, not frozen**, with `production_gpio_configuration_allowed: false`. It cannot authorize GPIO configuration, a driver, hardware arm or fabrication. KiCad source remains canonical; edit the schematic under the existing engineering rules, then regenerate this derived artifact after review.

The inventory covers 41 numbered module pins / 49 physical lands: 25 connected pins, 16 explicit no-connects, 36 GPIO identities and 20 assigned GPIOs. Three ground numbers include the nine same-numbered EPAD lands. Each entry retains the module number, manufacturer/library names, electrical type, GPIO, net/null, explicit NC flag, physical land multiplicity and strapping/Octal-PSRAM restrictions. Every unused pin remains explicitly represented; no NC is implicitly offered for reuse.

The generator calls the existing controller source tracer/library audit and consumes its validated connections. Source checking now returns that mapping to avoid duplicating schematic tracing. The manufacturer function/number/GPIO interpretation was rechecked against the module datasheet's top view and complete pin table. The reviewed PDF is version 1.8, SHA-256 `27d71971da07c280c6068d08c74720d1a25b8f20cf8494dc1765bdd28d40d435`, from the [manufacturer URL](https://documentation.espressif.com/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf); its bytes are not in Git. The inventory records this source identity and hashes all twenty canonical schematic files, the symbol library, module footprint and direct generation/checker sources. Source or metadata drift requires review and regeneration.

Check from the repository root:

```sh
python3 tools/check-board-pin-map.py
python3 -m unittest discover -s tools/tests -p test_board_pin_map.py -v
```

After source review, `python3 tools/check-board-pin-map.py --write` regenerates deterministic JSON. `--manifest PATH` writes/checks an alternate artifact. Default behavior is read-only. Duplicate keys, changed scalar types/metadata, reordered/missing/extra pins and noncanonical serialization fail checking. If a native check fails during `--write --netlist`, the prior artifact is preserved.

For an independent native comparison, first export the complete root schematic with KiCad 10, then pass that XML path through `--netlist`. The current local evidence uses:

```sh
python3 tools/check-board-pin-map.py --netlist hardware/coupon/rev-a/build/pin-map-review/coupon.xml
```

Native verification first applies the complete existing 497-item/1,814-pin circuit contract. It additionally checks U3 manufacturer/MPN/value/package/library/datasheet identity, each pin's function and electrical/NC type, and the exact request/decoder/candidate-output boundaries. `ROW_ENABLE_REQ_N` remains separate from actual `ROW_ENABLE_N`; candidate interlock outputs remain at their isolated test pads. Octal-PSRAM GPIO35/36/37 stay unconnected, native USB remains GPIO19/20, and strapping pins are identified without selecting target drive/pull behavior.

Eight test methods cover deterministic regeneration/CLI behavior and fault matrices for JSON, source and synthetic native XML, including USB swaps, explicit NCs, exact part identity, GPIO/strap/PSRAM flags, land counts, source hashes and display-boundary bypasses. Synthetic fixtures are not native KiCad evidence. CI checks the artifact and existing controller/library regressions from source-only checkout; it does not download a vendor PDF or run KiCad. The [local review record](../review/board-pin-map-source-check-2026-10-21.json) retains the separate fresh native XML/zero configured ERC result, tool versions, source hashes and raw evidence paths.

No symbol, footprint, circuit, PCB or current limit changed. The existing mixed-source PCB study still has unfinished routing and intrinsic DRC findings. Hardware defaults/arming, exact peripheral drivers, target timing/memory, independent review and an explicit pin-map freeze remain outstanding before production driver use or fabrication.
