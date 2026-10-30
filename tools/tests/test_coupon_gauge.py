# SPDX-License-Identifier: Apache-2.0
"""Catch gauge domain, pin-map and unpowered-boundary regressions."""

from pathlib import Path
import runpy
import shutil
import subprocess
import tempfile
import unittest


TOOLS = Path(__file__).resolve().parents[1]
CHECK = runpy.run_path(str(TOOLS / 'check-coupon-gauge.py'))
PROJECT = TOOLS.parent / 'hardware/coupon/rev-a'


class GaugeCaptureTests(unittest.TestCase):
    def test_source_and_deterministic_generator(self):
        CHECK['check_sources'](PROJECT)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'new'
            subprocess.run(['python3',str(TOOLS / 'generate-coupon-gauge.py'),'--output',str(output)],check=True,capture_output=True)
            self.assertEqual((output/'gauge.kicad_sch').read_bytes(),(PROJECT/'gauge.kicad_sch').read_bytes())

    def test_faults_change_checked_connections(self):
        for old,new in [
            ('(global_label "SYS_I2C_SDA"', '(global_label "SYS_I2C_SCL"'),
            ('(global_label "+BAT_GAUGE_SW"', '(global_label "+BAT"'),
            ('(property "Reference" "#FLG06"', '(property "Reference" "#FLG07"'),
            ('(no_connect (at 111.760 76.200)', '(no_connect (at 111.760 78.740)'),
            ('(property "Value" "2.2k 1%"', '(property "Value" "10k 1%"'),
        ]:
            with self.subTest(old=old), tempfile.TemporaryDirectory() as directory:
                project=Path(directory)/'project'
                shutil.copytree(PROJECT,project,ignore=shutil.ignore_patterns('build','.history'))
                sheet=project/'gauge.kicad_sch'
                text=sheet.read_text(encoding='utf-8')
                self.assertIn(old,text)
                sheet.write_text(text.replace(old,new,1),encoding='utf-8')
                with self.assertRaises(ValueError):
                    CHECK['check_sources'](project)


if __name__=='__main__':
    unittest.main()
