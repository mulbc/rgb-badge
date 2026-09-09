# SPDX-License-Identifier: Apache-2.0
"""Regression tests for the controller exact-part library audit."""

from pathlib import Path
import runpy
import shutil
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[2]
CHECK = runpy.run_path(str(REPO / "tools" / "check-controller-libraries.py"))
PROJECT = REPO / "hardware" / "coupon" / "rev-a"


class ControllerLibraryTests(unittest.TestCase):
    def project_copy(self):
        temporary = tempfile.TemporaryDirectory(prefix="rgb-badge-controller-library-")
        self.addCleanup(temporary.cleanup)
        target = Path(temporary.name)
        shutil.copytree(PROJECT / "symbols", target / "symbols")
        shutil.copytree(PROJECT / "footprints", target / "footprints")
        return target

    def test_controlled_libraries_pass(self):
        CHECK["check_libraries"](PROJECT)

    def test_psram_pin_rename_is_rejected(self):
        project = self.project_copy()
        path = project / "symbols" / "rgb-badge-coupon.kicad_sym"
        source = path.read_text(encoding="utf-8")
        path.write_text(source.replace('(name "GPIO35/PSRAM"', '(name "GPIO35"', 1), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "pin name mismatch"):
            CHECK["check_libraries"](project)

    def test_module_land_shift_is_rejected(self):
        project = self.project_copy()
        path = project / "footprints" / "rgb-badge-coupon.pretty" / "ESP32-S3-WROOM-1U.kicad_mod"
        source = path.read_text(encoding="utf-8")
        path.write_text(source.replace('(at -8.75 -8.26)', '(at -8.70 -8.26)', 1), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "pad 1 position mismatch"):
            CHECK["check_libraries"](project)

    def test_switch_contact_swap_is_rejected(self):
        project = self.project_copy()
        path = project / "footprints" / "rgb-badge-coupon.pretty" / "SW_Panasonic_EVQP7J01P.kicad_mod"
        source = path.read_text(encoding="utf-8")
        path.write_text(source.replace('(pad "1" smd rect (at -2.05 1.25)', '(pad "2" smd rect (at -2.05 1.25)', 1), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "contact pads mismatch"):
            CHECK["check_libraries"](project)


if __name__ == "__main__":
    unittest.main()
