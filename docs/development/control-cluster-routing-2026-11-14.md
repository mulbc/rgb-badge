<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Complete control-cluster routing checkpoint, 2026-11-14

The selected CAD study now has **32 native and independently counted physical
opens**, down from 33. U51.4 and U52.1 are one exact DISPLAY_CLEAR_3 group.
All 221 prior groups survive across 188 nets. This is CAD continuity evidence;
the zero-open goal and independent fabrication review remain open.

[ADR 0136](../decisions/0136-control-cluster-routing-checkpoint.md) selects
[the project](../../hardware/coupon/rev-a/staging/led-control-cluster-routing-trial-114mm.kicad_pro).
The immutable 33-open predecessor remains available. The
[complete frozen ledger](../../mechanical/review/control-cluster-routing-plan.json)
records exact poses, retirements, additions and source contact witnesses.

## Exact change

U52 SN74LVC1G08DSFR moves to (103.2,5.275) mm / 90 degrees on B.Cu; its original
C71 GRM155R71C104KA88D bypass follows to (103.0,6.75) mm / 180 degrees.
Local lands, numbering, nets, manufacturer identities and all other parts stay
unchanged. TI's DSF0006A drawing/pin table and the supplied Murata reference
were reviewed; Murata's document is dated November 11, 2014, lacks a recommended
land pattern and is not current approval. Exact-byte vendor copies stay ignored.

The bounded MODE_BOOT_N replacement preserves its exact old ends and interior
branch. A two-track ROW_SEL_14 detour preserves every external contact and makes
space for C71. Six private power/ground leaf items are replaced as recorded
before migration. Eleven original copper items are retired in total; 19,167
remain unchanged. Fifty-nine additions include twelve vias, with no centre
microvia. Three U52 necks use its existing 0.12 mm package rule, each below
0.750 mm; all remaining new tracks are 0.20 mm.

Calculated new copper lengths are 14.321185 mm DISPLAY_CLEAR_3, 10.195692 mm
MODE_BOOT_N, 3.682456 mm ROW_SEL_14, 0.691466 mm APP supply and 1.509320 mm GND.
These are layout calculations, not delay, impedance, current-capacity or bench
measurements. The relocated bypass has a local ground branch; electrical
loop/return and effective-capacitance qualification remain unresolved.

## Validation and limits

- Native and physical opens agree at 32, with 220 groups / 188 nets. All 221
  predecessor groups survive; source copper, original via types, part fields,
  local pads, unchanged poses and complete board/rule/profile structure pass.
- Full DRC has exactly the original 104 intrinsic findings. Only the eight U52
  pad-item coordinates in its four original findings follow its exact new pose.
  Independent integer transforms validate every moved pad; complete remaining
  finding payloads, severities and ignored checks stay identical. No warning
  or finding is waived.
- Two independent frozen-ledger replays, each with three stable refills, match
  selected SHA-256 `1d34fd1e29c8f65d22e7626cc0d2f0307be26b8d5255a0f6e16eb0eac46ceb6b`.
  The first search snapshot has different cached fill geometry and is not
  selected. The source-generated stable replay passes its own complete gates.
- The inverse reconstruction removes all additions, restores eleven source
  items and two old poses, and restores all 221 groups, 33 opens and exact old
  findings. Integer polygon XOR is empty for all nine original filled zones;
  serialized cached collinear vertices differ. Source bytes remain unchanged.
- Eighteen native/DRC fault cases reject altered parts/nets/poses, source copper,
  width, added inventory, via types/drills/spans, omitted contact evidence,
  actual signal disconnection, altered finding positions/descriptions, omitted
  findings and an added ignored check.
- All 33 source-workflow commands and canonical circuit/pin checks pass.
  Native B.Cu/In4.Cu/In3.Cu/In2.Cu/In1.Cu views show the actual additions against
  the component outlines. The failed forward path's APP split was rejected;
  only the group-preserving reverse path is retained.

Reproduce with `tools/check-control-cluster-routing.sh`. The
[machine checkpoint](../../mechanical/review/control-cluster-routing-checkpoint.json)
records raw hashes, source checks, replay/fault results and inspected images.
No PDFs, vendor renderings or unsigned manufacturing files are committed.
Zero opens, part/electrical/timing/return/thermal/HDI/stack/process/fit qualification,
557 historical centre microvias and independent Gate A remain unresolved.
Fabrication remains prohibited.

Contact-fixture follow-up: the original `omit-contacts` case inserted an empty wrong-name field. The [enable continuation](enable-routing-2026-11-14.md) corrects the fixture to omit the actual retirement contact catalog; its native predecessor rejection passes. The source PCB and historical evidence hashes remain unchanged.
