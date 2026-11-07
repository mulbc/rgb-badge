# SPDX-License-Identifier: Apache-2.0
"""Guard the unlinked converter's electrical pin map and source status."""

from pathlib import Path
import runpy
import shutil
import tempfile
import unittest


TOOLS=Path(__file__).resolve().parents[1]
PROJECT=TOOLS.parent/'hardware/coupon/rev-a'
CHECK=runpy.run_path(str(TOOLS/'check-coupon-3v3.py'))['check']
GENERATE=runpy.run_path(str(TOOLS/'generate-coupon-3v3.py'))['generate']


class ConverterSourceTests(unittest.TestCase):
    def test_pin_map_and_regeneration(self):
        self.assertEqual(len(CHECK(PROJECT)),24)
        self.assertEqual((PROJECT/'staging/3v3-converter.kicad_sch').read_text(),GENERATE())

    def test_fails_on_unsafe_source_mutations(self):
        for original,replacement in [
            ('(global_label "APP_ON_SW_DRAFT"','(global_label "+SYS_APP_IN_DRAFT"'),
            ('(global_label "APP_3V3_FB"','(global_label "+3V3_APP"'),
            ('(global_label "+SYS_APP_IN_DRAFT"','(global_label "+BAT_GAUGE_SW"'),
            ('(property "MPN" "DFE252012P-1R0M=P2"','(property "MPN" "OTHER"'),
            ('(wire (pts (xy 127.000 96.520) (xy 127.000 137.160))','(wire (pts (xy 127.000 96.520) (xy 127.000 134.620))'),
        ]:
            with self.subTest(original=original), tempfile.TemporaryDirectory() as directory:
                project=Path(directory)/'rev-a'
                shutil.copytree(PROJECT,project,ignore=shutil.ignore_patterns('build','.history'))
                sheet=project/'staging/3v3-converter.kicad_sch'
                source=sheet.read_text()
                self.assertIn(original,source)
                sheet.write_text(source.replace(original,replacement,1))
                with self.assertRaises(ValueError):
                    CHECK(project)


if __name__=='__main__':
    unittest.main()
