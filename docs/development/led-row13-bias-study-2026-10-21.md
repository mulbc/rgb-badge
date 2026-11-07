<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Row-13 coordinated pullup placement and escape

Status: **unbuilt, noncanonical geometry study**. No powered-board measurement,
package adoption, current-limit change or fabrication release.

The [saved derivative](../../hardware/coupon/rev-a/staging/led-row13-bias-trial-114mm.kicad_pcb)
moves only the existing exact 1 kΩ `ERJ2RKF1001X` pullup `R19` and connects both
of its terminals. Native opens decrease from **236 to 234**. Nine of sixteen
gate-side pullup terminals are now connected; rows **0, 2, 3, 4, 5, 6 and 7**
remain open. Some other pullups still lack their VLED terminal, and global
power delivery is incomplete. These counts do not establish row operation.

## Selected geometry

The source is the checked [control continuation](led-control-continuation-study-2026-10-21.md).
Both R19 terminals were isolated, so moving it abandons no existing connection.
Its centre changes from (59.75, 5.75) mm / 180° to **(72.95, 27.45) mm / 0°**.
Its exact footprint, value, pad numbers and net assignments are unchanged.
All other 482 footprints retain their placements and physical pad geometry.

Five 0.20 mm gate tracks and two adjacent B.Cu–In4.Cu 0.30/0.10 mm microvias
join R19.2 to the existing `ROW_GATE_13` copper of `PAIR14`. The short source
lead lands on the interior of an existing vertical gate segment; exact native
contact is checked after saving. Four rear 0.20 mm VLED tracks join R19.1 to
the existing main VLED group at `PAIR13.4`. All 14,483 source tracks/vias survive;
the derivative contains **14,494**. Widths/process assumptions are inherited
from the study and remain electrically and manufacturing-unqualified.
One new microvia is centred in R19.2's 0402 land; via filling/capping, solder
wicking and stencil/assembly qualification remain explicit process-review work.

The [generator](../../tools/generate-row13-bias-trial.py) replays this selected
geometry with compact collinear runs and deterministic UUIDs. It pins the input
hash and requires both original resistor pads to be isolated. It does not
depend on local search files or automatically relocate any other component.
The canonical schematic/BOM, candidate device libraries and display-interlock
boundaries are unchanged; this is a placement/routing continuation under the
existing unapproved row-package study, not a material circuit selection.

## Search and rejected approaches

A bounded endpoint-only search on the original eight gate nets found no joins.
The follow-on search co-designed placement with gate escape: native shape
clearance checked short leads from points along existing gate copper; a
0.05 mm, six-layer search then sought a clear resistor site and courtyard.
For row 13 it found the selected site after 84,267 expanded nodes. A separate
guarded VLED search joined the moved supply pad after 9,232 nodes, with zone
refill and physical-cluster preservation. Compact replay is separately checked
with full DRC; a search's occupancy approximation is not acceptance evidence.

The sampled searches for rows 0, 2, 3, 4 and 5 found no placement. For rows
0/2/3/4, their explored rear copper regions also had no native-clear candidate
B.Cu–In4 microvia at the sampled grid points. These are bounded, placement-
dependent results, not impossibility proofs. Further work needs coordinated
nearby placement/escape changes; simply retrying the same endpoint search is
unlikely to help. Exploratory probes remain ignored under `hardware/.../build/`.

## Validation

- Full KiCad 10.0.6 DRC retains the **exact complete multiset of 104 intrinsic
  footprint-clearance findings**, with no added finding. This is not clean DRC.
  [Raw native report](led-row13-bias-drc-2026-10-21.json).
- The [saved-board checker](../../tools/check-row13-bias-trial.py) independently
  transforms a copy of the original R19 land, preserves every original track
  and physical pad group (including duplicate drain lands), checks the two
  exact terminal merges, actual via layer adjacency/dimensions and all eighteen
  physical anode pads per row. [Result](../../mechanical/review/row13-bias-check.json).
- [Per-net native counts](../../mechanical/review/row13-bias-open-nets.json)
  reconcile all 234 opens: GND remains 27, VLED decreases 15 → 14, and application
  3.3 V / USB 3.3 V remain 7 / 4. Only VLED and `ROW_GATE_13` pad groups merge.
- All 256 exact LED placements, rotations, pad maps and nets pass. Eight isolated
  native guard checks include gate/supply breaks without item-count changes,
  deleted source copper, altered duplicate drain geometry, moved unrelated
  parts, pad-net swaps and nonadjacent microvias. These test checker rejection,
  not electrical fault response or an independent Gate A review.
- Two full generations are byte-identical. [Manifest](../../mechanical/review/row13-bias-trial.json),
  [reproduction](../../mechanical/review/row13-bias-reproduction.json) and
  [source/raw-evidence identities](../../mechanical/review/row13-bias-validation.json)
  record the accepted files and local host/native checks.

Reproduce with KiCad's bundled Python:

```sh
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 tools/generate-row13-bias-trial.py
./tools/check-row13-bias.sh
```

Saved-board SHA-256: `7541a0f2eb8eabc383e89ae153131e0bc53d14a257033c8e79b72a7b9ead16f0`.

Seven gate terminals, remaining bias supplies/ground/control/clock/USB routing,
source/package synchronization, current capacity, capacitor/return locality,
timing/interlock faults, fine-pitch/HDI assembly, RF, battery/enclosure fit and
independent Gate A remain open. No hardware or target firmware was exercised.
