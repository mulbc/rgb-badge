<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Coupon Rev A controller capture

Status: exact-part library and generated schematic source complete; automated source checks pass; owner KiCad 10.0.6 ERC/render/netlist review and independent Gate A review pending

## Controlled parts and evidence

| Function | Exact part | Package / selected value | Controlled evidence |
|---|---|---|---|
| Controller / BLE / native USB | `ESP32-S3-WROOM-1U-N16R8` | 18 × 19.2 × 3.2 mm external-antenna module; 16 MB flash; 8 MB octal PSRAM | [Espressif module datasheet v1.81](https://documentation.espressif.com/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf) and [hardware guidelines](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/schematic-checklist.html) |
| Mode / ROM-recovery button | `EVQP7J01P` | side-push SPST-NO, 1.6 N, 1.35 mm high | [Panasonic EVQP7/P3/9P7 drawing](https://industrial.panasonic.com/cdbs/www-data/pdf/ATK0000/ATK0000C378.pdf) and [current product page](https://industry.panasonic.com/global/en/products/control/switch/light-touch/number/evqp7j01p) |
| EN and GPIO0 pull-ups | `ERJ-2RKF1002X` | 10 kΩ ±1%, 0402 | [Panasonic ERJ data sheet](https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf) |
| Native USB series resistors | `ERJ-2RKF22R0X` | 22 Ω ±1%, 0402 | same Panasonic ERJ data sheet |
| UART0 TX series resistor | `ERJ-2RKF4990X` | 499 Ω ±1%, 0402 | same Panasonic ERJ data sheet |
| Local bulk capacitor | `GRM188R60J106ME47D` | 10 µF ±20%, 6.3 V, X5R, 0603 | [Murata product record](https://pim.murata.com/en-global/pim/details/?partNum=GRM188R60J106ME47D) |
| EN-delay capacitor | `GRM155C71A105KE11D` | 1 µF ±10%, 10 V, X7S, 0402 | [Murata product record](https://pim.murata.com/en-global/pim/details/?partNum=GRM155C71A105KE11D) |
| Local high-frequency capacitor | `GRM155R71C104KA88D` | 100 nF ±10%, 16 V, X7R, 0402 | controlled driver-library record |

The obsolete `GRM155R61A105KE15D` was explicitly rejected during capture and replaced by the active `GRM155C71A105KE11D`. These remain candidate BOM lines, not purchasing authorization. Buy the module and passives through manufacturer-authorized distribution or a traceable LCSC/JLC global-sourcing channel. LCSC currently lists the exact Panasonic button, which is useful for turnkey assembly availability but does not authorize a substitute. An Alibaba CM may quote the exact MPNs with disclosed provenance; anonymous AliExpress critical-module or RF parts remain development-only.

## Pin and GPIO allocation

| Module pad / GPIO | Coupon net | Purpose |
|---|---|---|
| 4–7 / GPIO4–7 | `ROW_A0`–`ROW_A3` | row-decoder address |
| 12 / GPIO8 | `ROW_ENABLE_N` | active-high hardware-safe row blanking request; existing 100 kΩ pull-up keeps rows off |
| 17 / GPIO9 | `DISPLAY_ENABLE` | request to the pending hardware VLED gate; firmware alone is not the safety interlock |
| 18–22 / GPIO10–14 | `LED_LAT`, `LED_SIN`, `LED_SCLK`, `LED_GCLK`, `LED_SOUT` | TLC59581 control and readback |
| 10–11 / GPIO17–18 | `SYS_I2C_SDA`, `SYS_I2C_SCL` | charger/gauge/current-monitor service bus |
| 13–14 / GPIO19–20 | `USB_DN_MCU`, `USB_DP_MCU` | fixed native USB pins, then 22 Ω series resistors to `USB_D-` / `USB_D+` |
| 27 / GPIO0 | `MODE_BOOT_N` | active-low mode button and boot strap |
| 36 / GPIO44 | `UART0_RX` | hidden factory/recovery receive pad |
| 37 / GPIO43 | `UART0_TX_RAW` | 499 Ω series resistor to hidden `UART0_TX` pad |

GPIO35–GPIO37, module pads 28–30, are deliberately no-connect because the N16R8's octal PSRAM consumes them. Strapping GPIO3, GPIO45 and GPIO46 are also left isolated. GPIO46's internal weak pull-down combines with GPIO0 low for ROM joint-download mode. The remaining unused GPIOs have explicit no-connect markers so later edits cannot silently imply availability.

## Boot, power and failure defaults

`ESP_EN` has Espressif's baseline 10 kΩ pull-up and 1 µF capacitor. The coupon must measure the switched 3.3 V rise, EN threshold and reset timing; Gate A may require a supervisor if the final rail ramp makes an RC delay inadequate. Local 10 µF plus 100 nF decoupling follows the module supply guidance, while final placement and the regulator's own output network remain layout/power-sheet work.

`MODE_BOOT_N` has a 10 kΩ pull-up and the single user button to ground. During normal firmware execution, a roughly three-second hold enters programming mode and enables BLE. Holding the same button while switching the badge on requests ESP32-S3 ROM recovery. No capacitor is placed on GPIO0.

The pending power sheet must make `DISPLAY_ENABLE` fail-safe: VLED remains off through power-up, reset, programming and an unpowered controller regardless of GPIO glitches. Passing this controller source check does not satisfy that requirement.

## Recovery and observability

| Pad | Net |
|---|---|
| `TP2`, `TP3` | `ESP_EN`, `MODE_BOOT_N` |
| `TP4`, `TP5` | `UART0_TX`, `UART0_RX` |
| `TP6`, `TP7` | `LED_GCLK`, `ROW_ENABLE_N` |
| `TP8`, `TP9` | `+3V3_APP`, `GND` |
| `TP10` | `DISPLAY_ENABLE` |
| `TP11`, `TP12` | `SYS_I2C_SDA`, `SYS_I2C_SCL` |

Native USB remains available through the future USB-C receptacle when the application rail is on. R45/R46 belong beside U3 in layout; the receptacle, controlled-impedance pair, ESD array and Type-C circuits remain on the next power/input sheet.

## Library provenance and checks

The 41-pin symbol is an exact-MPN project-local transcription of Espressif's module pin table. The module footprint reproduces the perimeter and nine same-numbered central-ground lands from Espressif's official KiCad library release 3.2.1, checked against the current module drawing. The adapted footprint retains the upstream CC-BY-SA-4.0 attribution and KiCad-design exception in `NOTICE` and `LICENSES/Espressif-KiCad-CC-BY-SA-4.0.txt`; the schematic using it remains under the repository hardware license.

`python3 tools/check-controller-libraries.py` validates the symbol pin map, module pad coordinates/sizes/layers, central-ground array, capacitor lands and duplicated button contacts. `python3 tools/check-coupon-controller.py` traces every source connection, all explicit no-connects, exact part properties and test-pad nets. Its `--netlist` mode becomes the comprehensive 356-item / 1,360-logical-pin matrix + driver + row + controller contract. These are independent parsing checks, not KiCad ERC, PCB DRC, RF validation, assembly DFM or measurements.

## Native review still required

Run the macOS command in the project README. In the exported eight-page PDF, inspect page 8 for readable module pins, the two reset/boot networks, USB resistor direction, UART resistor, all eleven test pads and every no-connect marker. In the footprint exports, confirm the module perimeter pads, nine separate pad-41 lands, button duplicate contacts and the 0603 capacitor lands. A clean native run will gate this PR; independent Gate A review still gates fabrication.
