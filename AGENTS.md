<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Contributor and AI-agent instructions

These instructions apply to the complete repository.

## Read before changing the project

1. Read `CONTEXT.md`.
2. Read `docs/requirements.md`.
3. Read the relevant records under `docs/decisions/`.
4. Read the current revision README and every cited component datasheet.

## Truth and traceability

- Never describe an unbuilt board as working, tested, safe or production-ready.
- Label calculations, simulations, bench measurements and assumptions distinctly.
- Every measurement must identify hardware revision, firmware revision, setup and raw evidence location.
- Use exact manufacturer part numbers in the BOM. Never accept or make silent substitutions.
- Check every symbol pin number, footprint pad, polarity mark and package drawing against the current manufacturer datasheet.
- Record a material design change in an ADR and update affected requirements before implementation.

## Electrical safety

- Do not raise USB input, battery-charge, LED or regulator current limits without the exact source/cell limits and a reviewed calculation.
- Keep application firmware out of the fail-safe USB input-current limit.
- Default VLED and every LED row to disabled during boot, reset and programming.
- Do not bypass cell protection, NTC qualification, charger safety timers or hardware current limits.
- Do not release fabrication files until the required independent review is recorded.

## Source conventions

- KiCad source files are canonical for electronics; keep symbols, footprints and 3D models project-local.
- CadQuery source is canonical for the enclosure; STEP/STL files are reviewed release outputs.
- Production firmware uses ESP-IDF and native C/C++. Host-side tools may use Python.
- Prefer deterministic generation, tests and machine-readable manifests over manual release steps.
- Do not commit local KiCad backups, firmware build output or unsigned manufacturing output.

## Licensing

- `hardware/`, `mechanical/`, `manufacturing/` and hardware-oriented `docs/` use `CERN-OHL-S-2.0`.
- `firmware/` and `tools/` use `Apache-2.0`.
- New text/source files should carry the appropriate SPDX identifier where the format permits it.
