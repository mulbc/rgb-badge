#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Bounded, unselected 557-via replacement probe; never edits selected source."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import shutil
import pcbnew as p

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'hardware/coupon/rev-a/staging/led-converter-routing-trial-114mm.kicad_pcb'
DEST = ROOT / 'hardware/coupon/rev-a/build/hdi-centre-via-correction/trial.kicad_pcb'
SHA = '5e07fb866cc059de670e34102045d9dfd88c88f101355fcdbb27253c0ae26e43'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hole-um', type=int, choices=(200,300), default=300)
    args = parser.parse_args()
    destination = DEST.parent / str(args.hole_um) / DEST.name
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SHA
    old = p.LoadBoard(str(SOURCE))
    board = p.LoadBoard(str(SOURCE))
    replacements = []
    for via in board.GetTracks():
        if isinstance(via, p.PCB_VIA) and via.GetViaType() == p.VIATYPE_MICROVIA and (via.TopLayer(), via.BottomLayer()) == (board.GetLayerID('In2.Cu'), board.GetLayerID('In3.Cu')):
            assert via.GetWidth(via.TopLayer()) == 300000 and via.GetDrillValue() == 100000
            replacements.append({'uuid': via.m_Uuid.AsString(), 'net': via.GetNetname(),
                                 'position_iu': [via.GetPosition().x, via.GetPosition().y]})
            via.SetViaType(p.VIATYPE_BURIED)
            via.SetWidth(500000)
            via.SetDrill(args.hole_um * 1000)
    assert len(replacements) == 557
    board.GetDesignSettings().SetBoardThickness(800000)
    p.ZONE_FILLER(board).Fill(board.Zones())
    board.BuildConnectivity()
    pads = lambda b: {q.m_Uuid.AsString(): q for f in b.GetFootprints() for q in f.Pads() if q.GetNetname()}
    connected = lambda b, q: frozenset(z.m_Uuid.AsString() for z in b.GetConnectivity().GetConnectedItems(q) if isinstance(z, p.PAD))
    a, b = pads(old), pads(board)
    changed = []
    for key, pad in a.items():
        before, after = connected(old, pad), connected(board, b[key])
        if before != after:
            changed.append({'pad_uuid': key, 'reference': pad.GetParentFootprint().GetReference(),
                            'pad_number': pad.GetNumber(), 'lost_pad_uuids': sorted(before-after),
                            'gained_pad_uuids': sorted(after-before)})
    destination.parent.mkdir(parents=True, exist_ok=True)
    p.SaveBoard(str(destination), board)
    for ext in ('.kicad_pro', '.kicad_dru'):
        shutil.copyfile(SOURCE.with_suffix(ext), destination.with_suffix(ext))
    (destination.parent / 'fp-lib-table').write_text('(fp_lib_table (lib (name "rgb-badge-coupon")(type "KiCad")(uri "' + str(ROOT/'hardware/coupon/rev-a/footprints/rgb-badge-coupon.pretty') + '")(options "")(descr "Local source")))\n')
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SHA
    report = {'SPDX-License-Identifier': 'CERN-OHL-S-2.0',
              'status': 'UNSELECTED_CENTRE_VIA_EXPANSION_PROBE',
              'source_sha256': SHA, 'candidate_sha256': hashlib.sha256(destination.read_bytes()).hexdigest(),
              'replacements': sorted(replacements, key=lambda r: r['uuid']),
              'new_dimensions_mm': {'pad': .5, 'hole': args.hole_um / 1000, 'board_general_thickness': .8},
              'original_opens': old.GetConnectivity().GetUnconnectedCount(False),
              'candidate_opens': board.GetConnectivity().GetUnconnectedCount(False),
              'changed_pad_clusters': changed,
              'explicit_stackup_added': False, 'fabrication_release_allowed': False,
              'tool_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    destination.with_suffix('.audit.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print('Unselected centre-via probe:', len(replacements), 'replacements,', len(changed), 'pad-cluster changes,', report['candidate_opens'], 'opens')


if __name__ == '__main__':
    main()
