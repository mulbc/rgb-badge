<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0043: Fine-pitch signal escape study

Date: 2026-10-23
Status: Evaluated; no narrower-track or smaller-via exception selected.

## Context

The frozen 215-edge native-control study uses 0.20 mm tracks and 0.20 mm clearance. Its exact manufacturer DSF0006A lands are 0.17 mm wide on 0.35 mm pitch. A 0.20 mm track centred on such a pad has only 0.165 mm calculated lateral clearance to its neighbour. A straight 0.12 mm escape would have 0.205 mm calculated lateral clearance. This explains a real fine-pitch obstacle without changing the manufacturer's land pattern.

Sources reviewed on 2026-10-23: [TI SN74LVC1G04 Rev. AF and appended DSF0006A land drawing](https://www.ti.com/lit/ds/symlink/sn74lvc1g04.pdf), the [project package audit](../../hardware/coupon/rev-a/display-interlock-library-audit.md), and [JLCPCB's published capabilities](https://jlcpcb.com/capabilities/Capabilities). The latter lists HDI 3 mil trace/space and 0.075–0.15 mm laser drills. These published limits supported screening narrower signal escapes; they do not qualify this board's complete sequential-lamination stack, copper thickness, stacked vias, finish or stencil, or select a fabricator.

## Decision and evidence

Local probes screened bounded 0.12 mm IC escapes and low-current signal routes while keeping 0.20 mm clearance. None is selected in the 150-edge checkpoint. Localizing suitable unrouted passives under ADR 0044 and combining independently checked routes reached the target using the original 0.20 mm track minimum, 0.20 mm clearance and 0.30/0.10 mm adjacent-layer microvias. The selected replay and independent checker enforce those original dimensions.

A separate 0.25/0.10 mm microvia probe produced 106 native findings, including 0.075 mm annular width against the unchanged 0.100 mm requirement. It was rejected. [The fabricator's HDI FAQ](https://jlcpcb.com/help/article/hdi-pcb-capabilities-faq) describes a blind-via pad at least 0.15 mm larger than its laser hole; that published capability does not override this project's annular-width rule.

No component, land, net, current setting, protection feature or enable-domain separation changes through this study. The exact 104 existing intrinsic findings, controlled impedance, return paths, power/thermal capacity, HDI stack/process and tiny-package assembly remain unresolved. Independent Gate A review is required before fabrication. The rejected local candidates and manufacturer PDFs are not repository artifacts.
