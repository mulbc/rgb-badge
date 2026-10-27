#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Isolated native faults for the routing/placement checkpoint's verifier."""
from collections import Counter
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest
import pcbnew as p

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('check',ROOT/'tools/check-routing-progress-trial.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)


class RoutingProgressGuards(unittest.TestCase):
    def setUp(self):
        self.old=p.LoadBoard(str(c.SOURCE));self.new=p.LoadBoard(str(c.OUTPUT))
        self.plan=json.loads(c.PLAN.read_text());self.parts={f.GetReference():f for f in self.new.GetFootprints()}
        originals=Counter(c.signature(self.old,t) for t in self.old.GetTracks());self.added=[]
        for item in self.new.GetTracks():
            sig=c.signature(self.new,item)
            if originals[sig]:originals[sig]-=1
            else:self.added.append(item)

    def reject(self):
        p.ZONE_FILLER(self.new).Fill(self.new.Zones());self.new.BuildConnectivity()
        with self.assertRaises(AssertionError):c.validate_geometry(self.old,self.new,self.plan)

    def test_zero_cleanup_preserves_every_source_group_exactly(self):
        groups={}
        for part in self.old.GetFootprints():
            for pad in part.Pads():
                if pad.GetNetname():groups.setdefault(c.physical_cluster(self.old,pad),pad)
        original_items=list(self.old.GetTracks())
        retired=[t for t in original_items if not isinstance(t,p.PCB_VIA) and t.GetStart()==t.GetEnd()]
        self.assertEqual(len(retired),116)
        for item in retired:self.old.Remove(item)
        p.ZONE_FILLER(self.old).Fill(self.old.Zones());self.old.BuildConnectivity()
        self.assertEqual(self.old.GetConnectivity().GetUnconnectedCount(False),215)
        for group,pad in groups.items():self.assertEqual(group,c.physical_cluster(self.old,pad))

    def test_selected_checkpoint_passes(self):
        self.assertLessEqual(c.validate_geometry(self.old,self.new,self.plan)['native_open_edges'],100)

    def test_unreviewed_ic_move(self):
        self.parts['U39'].Move(p.VECTOR2I(100000,0));self.reject()

    def test_reviewed_pose_not_applied(self):
        entry=self.plan['placements'][0];part=self.parts[entry['reference']]
        part.SetPosition(p.VECTOR2I(*entry['old_position_iu']));part.SetOrientationDegrees(entry['old_angle_deg']);self.reject()

    def test_duplicate_physical_drain_land_changed(self):
        pads=[q for q in self.parts['PAIR01'].Pads() if q.GetNumber()=='3']
        self.assertEqual(len(pads),2);pads[0].Move(p.VECTOR2I(100000,0));self.reject()

    def test_nonzero_original_copper_removed(self):
        for item in self.new.GetTracks():
            if item.GetNetname()=='ROW_00_A' and not isinstance(item,p.PCB_VIA) and item.GetStart()!=item.GetEnd():
                self.new.Remove(item);break
        else:self.fail('Original row copper witness missing')
        self.reject()

    def test_94_checkpoint_cannot_be_retired_in_candidate_and_plan(self):
        prior=json.loads((ROOT/'mechanical/review/routing-progress-94-checkpoint.json').read_text())
        old=json.loads((ROOT/'mechanical/review/routing-progress-100-checkpoint.json').read_text())
        row=next(row for row in prior['added_copper'] if row[0]=='track' and row[1]=='MODE_BOOT_N' and row not in old['added_copper'])
        item=next(t for t in self.new.GetTracks() if c.signature(self.new,t)==tuple(row))
        self.new.Remove(item);self.plan['added_copper'].remove(row)
        self.new.BuildConnectivity()
        with self.assertRaisesRegex(AssertionError,'Accepted 94-edge copper changed'):
            c.validate_geometry(self.old,self.new,self.plan)

    def test_91_checkpoint_cannot_be_retired_in_candidate_and_plan(self):
        prior=json.loads((ROOT/'mechanical/review/routing-progress-91-checkpoint.json').read_text())
        old=json.loads((ROOT/'mechanical/review/routing-progress-94-checkpoint.json').read_text())
        row=next(row for row in prior['added_copper'] if row[0]=='track' and row[1]=='MODE_BOOT_N' and row not in old['added_copper'])
        item=next(t for t in self.new.GetTracks() if c.signature(self.new,t)==tuple(row))
        self.new.Remove(item);self.plan['added_copper'].remove(row);self.new.BuildConnectivity()
        with self.assertRaisesRegex(AssertionError,'Accepted 91-edge copper changed'):
            c.validate_geometry(self.old,self.new,self.plan)

    def test_84_checkpoint_cannot_be_retired_in_candidate_and_plan(self):
        prior=json.loads((ROOT/'mechanical/review/routing-progress-84-checkpoint.json').read_text())
        old=json.loads((ROOT/'mechanical/review/routing-progress-91-checkpoint.json').read_text())
        row=next(row for row in prior['added_copper'] if row[0]=='track' and row[1]=='ROW_A2' and row not in old['added_copper'])
        item=next(t for t in self.new.GetTracks() if c.signature(self.new,t)==tuple(row))
        self.new.Remove(item);self.plan['added_copper'].remove(row);self.new.BuildConnectivity()
        with self.assertRaisesRegex(AssertionError,'Accepted 84-edge copper changed'):
            c.validate_geometry(self.old,self.new,self.plan)

    def test_added_route_detached(self):
        next(t for t in self.added if not isinstance(t,p.PCB_VIA)).Move(p.VECTOR2I(0,5000000));self.reject()

    def test_land_corner_radius_changed(self):
        pad=next(iter(self.parts['R89'].Pads()));value=pad.GetRoundRectRadiusRatio()
        pad.SetRoundRectRadiusRatio(.1 if value!=.1 else .2);self.reject()

    def test_pad_net_changed(self):
        pad=next(q for q in self.parts['U3'].Pads() if q.GetNumber()=='4')
        pad.SetNet(self.new.FindNet('GND'));self.reject()

    def test_power_trace_narrowed(self):
        item=next(t for t in self.added if not isinstance(t,p.PCB_VIA) and t.GetNetname()=='GND')
        item.SetWidth(120000);self.reject()

    def test_neck_metadata_cannot_be_omitted(self):
        self.assertTrue(self.plan.get('pad_necks'))
        self.plan.pop('pad_necks');self.reject()

    def test_neck_policy_rejects_coordinated_geometry_edit(self):
        entry=self.plan['pad_necks'][0];row=entry['track']
        original=list(row)
        item=next(t for t in self.added if c.signature(self.new,t)==tuple(row))
        # Even a coordinated candidate/plan edit cannot extend the exception.
        item.SetEnd(p.VECTOR2I(row[4],row[5]+100000));row[5]+=100000
        self.plan['added_copper']=[list(row) if r==original else r for r in self.plan['added_copper']]
        with self.assertRaises(AssertionError):c.validate_geometry(self.old,self.new,self.plan)

    def test_nonadjacent_microvia(self):
        via=next(t for t in self.added if isinstance(t,p.PCB_VIA));stack=list(self.new.GetEnabledLayers().CuStack())
        via.SetLayerPair(stack[0],stack[2]);self.reject()

    def test_zero_length_source_artifact_restored(self):
        net,x,y,layer,width=self.plan['retired_zero_length_tracks'][0]
        item=p.PCB_TRACK(self.new);item.SetStart(p.VECTOR2I(x,y));item.SetEnd(p.VECTOR2I(x,y))
        item.SetLayer(self.new.GetLayerID(layer));item.SetWidth(width);item.SetNetCode(self.new.FindNet(net).GetNetCode());self.new.Add(item);self.reject()

    def test_original_usb_branch_cannot_be_relabelled(self):
        originals={c.signature(self.old,t) for t in self.old.GetTracks()}
        item=next(t for t in self.new.GetTracks() if not isinstance(t,p.PCB_VIA) and t.GetNetname()=='+3V3_USB' and c.signature(self.new,t) in originals)
        item.SetNetCode(self.new.FindNet('+3V3_APP').GetNetCode())
        # A refill may propagate the neighbouring net and undo this injected fault.
        with self.assertRaises(AssertionError):c.validate_geometry(self.old,self.new,self.plan)

    def test_original_zone_clearance_changed(self):
        zone=next(z for z in self.new.Zones() if not z.GetZoneName().startswith('ADR0049-'))
        zone.SetLocalClearance(120000);self.reject()

    def test_power_zone_net_changed(self):
        zone=next(z for z in self.new.Zones() if z.GetZoneName().startswith('ADR0049-'))
        zone.SetNetCode(self.new.FindNet('GND').GetNetCode());self.reject()

    def test_power_zone_boundary_changed(self):
        zone=next(z for z in self.new.Zones() if z.GetZoneName().startswith('ADR0049-'))
        zone.Move(p.VECTOR2I(100000,0));self.reject()

    def test_power_zone_unanchored_islands_allowed(self):
        zone=next(z for z in self.new.Zones() if z.GetZoneName().startswith('ADR0049-'))
        zone.SetIslandRemovalMode(p.ISLAND_REMOVAL_MODE_NEVER);self.reject()

    def test_orphan_via_restored_without_witness(self):
        _,net,x,y,top,bottom,diameter,drill=self.plan['retired_orphan_microvias'][0]
        via=p.PCB_VIA(self.new);via.SetNetCode(self.new.FindNet(net).GetNetCode())
        via.SetPosition(p.VECTOR2I(x,y));via.SetViaType(p.VIATYPE_MICROVIA)
        via.SetLayerPair(self.new.GetLayerID(top),self.new.GetLayerID(bottom));via.SetWidth(diameter);via.SetDrill(drill)
        self.new.Add(via);self.reject()

    def test_exact_mpn_changed(self):
        self.parts['R89'].GetField('MPN').SetText('UNREVIEWED_SUBSTITUTE');self.reject()


if __name__=='__main__':
    if any(arg.startswith('RoutingProgressGuards.') for arg in sys.argv[1:]):unittest.main()
    else:
        names=unittest.defaultTestLoader.getTestCaseNames(RoutingProgressGuards)
        for name in names:subprocess.run([sys.executable,__file__,'RoutingProgressGuards.'+name,'-v'],check=True)
        print('All %d isolated native routing-progress guard checks passed.'%len(names))
