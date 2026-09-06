<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Product requirements

Status: Baseline accepted; measurements pending
Source: requirements interview completed 2026-09-05

“Coupon” means the production-intent 16 × 16 validation board. “Final” means a complete cased 48 × 16 badge.

| ID | Requirement | Verification | Applies to |
|---|---|---|---|
| DSP-001 | Provide 48 × 16 individually controlled RGB pixels. | Design inspection and pixel self-test | Final |
| DSP-002 | Pixel pitch shall be no greater than 1.95 mm; baseline is exactly 1.95 mm. | PCB dimension inspection | Coupon/final |
| DSP-003 | Accept 24-bit source art and apply gamma and programmable white balance. | Golden-image firmware test and visual test | Coupon/final |
| DSP-004 | Support 60 content-frame updates per second and at least 1 kHz visual refresh. | Logic trace and camera test | Coupon/final |
| DSP-005 | Brightness shall remain at the user-programmed fixed value during normal playback. | Runtime state/telemetry test | Coupon/final |
| DSP-006 | Safety logic may disable the display on an electrical or thermal fault, but shall not silently dim it. | Fault-injection test | Coupon/final |
| DSP-007 | Coupon columns 0–7 shall use `EAST10105RGBA0` and columns 8–15 shall use `QBLP1515A-RGB2A`, both at 1.95 mm pitch; substitutions require written design review. | BOM, placement and incoming-part inspection | Coupon |
| MEC-001 | Complete case shall not exceed 110 × 35 × 11 mm, excluding attachment thickness. | Caliper inspection | Final |
| MEC-002 | Complete badge shall aim for ≤75 g and shall never exceed 100 g, including cell, case and magnetic attachment. | Calibrated scale | Final |
| MEC-003 | Development case shall use two M2 screws plus tabs and support a replaceable diffuser. | Fit inspection | Coupon/final prototype |
| MEC-004 | Final design shall tolerate sweat and incidental splashes without claiming an IP rating. | Defined splash demonstration and inspection | Final |
| PWR-001 | A new selected cell shall provide roughly 6 h for the published reference workload and fixed brightness. | Logged full-charge runtime test | Final |
| PWR-002 | Continuous maximum full-white runtime shall be measured and published separately. | Logged stress runtime test | Final |
| PWR-003 | OFF-state battery drain with USB absent shall be below 50 µA. | Ammeter measurement after settling | Coupon/final |
| PWR-004 | Switch OFF shall disable the ESP32, display drivers, 3.3 V rail and LED rail. | Rail/current measurement | Coupon/final |
| PWR-005 | Charging, cell qualification and charge status shall operate autonomously while the switch is OFF. | State-matrix test | Coupon/final |
| PWR-006 | Operation while charging shall remain stable; the charger power path shall respect the input limit. | Load/charge test and USB power log | Coupon/final |
| USB-001 | Use a USB-C receptacle on the right short edge with 5 V input only; USB PD is not required. | Inspection and source test | Coupon/final |
| USB-002 | Enumerate native USB in both connector orientations with compliant A-to-C and C-to-C cables while switched ON. | Enumeration matrix | Coupon/final |
| USB-003 | Hardware shall default to a conservative input limit and shall not depend on application firmware to unlock higher Type-C current. | Unprogrammed-board and attach-state test | Coupon/final |
| CHG-001 | Target approximately 80% charge in 45–60 min and full charge in 75–100 min with the display off, a capable source and a cell rated for the selected current. | Charge log | Coupon/final |
| CHG-002 | Charge current shall never exceed the exact terminated-pack rating. | BOM/calculation review and current log | Coupon/final |
| CHG-003 | A pack NTC and charger safety timer shall qualify charging without MCU assistance. | NTC boundary/fault tests | Coupon/final |
| RF-001 | BLE shall be disabled during normal playback. | Firmware state and current test | Coupon/final |
| RF-002 | Holding the mode button for approximately three seconds shall enter programming mode and enable BLE. | Functional test | Coupon/final |
| RF-003 | Programming-mode BLE shall work at 3 m line-of-sight in normal worn orientation. | Range test | Coupon/final |
| CTL-001 | Provide one momentary mode button and one real latching slide switch on the top edge. | Inspection and functional test | Coupon/final |
| STO-001 | Store at least 24 representative assets totalling five minutes alongside two application slots. | Image/partition and playback test | Coupon/final |
| MFG-001 | Maintain vendor-neutral KiCad, Gerber, drill, BOM and placement sources. | Release inspection | Coupon/final |
| MFG-002 | PCBA delivery shall require no manual SMT soldering by the user. | Purchase package and incoming inspection | Coupon/final |
| MFG-003 | Critical component substitutions require a written engineering review and updated BOM. | Release audit | Coupon/final |
| SAF-001 | Use a protected, NTC-equipped, documented and keyed connectorized LiPo pack. | Supplier documentation and inspection | Coupon/final |
| SAF-002 | No cell surface may contact a component, solder joint, magnet or screw boss; swelling clearance is required. | CAD interference and physical inspection | Final |
| SAF-003 | An experienced hardware engineer shall review the coupon schematic and preliminary layout before fabrication. | Recorded review disposition | Coupon |
| SRC-001 | Quote JLCPCB, PCBWay and a vetted Alibaba turnkey PCBA supplier against the same frozen package. | Quote comparison | Final |
| CST-001 | Target USD 500–800 for coupon, five final PCBAs, cells, basic test tools and shipping, excluding independent review and case filament/design. | Quote ledger | Project |

## Reference workload

The provisional runtime workload consists of representative text, icons and animations with approximately 35% of pixels lit and brightness fixed at 25% of the validated hardware maximum. It is a repeatable engineering benchmark, not a restriction on user content. Coupon measurements will define the final asset bundle and calibrated power model.
