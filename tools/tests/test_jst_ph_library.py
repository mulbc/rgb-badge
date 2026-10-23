# SPDX-License-Identifier: Apache-2.0
"""Fault injection for the staged battery-header contact map."""

from pathlib import Path
import runpy
import tempfile
import unittest


CHECK = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'check-jst-ph-library.py'))


class JstPhLibraryTests(unittest.TestCase):
    def test_staged_header_land(self):
        self.assertTrue(CHECK['check']())

    def test_reversed_contact_numbers_are_rejected(self):
        function = CHECK['check']
        source = function.__globals__['SOURCE']
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / source.name
            text = source.read_text(encoding='utf-8')
            text = text.replace('(pad "1" smd', '(pad "X" smd', 1)
            text = text.replace('(pad "2" smd', '(pad "1" smd', 1)
            text = text.replace('(pad "X" smd', '(pad "2" smd', 1)
            copy.write_text(text, encoding='utf-8')
            function.__globals__['SOURCE'] = copy
            try:
                with self.assertRaisesRegex(ValueError, 'pad map changed'):
                    function()
            finally:
                function.__globals__['SOURCE'] = source


if __name__ == '__main__':
    unittest.main()
