# SPDX-License-Identifier: Apache-2.0
"""Regression tests for the shell wrapper, not KiCad or electrical validation."""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]
CHECK_SCRIPT = REPO_ROOT / "tools" / "check-kicad.sh"
CLI_STUB = Path(__file__).resolve().parent / "fixtures" / "kicad_cli_stub.py"


class CheckKiCadWrapperTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="rgb-badge-wrapper-test-")
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.output = self.directory / "review output with spaces"

    def run_check(self, **test_environment):
        environment = {
            key: value for key, value in os.environ.items()
            if not key.startswith("RGB_BADGE_TEST_")
        }
        environment.update({
            "RGB_BADGE_KICAD_CLI": str(CLI_STUB),
            "RGB_BADGE_KICAD_CHECK_OUTPUT": str(self.output),
            **test_environment,
        })
        return subprocess.run(
            ["bash", str(CHECK_SCRIPT)],
            cwd=self.directory,
            env=environment,
            capture_output=True,
            text=True,
            timeout=30,
        )

    def test_separate_raw_views_and_numbered_copies(self):
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(len(list((self.output / "symbols").glob("*.svg"))), 2)
        for view in ("fabrication", "copper", "numbered"):
            self.assertEqual(len(list((self.output / "footprints" / view).glob("*.svg"))), 2)
        self.assertTrue((self.output / "coupon-erc.rpt").is_file())
        self.assertTrue((self.output / "coupon-matrix.xml").is_file())
        self.assertTrue((self.output / "coupon-schematic.pdf").is_file())

    def test_numbering_failure_is_not_hidden(self):
        result = self.run_check(RGB_BADGE_TEST_BAD_LABELS="1")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Numbered footprint review failed", result.stderr)
        self.assertFalse((self.output / "coupon-erc.rpt").exists())

    def test_missing_specific_copper_file_is_rejected(self):
        result = self.run_check(RGB_BADGE_TEST_MISSING="1")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Expected non-empty SVG", result.stderr)
        self.assertIn("copper/LED_QTBrightek_QBLP1515A-RGB2A.svg", result.stderr)
        self.assertFalse((self.output / "coupon-erc.rpt").exists())

    def test_empty_specific_copper_file_is_rejected(self):
        result = self.run_check(RGB_BADGE_TEST_EMPTY="1")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Expected non-empty SVG", result.stderr)

    def test_export_failure_is_not_hidden(self):
        result = self.run_check(RGB_BADGE_TEST_FAIL="copper")
        self.assertEqual(result.returncode, 7)
        self.assertNotIn("ERC passed", result.stdout)

    def test_erc_failure_is_not_hidden(self):
        result = self.run_check(RGB_BADGE_TEST_FAIL="sch/erc")
        self.assertEqual(result.returncode, 5)
        self.assertNotIn("ERC passed", result.stdout)

    def test_bad_matrix_netlist_is_not_hidden(self):
        result = self.run_check(RGB_BADGE_TEST_BAD_MATRIX="1")
        self.assertEqual(result.returncode, 1)
        self.assertIn('Matrix check failed', result.stderr)
        self.assertFalse((self.output / 'coupon-schematic.pdf').exists())

    def test_netlist_and_pdf_export_failures_are_not_hidden(self):
        for stage in ('netlist', 'pdf'):
            with self.subTest(stage=stage):
                self.output = self.directory / stage
                result = self.run_check(RGB_BADGE_TEST_FAIL=stage)
                self.assertEqual(result.returncode, 7)
                self.assertNotIn('matrix connectivity and Coupon Rev A ERC passed', result.stdout)

    def test_wrong_kicad_version_is_rejected(self):
        result = self.run_check(RGB_BADGE_TEST_VERSION="9.0.0")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Expected stable KiCad 10.0.x", result.stderr)
        self.assertFalse(self.output.exists())

    def test_existing_output_is_preserved(self):
        self.output.mkdir()
        sentinel = self.output / "keep.txt"
        sentinel.write_text("Existing review evidence\n", encoding="utf-8")
        result = self.run_check()
        self.assertEqual(result.returncode, 2)
        self.assertIn("path that does not exist", result.stderr)
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "Existing review evidence\n")


if __name__ == "__main__":
    unittest.main()
