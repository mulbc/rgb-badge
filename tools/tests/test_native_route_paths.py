# SPDX-License-Identifier: Apache-2.0
"""Host-only guards for exploratory native-route output and evidence paths."""
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('search', ROOT/'tools/search-native-control-routes.py')
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)


class NativeRoutePaths(unittest.TestCase):
    def test_relative_outputs_produce_absolute_snapshot_paths(self):
        with tempfile.TemporaryDirectory() as folder:
            build = Path(folder)/'build'
            source, output, report = s.review_paths(Path(folder)/'source.kicad_pcb',
                os.path.relpath(build/'trial.kicad_pcb'), os.path.relpath(build/'report.json'), build)
            snapshot = s.rejection_snapshot_path(output, source, 'UART0_TX', 'TP4', '1')
            self.assertEqual(snapshot.relative_to(build.resolve()),
                             Path('trial-rejected/UART0_TX-TP4-1.kicad_pcb'))
            self.assertTrue(report.is_absolute())

    def test_different_probe_outputs_cannot_overwrite_each_others_rejections(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder).resolve()
            a = s.rejection_snapshot_path(base/'first.kicad_pcb', base/'source.kicad_pcb', 'X', 'U1', '1')
            b = s.rejection_snapshot_path(base/'second.kicad_pcb', base/'source.kicad_pcb', 'X', 'U1', '1')
            self.assertNotEqual(a, b)
            self.assertNotEqual(a.with_suffix('.json'), b.with_suffix('.json'))

    def test_snapshot_names_keep_slashes_and_traversal_inside_the_output_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder).resolve()
            path = s.rejection_snapshot_path(base/'trial.kicad_pcb', base/'source.kicad_pcb',
                                             'net/../name', '../U1', '1/2')
            self.assertEqual(path.parent, base/'trial-rejected')
            self.assertIn('%2F', path.name)

    def test_source_tree_and_colliding_destinations_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder).resolve(); build = base/'build'; source = base/'source.kicad_pcb'
            for output, report in [(source, build/'report.json'),
                                   (build/'trial.kicad_pcb', source),
                                   (build/'same', build/'same')]:
                with self.subTest(output=output, report=report), self.assertRaises(ValueError):
                    s.review_paths(source, output, report, build)

    def test_rejected_board_and_sidecar_cannot_overwrite_the_input(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder).resolve()
            output = base/'trial.kicad_pcb'
            path = s.rejection_snapshot_path(output, base/'source.kicad_pcb', 'X', 'U1', '1')
            for source in (path, path.with_suffix('.json')):
                with self.subTest(source=source), self.assertRaises(ValueError):
                    s.rejection_snapshot_path(output, source, 'X', 'U1', '1')

    def test_help_and_invalid_arguments_work_without_importing_kicad(self):
        tool = str(ROOT/'tools/search-native-control-routes.py')
        self.assertEqual(subprocess.run([sys.executable, tool, '--help'], capture_output=True).returncode, 0)
        for arguments in [ ['--nets', 'VLED'], ['--max-nodes', '0'],
                           ['--output', str(ROOT/'hardware/coupon/rev-a/staging/forbidden.kicad_pcb')],
                           ['--heuristic', 'unknown'] ]:
            with self.subTest(arguments=arguments):
                result = subprocess.run([sys.executable, tool]+arguments, capture_output=True, text=True)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertNotIn('ModuleNotFoundError', result.stderr)


if __name__ == '__main__':
    unittest.main()
