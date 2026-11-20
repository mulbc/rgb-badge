<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0156: Coupled heartbeat and plane restoration feasibility

Date: 2026-11-15
Status: Accepted for ignored restoration only; no successor selected.

The ADR 0154 prepared source preserves all 217 selected-source groups. Both
alternative searches find input paths but reject their filled-plane splits.
Independent source comparison disqualifies the forward paths at 126.286 mm
and 133.845 mm, above the existing 120 mm signal ceiling. Do not adopt or
continue those over-bound paths.

Only the reverse In3-preference rejected snapshot at
`heartbeat-input-in3-rejected/DISPLAY_HEARTBEAT-R103-1.kicad_pcb`, SHA-256
`104b010b4eac881d4b3edec2a09ee7ce3a134128740343ea3726b14383021fc6`,
is eligible for this ignored coupled study. Its calculated new signal length
is 99.434656 mm including the 0.500 mm neck. It preserves 214/217 source groups
and loses parts of GND, +3V3_USB and +BAT_PROTECTED_DRAFT. Native/physical opens
are 32/31, so neither its apparent signal join nor a later lower native count
alone is progress. The selected 29-open source stays immutable.

Preserve all exact snapshot source items, parts/poses/local pads/nets/rules,
the accepted clock join and every actual external branch. Restore only GND,
+3V3_USB and +BAT_PROTECTED_DRAFT using additive ordinary 0.20 mm supported
adjacent paths and actual group/filled-plane witnesses. Bound each new rail's
track length to 120 mm, retain 0.30/0.10 mm outer microvias and 0.50/0.30 mm
In2/In3 mechanical buried vias, ADR 0147's narrowly supported-span prefilter,
all other hole/copper/edge checks and exact unchanged native profiles/rules.
No new centre microvia, placement, retirement, width exception, current setting
or protection/default-off alteration. Each restoration must preserve every
live group in its own input; final comparison must independently restore all
217 groups and source copper from the immutable selected 29-open board.

Require complete DISPLAY_HEARTBEAT, actual matching native/physical count below
29 and exact original 104 findings under only the existing two transforms,
with all source/orphan/external-contact/hole/replay/inverse/fault/source/visual
proofs before selection. Any remaining plane split, native discrepancy,
dangling source fragment, new finding or excessive signal length rejects the
successor. This permission does not qualify current capacity or return paths.
All electrical/part/HDI/stack/process/fit/Gate A and fabrication holds remain.

The first reused snapshot lacked a copied `.kicad_dru`; diagnostic native DRC
also auto-created a default project profile. Discard all coupled-search and DRC
results from that context, including its reported group misses. The original
rejected PCB hash and the selected source are unchanged. Preserve the diagnostic
profile separately, restore exact selected `.kicad_pro`/`.kicad_dru` bytes to
the snapshot, refill in a distinct ignored output and repeat native DRC before
restoration. Use an ignored search variant that rejects missing/changed exact
profile hashes before loading and copies both files with every rejection
snapshot. Record this provenance; no accepted-checkpoint gate is relaxed.
