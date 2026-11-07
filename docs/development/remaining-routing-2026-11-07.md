<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Remaining routing: 42-open checkpoint

The zero-open goal remains **in progress**. The selected
[remaining-routing project](../../hardware/coupon/rev-a/staging/led-remaining-routing-trial-114mm.kicad_pro)
has **42 native and independently counted physical opens**, with the exact
unchanged **104 intrinsic DRC findings**. Every copper item and all 231 live
pad groups in the immutable 43-open switch source survive. This is unbuilt
Coupon Rev A CAD continuity, with no powered hardware/firmware measurement.
Fabrication remains prohibited pending qualification and independent Gate A.

[ADR 0091](../decisions/0091-zero-open-routing-study.md), the
[exact plan](../../mechanical/review/remaining-routing-plan.json),
[manifest](../../mechanical/review/remaining-routing-checkpoint.json) and
[native DRC](remaining-routing-drc-2026-11-07.json) bind the checkpoint. PCB SHA:
`844fd52387c41f6cfbbce1790e6a564a63d3285417b020769f91088d870ba4ca`.
The 43-open parent and its complete validation stay unchanged.

U3.14–R46.1 now form one physical USB_DP_MCU group. An initial path split APP
supply groups; explicit APP restoration preserves all prior connections. The
ledger adds 72 ordinary 0.20 mm tracks and eleven 0.30/0.10 mm adjacent outer
microvias. No part moves, existing copper retirement, new central transition,
rule relaxation, circuit/net/current/default-off or firmware change occurs.
Added trace centre-line lengths are 53.827927 mm for USB_DP_MCU and 3.841421 mm
for +3V3_APP, excluding pad/via/plane travel. The USB negative MCU path and other
USB nets still have opens. This route does not establish differential pairing,
impedance, skew, return quality or functional USB operation. APP supply-path
current capacity, voltage drop and thermal review remain open.

Validation passes:

- Exact copper/part/field/local-pad/net/pose/profile/outline/zone structure,
  all 231 prior groups, 483 footprints and 2,092 physical pads.
- Three stable fills per generation, two independent byte-identical replays,
  and exact selected-board native/physical 42-open agreement.
- Exact unchanged 104 native findings. Original-orphan restoration preserves
  every live group and adds only the three original dangling-via warnings.
- Seven isolated rejection cases, including actual USB and APP-supply
  disconnections, unsupported full-span microvia, smaller via, narrowing,
  changed converter default and deletion of prior switch-route copper.
- The source contract retains 465 common components and 1,718 logical pins.
  All 27 source-only workflow commands pass locally; results are recorded in
  the manifest without claiming remote CI success.
- Native bottom-copper endpoint views inspected at U3 and R46. Raw views,
  searches, replay/fault logs remain ignored in `build/remaining-routing/`
  and `build/zero-open-routing/`.

Remaining opens are inventoried by net in the manifest. The named successor
may grow through exact validated ledgers as the goal continues; the immutable
43-open source stays available. All supplier/stack, 557 historical centre-via,
part/electrical/process/fit and independent Gate A holds remain open.
