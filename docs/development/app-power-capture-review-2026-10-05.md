<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Provisional application-power schematic review, 2026-10-05

Scope: source branch `coupon-power-rev-a`, fourteen-page KiCad coupon schematic after adding SW2 application control and U36 TPS631000 converter. This is a **first-author source review**, not an independent Gate A review or a bench test. No board exists.

## Captured connections

- `SW2` (`JS202011JCQN`) contact 2 connects to `+SYS_APP_IN_DRAFT`; contact 3 connects to `APP_ON_SW_DRAFT` and U36 EN. Contact 1 and all three contacts of pole 2 have explicit no-connect markers. Pole 2 is reserved for later gauge supply isolation.
- `R83` is the 100 kΩ EN-to-GND pull-down. U36 VIN and both 22 µF input capacitors connect to `+SYS_APP_IN_DRAFT`, which still has draft `#FLG07` because there is no charger OUT circuit. U36 VOUT, both 47 µF output capacitors and the feedback divider connect to `+3V3_APP`. Each inductor terminal connects only to its corresponding LX pin. U36 MODE and ground are tied to GND.
- The previous `+3V3_APP` flag `#FLG01` was removed from the driver. The converter output now supplies the schematic rail. Gauge `#FLG06`, VLED `#FLG03`, USB source `#FLG05` and GND `#FLG02` retain their existing scope; none represents a completed new supply here.

## Native checks and visual inspection

KiCad CLI **10.0.6** ran the full `tools/check-kicad.sh` pipeline. Host source checks passed. Native ERC returned **zero configured violations**; the complete KiCad XML export matched **410 PCB items and 1,537 logical pins**. The XML explicitly showed `SW2.2` on `+SYS_APP_IN_DRAFT`, `SW2.3` and `U36.5` on `APP_ON_SW_DRAFT`, `U36.1` on `+3V3_APP`, and `U36.2/3` connected to the opposite terminals of L1. The exported fourteen-page PDF was inspected on root page 1 and new pages 13 and 14: labels and all new symbols are legible, with separate notes identifying the draft source and open gauge pole. Reproduce with `./tools/check-kicad.sh`. Raw export digests from the review run: ERC `ea4863eaf20d0af6c17d5f1a0cec9b72c27fa4fff75c66bce1d5c7bdc65d67b1`, XML `d544188fc86ce2b451775a3f7d914cfbc14b41bdb86b2c9c69ec1e2b56ff8956`, PDF `ce0a3892fdcb3a2c0dc9780aebfe4263ac663e9a917d29122de71f757068d36e` (SHA-256). These temporary exports are reproducible, not release files.

## Open findings

1. `+SYS_APP_IN_DRAFT` is a PWR_FLAG, not the protected battery/charger PowerPath. Do not infer converter input voltage, startup, inrush or OFF leakage from ERC.
2. JCQN is vertical SMT; ADR 0015's right-angle JAQN may better meet the top-edge actuator requirement. Validate the manufacturer's physical throw direction, footprint numbering/lands, service access and enclosure clearance before a final switch selection.
3. SW2 pole 2 is open. The gauge still uses its temporary switched-BAT source flag; bus isolation and arbitrary contact-order behavior are unresolved. No OFF-current or gauge-isolation claim follows from this capture.
4. VLED and row hardware interlock, charger/NTC/timer, pack connector, USB input protection and source permission remain uncaptured or provisional. Capacitor combined derating, converter transient and thermal behavior remain review/bench tasks. Independent Gate A remains mandatory before fabrication.
