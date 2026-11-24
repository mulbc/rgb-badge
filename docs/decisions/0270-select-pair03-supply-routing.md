<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0270: Select the fully qualified PAIR03 supply checkpoint

Date: 2026-11-20
Status: Accepted for CAD source selection only.

ADR0269 qualification passes:22 matching native/physical opens,210
physical groups/188 nets, every211 prior group/all19349 attached source
Cu, no orphan Cu, GND197/VLED39/USB32; all483 exact parts/pads/fields/
poses and all raw fixed declarations/profiles unchanged. The17 ordinary
tracks and one supported B/In4 microvia pass the full source hole audit.
Full native CLI DRC has exactly the unchanged104 findings. Four initial
fills and two independent three-fill replays share SHA03e74104c51811a1.
Removal restores source9574949d6bd56caa byte for byte across three fills,
all211 source groups, all nine integer zone XORs empty and exact104.
32 deliberate native/raw/part/copper/via/source/DRC faults reject;
eight hole controls pass. All43 portable source checks and native B/In4
before/after visual review pass. No part moves, no copper retires.

Select led-pair03-supply-routing-trial-114mm at full board SHA
03e74104c51811a18d558cdc7bd28513f9f1fcb5058ef8a7c7f62f612d8a252d.
The23-open source remains immutable. Copy only the qualified exact PCB
and unchanged project/rules; verify canonical fingerprints and gates.
The zero-open goal, trial-package/power-copper/electrical/return/thermal/
stack/process/assembly/fit and independent Gate A remain unresolved.
No fabricated or tested hardware is claimed; fabrication is prohibited.
