<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0077: Local VLED stage connections feasibility

Date: 2026-11-01
Status: Ignored additive feasibility; no canonical placement or retirement.

The ADR 0075/0076 pair study restores old groups at 56 opens, but leaves the
other eleven stage components remote. Investigate the already screened full
thirteen-part seed using the exact ADR 0074 stage probe, SHA-256
`1b50456d58c23e7582a043dc59185ee79a1699c44f7b7693eb3f1b0c58beb49e`.
All exact parts, current pad geometry and thirteen poses remain fixed. The
accepted 58-edge source and the completed two-part experiment remain unchanged.

Permit ignored ordinary-width additive local connections on SYS, VLED,
VLED_FB, VLED_FB_TOP_MID and VLED_ENABLE_DRAFT, solely between the thirteen
stage components U37/L2/C44–C49/C63/R84–R87. Keep both switching paths and every
other existing copper item. Use B.Cu 0.20 mm tracks with unchanged 0.20 mm
clearance for the initial finite screen, at most 25 mm new track per net and
5 mm per local pair. Begin with direct/dogleg connections between input/output
capacitors and their IC pads, the feedback divider and EN pull-down. Reject
crossings of foreign-net native shapes, including old copper. No source or zone
removal, other pose, narrower copper, new via, current/protection/enable circuit
change or power-stage qualification is permitted by this screen.

Record every attempted path and obstruction, native/full DRC, local pad-group
changes and all accepted prior-group losses. An intermediate may retain the
known stage-probe old-group losses; it must not introduce a new split of any
previously intact accepted group or increase the stage probe's existing losses.
Do not describe local joins as restoration of all old groups unless independently
proved. A later global reconnection or via extension requires its own bounded
policy. Source adoption still requires exact retention/retirement/pose policy,
full independent replay/fault/source/orphan evidence, suitable power/bypass/
feedback/return geometry and all standing qualification/Gate A restrictions.

The historical vled-routing-trial may inform local topology only; use current
numbered pads and exact current capacitor packages as endpoints. It does not
approve its obsolete capacitor geometry or establish operating hardware. Ground
pad cluster membership alone does not establish a short low-inductance return.

## Recorded result

The [native study](../development/vled-local-stage-feasibility-2026-11-01.md)
records ten initial local joins, a contact-preserving ordinary-width UART
transfer and two additional local joins. The ignored full-stage candidate has
60 native / 57 physical opens, the exact input-stage 118 findings and two
remaining accepted SYS/VLED group losses. Deterministic replay/stable fills,
independent native audit and CLI rejection checks pass. No canonical source
move or retirement is selected; further supply/local-path and qualification
work remains open.
