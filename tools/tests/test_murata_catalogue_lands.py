# SPDX-License-Identifier: Apache-2.0
"""Regression evidence for the supplied drawing's a/b interpretation."""
from decimal import Decimal as D
from pathlib import Path
import runpy
import unittest

ROOT=Path(__file__).resolve().parents[2]
M=runpy.run_path(str(ROOT/'tools/review-murata-catalogue-lands.py'))


class CatalogueLandReview(unittest.TestCase):
    def test_grm18_observed_land_length_is_not_the_gap(self):
        fp=M['PARSE'](M['FOOTPRINTS']/'C_Murata_GRM18_0603.kicad_mod')
        measured=M['dimensions'](fp)
        self.assertEqual(measured,{'a':D('0.7'),'b':D('0.9'),'c':D('0.9')})
        self.assertIn('b',M['mismatches'](measured,M['ROWS']['18_0.15_or_0.20']))

    def test_grm21_observed_gap_and_land_both_conflict(self):
        fp=M['PARSE'](M['FOOTPRINTS']/'C_Murata_GRM21_0805.kicad_mod')
        measured=M['dimensions'](fp)
        self.assertEqual(measured['a'],D('0.7'))
        self.assertEqual(measured['b'],D('1.2'))
        self.assertEqual(M['mismatches'](measured,M['ROWS']['21_0.20']),['a','b'])

    def test_corrected_other_part_does_not_use_the_wide_tolerance_row(self):
        fp=M['PARSE'](M['FOOTPRINTS']/'C_Murata_GRM188R60J106ME47_0603.kicad_mod')
        measured=M['dimensions'](fp)
        self.assertFalse(M['mismatches'](measured,M['ROWS']['18_within_0.10']))
        self.assertTrue(M['mismatches'](measured,M['ROWS']['18_0.15_or_0.20']))

    def test_family_catalogue_cannot_grant_exact_part_approval(self):
        result=M['report']()
        self.assertFalse(result['source_geometry_changed'])
        self.assertFalse(result['fabrication_release_allowed'])
        for part in result['parts'].values():
            self.assertFalse(part['current_exact_part_drawing_approved'])
            self.assertTrue(part['source_identity_is_provisional_without_packaging_code'])


if __name__=='__main__':unittest.main()
