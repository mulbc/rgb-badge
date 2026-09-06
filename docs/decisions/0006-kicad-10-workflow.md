<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0006: Target KiCad 10 stable

- Status: Accepted
- Date: 2026-09-06

## Context

The electronics have not yet been captured, so the project can choose its file-format baseline before any KiCad files are created. The owner develops on macOS and is willing to install the latest stable KiCad. A named version is still necessary because opening and saving a project with a newer major release can migrate files and prevent contributors using the earlier major release from editing them safely.

KiCad 10.0.6 is the current stable macOS release as of this decision. It was released on 2026-08-29 and supports macOS 12 and newer.

## Decision

- Create and initially save the coupon project with **KiCad 10.0.6**.
- Treat the latest validated `10.0.x` patch release as compatible. A patch update is a deliberate repository change and must pass the existing ERC, DRC and manufacturing-export checks before it becomes the new baseline.
- Do not use release candidates, testing builds or nightly builds for canonical project files.
- A move to KiCad 11 or another major release requires a new ADR, a dedicated migration commit and before/after ERC, DRC, BOM, placement and plot comparisons.
- Keep symbols, footprints and 3D models required by a hardware revision inside that revision's directory. Do not rely on a contributor's global personal libraries.
- Record the authoring and `kicad-cli` versions in each signed manufacturing release manifest.

## Consequences

- Contributors can reproduce checks with a known KiCad major and file format.
- The project may take bug-fix updates without silently accepting a major migration.
- KiCad source creation remains blocked until the exact component symbol pins and footprint pads have been checked against current manufacturer drawings.

## References

- [KiCad 10.0.6 release announcement](https://www.kicad.org/blog/2026/08/KiCad-10.0.6-Release/)
- [Official KiCad macOS download](https://www.kicad.org/download/macos/)
