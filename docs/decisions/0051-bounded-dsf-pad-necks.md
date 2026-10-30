<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0051: Bounded DSF pad-neck routing study

Date: 2026-10-26
Status: Accepted for explicitly enumerated, independently verified unqualified pad escapes only.

## Geometry and reviewed sources

Original-width short and native-grid searches leave the 100-edge board unchanged. U48/U52 use exact SN74LVC1G04DSFR/SN74LVC1G08DSFR. TI's current [inverter Rev. AF](https://www.ti.com/lit/ds/symlink/sn74lvc1g04.pdf), [AND gate Rev. AA](https://www.ti.com/lit/ds/symlink/sn74lvc1g08.pdf), and the existing package audit were read on 2026-10-26. Their DSF0006A 4220597/B land drawing specifies 0.60 × 0.17 mm pads at 0.35 mm pitch, matching the unchanged project footprint. A centred 0.20 mm track gives a calculated 0.165 mm neighbour clearance; 0.12 mm gives 0.205 mm. The intrinsic pad gaps remain recorded findings. NC pins remain unconnected.

## Decision

Permit only enumerated straight 0.12 mm B.Cu necks from the centres of U48 pins 2/3/4/6 and U52 pins 1/2/3/4/6, horizontally outward, with length 0.50–0.70 mm. Each selected neck must match the exact fixed pad position and numbered net. These are individual IC pin escapes, including local VDD/GND where selected, never narrowed supply distribution. The independent integer checker must reject any other narrow track, wrong pin/net/layer/direction, bent or extended neck. Permit at most one neck per selected pin. Retain all accepted 100-edge copper, poses except separately audited R/C moves, zone definitions and completed physical pad groups under ADR 0050.

Set the absolute project track floor to 0.12 mm only when necks are selected. Native custom rules retain 0.20 mm everywhere except the named nets on B.Cu intersecting the courtyards of these two exact footprints; independent pad-centre/direction/length checks narrow this permission to the selected neck signatures. Keep the default netclass at 0.20 mm and all other added tracks at 0.20 mm. Clearance stays 0.20 mm; adjacent microvias stay 0.30/0.10 mm and the annular floor 0.10 mm. Pin project/custom rules and selected neck metadata in deterministic replay evidence. Full native DRC must retain exactly the 104 existing findings; no dangling seed escapes may be selected.

## Calculation and limitations

Illustrative DC calculation, not bench evidence or a copper/process rating: assume 18 µm finished copper and resistivity 1.724e-8 ohm metre at 20 °C. A 0.55 mm × 0.12 mm neck is 4.39 milliohms. At the devices' listed 24 mA output-drive magnitude its calculated drop is 0.105 mV and dissipation 2.53 µW. A 100 mA sensitivity case gives 0.439 mV / 43.9 µW; the datasheets identify 100 mA through VCC/GND as an absolute stress limit, not a permitted operating target. Neither calculation raises a current setting, establishes ampacity, bounds transient heating or qualifies the finished board.

Published generic fabrication capabilities do not qualify this sequential-lamination board. Finished copper, neck/land transitions, via process, transient supply/return and bypass locality, SI/timing, mask/stencil and assembly require engineering review and physical validation. Existing source/cell/charger/regulator/LED limits, protection, firmware and isolated enable boundaries remain unchanged. Independent Gate A remains mandatory before fabrication. This decision supersedes the selected-track floor only for the exact neck inventory; ADR 0047's broad/long digital-width candidate remains unselected.

Native scope evidence: the installed CLI did not match `intersectsBackCourtyard` on the unchanged mirrored rectangle, producing one extra track-width finding. `intersectsCourtyard` with the explicit B.Cu condition matches the selected escape and restores the exact baseline. The independent integer policy still enforces exact pad/side/net/length.
