<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0127: Ordinary-width routing near the actual board edge

Date: 2026-11-12
Status: Accepted for ignored feasibility only; no successor selected.

Continue from the immutable selected 33-open board, SHA-256
`14f0c49582063bab84ea685a8cec798011eb4cd66389b085a3a47777180a13ce`.
The existing ignored control search limits centres to x=0.7..113.3 and
y=0.7..31.8 mm. It reports no grid endpoint at U52.1. A read-only actual-B.Cu
pad-cap screen finds ordinary 0.20 mm contact stubs above that search boundary;
a clear cap alone is neither a usable path nor a new circuit connection.

Permit a separate ignored additive search with centres within
x=0.35..113.65 and y=0.35..32.15 mm. Preserve ordinary 0.20 mm width and the
existing 0.20 mm foreign-copper and board-edge rules. Screen every new trace
against the native board/cutout outline, using a 0.325 mm inward offset and
samples at most 0.025 mm apart, leaving at least 0.2125 mm between a 0.20 mm
trace and the original boundary. Screen new 0.30/0.10 mm adjacent microvias
inside a 0.36 mm inward offset and 0.50/0.30 mm central/full-span vias inside
a 0.46 mm inward offset; retain all actual copper/hole checks. No new centre
microvia, narrower track, rule relaxation, pad/part/pose/net change or source
copper retirement is authorized.

Read-only cap screening must use actual `IsOnLayer` membership. A pad object's
nominal `GetLayer` is not its copper-layer set; the preliminary nominal-layer
screen is invalid and excluded. No candidate board was generated from it.
The corrected screen retains all no-net/mechanical copper in clearance checks.

Refill and preserve every current physical group after each proposed join.
Selection requires all 221 original source groups and source copper/parts,
matching native/physical count below 33, exact original 104 DRC findings,
complete frozen ledger, deterministic stable replays, native fault/source
checks and visual review. Search-grid results do not prove feasibility or
infeasibility beyond that graph. All electrical, process, controlled-stack,
mechanical and independent Gate A holds remain; no fabrication is authorized.
