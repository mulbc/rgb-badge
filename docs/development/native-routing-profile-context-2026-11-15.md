<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Native routing probe context correction, 2026-11-15

The selected board remains ADR 0153's **29-open** inverter checkpoint, unchanged
at `a4d27c5babed5556002cf71b8fae3c3280f627edeb0ff673b9b787d21d4b91ab`.
This follow-up fixes evidence context for future routing probes. It adopts no
new copper or rule setting and does not complete the zero-open goal.

A reused rejected heartbeat snapshot lacked its custom-rule sidecar. Diagnostic
DRC then auto-created a default project file. The first coupled restoration
could not be relied on and ultimately failed when copying the absent rule file.
Its results are discarded. The original rejected PCB bytes and every accepted
checkpoint remain unchanged. The profile and rule bytes were restored from the
known selected source, the snapshot was refilled in a separate output and the
coupled study repeated under that exact context. Footprint-library resolution
was also supplied before interpreting native DRC; 199 initial library warnings
were context diagnostics, not routing violations to waive.

[ADR 0159](../decisions/0159-preserve-native-probe-project-context.md) and the
[validation manifest](../../mechanical/review/native-profile-context-validation.json)
record the fix. Future probes should use the versioned successors:

- `tools/search-native-control-profiled.py`
- `tools/search-routing-closure-profiled.py`
- `tools/search-u36-stage-profiled.py`

They preserve the corresponding historical search algorithm and add exact
project/rule copying, source-change checks and PCB/profile-bound context
manifests for rejected snapshots and final outputs. Reused manifested probes
reject missing or changed settings and changed board bytes before importing
KiCad. Intentionally absent custom rules stay explicitly absent; stale target
rules are rejected. Library resolution remains a separate native gate.

The historical tool files remain byte-identical. A direct edit initially
tripped the existing remaining-routing tool fingerprint guard; that guard was
retained, and the fix was moved to versioned successors. No historical manifest
or accepted-source fingerprint was rewritten. Fourteen regression tests cover
exact bytes, missing/changed/stale settings, source changes, safe source
preservation and all three entry points. All 36 source-workflow commands pass.
A bounded native run of the profiled closure tool accepts no new copper,
retains 29 native opens and round-trips exact project/rule bytes and hashes.
All referenced accepted-checkpoint evidence hashes remain unchanged.

The related routing work is still unselected. The prepared heartbeat capture
preserves all 217 prior groups; larger searches find routes but split old
supply/ground groups. Two forward paths exceed the 120 mm signal bound and
are disqualified. The 99.435 mm reverse path loses three old groups, leaves
two original USB vias dangling and has unequal native/physical counts. Its
correctly profiled coupled restoration still selects no join. Additional In1/front preferences also reject old GND/USB splits. Their cost
function retained In2 at the lowest cost despite the explicit preference;
ADR 0154 scopes a further ignored cost-only variant to honor that preference.
No outcome from the unfinished variant is claimed here.

Exact-pad discovery screens 79 physical pads on small disconnected groups;
40 yield recorded outer-capture samples and 32 yield a clear additional
adjacent transition. These are first-eight bounded samples per pad, not global
placement proofs. PAIR07's two exact outer captures preserve every source
group, but the VLED search exhausts 1,215 sampled points without a join. Its
read-only through-hole alternative screens 1,681 positions: 1,227 fail foreign
copper and 454 do not make the required pad contact. It selects no capture.
The literal paired-row trial value and provisional status are unchanged.

No board has been built or measured. All electrical/current/protection/NTC/
timer/default-off, part/return/timing/thermal/HDI/stack/process/fit and independent
Gate A holds remain. Fabrication remains prohibited.
