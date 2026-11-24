<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0273: PAIR05 ground-capture gateway discovery

Date: 2026-11-20
Status: Accepted for bounded read-only prerequisite discovery.

ADR0272 identifies two B/In4 GND captures and their source leaf as the
left PAIR05 supply wall. The exact three-item source/outside-contact
catalogue is ground-leaf-contacts.json in the ignored fixed-pair05 study.
Prospectively omit only typed original B/In4 microvias05f286c9-7c4e-51f3-
b4b7-1407ff44ae40 at74.2,11.7 and0b7b7683-0f33-592b-b7d4-c599b44dd6da
at74.2,12.0 plus ordinary B GND track7aaf0a01-8cc2-5b16-90bb-2a8ad0bf5f0a
74.2,10.0 to74.2,11.7. All483 parts and other19364 source Cu stay fixed.

Test one supported0.30/0.10 mm B/In4 GND microvia on0.05 mm grid
x73.4..74.0/y10.8..11.6. Restore B from actual old74.2,10.0 port by
ordinary0.20 mm45-degree then vertical path to the new capture. Restore
In4 from that capture to retained original GND via74.2,11.8, then old
74.2,12.0 port. Preserve every retained outside conductor and its group;
deleted UUIDs are not required to remain. Require native source/new Cu,
source holes, original contacts, every210 old pad group/all19364 retained
attached source Cu, GND197/VLED39/USB32,22 matching opens and zero orphans
after an in-memory fill. No source item outside the three may retire.

No PCB is written or selected. Supply closure still needs an actual
main-supply contact and a separate complete frozen prototype with exact104,
replay/inverse/fault/source/visual qualification. Ground return/electrical,
trial-package/stack/process/fit and independent Gate A holds remain;
fabrication is prohibited.
