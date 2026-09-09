# SPDX-License-Identifier: Apache-2.0
"""Tests for strict staged-boundary handling in KiCad ERC reports."""

from pathlib import Path
import runpy
import tempfile
import unittest


CHECK = runpy.run_path(str(Path(__file__).resolve().parents[1] / "check-erc-report.py"))


def report(records: str, total: int, errors: int, warnings: int) -> str:
    return f"""ERC report (test fixture, Encoding UTF8)
Report includes: Errors, Warnings, Exclusions

***** Sheet /
{records}
 ** ERC messages: {total}  Errors {errors}  Warnings {warnings}
"""


USB_WARNINGS = """[isolated_pin_label]: Label connected to only one pin
    ; warning
    @(350.52 mm, 66.04 mm): Global Label 'USB_D-'
[isolated_pin_label]: Label connected to only one pin
    ; warning
    @(350.52 mm, 81.28 mm): Global Label 'USB_D+'
"""

USB_DN_WARNING = """[isolated_pin_label]: Label connected to only one pin
    ; warning
    @(350.52 mm, 66.04 mm): Global Label 'USB_D-'
"""


class ErcReportTests(unittest.TestCase):
    def check(self, contents: str) -> str:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "erc.rpt"
            path.write_text(contents, encoding="utf-8")
            return CHECK["check_report"](path)

    def test_zero_violations_pass(self):
        self.assertIn("0 violations", self.check(report("", 0, 0, 0)))

    def test_exact_usb_boundary_pair_passes(self):
        self.assertIn("temporary USB-boundary", self.check(report(USB_WARNINGS, 2, 0, 2)))

    def test_partial_pair_is_rejected(self):
        with self.assertRaises(ValueError):
            self.check(report(USB_DN_WARNING, 1, 0, 1))

    def test_unexpected_warning_is_rejected(self):
        unexpected = """[isolated_pin_label]: Label connected to only one pin
    ; warning
    @(10.00 mm, 20.00 mm): Global Label 'UNEXPECTED'
"""
        with self.assertRaises(ValueError):
            self.check(report(unexpected, 1, 0, 1))

    def test_inconsistent_summary_is_rejected(self):
        with self.assertRaises(ValueError):
            self.check(report(USB_WARNINGS, 1, 0, 1))


if __name__ == "__main__":
    unittest.main()
