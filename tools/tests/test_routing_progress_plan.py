#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Portable negative checks for the routing study's scoped copper exceptions."""
import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('progress',ROOT/'tools/check-routing-progress-plan.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


class PlanGuards(unittest.TestCase):
    def setUp(self):
        digest='da3c3e093acef457ce2d0ebe73b57fd5006b9139a57b7fe8acfcd77e612dc246'
        self.plan=dict(source_sha256=digest,open_edges=150,open_edges_by_net={'GND':150},
                       retired_zero_length_tracks=[['GND',i,0,'B.Cu',200000] for i in range(116)],
                       placements=[],added_copper=[['track','ROW_A0',0,0,1000000,0,'B.Cu',200000]])
        self.manifest=dict(source_sha256=digest,native_open_edges=150,fabrication_release_allowed=False)

    def test_ic_relocation_is_rejected(self):
        self.plan['placements']=[dict(reference='U39',old_position_iu=[0,0],new_position_iu=[1,0])]
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
