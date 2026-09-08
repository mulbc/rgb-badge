# SPDX-License-Identifier: Apache-2.0
"""Regression tests for the independent row-selection library audit."""
from pathlib import Path
import runpy
import shutil
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[2]
CHECK = runpy.run_path(str(REPO / "tools" / "check-row-libraries.py"))
PROJECT = REPO / "hardware" / "coupon" / "rev-a"


class RowLibraryTests(unittest.TestCase):
    def test_controlled_libraries_pass(self):
        CHECK["check_libraries"](PROJECT)

    def project_copy(self):
        temporary = tempfile.TemporaryDirectory(prefix="rgb-badge-row-library-")
        self.addCleanup(temporary.cleanup)
        target = Path(temporary.name)
        shutil.copytree(PROJECT / "symbols", target / "symbols")
        shutil.copytree(PROJECT / "footprints", target / "footprints")
        return target

    def test_decoder_pin_swap_is_rejected(self):
        project = self.project_copy()
        path = project / "symbols" / "rgb-badge-coupon.kicad_sym"
        text = path.read_text(encoding="utf-8")
        text = text.replace('(name "Q0" (effects', '(name "BAD" (effects', 1)
        path.write_text(text, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "pin name mismatch"):
            CHECK["check_libraries"](project)

    def test_mosfet_pad_swap_is_rejected(self):
        project = self.project_copy()
        path = project / "footprints" / "rgb-badge-coupon.pretty" / "SC59_Diodes_DMP2066LSN.kicad_mod"
        text = path.read_text(encoding="utf-8").replace('(pad "1"', '(pad "9"', 1)
        path.write_text(text, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "SC-59 pad numbers mismatch"):
            CHECK["check_libraries"](project)

    def test_land_pattern_change_is_rejected(self):
        project = self.project_copy()
        path = project / "footprints" / "rgb-badge-coupon.pretty" / "SOT23_Diodes_2N7002K.kicad_mod"
        text = path.read_text(encoding="utf-8").replace('(size 0.8 0.9)', '(size 0.7 0.9)', 1)
        path.write_text(text, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "size differs from audit"):
            CHECK["check_libraries"](project)


if __name__ == "__main__":
    unittest.main()
