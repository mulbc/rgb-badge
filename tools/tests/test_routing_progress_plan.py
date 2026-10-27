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

    def test_accepted_100_checkpoint_is_preserved(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        m.validate_100_checkpoint(plan)

    def test_accepted_100_copper_cannot_be_dropped(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        prior=json.loads((ROOT/'mechanical/review/routing-progress-100-checkpoint.json').read_text())
        plan['added_copper'].remove(prior['added_copper'][-1])
        with self.assertRaises(AssertionError):m.validate_100_checkpoint(plan)

    def test_accepted_100_join_cannot_be_lost(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        prior=json.loads((ROOT/'mechanical/review/routing-progress-100-checkpoint.json').read_text())
        net,before,after=prior['physical_group_witnesses'][0];member=after[-1]
        for row in plan['physical_group_witnesses']:
            if row[0]==net:row[2]=[x for x in row[2] if x!=member]
        with self.assertRaises(AssertionError):m.validate_100_checkpoint(plan)

    def test_accepted_94_checkpoint_is_preserved(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        m.validate_94_checkpoint(plan)

    def test_accepted_94_copper_cannot_be_dropped(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        prior=json.loads((ROOT/'mechanical/review/routing-progress-94-checkpoint.json').read_text())
        new=next(row for row in prior['added_copper'] if row not in json.loads((ROOT/'mechanical/review/routing-progress-100-checkpoint.json').read_text())['added_copper'])
        plan['added_copper'].remove(new)
        with self.assertRaises(AssertionError):m.validate_94_checkpoint(plan)

    def test_accepted_94_join_cannot_be_lost(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        prior=json.loads((ROOT/'mechanical/review/routing-progress-94-checkpoint.json').read_text())
        row=next(row for row in prior['physical_group_witnesses'] if row[0]=='MODE_BOOT_N')
        member=next(item for item in row[2] if item[0]=='SW1')
        for witness in plan['physical_group_witnesses']:
            if witness[0]==row[0]:witness[2]=[item for item in witness[2] if item!=member]
        with self.assertRaises(AssertionError):m.validate_94_checkpoint(plan)

    def test_accepted_94_neck_metadata_cannot_change(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        plan['pad_necks']=[]
        with self.assertRaises(AssertionError):m.validate_94_checkpoint(plan)

    def test_accepted_91_checkpoint_is_preserved(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        m.validate_91_checkpoint(plan)

    def test_accepted_91_copper_cannot_be_dropped(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        prior=json.loads((ROOT/'mechanical/review/routing-progress-91-checkpoint.json').read_text())
        old=json.loads((ROOT/'mechanical/review/routing-progress-94-checkpoint.json').read_text())
        row=next(row for row in prior['added_copper'] if row not in old['added_copper'])
        plan['added_copper'].remove(row)
        with self.assertRaises(AssertionError):m.validate_91_checkpoint(plan)

    def test_accepted_91_join_cannot_be_lost(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        for row in plan['physical_group_witnesses']:
            if row[0]=='MODE_BOOT_N':row[2]=[item for item in row[2] if item[0]!='TP3']
        with self.assertRaises(AssertionError):m.validate_91_checkpoint(plan)

    def test_accepted_84_checkpoint_is_preserved(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        m.validate_84_checkpoint(plan)

    def test_accepted_84_copper_cannot_be_dropped(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        prior=json.loads((ROOT/'mechanical/review/routing-progress-84-checkpoint.json').read_text())
        old=json.loads((ROOT/'mechanical/review/routing-progress-91-checkpoint.json').read_text())
        row=next(row for row in prior['added_copper'] if row not in old['added_copper'])
        plan['added_copper'].remove(row)
        with self.assertRaises(AssertionError):m.validate_84_checkpoint(plan)

    def test_accepted_84_join_cannot_be_lost(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        for row in plan['physical_group_witnesses']:
            if row[0]=='ROW_A2':row[2]=[item for item in row[2] if item[0]!='U2']
        with self.assertRaises(AssertionError):m.validate_84_checkpoint(plan)

    def test_accepted_82_checkpoint_is_preserved(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        m.validate_82_checkpoint(plan)

    def test_accepted_82_copper_cannot_be_dropped(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        prior=json.loads((ROOT/'mechanical/review/routing-progress-82-checkpoint.json').read_text())
        old=json.loads((ROOT/'mechanical/review/routing-progress-84-checkpoint.json').read_text())
        row=next(row for row in prior['added_copper'] if row not in old['added_copper'])
        plan['added_copper'].remove(row)
        with self.assertRaises(AssertionError):m.validate_82_checkpoint(plan)

    def test_accepted_82_join_cannot_be_lost(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        for row in plan['physical_group_witnesses']:
            if row[0]=='ROW_A1':row[2]=[item for item in row[2] if item[0]!='U3']
        with self.assertRaises(AssertionError):m.validate_82_checkpoint(plan)

    def test_accepted_76_checkpoint_is_preserved(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        m.validate_76_checkpoint(plan)

    def test_accepted_76_copper_cannot_be_dropped(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        prior=json.loads((ROOT/'mechanical/review/routing-progress-76-checkpoint.json').read_text())
        row=next(row for row in prior['added_copper'] if row[1]=='USB_CONN_DP')
        plan['added_copper'].remove(row)
        with self.assertRaises(AssertionError):m.validate_76_checkpoint(plan)

    def test_accepted_76_join_cannot_be_lost(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        for row in plan['physical_group_witnesses']:
            if row[0]=='USB_CONN_DP':row[2]=[item for item in row[2] if item[:2]!=['U32','3']]
        with self.assertRaises(AssertionError):m.validate_76_checkpoint(plan)

    def replacement_fixture(self):
        policy=m.runpy.run_path(str(ROOT/'tools/routing_track_replacements.py'))
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        return policy,plan

    def test_reviewed_replacement_catalog_is_preserved(self):
        policy,plan=self.replacement_fixture();policy['validate_plan'](plan,required=True)

    def test_replacement_metadata_cannot_be_omitted(self):
        policy,plan=self.replacement_fixture();del plan['track_replacements']
        with self.assertRaises(AssertionError):policy['validate_plan'](plan,required=True)

    def test_unreviewed_replacement_original_is_rejected(self):
        policy,plan=self.replacement_fixture();plan['track_replacements'][0]['original'][2]+=100000
        with self.assertRaises(AssertionError):policy['validate_plan'](plan,required=True)

    def test_reviewed_replacement_copper_cannot_be_dropped(self):
        policy,plan=self.replacement_fixture();plan['added_copper'].remove(plan['track_replacements'][0]['replacement'][0])
        with self.assertRaises(AssertionError):policy['validate_plan'](plan,required=True)

    def test_reviewed_source_junction_cannot_be_omitted(self):
        policy,plan=self.replacement_fixture();plan['track_replacements'][0]['junction_contacts'].pop()
        with self.assertRaises(AssertionError):policy['validate_plan'](plan,required=True)

    def test_replacement_cannot_narrow_a_track(self):
        policy,plan=self.replacement_fixture();plan['track_replacements'][0]['replacement'][0][7]=120000
        with self.assertRaises(AssertionError):policy['validate_plan'](plan,required=True)

    def test_valid_low_current_signal(self):m.validate(self.plan,self.manifest)

    def test_narrow_power_is_rejected(self):
        self.plan['added_copper'][0][1]='VLED';self.plan['added_copper'][0][-1]=120000
        with self.assertRaises(AssertionError):m.validate(self.plan,self.manifest)

    def test_narrow_signal_is_rejected(self):
        self.plan['added_copper'][0][-1]=120000
        with self.assertRaises(AssertionError):m.validate(self.plan,self.manifest)

    def neck(self):
        row=['track','+3V3_APP',63850000,650000,63300000,650000,'B.Cu',120000]
        self.plan['added_copper']=[row]
        self.plan['pad_necks']=[dict(reference='U48',pin='6',track=row)]
        return row

    def test_exact_reviewed_neck_is_permitted(self):
        self.neck();m.validate(self.plan,self.manifest)

    def test_neck_on_wrong_net_is_rejected(self):
        self.neck()[1]='VLED'
        with self.assertRaises(AssertionError):m.validate(self.plan,self.manifest)

    def test_neck_on_wrong_layer_is_rejected(self):
        self.neck()[6]='In4.Cu'
        with self.assertRaises(AssertionError):m.validate(self.plan,self.manifest)

    def test_neck_extension_is_rejected(self):
        self.neck()[4]=63000000
        with self.assertRaises(AssertionError):m.validate(self.plan,self.manifest)

    def test_neck_wrong_direction_is_rejected(self):
        self.neck()[4]=64400000
        with self.assertRaises(AssertionError):m.validate(self.plan,self.manifest)

    def test_neck_bend_is_rejected(self):
        self.neck()[5]+=10000
        with self.assertRaises(AssertionError):m.validate(self.plan,self.manifest)

    def test_neck_not_on_exact_pad_is_rejected(self):
        row=self.neck();row[2]-=10000;row[4]-=10000
        with self.assertRaises(AssertionError):m.validate(self.plan,self.manifest)

    def test_duplicate_neck_pin_is_rejected(self):
        self.neck();self.plan['pad_necks']*=2
        with self.assertRaises(AssertionError):m.validate(self.plan,self.manifest)

    def test_unreviewed_neck_pin_is_rejected(self):
        self.neck();self.plan['pad_necks'][0]['pin']='5'
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
