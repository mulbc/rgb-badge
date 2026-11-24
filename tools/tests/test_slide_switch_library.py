# SPDX-License-Identifier: Apache-2.0
from pathlib import Path
import runpy
import re
import shutil
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[2]
m=runpy.run_path(str(ROOT/'tools/check-slide-switch-library.py'))

class PrintedSwitchLibrary(unittest.TestCase):
    def test_printed_drawing_numbering_passes(self):m['check']()
    def fault(self,kind):
        with tempfile.TemporaryDirectory() as folder:
            project=Path(folder)
            for name in ('symbols','footprints'):shutil.copytree(ROOT/'hardware/coupon/rev-a'/name,project/name)
            if kind=='symbol':
                p=project/'symbols/rgb-badge-coupon.kicad_sym';t=p.read_text();a=t.index('(symbol "JS202011JCQN"');b=t.index('(symbol "JS202011JCQN_1_1"',a);end=t.index('\n)',b)+2
                block=t[a:end];block=re.sub(r'\(number "([567])"',lambda q:'(number "'+str(int(q[1])-1)+'"',block);p.write_text(t[:a]+block+t[end:])
            else:
                p=project/'footprints/rgb-badge-coupon.pretty'/f'{m["FOOTPRINT"]}.kicad_mod';t=p.read_text()
                if kind=='legacy':t=re.sub(r'\(pad "([567])"',lambda q:'(pad "'+str(int(q[1])-1)+'"',t)
                else:t=t.replace('(pad "6"','(pad "temporary"').replace('(pad "7"','(pad "6"').replace('(pad "temporary"','(pad "7"')
                p.write_text(t)
            with self.assertRaises(AssertionError):m['check'](project)
    def test_legacy_footprint_numbers_are_rejected(self):self.fault('legacy')
    def test_common_and_throw_land_swap_is_rejected(self):self.fault('swap')
    def test_legacy_symbol_numbers_are_rejected(self):self.fault('symbol')

if __name__=='__main__':unittest.main()
