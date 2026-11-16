<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0159: Preserve native routing probe project context

Date: 2026-11-15
Status: Accepted for routing-tool evidence integrity; no PCB/rule change.

Reusing an ignored rejected snapshot exposed an omitted custom-rule file and
an auto-created project profile. The 29-open selected checkpoint and every
accepted gate are unaffected; the incorrect-context coupled results are
explicitly discarded in ADR 0156 and repeated with exact settings.

Add profile-preserving successors to all three public native search entry points,
requiring a readable source
project profile before loading KiCad, preserve its exact bytes and any custom
rule bytes with rejected snapshots and final outputs, and record source-profile
hashes. Existing sources with intentionally absent custom rules retain explicit
absence. Refuse a stale destination rule file when the source has none.

Write a separate profile-context manifest bound to the saved PCB hash. When a
probe carrying this manifest is reused, reject changed/missing project or rule
bytes and changed PCB bytes before importing native KiCad. Recheck source
profile bytes when copying outputs, so changes during the search cannot pass.
Keep existing snapshot pad-split JSON formats and safe ignored-output paths.
Add the helper to actual search-source fingerprints and regression-test missing,
changed, stale, binary-preservation and source-overwrite cases without KiCad.
Legacy snapshots without a manifest require explicit reconstruction from their
known source before their results can be relied on; a default profile is not
proof of original context. Native library resolution remains a separate gate.

No route geometry, heuristic, via policy, profile/rule value, source ledger,
electrical limit, protection/default-off boundary or fabrication gate changes.
Historical evidence hashes remain historical and are not rewritten. Record
new validation and current-source fingerprints for this fix.

The initial direct edit of a historical search file triggers the existing
remaining-routing fingerprint guard. Preserve all three historical tool files
byte for byte and their recorded fingerprints; do not rewrite old manifests.
Ship the corrected successors as `search-native-control-profiled.py`,
`search-routing-closure-profiled.py` and `search-u36-stage-profiled.py`. Their
search algorithms retain the corresponding frozen predecessor behavior, with
only project-context preservation/validation and traceability added. Use these
versioned entries for future probes. The regression tests exercise all three
new entry points. Record the rejected direct-edit check as development evidence.
