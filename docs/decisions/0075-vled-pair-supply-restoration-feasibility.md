<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0075: VLED pair supply-restoration feasibility

Date: 2026-11-01
Status: Ignored additive feasibility only; no new source selection or retirement.

ADR 0074 establishes short local switching paths for the two-part U37/L2 move,
but leaves the former SYS and VLED pad groups split. Investigate restoring those
exact prior contacts before considering any obsolete-copper cleanup. Input is
its deterministic two-part probe, SHA-256 `9e244a34515d42cf3b5bdf7b1bba52c55fcdd4ce319c8fbeb86159c1f202828b`;
the accepted 58-edge source remains unchanged.

Permit ignored additions only on +SYS_APP_IN_DRAFT and VLED, connecting U37
pins 1/10/11 to the existing SYS group and pins 4/5 to the existing VLED group.
Keep every existing copper item, both local switching paths, all poses, exact
source parts/pads/nets, zone definitions and electrical settings. Add only
0.20 mm tracks at unchanged 0.20 mm clearance and 0.30/0.10 mm adjacent
microvias. Bound new aggregate track length to 25 mm per supply net. This is a
finite geometric reconnection bound, not permission to use long power/bypass
loops in a qualified converter layout. No other component, net, width or source
via is unlocked. Retain all earlier groups after every refill; reject ground,
signal or other-supply splits regardless of aggregate open count.

TPS63020 Rev I pin/layout guidance and the unchanged exact inductor reference
remain as recorded in ADR 0074. VINA/PGND/control-ground separation, nearby
capacitors, suitable power-path widths, feedback/return layout, the remaining
capacitor land/order-code findings and effective capacitance remain open.
Current limits, protection, EN pull-down, display interlock and firmware do not
change. A geometrically restored source group is not electrical qualification.

Record additions, lengths, all old-group retention/losses, native/physical
counts, full DRC and three stable fills for any complete reconnection. Source
retirement, normalization of moved intrinsic findings and canonical pose
adoption require separate exact policies and full independent replay/fault/
source/orphan evidence. All existing qualification and independent Gate A holds
remain; no fabrication output is authorized.

## Recorded result

The [native evidence](../development/vled-supply-cleanup-feasibility-2026-11-01.md)
records complete prior-group restoration and exact cleanup at 56 native/physical
opens / 104 intrinsic findings. Replays/fills, independent audit, eight fault
cases and original-orphan restoration pass. This remains an ignored experiment;
no canonical pose or copper retirement is selected.
