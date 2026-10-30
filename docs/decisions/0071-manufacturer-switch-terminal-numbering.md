<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0071: Transcribe the printed JS202011JCQN terminal numbers

Date: 2026-10-30
Status: Selected for the exact 58-edge source checkpoint; physical/electrical qualification remains open.

The owner supplied Littelfuse-CK-Slide-JS-Series-Datasheet.pdf, revision
VL 01/14/26, SHA-256
0f35cdf47a1f93da71bb7235581f3c77915516488be930d7a3ea4f4942ff0f3b.
Rendered page 9 identifies JS202011JCQN and shows a bottom-view DPDT circuit
numbered 1/2/3 and 5/6/7, with 2 and 6 marked common. The existing project
symbol/land instead uses 1/2/3 and 4/5/6, with common 5. The historical first-author
audit explicitly left manufacturer pin-direction reconciliation open. Do not
represent the old labels as manufacturer-verified.

Correct only terminal identity: old 4 → printed 5 (unused second-pole throw),
old 5 → printed 6 (second-pole common, protected BAT), old 6 → printed 7
(second-pole gauge throw). Pins 1/2/3 retain identity. Preserve every physical
land coordinate/size/layer, component pose, net at its physical land and copper
item; this is not an electrical rewiring or current-setting change. Do not
infer a different actuator direction or silently mirror the land pattern.

Keep the historical legacy footprint unchanged for frozen PCB replay. Introduce
a dedicated manufacturer-numbered footprint and update the exact symbol,
embedded/placed control sheet, deterministic generator, canonical pin contract
and explicit native mapping. Compare corrected physical pads back to their
checked legacy numbers for historical group/interface witnesses. Historical
source comparison must opt into and report the legacy switch assignment rather
than silently accepting it. Preserve canonical snapshots for earlier evidence.

ADR 0070's candidate must require SW2.7/C39.1/U46.1 under these printed numbers;
its physical route and all previous 59-edge copper/groups remain unchanged.
Require source-pin fault checks, native XML/ERC and rendering, native/physical
counts, complete DRC, stable fills/replay, original-orphan restoration and all
previous guards before canonical selection. A source-count reduction cannot
justify the old numbering.

The sheet's bottom-view notation, terminal-1 side-view indication and the
captured mechanical orientation still need independent assembly/physical
reconciliation. Functional ON is the pair of throws 3/7 opposite the shown
1/5 pair in the bottom-view schematic; no top-edge physical ON direction is
qualified here. Actual received-part numbering, orientation, switch-contact
transitions, OFF leakage, stencil/assembly, enclosure and independent Gate A
remain open. This unbuilt source correction is not a fabrication release.

## Selected source evidence

The [58-edge record](../development/led-routing-progress-58-study-2026-10-30.md) passes complete retention, source/native/ERC/rendering, stable fills/replay, orphan restoration, 65 native and 116 portable guards. Printed switch labels are checked without changing physical contacts. All engineering and fabrication holds remain open.
