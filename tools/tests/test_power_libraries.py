# SPDX-License-Identifier: Apache-2.0
"""Regression tests for the independent power-library audit."""

from pathlib import Path
from copy import deepcopy
import runpy
import shutil
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[2]
CHECK = runpy.run_path(str(REPO / "tools" / "check-power-libraries.py"))
PROJECT = REPO / "hardware" / "coupon" / "rev-a"


class PowerLibraryTests(unittest.TestCase):
    def test_permission_ground_pin_and_open_drain_faults(self):
        # DBV6 AND3 ground is pin 2, unlike DBV5 AND2 pin 3.
        cases = [
            ('TPS70933DBVR', '(number "1"', '(number "6"', 'pin numbers mismatch'),
            ('SN74LVC2G17DBVR', '(name "1Y"', '(name "2Y"', 'pin name mismatch'),
            ('SN74LVC2G17DBVR', '(pin output line', '(pin output inverted', 'non-inverting buffer'),
            ('SN74LVC1G11DBVR', '(number "2"', '(number "7"', 'pin numbers mismatch'),
            ('TPS3808G01DBVR', '(name "SENSE"', '(name "CT"', 'pin name mismatch'),
            ('SN74LVC1G06DBVR', '(pin open_collector inverted', '(pin output inverted', 'electrical type mismatch'),
            ('SN74LVC1G00DBVR', '(pin output inverted', '(pin output line', 'output inversion mismatch'),
            ('SN74LVC1G08DBVR', '(pin output line', '(pin output inverted', 'output inversion mismatch'),
            ('TPS3808G01DBVR', '(pin open_collector inverted', '(pin open_collector line', 'active-low inversion'),
        ]
        for mpn, old, new, error in cases:
            with self.subTest(mpn=mpn, error=error):
                project = self.project_copy()
                path = project / 'symbols' / 'rgb-badge-coupon.kicad_sym'
                source = path.read_text()
                before, rest = source.split(f'(symbol "{mpn}"', 1)
                self.assertIn(old, rest)
                path.write_text(before + f'(symbol "{mpn}"' + rest.replace(old, new, 1))
                with self.assertRaisesRegex(ValueError, error):
                    CHECK['check_libraries'](project)

    def test_dbv_geometry_regressions(self):
        cases = [
            ('DBV0005A', '(start -0.8 -1.45) (end 0.8 1.45)', '(start -1.45 -1.60) (end 1.45 1.60)', 'F.Fab outline mismatch'),
            ('DBV0006A', '(pad "5" smd roundrect (at 1.3 0)', '(pad "5" smd roundrect (at 1.3 -0.95)', 'touch or overlap'),
            ('DBV0006A', '(solder_mask_margin 0.05)', '(solder_mask_margin 0.1)', 'mask margin mismatch'),
            ('DBV0006A', '(solder_paste_ratio 0)', '(solder_paste_ratio -0.1)', 'stencil margin mismatch'),
            ('DBV0006A', '(roundrect_rratio 0.0833)', '(roundrect_rratio 0.2)', 'corner radius mismatch'),
        ]
        for package, old, new, error in cases:
            with self.subTest(package=package, error=error):
                project = self.project_copy()
                path = project / 'footprints' / 'rgb-badge-coupon.pretty' / f'SOT23_TI_{package}.kicad_mod'
                source = path.read_text()
                self.assertIn(old, source)
                path.write_text(source.replace(old, new, 1))
                with self.assertRaisesRegex(ValueError, error):
                    CHECK['check_libraries'](project)

    def test_copper_separation_rejects_original_short_independently(self):
        root = CHECK["footprint"](PROJECT, CHECK["PARTS"]["BQ25616JRTWT"]["footprint"])
        ep = next(p for p in CHECK["children"](root, "pad") if p[1] == "25")
        CHECK["one"](ep, "size", "EP")[1:] = ["3.1", "3.1"]
        with self.assertRaisesRegex(ValueError, "touch or overlap"):
            CHECK["check_copper_separation"](root)

    def test_copper_guard_rejects_overlap_and_contact_but_allows_same_pad(self):
        root = ["footprint", "test", ["pad", "1", "smd", "rect",
                ["at", "0", "0"], ["size", "1", "1"], ["layers", "F.Cu"]]]
        second = deepcopy(root[2])
        second[1] = "2"
        root.append(second)
        for x in ("0.9", "1"):
            second[4][1] = x
            with self.assertRaisesRegex(ValueError, "touch or overlap"):
                CHECK["check_copper_separation"](root)
        second[4][1] = "1.01"
        CHECK["check_copper_separation"](root)
        second[4][1], second[1] = "0.9", "1"
        CHECK["check_copper_separation"](root)

    def test_top_pin_header_collision_is_rejected(self):
        symbols = CHECK["check_symbol_libraries"](PROJECT)
        for mpn, old_y in (("BQ25616JRTWT", "17.78"), ("SN74LVC1G04DBVR", "6.35"),
                           ("INA232AIDDFR", "8.89"), ("TUSB320LAIRWBR", "13.97")):
            with self.subTest(mpn=mpn):
                symbol = deepcopy(symbols[mpn])
                field = next(p for p in CHECK["children"](symbol, "property") if p[1] == "Value")
                CHECK["one"](field, "at", "value")[2] = old_y
                with self.assertRaisesRegex(ValueError, "header overlaps"):
                    CHECK["check_symbol_header_clearance"](symbol)

    def test_signal_paste_and_mask_settings_are_checked(self):
        for setting, wrong, message in (("solder_paste_margin", "0", "paste reduction"),
                                        ("solder_mask_margin", "0", "mask margin")):
            project = self.project_copy()
            path = project / "footprints" / "rgb-badge-coupon.pretty" / \
                "QFN_TI_RTW0024A_4x4mm_P0.5mm_EP2.7mm.kicad_mod"
            text = path.read_text(encoding="utf-8")
            old = "-0.025" if setting == "solder_paste_margin" else "0.07"
            self.assertIn(f"({setting} {old})", text)
            path.write_text(text.replace(f"({setting} {old})", f"({setting} {wrong})", 1), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, message):
                CHECK["check_libraries"](project)

    def test_adg_symbol_faults(self):
        for old, new, error in (
            ('(number "0"', '(number "17"', 'pin numbers mismatch'),
            ('(name "S1"', '(name "D1"', 'pin name mismatch'),
            ('(pin input line', '(pin input inverted', 'active high'),
        ):
            with self.subTest(error=error):
                project = self.project_copy()
                path = project / 'symbols' / 'rgb-badge-coupon.kicad_sym'
                before, rest = path.read_text().split('(symbol "ADG4612BCPZ-REEL7"', 1)
                self.assertIn(old, rest)
                path.write_text(before + '(symbol "ADG4612BCPZ-REEL7"' + rest.replace(old, new, 1))
                with self.assertRaisesRegex(ValueError, error):
                    CHECK['check_libraries'](project)

    def test_adg_land_and_stencil_faults(self):
        for old, new, error in (
            ('(pad "0"', '(pad "17"', 'pad numbers/count'),
            ('(at -1.45 -0.75)', '(at 1.45 -0.75)', 'touch or overlap|geometry mismatch'),
            ('(size 1.75 1.75)', '(size 1.6 1.6)', 'exposed-pad geometry'),
            ('(layers "F.Cu" "F.Mask")', '(layers "F.Cu" "F.Paste" "F.Mask")', 'separate paste'),
            ('(at -0.425 -0.425)', '(at -0.4 -0.425)', 'stencil positions'),
        ):
            with self.subTest(error=error):
                project = self.project_copy()
                path = project / 'footprints' / 'rgb-badge-coupon.pretty' / (CHECK['PARTS']['ADG4612BCPZ-REEL7']['footprint'] + '.kicad_mod')
                source = path.read_text()
                self.assertIn(old, source)
                path.write_text(source.replace(old, new, 1))
                with self.assertRaisesRegex(ValueError, error):
                    CHECK['check_libraries'](project)

    def test_controlled_libraries_pass(self):
        CHECK["check_libraries"](PROJECT)

    def test_replacement_pin_map_faults(self):
        for name in ("ITERM", "GOOD_BAT", "HSD+"):
            with self.subTest(name=name):
                project = self.project_copy()
                path = project / "symbols" / "rgb-badge-coupon.kicad_sym"
                source = path.read_text(encoding="utf-8")
                old = f'(name "{name}" (effects'
                self.assertEqual(source.count(old), 1)
                path.write_text(source.replace(old, '(name "BAD" (effects'), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "pin name mismatch"):
                    CHECK["check_libraries"](project)

    def test_replacement_active_low_graphics(self):
        symbols = CHECK["check_symbol_libraries"](PROJECT)
        for mpn, number in (("BQ24074RGTR", "4"), ("BQ24392RSER", "4"),
                            ("TS3USB31ERSER", "1")):
            with self.subTest(mpn=mpn):
                self.assertEqual(CHECK["library_pins"](symbols[mpn])[number][2], "inverted")

    def test_replacement_land_and_stencil_faults(self):
        cases = [
            ("BQ24074RGTR", '(size 1.68 1.68)', '(size 1.70 1.68)', "central pad size"),
            ("BQ24074RGTR", '(size 1.55 1.55)', '(size 1.50 1.55)', "central pad size"),
            ("BQ24392RSER", '(at -0.675 -0.75)', '(at -0.65 -0.75)', "position mismatch"),
            ("TS3USB31ERSER", '(size 0.3 0.6)', '(size 0.3 0.55)', "size mismatch"),
        ]
        for mpn, old, new, message in cases:
            with self.subTest(mpn=mpn, old=old):
                project = self.project_copy()
                path = project / "footprints" / "rgb-badge-coupon.pretty" / \
                    (CHECK["PARTS"][mpn]["footprint"] + ".kicad_mod")
                source = path.read_text(encoding="utf-8")
                self.assertIn(old, source)
                path.write_text(source.replace(old, new, 1), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, message):
                    CHECK["check_libraries"](project)

    def test_rse_middle_pads_cannot_be_widened_to_outer_pad_size(self):
        for mpn in ("BQ24392RSER", "TS3USB31ERSER"):
            with self.subTest(mpn=mpn):
                project = self.project_copy()
                path = project / "footprints" / "rgb-badge-coupon.pretty" / \
                    (CHECK["PARTS"][mpn]["footprint"] + ".kicad_mod")
                source = path.read_text(encoding="utf-8")
                self.assertIn('(size 0.55 0.2)', source)
                path.write_text(source.replace('(size 0.55 0.2)', '(size 0.55 0.25)'), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "pad 2 size mismatch"):
                    CHECK["check_libraries"](project)

    def test_replacement_corner_radius_cannot_be_doubled(self):
        for mpn in ("BQ24074RGTR", "BQ24392RSER", "TS3USB31ERSER"):
            with self.subTest(mpn=mpn):
                project = self.project_copy()
                path = project / "footprints" / "rgb-badge-coupon.pretty" / \
                    (CHECK["PARTS"][mpn]["footprint"] + ".kicad_mod")
                source = path.read_text(encoding="utf-8")
                old = "0.208333" if mpn == "BQ24074RGTR" else "0.2"
                self.assertIn(f'(roundrect_rratio {old})', source)
                path.write_text(source.replace(f'(roundrect_rratio {old})',
                    '(roundrect_rratio 0.4)', 1), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "corner radius mismatch"):
                    CHECK["check_libraries"](project)

    def test_rse10_body_axes_cannot_be_swapped(self):
        project = self.project_copy()
        path = project / "footprints" / "rgb-badge-coupon.pretty" / \
            (CHECK["PARTS"]["BQ24392RSER"]["footprint"] + ".kicad_mod")
        source = path.read_text(encoding="utf-8")
        old = '(start -0.75 -1) (end 0.75 1)'
        self.assertIn(old, source)
        path.write_text(source.replace(old, '(start -1 -0.75) (end 1 0.75)'), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "F.Fab outline mismatch"):
            CHECK["check_libraries"](project)

    def project_copy(self):
        temporary = tempfile.TemporaryDirectory(prefix="rgb-badge-power-library-")
        self.addCleanup(temporary.cleanup)
        target = Path(temporary.name)
        shutil.copytree(PROJECT / "symbols", target / "symbols")
        shutil.copytree(PROJECT / "footprints", target / "footprints")
        return target

    def test_charger_pin_swap_is_rejected(self):
        project = self.project_copy()
        path = project / "symbols" / "rgb-badge-coupon.kicad_sym"
        text = path.read_text(encoding="utf-8").replace(
            '(name "VAC" (effects', '(name "BAD" (effects', 1)
        path.write_text(text, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "pin name mismatch"):
            CHECK["check_libraries"](project)

    def test_charger_stencil_change_is_rejected(self):
        project = self.project_copy()
        path = project / "footprints" / "rgb-badge-coupon.pretty" / \
            "QFN_TI_RTW0024A_4x4mm_P0.5mm_EP2.7mm.kicad_mod"
        text = path.read_text(encoding="utf-8").replace(
            '(at -0.7 -0.7) (size 1.1 1.1)', '(at -0.6 -0.7) (size 1.1 1.1)', 1)
        path.write_text(text, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "stencil aperture positions mismatch"):
            CHECK["check_libraries"](project)

    def test_converter_land_change_is_rejected(self):
        project = self.project_copy()
        path = project / "footprints" / "rgb-badge-coupon.pretty" / "SOT5X3_TI_DRL0008A.kicad_mod"
        text = path.read_text(encoding="utf-8").replace('(size 0.67 0.3)', '(size 0.60 0.3)', 1)
        path.write_text(text, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "DRL pad 1 size mismatch"):
            CHECK["check_libraries"](project)

    def test_esd_ground_land_change_is_rejected(self):
        project = self.project_copy()
        path = project / "footprints" / "rgb-badge-coupon.pretty" / "USON_TI_DQA0010A.kicad_mod"
        text = path.read_text(encoding="utf-8").replace(
            '(pad "3" smd roundrect (at -0.4175 0) (size 0.565 0.4)',
            '(pad "3" smd roundrect (at -0.4175 0) (size 0.565 0.2)', 1)
        path.write_text(text, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "DQA0010A pad 3 size mismatch"):
            CHECK["check_libraries"](project)

    def test_current_monitor_pin_swap_is_rejected(self):
        project = self.project_copy()
        path = project / "symbols" / "rgb-badge-coupon.kicad_sym"
        text = path.read_text(encoding="utf-8").replace(
            '(name "IN+" (effects', '(name "BAD" (effects', 1)
        path.write_text(text, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "pin name mismatch"):
            CHECK["check_libraries"](project)

    def test_type_c_detector_side_stencil_change_is_rejected(self):
        project = self.project_copy()
        path = project / "footprints" / "rgb-badge-coupon.pretty" / \
            "X2QFN_TI_RWB0012A_1.6x1.6mm_P0.4mm.kicad_mod"
        text = path.read_text(encoding="utf-8").replace(
            '(pad "" smd roundrect (at -0.65 -0.20) (size 0.67 0.20)',
            '(pad "" smd roundrect (at -0.65 -0.20) (size 0.70 0.20)', 1)
        path.write_text(text, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "side stencil aperture size mismatch"):
            CHECK["check_libraries"](project)

    def test_type_c_detector_pin_swap_is_rejected(self):
        project = self.project_copy()
        path = project / "symbols" / "rgb-badge-coupon.kicad_sym"
        text = path.read_text(encoding="utf-8").replace(
            '(name "CC1" (effects', '(name "BAD" (effects', 1)
        path.write_text(text, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "pin name mismatch"):
            CHECK["check_libraries"](project)

    def test_led_converter_thermal_finger_change_is_rejected(self):
        project = self.project_copy()
        path = project / "footprints" / "rgb-badge-coupon.pretty" / \
            "VSON_TI_DSJ0014_4x3mm_P0.5mm_EP2.85x1.58mm.kicad_mod"
        text = path.read_text(encoding="utf-8").replace(
            '(at -1.8125 -0.69) (size 0.775 0.20)',
            '(at -1.8125 -0.69) (size 0.700 0.20)', 1)
        path.write_text(text, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "thermal-finger size mismatch"):
            CHECK["check_libraries"](project)

    def test_led_converter_stencil_change_is_rejected(self):
        project = self.project_copy()
        path = project / "footprints" / "rgb-badge-coupon.pretty" / \
            "VSON_TI_DSJ0014_4x3mm_P0.5mm_EP2.85x1.58mm.kicad_mod"
        text = path.read_text(encoding="utf-8").replace(
            '(at -0.725 -0.46) (size 1.25 0.66)',
            '(at -0.725 -0.30) (size 1.25 0.66)', 1)
        path.write_text(text, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "central stencil positions mismatch"):
            CHECK["check_libraries"](project)

    def test_led_converter_pin_swap_is_rejected(self):
        project = self.project_copy()
        path = project / "symbols" / "rgb-badge-coupon.kicad_sym"
        text = path.read_text(encoding="utf-8").replace(
            '(name "VINA" (effects', '(name "BAD" (effects', 1)
        path.write_text(text, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "pin name mismatch"):
            CHECK["check_libraries"](project)

    def test_fuel_gauge_land_change_is_rejected(self):
        project = self.project_copy()
        path = project / "footprints" / "rgb-badge-coupon.pretty" / \
            "TDFN_Maxim_T822-3_2x2mm_P0.5mm_EP0.7x1.38mm.kicad_mod"
        text = path.read_text(encoding="utf-8").replace(
            '(at -0.99 -0.75) (size 0.80 0.30)',
            '(at -0.95 -0.75) (size 0.80 0.30)', 1)
        path.write_text(text, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "pad 1 position mismatch"):
            CHECK["check_libraries"](project)

    def test_fuel_gauge_pin_swap_is_rejected(self):
        project = self.project_copy()
        path = project / "symbols" / "rgb-badge-coupon.kicad_sym"
        text = path.read_text(encoding="utf-8").replace(
            '(name "CTG" (effects', '(name "BAD" (effects', 1)
        path.write_text(text, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "pin name mismatch"):
            CHECK["check_libraries"](project)


if __name__ == "__main__":
    unittest.main()
