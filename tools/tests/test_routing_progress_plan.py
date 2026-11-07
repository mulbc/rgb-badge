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

    def test_accepted_71_checkpoint_is_preserved(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        m.validate_71_checkpoint(plan)

    def test_accepted_71_copper_cannot_be_dropped(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        prior=json.loads((ROOT/'mechanical/review/routing-progress-71-checkpoint.json').read_text())
        row=next(row for row in prior['added_copper'] if row[1]=='LED_SIN')
        plan['added_copper'].remove(row)
        with self.assertRaises(AssertionError):m.validate_71_checkpoint(plan)

    def test_accepted_71_join_cannot_be_lost(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        for row in plan['physical_group_witnesses']:
            if row[0]=='LED_SIN':row[2]=[item for item in row[2] if item[:2]!=['U1','26']]
        with self.assertRaises(AssertionError):m.validate_71_checkpoint(plan)

    def test_accepted_70_checkpoint_is_preserved(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        m.validate_70_checkpoint(plan)

    def test_accepted_70_copper_cannot_be_dropped(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        prior=json.loads((ROOT/'mechanical/review/routing-progress-70-checkpoint.json').read_text())
        row=next(row for row in prior['added_copper'] if row[1]=='GND')
        plan['added_copper'].remove(row)
        with self.assertRaises(AssertionError):m.validate_70_checkpoint(plan)

    def test_accepted_70_join_cannot_be_lost(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        for row in plan['physical_group_witnesses']:
            if row[0]=='GND':row[2]=[item for item in row[2] if item[:2]!=['PAIR10','1']]
        with self.assertRaises(AssertionError):m.validate_70_checkpoint(plan)


    def test_accepted_69_checkpoint_is_preserved(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        m.validate_69_checkpoint(plan)

    def test_accepted_69_copper_cannot_be_dropped(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        prior=json.loads((ROOT/'mechanical/review/routing-progress-69-checkpoint.json').read_text())
        plan['added_copper'].remove(prior['added_copper'][-1])
        with self.assertRaises(AssertionError):m.validate_69_checkpoint(plan)

    def test_accepted_69_join_cannot_be_lost(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        for row in plan['physical_group_witnesses']:
            if row[0]=='GND':row[2]=[q for q in row[2] if q[:2]!=['TH1','2']]
        with self.assertRaises(AssertionError):m.validate_69_checkpoint(plan)

    def test_accepted_65_checkpoint_is_preserved(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        m.validate_65_checkpoint(plan)

    def test_accepted_65_copper_cannot_be_dropped(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        prior=json.loads((ROOT/'mechanical/review/routing-progress-65-checkpoint.json').read_text())
        plan['added_copper'].remove(prior['testpad_placements'][0]['connection'][0])
        with self.assertRaisesRegex(AssertionError,'Accepted 65-edge copper changed'):m.validate_65_checkpoint(plan)

    def test_accepted_65_join_cannot_be_lost(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        for row in plan['physical_group_witnesses']:
            if row[0]=='USB_RAW_OUT1':row[2]=[q for q in row[2] if q[:2]!=['TP20','1']]
        with self.assertRaises(AssertionError):m.validate_65_checkpoint(plan)

    def test_accepted_65_testpad_pose_is_frozen(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        plan['testpad_placements'][0]['new_position_iu'][0]+=100000
        with self.assertRaisesRegex(AssertionError,'65-edge testpad_placements changed'):m.validate_65_checkpoint(plan)

    def test_accepted_65_passive_pose_is_frozen(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        plan['placements'][0]['new_position_iu'][0]+=100000
        with self.assertRaisesRegex(AssertionError,'65-edge placements changed'):m.validate_65_checkpoint(plan)

    def test_accepted_65_replacement_is_frozen(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        plan['track_replacements'][0]['junction_contacts'].pop()
        with self.assertRaisesRegex(AssertionError,'65-edge track_replacements changed'):m.validate_65_checkpoint(plan)

    def test_accepted_64_checkpoint_is_preserved(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        m.validate_64_checkpoint(plan)

    def test_accepted_64_copper_cannot_be_dropped(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        prior=json.loads((ROOT/'mechanical/review/routing-progress-64-checkpoint.json').read_text())
        plan['added_copper'].remove(prior['added_copper'][-1])
        with self.assertRaisesRegex(AssertionError,'Accepted 64-edge copper changed'):m.validate_64_checkpoint(plan)

    def test_accepted_64_temperature_join_cannot_be_lost(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        for row in plan['physical_group_witnesses']:
            if row[0]=='TEMP_OK':row[2]=[q for q in row[2] if q[:2]!=['U39','6']]
        with self.assertRaises(AssertionError):m.validate_64_checkpoint(plan)

    def test_accepted_64_replacement_is_frozen(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        next(e for e in plan['track_replacements'] if e['original'][1]=='COL_02_R')['junction_contacts'].pop()
        with self.assertRaisesRegex(AssertionError,'64-edge replacement changed'):m.validate_64_checkpoint(plan)

    def digital_fixture(self):
        spec=importlib.util.spec_from_file_location('digital_width_test',ROOT/'tools/routing_digital_width.py')
        policy=importlib.util.module_from_spec(spec);spec.loader.exec_module(policy)
        return policy,json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())

    def test_exact_digital_catalog_passes(self):
        policy,plan=self.digital_fixture()
        self.assertEqual(sum(policy.validate_plan(plan,required=True).values()),174)

    def test_digital_catalog_cannot_be_omitted(self):
        policy,plan=self.digital_fixture();del plan['digital_width']
        with self.assertRaises(AssertionError):policy.validate_plan(plan,required=True)

    def test_digital_copper_cannot_be_dropped(self):
        policy,plan=self.digital_fixture();plan['added_copper'].remove(plan['digital_width']['added_copper'][0])
        with self.assertRaisesRegex(AssertionError,'Reviewed digital copper missing'):policy.validate_plan(plan)

    def test_extra_narrow_digital_copper_is_rejected(self):
        policy,plan=self.digital_fixture();plan['added_copper'].append(['track','USB_RAW_OUT2',0,0,1000000,0,'B.Cu',120000])
        with self.assertRaisesRegex(AssertionError,'Unreviewed narrow digital copper'):policy.validate_plan(plan)

    def test_digital_net_scope_is_independent_of_catalog(self):
        policy,plan=self.digital_fixture();row=plan['digital_width']['added_copper'][0]
        plan['added_copper'].remove(row);row[1]='GND';plan['added_copper'].append(row.copy());policy.catalog=lambda:plan['digital_width']
        with self.assertRaisesRegex(AssertionError,'Net outside digital-width scope'):policy.validate_plan(plan)

    def test_digital_width_is_independent_of_catalog(self):
        policy,plan=self.digital_fixture();row=plan['digital_width']['added_copper'][0]
        plan['added_copper'].remove(row);row[7]=110000;plan['added_copper'].append(row.copy());policy.catalog=lambda:plan['digital_width']
        with self.assertRaises(AssertionError):policy.validate_plan(plan)

    def test_digital_length_is_independent_of_catalog(self):
        policy,plan=self.digital_fixture();row=plan['digital_width']['added_copper'][0]
        plan['added_copper'].remove(row);row[4]+=121000000;plan['added_copper'].append(row.copy());policy.catalog=lambda:plan['digital_width']
        with self.assertRaisesRegex(AssertionError,'Digital-width length bound exceeded'):policy.validate_plan(plan)

    def test_native_digital_rule_has_only_the_selected_net(self):
        policy,plan=self.digital_fixture();rule=policy.native_rule(plan)
        self.assertIn("A.NetName == 'USB_RAW_OUT2'",rule)
        self.assertIn("A.NetName == 'UART0_TX'",rule)
        self.assertIn("A.NetName == 'LED_SOUT'",rule);self.assertNotIn('GND',rule)

    def test_accepted_63_checkpoint_is_preserved(self):
        m.validate_63_checkpoint(json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text()))

    def test_accepted_63_copper_cannot_be_dropped(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        prior=json.loads((ROOT/'mechanical/review/routing-progress-63-checkpoint.json').read_text())
        plan['added_copper'].remove(prior['digital_width']['added_copper'][0])
        with self.assertRaisesRegex(AssertionError,'Accepted 63-edge copper changed'):m.validate_63_checkpoint(plan)

    def test_accepted_63_join_cannot_be_lost(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        for row in plan['physical_group_witnesses']:
            if row[0]=='USB_RAW_OUT2':row[2]=[x for x in row[2] if x[:2]!=['U31','8']]
        with self.assertRaises(AssertionError):m.validate_63_checkpoint(plan)

    def test_accepted_62_checkpoint_is_preserved(self):
        m.validate_62_checkpoint(json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text()))

    def test_accepted_62_copper_cannot_be_dropped(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        plan['added_copper'].remove(plan['source_chain_replacement']['replacement'][0])
        with self.assertRaisesRegex(AssertionError,'Accepted 62-edge copper changed'):m.validate_62_checkpoint(plan)

    def test_accepted_62_join_cannot_be_lost(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        for row in plan['physical_group_witnesses']:
            if row[0]=='UART0_TX':row[2]=[x for x in row[2] if x[:2]!=['TP4','1']]
        with self.assertRaises(AssertionError):m.validate_62_checkpoint(plan)

    def test_accepted_61_checkpoint_is_preserved(self):
        m.validate_61_checkpoint(json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text()))

    def test_accepted_61_copper_cannot_be_dropped(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        row=next(e['track'] for e in plan['pad_necks'] if e['reference']=='U52' and e['pin']=='3')
        plan['added_copper'].remove(row)
        with self.assertRaisesRegex(AssertionError,'Accepted 61-edge copper changed'):m.validate_61_checkpoint(plan)

    def transfer_fixture(self):
        spec=importlib.util.spec_from_file_location('transfer_test',ROOT/'tools/routing_track_replacements.py')
        policy=importlib.util.module_from_spec(spec);spec.loader.exec_module(policy)
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        policy.catalog=lambda:plan['track_replacements']
        return policy,plan,next(e for e in plan['track_replacements'] if e['original'][1]=='COL_10_R')

    def test_colour_transfer_original_is_independent_of_catalog(self):
        policy,plan,entry=self.transfer_fixture();entry['original'][2]+=1
        with self.assertRaisesRegex(AssertionError,'Unreviewed colour-transfer original'):policy.validate_plan(plan)

    def test_colour_transfer_length_is_independent_of_catalog(self):
        policy,plan,entry=self.transfer_fixture();row=entry['replacement'][0]
        plan['added_copper'].remove(row);row[4]+=3000000;plan['added_copper'].append(row.copy())
        with self.assertRaisesRegex(AssertionError,'Colour-transfer length bound exceeded'):policy.validate_plan(plan)

    def test_row_colour_transfer_original_is_independent_of_catalog(self):
        policy,plan,_=self.transfer_fixture();entry=next(e for e in plan['track_replacements'] if e['original'][1]=='COL_03_B');entry['original'][2]+=1
        with self.assertRaisesRegex(AssertionError,'Unreviewed colour-transfer original'):policy.validate_plan(plan)

    def test_row_colour_transfer_length_is_independent_of_catalog(self):
        policy,plan,_=self.transfer_fixture();entry=next(e for e in plan['track_replacements'] if e['original'][1]=='COL_03_B');row=entry['replacement'][0]
        plan['added_copper'].remove(row);row[4]+=3000000;plan['added_copper'].append(row.copy())
        with self.assertRaisesRegex(AssertionError,'Colour-transfer length bound exceeded'):policy.validate_plan(plan)

    def chain_fixture(self):
        spec=importlib.util.spec_from_file_location('chain_test',ROOT/'tools/routing_source_chain.py')
        policy=importlib.util.module_from_spec(spec);spec.loader.exec_module(policy)
        return policy,json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())

    def test_exact_source_chain_passes(self):
        policy,plan=self.chain_fixture();self.assertEqual(sum(policy.validate_plan(plan,required=True).values()),7)

    def test_source_chain_metadata_cannot_be_omitted(self):
        policy,plan=self.chain_fixture();del plan['source_chain_replacement']
        with self.assertRaises(AssertionError):policy.validate_plan(plan,required=True)

    def test_source_chain_copper_cannot_be_dropped(self):
        policy,plan=self.chain_fixture();plan['added_copper'].remove(plan['source_chain_replacement']['replacement'][0])
        with self.assertRaisesRegex(AssertionError,'Source-chain replacement copper missing'):policy.validate_plan(plan)

    def test_source_chain_original_is_independent_of_catalog(self):
        policy,plan=self.chain_fixture();plan['source_chain_replacement']['original'][0][2]+=1
        policy.catalog=lambda:plan['source_chain_replacement']
        with self.assertRaisesRegex(AssertionError,'Source-chain original inventory differs'):policy.validate_plan(plan)

    def test_source_chain_width_is_independent_of_catalog(self):
        policy,plan=self.chain_fixture();plan['source_chain_replacement']['replacement'][0][7]=190000
        policy.catalog=lambda:plan['source_chain_replacement']
        with self.assertRaisesRegex(AssertionError,'Source-chain width/net/layer changed'):policy.validate_plan(plan)

    def test_source_chain_net_is_independent_of_catalog(self):
        policy,plan=self.chain_fixture();plan['source_chain_replacement']['replacement'][0][1]='GND'
        policy.catalog=lambda:plan['source_chain_replacement']
        with self.assertRaisesRegex(AssertionError,'Source-chain width/net/layer changed'):policy.validate_plan(plan)

    def test_source_chain_length_is_independent_of_catalog(self):
        policy,plan=self.chain_fixture();plan['source_chain_replacement']['replacement'][0][4]+=60000000
        policy.catalog=lambda:plan['source_chain_replacement']
        with self.assertRaisesRegex(AssertionError,'Source-chain length bound exceeded'):policy.validate_plan(plan)

    def test_source_chain_original_cannot_be_restored(self):
        policy,plan=self.chain_fixture();plan['added_copper'].append(plan['source_chain_replacement']['original'][0].copy())
        with self.assertRaisesRegex(AssertionError,'Source-chain original restored'):policy.validate_plan(plan)

    def test_uart_source_pin_inventory_is_independent(self):
        policy,plan=self.digital_fixture();plan['digital_width']['joined_pads']['UART0_TX'][0][1]='1'
        policy.catalog=lambda:plan['digital_width']
        with self.assertRaises(AssertionError):policy.validate_plan(plan)

    def pad_placement_fixture(self):
        policy=m.runpy.run_path(str(ROOT/'tools/routing_testpad_placements.py'))
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        return policy,plan

    def test_testpad_catalog_is_preserved(self):
        policy,plan=self.pad_placement_fixture();policy['validate_plan'](plan,required=True)

    def test_testpad_catalog_cannot_be_omitted(self):
        policy,plan=self.pad_placement_fixture();del plan['testpad_placements']
        with self.assertRaises(AssertionError):policy['validate_plan'](plan,required=True)

    def test_unselected_testpad_reference_is_rejected(self):
        policy,plan=self.pad_placement_fixture();plan['testpad_placements'][0]['reference']='TP4'
        with self.assertRaises(AssertionError):policy['validate_plan'](plan,required=True)

    def test_testpad_net_cannot_change(self):
        policy,plan=self.pad_placement_fixture();plan['testpad_placements'][0]['net']='VLED'
        with self.assertRaises(AssertionError):policy['validate_plan'](plan,required=True)

    def test_testpad_pose_cannot_change(self):
        policy,plan=self.pad_placement_fixture();plan['testpad_placements'][0]['new_position_iu'][0]+=100000
        with self.assertRaises(AssertionError):policy['validate_plan'](plan,required=True)

    def test_testpad_lead_cannot_be_removed(self):
        policy,plan=self.pad_placement_fixture();plan['added_copper'].remove(plan['testpad_placements'][0]['connection'][0])
        with self.assertRaises(AssertionError):policy['validate_plan'](plan,required=True)

    def test_testpad_lead_cannot_be_narrowed(self):
        policy,plan=self.pad_placement_fixture();plan['testpad_placements'][0]['connection'][0][7]=120000
        with self.assertRaises(AssertionError):policy['validate_plan'](plan,required=True)

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

    def test_accepted_60_checkpoint_is_preserved(self):
        m.validate_60_checkpoint(json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text()))

    def test_accepted_60_copper_cannot_be_dropped(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        prior=json.loads((ROOT/'mechanical/review/routing-progress-60-checkpoint.json').read_text())
        plan['added_copper'].remove(prior['added_copper'][-1])
        with self.assertRaisesRegex(AssertionError,'Accepted 60-edge copper changed'):m.validate_60_checkpoint(plan)

    def test_accepted_60_join_cannot_be_lost(self):
        plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
        for row in plan['physical_group_witnesses']:
            if row[0]=='GND':row[2]=[p for p in row[2] if p[:2]!=['PAIR06','1']]
        with self.assertRaises(AssertionError):m.validate_60_checkpoint(plan)

    def test_accepted_digital_metadata_cannot_be_changed(self):
        policy,plan=self.digital_fixture()
        plan['digital_width']['joined_pads']['UART0_TX'][0][1]='1'
        with self.assertRaisesRegex(AssertionError,'Accepted digital pin inventory changed'):m.validate_60_checkpoint(plan)

    def test_serial_transfer_originals_are_independent_of_catalog(self):
        for net in ('COL_10_B','COL_14_B','COL_15_G','COL_15_R'):
            with self.subTest(net=net):
                policy,plan,_=self.transfer_fixture()
                entry=next(e for e in plan['track_replacements'] if e['original'][1]==net)
                entry['original'][2]+=1
                with self.assertRaisesRegex(AssertionError,'Unreviewed serial-transfer original'):policy.validate_plan(plan)

    def test_serial_transfer_lengths_are_independent_of_catalog(self):
        for net in ('COL_10_B','COL_14_B','COL_15_G','COL_15_R'):
            with self.subTest(net=net):
                policy,plan,_=self.transfer_fixture()
                row=next(e for e in plan['track_replacements'] if e['original'][1]==net)['replacement'][0]
                plan['added_copper'].remove(row);row[4]+=30000000;plan['added_copper'].append(row.copy())
                with self.assertRaisesRegex(AssertionError,'Serial colour-transfer length bound exceeded'):policy.validate_plan(plan)

    def test_serial_digital_length_cannot_be_relaxed_with_catalog(self):
        policy,plan=self.digital_fixture()
        row=next(row for row in plan['digital_width']['added_copper'] if row[0]=='track' and row[1]=='LED_SOUT')
        plan['added_copper'].remove(row);row[4]+=121000000;plan['added_copper'].append(row.copy());policy.catalog=lambda:plan['digital_width']
        with self.assertRaisesRegex(AssertionError,'Digital-width length bound exceeded'):policy.validate_plan(plan)

    def test_serial_source_pin_inventory_is_independent_of_catalog(self):
        policy,plan=self.digital_fixture();plan['digital_width']['joined_pads']['LED_SOUT'][0][1]='43'
        policy.catalog=lambda:plan['digital_width']
        with self.assertRaises(AssertionError):policy.validate_plan(plan)

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
