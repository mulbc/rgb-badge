#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Native fault injection for the saved control-continuation checker."""
from collections import Counter
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest
import pcbnew as p

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('check', ROOT / 'tools/check-native-control-trial.py')
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


class NativeControlGuards(unittest.TestCase):
    def setUp(self):
        self.old = p.LoadBoard(str(check.SOURCE))
        self.new = p.LoadBoard(str(check.OUTPUT))
        self.parts = {f.GetReference(): f for f in self.new.GetFootprints()}
        self.joins = json.loads((ROOT / 'mechanical/review/native-control-routing-plan.json').read_text())['intended_joins']
        grid = check.module('grid', 'generate-colour-fanout-grid-trial.py')
        originals = Counter(grid.signature(t) for t in self.old.GetTracks())
        self.added = []
        for item in self.new.GetTracks():
            signature = grid.signature(item)
            if originals[signature]:
                originals[signature] -= 1
            else:
                self.added.append(item)

    def reject(self):
        p.ZONE_FILLER(self.new).Fill(self.new.Zones())
        self.new.BuildConnectivity()
        with self.assertRaises(AssertionError):
            check.validate_geometry(self.old, self.new, self.joins)

    def test_saved_study_passes(self):
        self.assertEqual(check.validate_geometry(self.old, self.new, self.joins)['checked_joins'], 15)

    def test_ground_escape_detached_without_changing_item_counts(self):
        for item in self.added:
            if item.GetNetname() == 'GND':
                item.Move(p.VECTOR2I(0, 5000000))
        self.reject()

    def test_row_select_replacement_detached_without_changing_item_counts(self):
        for item in self.added:
            if item.GetNetname() == 'ROW_SEL_04':
                item.Move(p.VECTOR2I(0, 5000000))
        self.reject()

    def test_original_source_track_cannot_be_restored_through_ground_escape(self):
        item = p.PCB_TRACK(self.new)
        item.SetStart(p.VECTOR2I(38600000, 7250000))
        item.SetEnd(p.VECTOR2I(54000000, 7250000))
        item.SetLayer(p.In4_Cu)
        item.SetWidth(200000)
        item.SetNet(self.new.FindNet('ROW_SEL_04'))
        self.new.Add(item)
        with self.assertRaisesRegex(AssertionError, 'one reviewed replacement'):
            check.validate_geometry(self.old, self.new, self.joins)

    def test_connected_gauge_ic_data_that_cuts_pullup_supply_is_rejected(self):
        # The reverse-search route joins U35.8 but cuts four APP supply pads.
        # Undo only the reviewed 1 mm layer detour, retaining all item counts.
        changed = 0
        endpoints = frozenset(((40900000, 14800000), (40900000, 15800000)))
        for item in self.added:
            if isinstance(item, p.PCB_VIA) or item.GetNetname() != 'GAUGE_I2C_SDA':
                continue
            pair = frozenset(((item.GetStart().x, item.GetStart().y),
                              (item.GetEnd().x, item.GetEnd().y)))
            if pair == endpoints:
                self.assertEqual(item.GetLayer(), p.In3_Cu)
                item.SetLayer(p.In4_Cu)
                changed += 1
        self.assertEqual(changed, 1)
        p.ZONE_FILLER(self.new).Fill(self.new.Zones())
        self.new.BuildConnectivity()
        def pad(ref, number):
            return next(q for q in self.parts[ref].Pads() if q.GetNumber() == number)
        self.assertEqual(check.cluster(self.new, pad('U35', '8')),
                         check.cluster(self.new, pad('R101', '2')))
        for ref in ('R42', 'R43', 'R44', 'R79'):
            self.assertNotEqual(check.cluster(self.new, pad(ref, '1')),
                                check.cluster(self.new, pad('U3', '2')))
        with self.assertRaisesRegex(AssertionError, 'Existing physical pad cluster split'):
            check.validate_geometry(self.old, self.new, self.joins)

    def test_row_arm_detached_without_changing_item_counts(self):
        for item in self.added:
            if item.GetNetname() == 'ROW_ARM':
                item.Move(p.VECTOR2I(0, 5000000))
        self.reject()

    def test_usb_charge_request_detached_without_changing_item_counts(self):
        for item in self.added:
            if item.GetNetname() == 'USB_CHARGE_REQ':
                item.Move(p.VECTOR2I(0, 5000000))
        self.reject()

    def test_application_data_detached_without_changing_item_counts(self):
        for item in self.added:
            if item.GetNetname() == 'SYS_I2C_SDA':
                item.Move(p.VECTOR2I(0, 5000000))
        self.reject()

    def test_gauge_data_detached_without_changing_item_counts(self):
        for item in self.added:
            if item.GetNetname() == 'GAUGE_I2C_SDA':
                item.Move(p.VECTOR2I(0, 5000000))
        self.reject()

    def test_connected_gauge_data_that_loses_usb_bypass_is_rejected(self):
        # The real unbridged SDA route passed clearance and joined its target,
        # but zone refill disconnected C38. Keep all added item counts fixed.
        for item in self.added:
            if item.GetNetname() == '+3V3_USB':
                item.Move(p.VECTOR2I(0, -5000000))
        p.ZONE_FILLER(self.new).Fill(self.new.Zones())
        self.new.BuildConnectivity()
        def pad(ref, number):
            return next(q for q in self.parts[ref].Pads() if q.GetNumber() == number)
        self.assertEqual(check.cluster(self.new, pad('U46', '3')),
                         check.cluster(self.new, pad('R101', '2')))
        self.assertNotEqual(check.cluster(self.new, pad('C38', '1')),
                            check.cluster(self.new, pad('C36', '1')))
        with self.assertRaisesRegex(AssertionError, 'Existing physical pad cluster split'):
            check.validate_geometry(self.old, self.new, self.joins)

    def test_uart_receive_detached_without_changing_item_counts(self):
        for item in self.added:
            if item.GetNetname() == 'UART0_RX':
                item.Move(p.VECTOR2I(0, 5000000))
        self.reject()

    def test_uart_transmit_detached_without_changing_item_counts(self):
        for item in self.added:
            if item.GetNetname() == 'UART0_TX_RAW':
                item.Move(p.VECTOR2I(0, 5000000))
        self.reject()

    def test_connected_uart_transmit_without_usb_bypass_repair_is_rejected(self):
        endpoints = frozenset(((35150000, 4250000), (35150000, 2750000)))
        moved = 0
        for item in self.added:
            if item.GetNetname() != '+3V3_USB' or isinstance(item, p.PCB_VIA):
                continue
            pair = frozenset(((item.GetStart().x, item.GetStart().y),
                              (item.GetEnd().x, item.GetEnd().y)))
            if pair == endpoints:
                item.Move(p.VECTOR2I(0, -5000000))
                moved += 1
        self.assertEqual(moved, 1)
        p.ZONE_FILLER(self.new).Fill(self.new.Zones())
        self.new.BuildConnectivity()
        def pad(ref, number):
            return next(q for q in self.parts[ref].Pads() if q.GetNumber() == number)
        self.assertEqual(check.cluster(self.new, pad('U3', '37')),
                         check.cluster(self.new, pad('R47', '1')))
        self.assertNotEqual(check.cluster(self.new, pad('C59', '1')),
                            check.cluster(self.new, pad('C11', '1')))
        with self.assertRaisesRegex(AssertionError, 'Existing physical pad cluster split'):
            check.validate_geometry(self.old, self.new, self.joins)

    def test_gauge_clock_detached_without_changing_item_counts(self):
        for item in self.added:
            if item.GetNetname() == 'GAUGE_I2C_SCL':
                item.Move(p.VECTOR2I(0, 5000000))
        self.reject()

    def test_connected_gauge_clock_without_application_repair_is_rejected(self):
        for item in self.added:
            if item.GetNetname() == '+3V3_APP':
                item.Move(p.VECTOR2I(0, -5000000))
        self.check_clock_supply_failure('C37', 'C3')

    def test_connected_gauge_clock_without_usb_repair_is_rejected(self):
        # Preserve the previous C38/C36 bridge while withdrawing the new chain.
        endpoints = {
            frozenset(((42650000, 2750000), (42650000, 1750000))),
            frozenset(((42650000, 1750000), (37650000, 1750000))),
            frozenset(((37650000, 1750000), (37650000, 2750000))),
            frozenset(((42650000, 1750000), (52650000, 1750000))),
            frozenset(((45150000, 1750000), (45150000, 2750000))),
            frozenset(((47650000, 1750000), (47650000, 2750000))),
        }
        moved = 0
        for item in self.added:
            if item.GetNetname() != '+3V3_USB' or isinstance(item, p.PCB_VIA):
                continue
            pair = frozenset(((item.GetStart().x, item.GetStart().y),
                              (item.GetEnd().x, item.GetEnd().y)))
            if pair in endpoints:
                item.Move(p.VECTOR2I(0, -5000000))
                moved += 1
        self.assertEqual(moved, 6)
        self.check_clock_supply_failure('C23', 'C17')

    def check_clock_supply_failure(self, bypass, anchor):
        p.ZONE_FILLER(self.new).Fill(self.new.Zones())
        self.new.BuildConnectivity()
        def pad(ref, number):
            return next(q for q in self.parts[ref].Pads() if q.GetNumber() == number)
        self.assertEqual(check.cluster(self.new, pad('U46', '2')),
                         check.cluster(self.new, pad('R102', '2')))
        self.assertNotEqual(check.cluster(self.new, pad(bypass, '1')),
                            check.cluster(self.new, pad(anchor, '1')))
        with self.assertRaisesRegex(AssertionError, 'Existing physical pad cluster split'):
            check.validate_geometry(self.old, self.new, self.joins)

    def test_connected_clock_that_cuts_controller_supply_is_rejected(self):
        # Reproduce the real failure: a long In4 clock column left SCL joined
        # but severed U3.2 from its old supply group after zone refill.
        endpoints = {
            frozenset(((18550000, 23200000), (18550000, 8250000))),
            frozenset(((18550000, 8250000), (19650000, 8250000))),
            frozenset(((19650000, 8250000), (20400000, 7500000))),
        }
        changed = 0
        for item in self.added:
            if isinstance(item, p.PCB_VIA) or item.GetNetname() != 'SYS_I2C_SCL':
                continue
            pair = frozenset(((item.GetStart().x, item.GetStart().y),
                              (item.GetEnd().x, item.GetEnd().y)))
            if pair in endpoints:
                self.assertEqual(item.GetLayer(), p.In3_Cu)
                item.SetLayer(p.In4_Cu)
                changed += 1
        self.assertEqual(changed, 3)
        p.ZONE_FILLER(self.new).Fill(self.new.Zones())
        self.new.BuildConnectivity()
        def pad(ref, number):
            return next(q for q in self.parts[ref].Pads() if q.GetNumber() == number)
        self.assertEqual(check.cluster(self.new, pad('U3', '11')),
                         check.cluster(self.new, pad('R80', '2')))
        self.assertNotEqual(check.cluster(self.new, pad('U3', '2')),
                            check.cluster(self.new, pad('C74', '1')))
        with self.assertRaisesRegex(AssertionError, 'Existing physical pad cluster split'):
            check.validate_geometry(self.old, self.new, self.joins)

    def test_gate_copper_detached_without_changing_item_counts(self):
        for item in self.added:
            if item.GetNetname() == 'ROW_GATE_05':
                item.Move(p.VECTOR2I(0, -5000000))
        self.reject()

    def test_i2c_copper_detached_without_changing_item_counts(self):
        for item in self.added:
            if item.GetNetname() == 'SYS_I2C_SCL':
                item.Move(p.VECTOR2I(0, 5000000))
        self.reject()

    def test_source_drain_tie_removed(self):
        # Keep the detached native item alive until connectivity has rebuilt;
        # an immediately collected SWIG temporary can leave cached pointers.
        removed = next(t for t in self.new.GetTracks() if t.GetNetname() == 'ROW_00_A')
        self.new.Remove(removed)
        self.reject()

    def test_duplicate_physical_drain_land_changed(self):
        pads = [q for q in self.parts['PAIR01'].Pads() if q.GetNumber() == '3']
        self.assertEqual(len(pads), 2)
        pads[0].Move(p.VECTOR2I(100000, 0))
        self.reject()

    def test_footprint_moved(self):
        self.parts['U46'].Move(p.VECTOR2I(100000, 0))
        self.reject()

    def test_pad_net_changed(self):
        pad = next(q for q in self.parts['U46'].Pads() if q.GetNumber() == '7')
        pad.SetNet(self.new.FindNet('GND'))
        self.reject()

    def test_nonadjacent_microvia(self):
        via = next(t for t in self.added if isinstance(t, p.PCB_VIA))
        stack = list(self.new.GetEnabledLayers().CuStack())
        via.SetLayerPair(stack[0], stack[2])
        self.reject()


if __name__ == '__main__':
    if any(arg.startswith('NativeControlGuards.') for arg in sys.argv[1:]):
        unittest.main()
    else:
        # Separate native runtimes avoid KiCad's repeated BOARD-wrapper
        # destruction issue on macOS (see the preceding row-13 guard runner).
        names = unittest.defaultTestLoader.getTestCaseNames(NativeControlGuards)
        for name in names:
            subprocess.run([sys.executable, __file__, 'NativeControlGuards.'+name, '-v'], check=True)
        print(f'All {len(names)} isolated native control guard checks passed.')
