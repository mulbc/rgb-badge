# SPDX-License-Identifier: Apache-2.0
from pathlib import Path
import copy
import json
import runpy
import unittest
ROOT=Path(__file__).resolve().parents[2]
m=runpy.run_path(str(ROOT/'tools/routing_supply_join.py'))

class GaugeSupplyJoin(unittest.TestCase):
    def setUp(self):self.plan=json.loads((ROOT/'mechanical/review/routing-progress-plan.json').read_text())
    def test_exact_ordinary_width_inventory_passes(self):self.assertEqual(sum(m['validate_plan'](self.plan).values()),14)
    def test_removed_copper_is_rejected(self):
        self.plan['added_copper'].remove(self.plan['gauge_supply_join']['added_copper'][0])
        with self.assertRaisesRegex(AssertionError,'Exact gauge supply copper missing'):m['validate_plan'](self.plan)
    def test_changed_width_pin_scope_or_missing_catalog_is_rejected(self):
        original=copy.deepcopy(self.plan)
        for field in ('track_width_iu','required_joined_pads','added_copper'):
            self.plan=copy.deepcopy(original);self.plan['gauge_supply_join'][field]=[]
            with self.subTest(field=field),self.assertRaises(AssertionError):m['validate_plan'](self.plan)
        del self.plan['gauge_supply_join']
        with self.assertRaises(AssertionError):m['validate_plan'](self.plan,required=True)

if __name__=='__main__':unittest.main()
