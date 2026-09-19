<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Type-C-only charging: functional simplification

2026-09-18. Implements the owner-approved [ADR 0013](../../../docs/decisions/0013-type-c-only-fixed-current-charging.md) source-policy simplification. Native review accepted at `12a134f`; not a complete power circuit or fabrication release.

## Removed from the captured circuit

- BQ24392 U30, ballast R72–R74, bypass C33–C35 and derived power flag #FLG06.
- Eleven permission gates and their bypass capacitors: U10, U12–U16, U18–U22.
- Three dual input buffers and bypass capacitors, with six obsolete input pull resistors and test pads.
- All BC1.2 and application charging-grant nets. No ESP/USB-stack grant can enable charging.

This removes **47 PCB items**. Reference numbers are not compacted for the retained parts; R62/R63 and TP22/TP23 now belong to the reduced VBUS_VALID/LOGIC_READY input set, so old netlist/pin-map assumptions must not be mixed with this revision.

The remaining permission gates are U11 (invert OUT1), U17 (AND VBUS_VALID, LOGIC_READY and CC_HIGH) and U23 (open-drain request). U24/U25 condition the four inputs; U34 and its six-part supervisor group are retained. The request/test net is now USB_CHARGE_REQ, not USB_HIGH_REQ. OUT2 remains diagnostic and has no grant path. The abstract checker rejects firmware/BC input arguments and exhausts all 16 stable detector/supply combinations; the physical-wire evaluator separately compares the captured gate topology to that contract.

## Data and power boundaries

USB data is now J1 → application-powered TS3USB31E → existing controller series resistors → ESP32. Connector ESD and CC detection are retained. The isolator remains OFF with the application; no BC detector is needed on the data path. D+/D− mapping and power-domain isolation are checked independently. This is not yet a signal-integrity or powered bench result.

The fixed current setting will use the audited 3.65k and 3.48k precision resistors permanently in parallel. The two resistors form one setting; there is no switch, ADG4612, leakage-sensitive boost path or firmware-selected limit. Their capture awaits the charger sheet. Existing input/charge ceilings and exact-pack prerequisites are unchanged.

The protected-input bridge, VBUS qualification and physical charger standby control remain open. USB_A/default sources do not charge; data while ON requires battery power if no supported source is present. Battery-absent/depleted recovery on unsupported sources is not guaranteed.

## Review scope

- Conditioning/permission: 27 items, 70 logical pins including two NCs.
- USB interface: 13 items, 62 logical pins including eleven NCs.
- Complete coupon: **396 items / 1,492 logical pins**, eleven pages.
- Library exports: 46 symbols / 27 footprints per raw view, unchanged. Historical candidate libraries are retained and are not selected merely by their presence.

Generators reproduce all three canonical sheets. Synthetic netlist fixtures are separately transcribed and do not count as native KiCad results. The combined native review should inspect all three changed USB pages and require zero ERC violations. No new native review is requested for individual component removals.

Host validation completed 2026-09-19: all 140 tests pass, including regeneration, independent gate evaluation, source fault injection and the separately transcribed full XML fixture. The fixture contains 396 items / 1,492 pins. `git diff --check` passes. The strict USB-closure check still rejects the explicitly unfinished power circuit. Native KiCad review remains pending.

Native cb81e86 stopped on isolated USB_OUT2: see the [finding and source correction](../../../docs/development/type-c-only-review-cb81e86.md). TP21 now probes conditioned OUT2; no components added. Seven targeted permission-capture tests pass, including the new regression and complete synthetic XML fault checks. Native ERC/PDF/XML review remains pending.

Native closure (2026-09-19): owner KiCad 10.0.6 at `12a134f` reports zero ERC violations and exports the complete 396-item / 1,492-pin XML. The uploaded XML was independently rerun through the repository checker; pages 9–11 passed first-author visual review. This closes the OUT2 finding and the combined simplification checkpoint. Earlier pending statements above describe preceding checkpoints. See [evidence](../../../docs/development/type-c-only-review-12a134f.md).
