<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# Historical 39-open follow-up routing screens

These experiments use the historical accepted source in commit `772c83a`, SHA
`aab8f44a9ec3ae65aed4ee2500d52d57d4d3872c8428b8f50c765bfedd205a1e`,
with **39 native/physical opens and exactly 104 intrinsic findings**. No trial
below is adopted. The later [38-open successor](remaining-routing-2026-11-07.md)
selects a different coordinated permission-lead replacement under ADR 0099. The board is unbuilt; there is no hardware measurement or
firmware revision associated with these CAD screens. The zero-open goal and
all electrical/process/thermal/stack/fit/Gate A holds remain open.

## Temperature supply

The reproducible [direct-capture screen](tmp390-supply-screen-2026-11-07.md)
finds no eligible sampled pose. A separate ADR 0097 off-pad experiment moves
U39 to (58.10,16.20) mm / 270°, R89 to (57.50,13.83) mm / 90° and R90 to
(59.35,14.20) mm / 0°, with unchanged exact parts/settings. Its exact seventeen
local B.Cu tracks are replaced in an ignored copy; all 227 preceding live pad
groups and every other copper item survive at 39 native/physical opens.
This is only an escape-entry experiment, not a completed supply connection.

The full native report has **106 findings: the existing 104 clearances and
two dangling-via warnings**. One warning is the retained GND microvia at
(57.45,17.65) mm; the other is the new unconnected USB-supply entry at
(57.95,17.60) mm. Do not describe both as ground warnings or waive them.
Adding an inner-layer entry at (57.95,18.20) mm still leaves 39 opens. Both
native-grid supply searches exhaust their reachable sampled graph at 214
expanded nodes. This does not prove wider routing impossible. The original
sensor pose, old returns and accepted 39-open bytes remain selected.

## Heartbeat and supply-plane restoration

An ordinary-width HEARTBEAT_SEEN trial joins its intended signal pads but
splits accepted APP/USB/protected-battery supply groups. DISPLAY_CLEAR_OK has
the same failure pattern; HEARTBEAT_FALL_CLK has no usable grid endpoint in
this screen. Restricting the search to B.Cu/In4.Cu also fails the pad-group
retention gate. These results cannot be adopted simply because their intended
signal endpoints join.

Further ignored restoration joins some APP/USB groups, reaching a 40-open
copy, but protected-battery groups remain split. A bounded straight plane
bridge restores one APP group in a separate copy; it does not repair the
whole candidate. Six-millimetre adjacent-layer bridge screening and moving
only new heartbeat segments to B.Cu produce no complete successor. Original
39-open copper is never deleted by these trials. Power-path dimensions and
qualification are not established by their continuity checks.

## Other local approaches

A retained-copper endpoint at an added PAIR07 VLED escape preserves 39 opens
but its sampled follow-on graph exhausts at 1,215 nodes. All 304 bounded
three-segment In4.Cu local paths are obstructed. Two nearby isolated VLED
pad groups are also separated by existing row-selection conductors; their
proximity is not proof of a physical join.

U35.2 and U35.3 already belong to one physical group and already have a B.Cu
connection. The precondition guard rejects a proposed duplicate; it is not
counted as progress. Manufacturer Rev. 7 pin descriptions were read through
the [official Analog Devices PDF](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX17048-MAX17049.pdf): CELL is pin 2 and VDD pin 3. Direct download
failed with an HTTP/2 reset and an HTTP/1.1 timeout; no downloaded or modified
vendor bytes are claimed. The existing library audit remains the package
traceability record.

[ADR 0098](../decisions/0098-remaining-enable-test-land-locality.md) separately
bounds a TP13/TP14 experiment with unchanged 1.0 mm lands and
at most 5 mm of ordinary B.Cu lead. The completed 0.10 mm centre-grid screen
finds no complete direct/L-shaped path for either land; both remain fixed. Fixed traces surround the ROW_ENABLE_N
output, including ROW_ENABLE_REQ_N and USB_RAW_LOGIC_READY; further work must
preserve their external contacts rather than merely cross or erase them.

Raw scripts, finite candidate details, logs and rejected PCBs remain ignored
under `hardware/coupon/rev-a/build/zero-open-routing/`. The machine-readable
[sensor result](../../mechanical/review/tmp390-supply-screen.json) is committed;
other ignored prototypes are deliberately not release artifacts. Future
selection still requires an exact complete ledger, native/physical agreement,
unchanged full DRC, source checks, replay/fills, faults and visual review.

The [current open-group inventory](../../mechanical/review/remaining-open-pad-groups.json)
is updated for the latest selected source from actual native connectivity by
[the read-only reporter](../../tools/report-open-pad-groups.py). It lists
numbered pads in every open net group and nearest pad-centre pairs, avoiding
assumptions that two adjacent same-net pins must still be disconnected.
Distances are geometry, never routing or operating evidence.

An additional U52 ground screen samples 2,928 off-pad capture sites within
3 mm of U52.3, using ordinary B.Cu lead plus two adjacent 0.30/0.10 mm
microvias and a 0.50/0.30 mm In2/In3 buried via. Every sampled stack is
obstructed by existing foreign copper before a refill is attempted. No
unsupported central microvia is substituted and no stack is selected.
