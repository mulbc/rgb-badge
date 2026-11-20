# SPDX-License-Identifier: Apache-2.0
"""Protect source evidence and pad-label identity in derived review SVGs."""

from copy import deepcopy
import hashlib
from pathlib import Path
import runpy
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET

from fixtures.kicad_cli_stub import fabrication_svg


SCRIPT = Path(__file__).resolve().parents[1] / "number-footprint-review.py"
numbered_review = runpy.run_path(str(SCRIPT))["numbered_review"]
NS = {"svg": "http://www.w3.org/2000/svg"}


class NumberedFootprintReviewTests(unittest.TestCase):
    def test_original_geometry_and_glyphs_preserved(self):
        source = fabrication_svg().encode()
        original = ET.fromstring(source)
        result = ET.fromstring(numbered_review(source))
        original_groups = original.findall("svg:g", NS)
        result_groups = result.findall("svg:g", NS)
        self.assertEqual(
            [ET.tostring(item) for item in result_groups[:-1]],
            [ET.tostring(item) for item in original_groups],
        )
        self.assertIn(hashlib.sha256(source).hexdigest(), result.findtext("svg:metadata", namespaces=NS))
        overlay = result_groups[-1]
        self.assertEqual(overlay.get("id"), "review-pad-labels")
        self.assertEqual([group.get("data-pad") for group in overlay], ["1", "2", "3", "4"])
        for original_group, new_group in zip(original_groups, overlay):
            glyph = original_group.find("svg:g", NS)
            halo, ink = list(new_group)
            self.assertEqual(ET.tostring(ink), ET.tostring(glyph))
            self.assertIn("stroke:#ffffff", halo.get("style"))
            self.assertEqual(
                [path.get("d") for path in halo.findall("svg:path", NS)],
                [path.get("d") for path in glyph.findall("svg:path", NS)],
            )

    def test_missing_duplicate_and_transformed_labels_rejected(self):
        original = ET.fromstring(fabrication_svg())
        for change in ("missing", "duplicate", "transform"):
            with self.subTest(change=change):
                root = deepcopy(original)
                if change == "missing":
                    root.remove(root.findall("svg:g", NS)[-1])
                elif change == "duplicate":
                    root.append(deepcopy(root.findall("svg:g", NS)[-1]))
                else:
                    root.findall("svg:g", NS)[0].set("transform", "translate(1 0)")
                with self.assertRaises(ValueError):
                    numbered_review(ET.tostring(root))

    def test_compound_pad_profile_preserves_geometry_and_first_glyph(self):
        source = fabrication_svg("rpw").encode()
        original = ET.fromstring(source)
        result = ET.fromstring(numbered_review(source, "rpw"))
        overlay = result.findall("svg:g", NS)[-1]
        self.assertEqual([g.get("data-pad") for g in overlay],
                         [str(n) for n in range(1, 11)])
        first = {}
        for parent in original.findall("svg:g", NS):
            for glyph in list(parent):
                number = glyph.findtext("svg:desc", namespaces=NS)
                if number and number.isdigit():
                    first.setdefault(number, deepcopy(glyph))
                    parent.remove(glyph)
        self.assertEqual([ET.tostring(g) for g in original.findall("svg:g", NS)],
                         [ET.tostring(g) for g in result.findall("svg:g", NS)[:-1]])
        for group in overlay:
            self.assertEqual(ET.tostring(group[-1]), ET.tostring(first[group.get("data-pad")]))
        self.assertIn(hashlib.sha256(source).hexdigest(), result.findtext("svg:metadata", namespaces=NS))

    def test_compound_pad_profile_rejects_wrong_multiplicity(self):
        source = fabrication_svg("rpw")
        for changed in (source.replace("<desc>10</desc>", "<desc>9</desc>", 1),
                        fabrication_svg()):
            with self.assertRaises(ValueError):
                numbered_review(changed.encode(), "rpw")
        with self.assertRaises(ValueError):
            numbered_review(source.encode())

    def test_existing_evidence_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "original.svg"
            source.write_text(fabrication_svg())
            before = source.read_bytes()
            result = subprocess.run(
                ["python3", str(SCRIPT), str(source), str(source)],
                capture_output=True, text=True, timeout=10,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(source.read_bytes(), before)

    def test_derived_output_cannot_be_reprocessed(self):
        with self.assertRaises(ValueError):
            numbered_review(numbered_review(fabrication_svg().encode()))


if __name__ == "__main__":
    unittest.main()
