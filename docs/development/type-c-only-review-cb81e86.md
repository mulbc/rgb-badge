<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Type-C-only native finding: cb81e86

2026-09-19. Native checkpoint **not accepted**. Owner KiCad 10.0.6 stopped at ERC with one isolated_pin_label warning for USB_OUT2 at 104.14 mm, 78.74 mm. No schematic PDF or XML netlist was produced; no visual schematic or native connectivity review is claimed.

ZIP SHA-256: `3a899bf0d18f50edee475caf6d61d1c70eec7f187f8535e42e647937cc095a47`.
ERC SHA-256: `4527b4caecc76f1ce3575b25af106b0536da975c194010b6d51c1757273ad845`.

The simplified policy no longer consumes conditioned OUT2. Its only pin was the U24 output, while diagnostic pad TP21 still observed raw OUT2. Move TP21 to USB_OUT2, terminating and exposing the conditioned signal; raw OUT2 remains connected to the detector, buffer input and pull-up. No part or warning suppression is added. OUT2 still has no charging-grant path.

Generator, independent pin map and synthetic XML fixture now reflect TP21's conditioned signal. A regression test restores TP21 to raw OUT2 and verifies rejection. Population remains 396 items / 1,492 pins. The next native run must confirm zero ERC violations and produce the complete PDF/XML for review of all three simplified USB sheets.
