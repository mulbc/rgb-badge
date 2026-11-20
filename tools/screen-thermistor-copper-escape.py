#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Read-only ADR 0122 thermistor escape screen; never saves or edits a PCB.

Run with native KiCad Python. Finite copper/hole screening does not include
zone refills, connectivity, DRC or electrical/thermal qualification.
"""
import argparse
import pcbnew as p
import hashlib
import json
import runpy
from pathlib import Path
from collections import defaultdict, Counter


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--offset', action='store_true')
    args = parser.parse_args()
    args.output = args.output.resolve()
    build = Path(__file__).resolve().parents[1]/'hardware/coupon/rev-a/build'
    assert build.resolve() in args.output.parents and args.output.suffix == '.json'
    args.output.parent.mkdir(parents=True, exist_ok=True)
    root = Path(__file__).resolve().parents[1]
    source = root / 'hardware/coupon/rev-a/staging/led-usb-en1-routing-trial-114mm.kicad_pcb'
    sha = lambda x: hashlib.sha256(x.read_bytes()).hexdigest()
    before = sha(source)
    assert before == '92f942e46281475cbdadf6e9a0ad7a0d531e38c3032f85a4206bbf9e9bc1fccd'
    b = p.LoadBoard(str(source))
    uid = '7ffcb702-53ec-5778-9cd1-6c4d4972e179'
    old = next((t for t in b.GetTracks() if t.m_Uuid.AsString() == uid))
    sig = runpy.run_path(str(root/'tools/check-routing-progress-trial.py'))['signature']
    assert old.GetNetname() == 'COL_01_R'
    items = list(b.GetTracks()) + [q for f in b.GetFootprints() for q in f.Pads()]
    contacts = []
    for o in items:
        if o.m_Uuid.AsString() != uid and o.IsOnLayer(p.In4_Cu) and (o.GetNetCode() == old.GetNetCode()) and old.GetEffectiveShape(p.In4_Cu).Collide(o.GetEffectiveShape(p.In4_Cu), 0):
            contacts.append(dict(uuid=o.m_Uuid.AsString(), pad=[o.GetParentFootprint().GetReference(), o.GetNumber()] if isinstance(o, p.PAD) else None, signature=list(sig(b, o)) if not isinstance(o, p.PAD) else None, position_iu=list(o.GetPosition())))
    bins = defaultdict(list)

    def cells(box):
        return [(x, y) for x in range(box.GetX() // 1000000, box.GetRight() // 1000000 + 1) for y in range(box.GetY() // 1000000, box.GetBottom() // 1000000 + 1)]
    for o in items:
        for l in [p.In3_Cu, p.In4_Cu, p.B_Cu]:
            if o.IsOnLayer(l):
                bb = o.GetBoundingBox()
                bb.Inflate(501000)
                for c in cells(bb):
                    bins[(l, *c)].append(o)

    def blockers(t, l):
        obs = {o.m_Uuid.AsString(): o for c in cells(t.GetBoundingBox()) for o in bins[(l, *c)]}
        return [uid for uid, o in obs.items() if o.GetNetCode() != t.GetNetCode() and t.GetEffectiveShape(l).Collide(o.GetEffectiveShape(l), 199990)]
    counts = Counter()
    hits = Counter()
    clear = []
    for yy in range(15800000, 16300001, 50000) if args.offset else [16250000]:
        for x1 in range(53500000, 54400001, 50000):
            for x2 in range(55300000, 56000001, 50000):
                counts['sampled'] += 1
                parts = []
                for x in [x1, x2]:
                    v = p.PCB_VIA(b)
                    v.SetPosition(p.VECTOR2I(x, yy))
                    v.SetWidth(300000)
                    v.SetDrill(100000)
                    v.SetViaType(p.VIATYPE_MICROVIA)
                    v.SetLayerPair(p.In3_Cu, p.In4_Cu)
                    v.SetNetCode(old.GetNetCode())
                    parts.append(v)
                t = p.PCB_TRACK(b)
                t.SetStart(p.VECTOR2I(x1, yy))
                t.SetEnd(p.VECTOR2I(x2, yy))
                t.SetWidth(200000)
                t.SetLayer(p.In3_Cu)
                t.SetNetCode(old.GetNetCode())
                parts.append(t)
                for xx in [x1, x2]:
                    if yy == 16250000:
                        continue
                    stub = p.PCB_TRACK(b)
                    stub.SetStart(p.VECTOR2I(xx, yy))
                    stub.SetEnd(p.VECTOR2I(xx, 16250000))
                    stub.SetWidth(200000)
                    stub.SetLayer(p.In4_Cu)
                    stub.SetNetCode(old.GetNetCode())
                    parts.append(stub)
                bad = []
                for part in parts:
                    for l in [p.In3_Cu, p.In4_Cu]:
                        if part.IsOnLayer(l):
                            bad += blockers(part, l)
                if bad:
                    counts['copper_obstructed'] += 1
                    hits.update(set(bad))
                    continue
                holebad = False
                for v in parts[:2]:
                    for o in items:
                        if isinstance(o, p.PCB_VIA) or (isinstance(o, p.PAD) and max(o.GetDrillSize()) > 0):
                            if v.GetEffectiveHoleShape().Collide(o.GetEffectiveHoleShape(), 250000):
                                holebad = True
                                hits[o.m_Uuid.AsString()] += 1
                if holebad:
                    counts['hole_obstructed'] += 1
                    continue
                v = p.PCB_VIA(b)
                v.SetPosition(p.VECTOR2I(54850000, 16225000))
                v.SetWidth(300000)
                v.SetDrill(100000)
                v.SetViaType(p.VIATYPE_MICROVIA)
                v.SetLayerPair(p.In4_Cu, p.B_Cu)
                v.SetNetCode(b.FindNet('CHARGER_TS').GetNetCode())
                bad = [s for l in [p.In4_Cu, p.B_Cu] for s in blockers(v, l) if s != uid]
                if any((v.GetEffectiveShape(p.In4_Cu).Collide(q.GetEffectiveShape(p.In4_Cu), 199990) for q in parts if q.IsOnLayer(p.In4_Cu))):
                    bad.append('new-colour-capture')
                if bad:
                    counts['sense_capture_obstructed'] += 1
                    hits.update(set(bad))
                    continue
                section = p.PCB_TRACK(b)
                section.SetStart(p.VECTOR2I(x1, 16250000))
                section.SetEnd(p.VECTOR2I(x2, 16250000))
                section.SetWidth(200000)
                section.SetLayer(p.In4_Cu)
                section.SetNetCode(old.GetNetCode())
                contact_ids = {r['uuid'] for r in contacts}
                lost = [o.m_Uuid.AsString() for o in items if o.m_Uuid.AsString() in contact_ids and section.GetEffectiveShape(p.In4_Cu).Collide(o.GetEffectiveShape(p.In4_Cu), 0)]
                if lost:
                    counts['intermediate_contacts'] += 1
                    continue
                counts['clear_shape_template'] += 1
                clear.append([x1, x2, yy])
    assert sha(source) == before
    out = dict(spdx_license_identifier='CERN-OHL-S-2.0', offset_screen=args.offset, source_sha256=before, source_unchanged=True, status='READ_ONLY_UNSELECTED_TRANSFER_SCREEN', counts=dict(counts), clear=clear, original_contacts=contacts, blockers=hits.most_common(), limitations=['No zones/refills/group/DRC screened', 'TS capture alone does not join its charger endpoint'], fabrication_release_allowed=False, tool_sha256=sha(Path(__file__)))
    args.output.write_text(json.dumps(out, indent=2) + '\n')
    print(dict(counts))


if __name__ == '__main__':
    main()
