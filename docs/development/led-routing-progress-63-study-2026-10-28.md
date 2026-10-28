<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Routing continuation: 64 to 63 unconnected edges

Date: 2026-10-28. Unbuilt, unqualified source study; no hardware measurements or fabrication release. The 50-edge target remains open.

Native and independent physical-pad opens decrease **64 → 63**, retaining exactly **104 unchanged intrinsic DRC findings**. USB_RAW_OUT2 now joins U31.8, R61.1 and U24.3. Every accepted 64-edge copper item, physical pad group, component pose, zone, replacement and supply neck survives. The [64-edge integer plan](../../mechanical/review/routing-progress-64-checkpoint.json) freezes commit 9493793. No experimental ground retirement or smaller-clearance rule is selected.

## Exact transaction and source review

[ADR 0047](../decisions/0047-scoped-digital-signal-width-study.md) selects only the [pinned USB status inventory](../../mechanical/review/routing-progress-digital-width.json): **13 × 0.12 mm tracks / three adjacent 0.30/0.10 mm microvias**, calculated trace length 13.215457 mm. Ordinary width and all other-net clearance remain 0.20 mm. Native rules enforce the ordinary width plus the existing DSF exceptions and this single digital net; independent integer/native checks reject unlisted narrow additions and enforce the 120 mm per-net hard bound. Catalog SHA-256: `ab694bdd60606fbe29b2cb7dab18b357958e4398e6832eb539b18e293d8a7733`.

Rechecked [TI TUSB320LAI Rev. D](https://www.ti.com/lit/ds/symlink/tusb320lai.pdf) and [SN74LVC2G17 Rev. N](https://www.ti.com/lit/ds/symlink/sn74lvc2g17.pdf). Exact U31 TUSB320LAIRWBR pin 8 supplies GPIO-mode open-drain OUT2 to exact U24 SN74LVC2G17DBVR pin 3, a Schmitt input. Unchanged R61 is the 10 kΩ pull-up to their USB-only 3.3 V domain. Pin maps, packages, resistances, modes, protection and hardware current/enable settings are unchanged. This is a logic-status route. Illustrative DC calculation with assumed 18 µm copper at 20 °C gives about 0.1055 Ω; nominal 3.3 V / 10 kΩ pull-up current gives about 34.8 µV drop. These calculations do not qualify finished copper, partial-power behavior, noise or timing.

An initial candidate via had 0.1953 mm clearance. Moving only new signal copper by (−0.050, +0.025) mm restores the exact baseline. The search mask's extra via margin incorrectly assumed a 0.20 mm track; it now derives the margin from the actual trial width. Six regressions cover the default footprint, narrower cardinal/diagonal clearance, edge bounds, same-net space and equal diameters. Four fail before the correction. A conservative rerun rejects the earlier coarse route; the independently checked corrected candidate is selected. Native DRC remains authoritative.

Relative to the frozen 215-edge source, the selected board retains 15,392 nonzero copper items and adds **1,771 tracks / 837 microvias**. It contains **483 footprints / 18,000 copper items**. The six exact original-track replacements and their 27 direct contacts, three orphan retirements, 116 neutral zero-length cleanups, 34 R/C poses, four test-land poses, five original zones, four selected parcels and two exact supply necks remain unchanged. No firmware or circuit-topology change.

## Validation

[Full DRC](led-routing-progress-63-drc-2026-10-28.json), [native checks](../../mechanical/review/routing-progress-63-native-check-2026-10-28.json), [orphan-restoration DRC](led-routing-progress-63-orphan-restoration-drc-2026-10-28.json), [remaining-net counts](../../mechanical/review/routing-progress-open-nets.json) and [validation fingerprints](../../mechanical/review/routing-progress-63-validation-2026-10-28.json) record the selection. Board SHA-256: `a5807c556358dba4d0c17d69dfd629fc5369c7658637c9169331c012770f9ef6`.

Three stable refills and byte-identical PCB/project/custom-rule regeneration pass. The gate passes **43 isolated native guards / 87 portable plan guards**, canonical metadata and **256 LED checks**. Source-only CI also passes 21 canonical faults, 14 distance tests, six path tests and 13 clearance tests. Added faults preserve the 64-edge checkpoint, reject thinner/differently scoped copper and independently detach the actual U31 status pin. Restoring the three retired source vias leaves exactly 63 opens and adds only their original three dangling findings, without a group or other DRC difference.

## Excluded work and remaining review

The scoped-spacing, local ground-fanout and geometrically covered ground experiments in ADRs 0058–0060 remain ignored feasibility work. They are unnecessary for this connection. The R96/E1 setting relocation and local repair screens make no accepted join. A UART route restores one disrupted supply group but still isolates R82 ground; it remains excluded. Search bounds do not prove routing impossible. Vendor PDFs, binaries, generated exchange files and failed probes remain outside Git.

The 50-edge target is unfinished. Ground retains five opens, VLED eight and gauge supply three; controls, analogue settings, feedback, USB and converter paths remain incomplete. Electrical/return-path/timing, supply/thermal, RF, probe/assembly/fit and HDI process qualification remain open, together with the intrinsic DRC findings and existing trial-package/C45/SYS holds. Independent Gate A is mandatory before fabrication; this source checkpoint is not a manufacturing release.
