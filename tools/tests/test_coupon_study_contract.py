# SPDX-License-Identifier: Apache-2.0
"""Fault checks for schematic-to-study source assignment, not board operation."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('contract', ROOT/'tools/check-coupon-study-contract.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


class StudyContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.canonical = json.loads(c.CONTRACT.read_text())
        cls.inventory = c.read_board(c.BOARD)

    def setUp(self):
        self.data = copy.deepcopy(self.canonical)
        self.board = copy.deepcopy(self.inventory)

    def reject(self):
        with self.assertRaises(ValueError):
            c.compare(self.data, self.board)

    def test_current_study_has_only_explicit_exceptions(self):
        c.validate_contract(self.data)
        r = c.compare(self.data, self.board)
        self.assertEqual((r['canonical_components'], r['study_footprints']), (497, 483))
        self.assertEqual((r['matched_components'], r['matched_logical_pins'],
                          r['matched_physical_electrical_pads']), (465, 1718, 1747))
        self.assertEqual((r['non_copper_apertures'], r['netless_mechanical_pads']), (69, 2))
        self.assertEqual(len(r['pcb_references_with_blank_mpn_values']), 22)
        self.assertEqual(r['pcb_references_with_blank_mpn_values'], r['canonical_references_without_mpn'])
        self.assertEqual(len(r['canonical_references_without_manufacturer']), 5)
        self.assertTrue(r['shared_metadata_required'])
        self.assertFalse(r['fabrication_release_allowed'])

    def test_every_corrected_murata_land_is_enforced(self):
        for ref in c.MURATA['REFS']:
            for key,value in [('land_size',['.9','.9']),('land_at',['-.8','0']),
                              ('land_type',['smd','roundrect']),('land_layers',['B.Cu'])]:
                with self.subTest(ref=ref,key=key):
                    self.board=copy.deepcopy(self.inventory)
                    self.board[ref]['pads'][0][key]=value
                    self.reject()

    def test_legacy_assignment_requires_explicit_historical_mode_and_geometry(self):
        for ref in c.MURATA['REFS']:
            self.board[ref]['footprint']=c.MURATA['OLD']
            for q in self.board[ref]['pads']:
                q['land_at']=['-.8' if q['number']=='1' else '.8','0']
                q['land_size']=['.9','.9']
        self.reject()
        r=c.compare(self.data,self.board,legacy_land_study=True)
        self.assertEqual(set(r['historical_legacy_murata_assignments']),set(c.MURATA['REFS']))
        self.board['C3']['pads'][0]['land_size']=['.65','.70']
        with self.assertRaisesRegex(ValueError,'geometry differs'):
            c.compare(self.data,self.board,legacy_land_study=True)

    def test_legacy_switch_labels_require_explicit_historical_mode(self):
        self.board['SW2']['footprint']=c.SWITCH['OLD']
        for pad in self.board['SW2']['pads']:pad['number']=c.SWITCH['REVERSE'][pad['number']]
        self.reject()
        r=c.compare(self.data,self.board,legacy_switch_study=True)
        self.assertEqual(r['historical_legacy_switch_assignments'],['SW2'])
        next(q for q in self.board['SW2']['pads'] if q['number']=='5')['net']='+BAT_GAUGE_SW'
        with self.assertRaises(ValueError):c.compare(self.data,self.board,legacy_switch_study=True)

    def test_snapshot_net_drift_is_checked_against_existing_circuit_contract(self):
        self.data['components']['R47']['pins']['1']['native_net'] = 'UART0_TX'
        with self.assertRaisesRegex(ValueError, 'pin-to-net mismatch'):
            c.validate_contract(self.data)

    def test_snapshot_exact_part_drift_is_checked_against_placed_source(self):
        self.data['components']['R47']['mpn'] = 'ERJ2RKF0R00X'
        with self.assertRaisesRegex(ValueError, 'part identity differs'):
            c.validate_contract(self.data)

    def test_stale_source_fingerprint_is_rejected(self):
        key = next(iter(self.data['source_sha256']))
        self.data['source_sha256'][key] = '0'*64
        with self.assertRaisesRegex(ValueError, 'source drift'):
            c.validate_contract(self.data)

    def test_controller_net_change_is_rejected(self):
        next(q for q in self.board['U3']['pads'] if q['number'] == '36')['net'] = 'GND'
        self.reject()

    def test_explicit_no_connect_cannot_be_connected(self):
        number = next(n for n,p in self.data['components']['U3']['pins'].items() if p['no_connect'])
        next(q for q in self.board['U3']['pads'] if q['number'] == number)['net'] = 'GND'
        self.reject()

    def test_pin_removal_is_rejected(self):
        self.board['R47']['pads'] = [q for q in self.board['R47']['pads'] if q['number'] != '1']
        self.reject()

    def test_value_footprint_and_supplied_mpn_changes_are_rejected(self):
        for key,value in [('value','0R'),('footprint','rgb-badge-coupon:wrong'),
                          ('mpn','ERJ2RKF0R00X'),('manufacturer','Wrong manufacturer')]:
            with self.subTest(field=key):
                self.board = copy.deepcopy(self.inventory)
                self.board['R47'][key] = value
                self.reject()

    def test_removed_identity_fields_are_rejected_even_for_canonical_blanks(self):
        for ref in ('R47', 'TP4', 'J1'):
            for field in ('MPN', 'Manufacturer'):
                with self.subTest(ref=ref, field=field):
                    self.board = copy.deepcopy(self.inventory)
                    self.board[ref]['identity_fields'].remove(field)
                    self.reject()

    def test_cleared_or_invented_identity_values_are_rejected(self):
        for ref, key, value in [('R47', 'mpn', ''), ('R47', 'manufacturer', ''),
                                ('TP4', 'mpn', 'Invented copper part'), ('J1', 'manufacturer', 'Invented vendor')]:
            with self.subTest(ref=ref, field=key):
                self.board = copy.deepcopy(self.inventory)
                self.board[ref][key] = value
                self.reject()

    def test_historical_input_metadata_opt_out_still_rejects_substitution(self):
        self.board['R47']['mpn'] = ''
        self.board['R47']['identity_fields'] = []
        c.compare(self.data, self.board, require_metadata=False)
        self.board['R47']['mpn'] = 'Different part'
        with self.assertRaisesRegex(ValueError, 'mpn differs'):
            c.compare(self.data, self.board, require_metadata=False)

    def test_unexpected_missing_component_is_rejected(self):
        del self.board['R47']
        self.reject()

    def test_unexpected_extra_component_is_rejected(self):
        self.board['EXTRA'] = copy.deepcopy(self.board['TP4'])
        self.reject()

    def test_trial_pair_gate_swap_is_rejected(self):
        next(q for q in self.board['PAIR01']['pads'] if q['number'] == '2')['net'] = 'ROW_SEL_01'
        self.reject()

    def test_duplicate_drain_land_removal_is_rejected(self):
        pads = self.board['PAIR01']['pads']
        pads.remove(next(q for q in pads if q['number'] == '3'))
        self.reject()

    def test_projected_driver_cannot_gain_a_net(self):
        next(q for q in self.board['PROJ_U1_2']['pads'] if q['copper'])['net'] = 'GND'
        self.reject()

    def test_mechanical_mounting_pad_cannot_gain_a_net(self):
        next(q for q in self.board['J2']['pads'] if q['number'] == 'MP')['net'] = 'GND'
        self.reject()

    def test_unknown_netless_copper_pad_is_rejected(self):
        self.board['R47']['pads'].append(dict(number='99',net='',copper=True))
        self.reject()

    def test_trial_and_projected_mpn_annotations_cannot_select_other_parts(self):
        for ref,mpn in [('PAIR01','DMC1229UFDB-7'),('PROJ_U1_2','TLC59581RTQR')]:
            with self.subTest(ref=ref):
                self.board = copy.deepcopy(self.inventory)
                self.board[ref]['mpn'] = mpn
                self.reject()

    def test_duplicate_board_reference_is_rejected_by_parser(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'duplicate.kicad_pcb'
            part = '(footprint "local:test" (property "Reference" "TP4") (property "Value" "TestPoint_Pad"))'
            path.write_text('(kicad_pcb '+part+part+')')
            with self.assertRaisesRegex(ValueError, 'Duplicate PCB reference'):
                c.read_board(path)

    def test_stale_native_xml_cannot_refresh_source_fingerprints(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'stale.xml'
            path.write_text('<export/>')
            os.utime(path, (1, 1))
            with self.assertRaisesRegex(ValueError, 'predates canonical source'):
                c.refresh(path)


if __name__ == '__main__':
    unittest.main()
