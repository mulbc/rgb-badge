#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Inject native-board faults into the row-13 saved-geometry checker."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest
import pcbnew as p

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('check', ROOT / 'tools/check-row13-bias-trial.py')
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


class Row13Guards(unittest.TestCase):
    def setUp(self):
        self.old = p.LoadBoard(str(check.SOURCE))
        self.new = p.LoadBoard(str(check.OUTPUT))
        self.parts = {f.GetReference(): f for f in self.new.GetFootprints()}

    def reject(self):
        p.ZONE_FILLER(self.new).Fill(self.new.Zones())
        self.new.BuildConnectivity()
        with self.assertRaises(AssertionError):
            check.validate_geometry(self.old, self.new)

    def test_saved_study_passes(self):
        self.assertTrue(check.validate_geometry(self.old, self.new)['exactly_two_terminal_merges'])

    def test_gate_via_moved_away_from_resistor_is_rejected(self):
        via = next(t for t in self.new.GetTracks() if isinstance(t, p.PCB_VIA)
                   and t.GetNetname() == 'ROW_GATE_13' and t.GetPosition().x == 73450000)
        via.SetPosition(p.VECTOR2I(74450000, 27450000))
        self.reject()

    def test_supply_join_removed_without_changing_item_count_is_rejected(self):
        # Moving the long horizontal supply segment leaves both end stubs in
        # place, but disconnects the new resistor from the old VLED group.
        segment = next(t for t in self.new.GetTracks() if not isinstance(t, p.PCB_VIA)
                       and t.GetNetname() == 'VLED' and t.GetStart() == p.VECTOR2I(72450000, 26850000)
                       and t.GetEnd() == p.VECTOR2I(74800000, 26850000))
        segment.Move(p.VECTOR2I(0, -1000000))
        self.reject()

    def test_source_copper_removed_is_rejected(self):
        original = next(t for t in self.new.GetTracks() if t.GetNetname() == 'ROW_00_A')
        self.new.Remove(original)
        self.reject()

    def test_duplicate_physical_drain_land_geometry_changed_is_rejected(self):
        pads = [q for q in self.parts['PAIR01'].Pads() if q.GetNumber() == '3']
        self.assertEqual(len(pads), 2)
        pads[0].SetPosition(p.VECTOR2I(pads[0].GetPosition().x + 100000, pads[0].GetPosition().y))
        self.reject()

    def test_other_footprint_moved_is_rejected(self):
        self.parts['R20'].Move(p.VECTOR2I(100000, 0))
        self.reject()

    def test_resistor_pad_net_swap_is_rejected(self):
        pads = list(self.parts['R19'].Pads())
        nets = [q.GetNet() for q in pads]
        pads[0].SetNet(nets[1])
        pads[1].SetNet(nets[0])
        self.reject()

    def test_nonadjacent_microvia_is_rejected(self):
        via = next(t for t in self.new.GetTracks() if isinstance(t, p.PCB_VIA)
                   and t.GetNetname() == 'ROW_GATE_13' and t.GetPosition().x == 73450000)
        via.SetLayerPair(p.In3_Cu, p.B_Cu)
        self.reject()


if __name__ == '__main__':
    if any(arg.startswith('Row13Guards.') for arg in sys.argv[1:]):
        unittest.main()
    else:
        # KiCad 10's macOS Python bridge can lose its BOARD wrapper after many
        # repeated board-load/destruction cycles in one process. Isolate each
        # mutation so a fresh native runtime owns exactly its two boards.
        names = unittest.defaultTestLoader.getTestCaseNames(Row13Guards)
        for name in names:
            subprocess.run([sys.executable, __file__, 'Row13Guards.'+name, '-v'], check=True)
        print(f'All {len(names)} isolated native guard checks passed.')
