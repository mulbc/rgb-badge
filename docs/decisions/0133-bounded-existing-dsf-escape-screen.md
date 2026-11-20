<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0133: Bounded screening under the existing DSF neck rules

Date: 2026-11-14
Status: Accepted for ignored feasibility only; no successor selected.

Use immutable selected 33-open source
`14f0c49582063bab84ea685a8cec798011eb4cd66389b085a3a47777180a13ce`.
Its unchanged native rule file explicitly permits 0.12 mm B.Cu DSF necks on
U48 DISPLAY_HEARTBEAT/HEARTBEAT_FALL_CLK and U52 DISPLAY_CLEAR_3,
DISPLAY_ENABLE/DISPLAY_CLEAR_OK. All five corresponding original terminals
remain open. This is use of the existing exact package/net allowances, not a
new rule, clearance reduction or general narrowing permission.

For only U48.2, U48.4, U52.1, U52.2 and U52.4, screen native 0.025 mm B.Cu
paths of at most 0.750 mm from the unchanged actual pad to a supported
0.30/0.10 mm B/In4 capture. Keep centres within the native courtyard expanded
by at most 0.050 mm, and require every narrow segment's actual copper to
intersect the original courtyard. Check all foreign/no-net/mechanical copper,
board edges and all nearby holes. Beyond the frozen exact local neck, require
ordinary 0.20 mm copper and existing supported via geometries.

Do not move any part, alter a local pad/net, retire original source copper or
change rules/profiles, current/protection/default-off boundaries. A clear
proxy is not an actual connection. Any ignored capture prototype must preserve
all original 221 live groups after refill; final selection needs a real new
terminal join, native/physical count below 33, exact original 104 finding
payloads, an exact source/neck/ordinary-copper ledger, stable independent
replay/refills, isolated faults, source checks and visual review. Reject any
unlisted narrow copper or prior-group loss. All electrical/stack/process/fit
and independent Gate A holds remain; fabrication is prohibited.
