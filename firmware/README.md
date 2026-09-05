<!-- SPDX-License-Identifier: Apache-2.0 -->

# Firmware

Production firmware will use ESP-IDF and native C/C++. Initial scope is hardware validation: deterministic matrix scan timing, safe rail defaults, USB diagnostics, telemetry, test patterns, button state handling and a minimal BLE programming-mode transfer.

Host-test asset parsing, gamma conversion, frame scheduling and runtime-estimator maths before relying on target hardware. Do not create production drivers until exact devices and the machine-readable board pin map are frozen.
