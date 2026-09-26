# SPDX-License-Identifier: Apache-2.0
"""Regression checks for the distinct copper/assembly placement risks."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "screen-preliminary-placement.py"
spec = importlib.util.spec_from_file_location("preliminary_placement", SCRIPT)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class PlacementScreenTests(unittest.TestCase):
    def test_exact_library_courtyards_and_usb_guide(self):
        led = module.courtyard(module.FOOTPRINTS / module.PARTS["led"])
        usb = module.courtyard(module.FOOTPRINTS / module.PARTS["usb"])
        self.assertEqual((led.x0, led.y0, led.x1, led.y1), (-1.1, -0.85, 1.1, 0.85))
        self.assertEqual((usb.x0, usb.y0, usb.x1, usb.y1), (-6.4, -0.85, 6.4, 7.5))
        module.validate_usb_guide(module.FOOTPRINTS / module.PARTS["usb"])

    def test_detects_courtyard_collisions_even_after_copper_only_fix(self):
        report = module.analyze()
        self.assertEqual(report["centered"]["usb_courtyard_overlaps"], 8)
        self.assertEqual(report["centered"]["worst_horizontal_courtyard_gap_mm"], -1.525)
        self.assertEqual(report["shifted_trial"]["shift_left_mm"], 1.775)
        self.assertEqual(report["shifted_trial"]["usb_courtyard_overlaps"], 0)
        self.assertTrue(report["rear_trial"]["all_rear_boxes_inside_board"])
        self.assertFalse(report["rear_trial"]["any_rear_box_overlap"])

    def test_changed_guide_fails_closed(self):
        original = (module.FOOTPRINTS / module.PARTS["usb"]).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "usb.kicad_mod"
            path.write_text(original.replace("(start -4.62 0.55) (end 4.62 0.55)",
                                             "(start -4.62 0.65) (end 4.62 0.65)"), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "re-audit drawing"):
                module.validate_usb_guide(path)


if __name__ == "__main__":
    unittest.main()
