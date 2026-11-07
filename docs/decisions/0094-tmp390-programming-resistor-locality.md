<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0094: Localize the TMP390 cold programming resistor

Date: 2026-11-07
Status: Accepted for the validated 40-open remaining-routing successor.

TI TMP390 Rev A section 10.1 / Figure 10-1 places both programming resistors
near the sensor to limit leakage and parasitic capacitance. The 41-open study
leaves U39.2–R90.1 (TMP_COLD_SET) open with a remote resistor. Screen a local
R90 placement and ordinary 0.20 mm B.Cu connection, keeping U39 and its thermal
location fixed. R90 remains Panasonic ERJ2RKF1402X, 14 kΩ, 1%, in its existing
local footprint; no value, pin, package or circuit substitution is authorized.

Bound each resistor pad within 3 mm of its corresponding U39 SETB/GND pad.
Require unchanged local pads and identities, native courtyard/foreign-copper
clearance including no-net pads, and a common local B.Cu ground polygon for
R90.2 and U39.3. Retain every accepted copper item and every 41-open pad group;
no new dangling old ground via is permitted. New signal copper stays 0.20 mm;
no new via is needed or authorized by this bounded study. Refill and reject
any lost live group or copper/net propagation. Full native DRC, source, exact
ledger/replay and fault validation precede selection.

Temperature trip/hysteresis programming, thermal-sensor position, source/cell/
charge/LED/regulator limits, NTC/protection, default-disabled permissions and
firmware remain unchanged. Local placement does not qualify actual threshold,
leakage, thermal coupling, noise, assembly, stack or fabrication. Existing
independent Gate A and all electrical/process/fit holds remain open.

Sources read visually: TI TMP390 Rev A pages 3 and 18, package audit already
recorded locally; Panasonic ERJ catalogue dated 29-May-2025, ERJ2R dimensions
on page 4. Both public PDFs are cached byte-for-byte only in the ignored vendor
reference directory and indexed there by SHA-256. They are reference sheets,
not signed delivery/approval specifications.

- https://www.ti.com/lit/ds/symlink/tmp390.pdf
- https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf

## Exact local return replacement scope

The R90-only finite study finds 94 courtyard/copper-clear poses but no ordinary
local B.Cu path, including the tested extra bends. R89's existing GND return
closes the cold-pin exit. Permit this single additional scope before further
implementation: replace only the 0.20 mm B.Cu GND track
(59.865,16.000)–(58.365,16.000) mm with a 0.20 mm B.Cu local detour. Keep R89's
pose, hot-trip resistor, existing vertical feed and every other original copper
item. Bind the retired track, replacement rows, both original endpoints and
all direct source-layer contacts in the exact ledger. This is an explicit
exception to ADR 0093's no-additional-retirement continuation, not permission
to retire other tracks or original vias.

Bound replacement copper to x=58.30..60.75 mm, y=16.00..18.25 mm and total
length below 8 mm. Require retained contacts, every 41-open live group, local
shared ground polygon and unchanged 104 native findings. The target is a
cold-pin route inside the reshaped local return, with an unchanged 14 kΩ
resistor and fixed sensor/hot-programming geometry. Independent electrical,
leakage/noise/return-path/process/fit and Gate A qualification remain open.

## Selected bounded result

The exact successor moves R90 from (34.75,11.75) mm, 180° B.Cu to
(60.00,16.75) mm, 0° B.Cu. Three B.Cu cold tracks total 2.385 mm. Five
B.Cu GND replacement tracks total 5.770 mm, retaining both original endpoints
and all five direct source-layer contacts. The 1.500 mm original return is
the only retirement. Cold/ground pad-centre distances to U39.2/U39.3 are
1.688409/2.262902 mm, with a shared individual filled B.Cu ground polygon.
Native/physical 40 opens, exact unchanged 104 findings, stable replay/fills,
source and fifteen-fault checks pass. Electrical/thermal/process/fit and
independent Gate A remain open.
