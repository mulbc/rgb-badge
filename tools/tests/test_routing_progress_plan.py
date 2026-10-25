#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Portable negative checks for the routing study's scoped copper exceptions."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('progress',ROOT/'tools/check-routing-progress-plan.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


class PlanGuards(unittest.TestCase):
    def setUp(self):
        digest='da3c3e093acef457ce2d0ebe73b57fd5006b9139a57b7fe8acfcd77e612dc246'
        self.plan=dict(source_sha256=digest,open_edges=100,open_edges_by_net={'GND':100},
                       retired_zero_length_tracks=[['GND',i,0,'B.Cu',200000] for i in range(116)],
                       placements=[],added_copper=[['track','ROW_A0',0,0,1000000,0,'B.Cu',200000]])
        self.manifest=dict(source_sha256=digest,native_open_edges=100,fabrication_release_allowed=False)

    def test_ic_relocation_is_rejected(self):
        self.plan['placements']=[dict(reference='U39',old_position_iu=[0,0],new_position_iu=[1,0])]
        with self.assertRaises(AssertionError):m.validate(self.plan,self.manifest)

    def test_contacted_passive_pose_is_permitted(self):
        self.plan['placements']=[dict(reference='C31',old_position_iu=[0,0],new_position_iu=[1,0])]
        m.validate(self.plan,self.manifest)

    def test_usb_series_resistor_move_is_rejected(self):
        for ref in ('R45','R46'):
            self.plan['placements']=[dict(reference=ref,old_position_iu=[0,0],new_position_iu=[1,0])]
            with self.assertRaises(AssertionError):m.validate(self.plan,self.manifest)

    def test_accepted_150_checkpoint_is_preserved(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        m.validate_prior_checkpoint(plan)

    def test_accepted_150_copper_cannot_be_dropped(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        prior=json.loads((ROOT/'mechanical/review/routing-progress-150-checkpoint.json').read_text())
        plan['added_copper'].remove(prior['added_copper'][0])
        with self.assertRaises(AssertionError):m.validate_prior_checkpoint(plan)

    def test_accepted_150_join_cannot_be_lost(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        prior=json.loads((ROOT/'mechanical/review/routing-progress-150-checkpoint.json').read_text())
        net,before,after=prior['physical_group_witnesses'][0]
        member=after[0]
        for row in plan['physical_group_witnesses']:
            if row[0]==net:row[2]=[x for x in row[2] if x!=member]
        with self.assertRaises(AssertionError):m.validate_prior_checkpoint(plan)

    def power_zone(self):
        return dict(name='ADR0049-fixture',net='+5V_USB',layer='In1.Cu',
                    polygons_iu=[dict(outer=[[1000000,1000000],[2000000,1000000],[2000000,2000000]],holes=[])],definition=['zone'])

    def test_power_parcel_cannot_change_enable_net(self):
        zone=self.power_zone();zone['net']='DISPLAY_ENABLE';self.plan['power_zones']=[zone]
        with self.assertRaises(AssertionError):m.validate(self.plan,self.manifest)

    def test_power_parcel_stays_inside_board_margin(self):
        zone=self.power_zone();zone['polygons_iu'][0]['outer'][0][0]=100000;self.plan['power_zones']=[zone]
        with self.assertRaises(AssertionError):m.validate(self.plan,self.manifest)

    def test_duplicate_power_parcel_is_rejected(self):
        zone=self.power_zone();self.plan['power_zones']=[zone,zone]
        with self.assertRaises(AssertionError):m.validate(self.plan,self.manifest)

    def test_track_retirement_cannot_be_an_orphan_via(self):
        self.plan['retired_orphan_microvias']=[self.plan['added_copper'][0]]
        with self.assertRaises(AssertionError):m.validate(self.plan,self.manifest)

    def test_valid_low_current_signal(self):m.validate(self.plan,self.manifest)

    def test_narrow_power_is_rejected(self):
        self.plan['added_copper'][0][1]='VLED';self.plan['added_copper'][0][-1]=120000
        with self.assertRaises(AssertionError):m.validate(self.plan,self.manifest)

    def test_narrow_signal_is_rejected(self):
        self.plan['added_copper'][0][-1]=120000
        with self.assertRaises(AssertionError):m.validate(self.plan,self.manifest)

    def test_zero_length_track_is_rejected(self):
        self.plan['added_copper'][0][4]=0
        with self.assertRaises(AssertionError):m.validate(self.plan,self.manifest)

    def test_long_setting_route_is_rejected(self):
        self.plan['added_copper'][0][1]='TMP_HOT_SET';self.plan['added_copper'][0][4]=6000000
        with self.assertRaises(AssertionError):m.validate(self.plan,self.manifest)

    def test_skipped_microvia_layer_is_rejected(self):
        self.plan['added_copper']=[['via','ROW_A0',0,0,'B.Cu','In3.Cu',300000,100000]]
        with self.assertRaises(AssertionError):m.validate(self.plan,self.manifest)

    def test_smaller_microvia_is_rejected(self):
        self.plan['added_copper']=[['via','ROW_A0',0,0,'B.Cu','In4.Cu',250000,100000]]
        with self.assertRaises(AssertionError):m.validate(self.plan,self.manifest)

    def test_edge_count_cannot_be_relabelled(self):
        self.plan['open_edges_by_net']['GND']=149
        with self.assertRaises(AssertionError):m.validate(self.plan,self.manifest)

    def test_release_claim_is_rejected(self):
        self.manifest['fabrication_release_allowed']=True
        with self.assertRaises(AssertionError):m.validate(self.plan,self.manifest)


if __name__=='__main__':unittest.main()
