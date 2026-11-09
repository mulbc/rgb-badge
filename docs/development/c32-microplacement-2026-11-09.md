<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# C32 ground connection: 36-open checkpoint

The ADR 0105 successor has **36 native and independently counted physical
opens**, with the exact unchanged **104 intrinsic findings**. C32 moves
0.250 mm upward; no track, via or original copper item is added, removed,
resized or renetted. All 225 preceding live pad groups and 226 additions
survive, as do all 231 immutable 43-open parent groups. This is unbuilt
Coupon Rev A CAD, with no hardware/firmware measurement or fabrication release.

## Exact geometry and ground witness

The exact **GRM188R60J106ME47D**, 10 µF / 6.3 V / X5R capacitor keeps its
entire local footprint, fields, numbered nets and 180° orientation. Its
centre moves from (89.250,10.500) to (89.250,10.250) mm. Land 1 remains
+3V3_USB and land 2 remains GND. The supplied Murata June 14, 2026 reference
sheet, PDF page 2, was rendered and rechecked; no component, land-pattern,
approval or effective-capacitance substitution is inferred.

The original direct supply contact is independently rederived from the
37-open source: unchanged 0.20 mm B.Cu track
(90.050,10.500)–(93.200,10.500) mm, UUID
`e037136c-5457-59d0-8b7e-a2c3d68f7014`. It still touches land 1.
Land 2 previously had no external copper contact and belonged to a singleton
physical group. The shifted powered land leaves room for a ground corridor
around it, merging the capacitor's ground island with the main return.

The main ground group grows from 193 to 194 pads. A native witness requires
C32.2 and retained, previously main-connected copper to touch **one individual
filled B.Cu ground component**, independently of the zone object's identity.
The current witness uses zone `81b0abb6-bbba-5f7c-9599-18e6b0c72e0e`,
component 33, retained copper UUID `07b3115d-2653-5240-a616-04176b0f73fb`.
The other two ground opens remain; no permission boundary is bridged.

The local corridor was also calculated from the native polygon at x=90.000 mm.
A 1 µm sample places its filled interior at y=10.801–11.049 mm; the unchanged
zone minimum thickness is 0.250 mm. Eroding the component by 0.100 mm still
contains (90.000,10.925) mm, corroborating a local 0.20 mm copper disk.
This is CAD geometry, not a measured return/current/thermal capability.
Raw evidence is ignored at `build/remaining-routing/36-c32-neck.json`.

## Replay, contracts and rejection tests

The preceding 37-open PCB is commit `e17fa35733158734a4276d1731dc6819258ba8ac`,
SHA `ed6d3ff570f2481b47423d8375d9d4a40d756145cdd49e2c222bacc36edbfa57`.
The 36-open successor SHA is
`a24e9220226b77411ae8e8baea5cd629ce0fea8a97c377a708510d6791c2e439`.
The historical source is read from the pinned local Git object, byte-checked,
and cached only in ignored build storage for the independent contact proof.
Native replay therefore requires that recorded history to be available.

Three stable fills per generation, two independent replays and the canonical
output are identical. Full native/physical and exact DRC gates, strict
immutable-parent orphan proof, all 27 source workflow commands, 36 isolated
fault guards and before/after native B.Cu visual review pass. The separate
current-source orphan-restoration experiment remains rejected and is never
substituted for the actual 104-finding selected source. All 483 footprints,
2,092 physical pads, 465 common source components and 1,718 logical pins survive.

Six new rejection cases cover actual C32 ground disconnection with a matching
pose ledger, omitted original contact data, excess displacement with a
matching ledger, forged historical source, omitted contact guard and a silent
D-to-J packaging substitution. Earlier permission, temperature, supply,
USB, exact-width/via and historical-copper guards remain in force.

See the [exact plan](../../mechanical/review/remaining-routing-plan.json),
[checkpoint](../../mechanical/review/remaining-routing-checkpoint.json) and
[microplacement record](../../mechanical/review/c32-microplacement-2026-11-09.json).

## Finite placement screen

The C32 study evaluates 75 of the 0.05 mm sample positions within its 0.25 mm
bound, stopping at this first complete join. The earlier 74 retain 37 opens;
no optimum or global placement proof is claimed. The selected pose needs no
new capture or source-colour retirement.

An earlier PAIR01-only screen under ADR 0104 evaluates all 81 positions in
the same displacement bound: 74 fail foreign-copper clearance and seven
retain contacts/courtyards but cannot capture ground at the exact pad centre.
COL_09_R and/or COL_09_G obstruct In4. Six nonzero retained poses also exhaust
their forced actual-pad routing graphs at 259–300 nodes. No PAIR01 pose or
copper is selected; its existing NTLJD3119CTBG trial-only identity remains.
The manufacturer's top-view map and CASE 506AN lands were visually rechecked
without changing them or adopting a schematic/BOM substitution.

The complete earlier fixed-source ground search exhausts 3,141 nodes at
C32.2, 269 at PAIR01.1, 7,004 at U38.3 and 7,277 at U52.3. These finite
results motivated the small contact-preserving placement study; they do not
establish wider routing impossibility.

Effective capacitance, bypass/return behavior, copper current/thermal limits,
controlled stack, 557 historical centre vias, assembly/process/fit and
independent Gate A qualification remain open. The zero-open goal is ongoing;
fabrication remains prohibited.
