<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Hardware

Editable KiCad electronics live here. Each revision is self-contained and must include project-local symbols, footprints and 3D models plus a README identifying its status and evidence.

The authoring baseline is KiCad 10.0.6 under [ADR 0006](../docs/decisions/0006-kicad-10-workflow.md). Use only validated stable `10.0.x` releases for canonical files; do not save them with a testing, nightly or newer major build.

Each revision will use this structure when capture begins:

```text
<revision>/
├── <project>.kicad_pro
├── <project>.kicad_sch
├── <project>.kicad_pcb
├── sym-lib-table
├── fp-lib-table
├── symbols/
├── footprints.pretty/
└── 3dmodels/
```

Before committing an exact part, compare symbol pin numbers, exposed pads, footprint geometry, courtyard, polarity/orientation marks and tape orientation with the current manufacturer documentation. Imported library models are starting material, not evidence of correctness.

No hardware design has been fabricated yet.
