# SPDX-License-Identifier: Apache-2.0
"""Guard the exact supplied-sheet transcription against the discovered old land."""
from pathlib import Path
import importlib.util
import unittest

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('c32_land',ROOT/'tools/check-c32-land-candidate.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


class C32LandCandidate(unittest.TestCase):
    def setUp(self):
        self.fp=m.A['parse_sexpr'](m.FOOTPRINT)

    def test_exact_supplied_sheet_candidate_passes(self):
        self.assertFalse(m.validate(self.fp)['fabrication_release_allowed'])

    def test_legacy_oversized_lands_are_rejected(self):
        legacy=m.A['parse_sexpr'](ROOT/'hardware/coupon/rev-a/footprints/rgb-badge-coupon.pretty/C_Murata_GRM18_0603.kicad_mod')
        legacy[1]=self.fp[1]  # A new label must not bless the old geometry.
        with self.assertRaises(AssertionError):m.validate(legacy)

    def test_transposed_gap_and_land_length_are_rejected(self):
        for pad in m.A['children'](self.fp,'pad'):
            m.one(pad,'size')[1]='0.70'
            m.one(pad,'at')[1]='-0.675' if pad[1]=='1' else '0.675'
        with self.assertRaises(AssertionError):m.validate(self.fp)

    def test_wrong_part_identity_is_rejected(self):
        self.fp[1]='C_Murata_GRM187R61A226ME15_0603'
        with self.assertRaises(AssertionError):m.validate(self.fp)


if __name__=='__main__':unittest.main()
