#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Replay the unselected sensor gateway and real supply escape in memory."""
import json
import runpy
import uuid
import pcbnew as p
import routing_pair01_supply as source


def main():
    root = source.ROOT
    gateway = root / 'mechanical/review/sensor-gateway-discovery.json'
    escape = root / 'mechanical/review/sensor-supply-escape-discovery.json'
    assert source.sha(source.OUTPUT) == source.BOARD_SHA
    assert source.sha(gateway) == 'c8253d8a14f01244e920160d96a257e4d2dbe9b65f31209ddb1f34786c4763f7'
    assert source.sha(escape) == '6b8adae557b13638a23a07edd0163c02ce9d49a6fe26e091ed5e5dac6555abf1'
    plan, seed = (json.loads(path.read_text()) for path in (gateway, escape))
    assert plan['source_sha256'] == seed['source_sha256'] == source.BOARD_SHA
    assert plan['selected'] is seed['selected'] is False
    assert plan['fabrication_release_allowed'] is seed['fabrication_release_allowed'] is False
    old, board = (p.LoadBoard(str(source.OUTPUT)) for _ in range(2))
    retired = {row['uuid'] for row in plan['retired_copper']}
    assert len(retired) == 6
    assert source.contact_catalog(old, retired) == plan['source_retirement_contacts']
    helper = source.helper()
    held = []
    tracks = {o.m_Uuid.AsString(): o for o in board.GetTracks()}
    for row in plan['retired_copper']:
        obj = tracks[row['uuid']]
        assert list(helper['signature'](board, obj)) == row['signature']
        assert (int(obj.GetViaType()) if isinstance(obj, p.PCB_VIA) else None) == row['via_type']
        board.Remove(obj)
        held.append(obj)
    offsets = {'U39': 375000, 'R89': 100000, 'R90': 400000}
    assert plan['poses'].keys() == offsets.keys()
    for ref, pose in plan['poses'].items():
        fp = board.FindFootprintByReference(ref)
        assert pose['layer'] == 'B.Cu' and fp.GetLayer() == p.B_Cu
        assert fp.GetOrientationDegrees() % 360 == pose['orientation_degrees'] % 360
        x, y = fp.GetPosition()
        assert pose['position_iu'] == [x + offsets[ref], y]
        fp.SetPosition(p.VECTOR2I(*pose['position_iu']))
    for a in old.GetFootprints():
        z = board.FindFootprintByReference(a.GetReference())
        assert a.m_Uuid == z.m_Uuid and a.GetFPIDAsString() == z.GetFPIDAsString()
        assert sorted((v.GetName(), v.GetText(), v.m_Uuid.AsString()) for v in a.GetFields()) == sorted((v.GetName(), v.GetText(), v.m_Uuid.AsString()) for v in z.GetFields())
        assert sorted(helper['local_pad_signature'](q) for q in a.Pads()) == sorted(helper['local_pad_signature'](q) for q in z.Pads())
        pads = {q.m_Uuid.AsString(): q for q in z.Pads()}
        for q in a.Pads():
            x, y = q.GetPosition()
            assert list(pads[q.m_Uuid.AsString()].GetPosition()) == [x + offsets.get(a.GetReference(), 0), y]
    add = runpy.run_path(str(root / 'tools/generate-gauge-supply-routing.py'))['add']
    added = set()
    for label, rows in [('gateway', plan['fixed_geometry']), ('escape', seed['escape']['new_copper'])]:
        for i, row in enumerate(rows):
            uid = str(uuid.uuid5(uuid.NAMESPACE_URL, 'rgb-badge:sensor-discovery:' + label + ':' + str(i)))
            add(board, dict(row, uuid=uid))
            added.add(uid)
    new_tracks = {o.m_Uuid.AsString(): o for o in board.GetTracks()}
    for uid in added:
        obj = new_tracks[uid]
        if isinstance(obj, p.PCB_VIA):
            assert obj.GetViaType() == p.VIATYPE_MICROVIA
            assert (obj.TopLayer(), obj.BottomLayer()) == (p.In4_Cu, p.B_Cu)
            assert obj.GetWidth(obj.TopLayer()) == 300000 and obj.GetDrillValue() == 100000
        else:
            assert obj.GetWidth() == 200000 and obj.GetLayer() in (p.B_Cu, p.In4_Cu)
    source.hole_audit(board, added)
    pads = [q for fp in board.GetFootprints() for q in fp.Pads()]
    objects = list(new_tracks.values()) + pads
    layers = (p.F_Cu, p.In1_Cu, p.In2_Cu, p.In3_Cu, p.In4_Cu, p.B_Cu)
    targets = [new_tracks[uid] for uid in added] + [q for q in pads if q.GetParentFootprint().GetReference() in offsets]
    for obj in targets:
        box = obj.GetBoundingBox()
        box.Inflate(200000)
        for other in objects:
            if obj.m_Uuid == other.m_Uuid or obj.GetNetCode() == other.GetNetCode():
                continue
            if isinstance(obj, p.PAD) and isinstance(other, p.PAD) and obj.GetParentFootprint().m_Uuid == other.GetParentFootprint().m_Uuid:
                continue  # Unchanged package-internal pad geometry only.
            bounds = other.GetBoundingBox()
            if box.GetRight() < bounds.GetX() or bounds.GetRight() < box.GetX() or box.GetBottom() < bounds.GetY() or bounds.GetBottom() < box.GetY():
                continue
            for layer in layers:
                if obj.IsOnLayer(layer) and other.IsOnLayer(layer):
                    assert not obj.GetEffectiveShape(layer).Collide(other.GetEffectiveShape(layer), 199990), 'New external clearance: ' + obj.m_Uuid.AsString() + '/' + other.m_Uuid.AsString()
    geometry = runpy.run_path(str(root / 'tools/screen-converter-inductor-locality.py'))
    for ref in offsets:
        fp = board.FindFootprintByReference(ref)
        for other in board.GetFootprints():
            if other.GetLayer() != p.B_Cu or other.GetReference() == ref:
                continue
            assert all(not geometry['geometry'].intersects(a, z) for a in geometry['courtyards'](fp) for z in geometry['courtyards'](other)), 'Courtyard collision: ' + ref + '/' + other.GetReference()
    p.ZONE_FILLER(board).Fill(board.Zones())
    board.BuildConnectivity()
    aa, original, attached_old = source.components(old)
    bb, current, attached = source.components(board)
    assert aa.keys() == bb.keys() and len(original) == len(current) == 211
    lookup = {u: (g, cu) for g, (_, cu) in current.items() for u in g}
    for group, (uid, copper) in original.items():
        new_group, new_copper = lookup[uid]
        assert group <= new_group and copper - retired <= new_copper
    assert len(attached) == len(new_tracks) and added <= attached
    assert len(attached_old - retired) == 19343
    assert board.GetConnectivity().GetUnconnectedCount(False) == len(current) - len({q.GetNetname() for q in bb.values()}) == 23
    for ref, pin, count in [('C71', '2', 197), ('R18', '1', 38), ('U31', '12', 32), ('U39', '1', 2), ('U39', '2', 2), ('U39', '6', 4)]:
        pad = next(q for q in board.FindFootprintByReference(ref).Pads() if q.GetNumber() == pin)
        assert len(lookup[pad.m_Uuid.AsString()][0]) == count
    assert source.sha(source.OUTPUT) == source.BOARD_SHA
    print(json.dumps(dict(native_opens=23, physical_opens=23, prior_groups_preserved=211, retained_attached_source_copper=19343, orphan_copper=0, selected=False, pcb_written=False, full_drc_qualified=False, fabrication_release_allowed=False)))


if __name__ == '__main__':
    main()
