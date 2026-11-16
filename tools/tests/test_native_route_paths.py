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


class NativeProfileContext(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('profiles', ROOT/'tools/routing_snapshot_profiles.py')
        cls.profiles = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.profiles)

    def fixture(self, folder, rules=True):
        source, output = Path(folder)/'source.kicad_pcb', Path(folder)/'probe.kicad_pcb'
        source.write_bytes(b'(kicad_pcb source)\n');output.write_bytes(b'(kicad_pcb probe)\n')
        source.with_suffix('.kicad_pro').write_bytes(b'{"preserve": "\\u03bc"}\r\n')
        if rules:source.with_suffix('.kicad_dru').write_bytes(b'(version 1)\r\n# exact spaces  \r\n')
        return source, output

    def test_saved_probe_preserves_bytes_and_reloads_its_manifest(self):
        with tempfile.TemporaryDirectory() as folder:
            source, output = self.fixture(folder);original=source.read_bytes();expected=self.profiles.read_profiles(source)
            self.profiles.copy_profiles(source,output,expected)
            self.assertEqual(self.profiles.read_profiles(output),expected)
            for ext,data in expected.items():self.assertEqual(output.with_suffix(ext).read_bytes(),data)
            self.assertEqual(source.read_bytes(),original)

    def test_project_profile_is_required(self):
        with tempfile.TemporaryDirectory() as folder:
            source, _ = self.fixture(folder);source.with_suffix('.kicad_pro').unlink()
            with self.assertRaisesRegex(ValueError,'project profile'):self.profiles.read_profiles(source)

    def test_manifest_rejects_missing_rule_and_changed_profile_or_board(self):
        for change in ['missing-rule','changed-project','changed-board']:
            with self.subTest(change=change), tempfile.TemporaryDirectory() as folder:
                source,output=self.fixture(folder);self.profiles.copy_profiles(source,output,self.profiles.read_profiles(source))
                if change=='missing-rule':output.with_suffix('.kicad_dru').unlink()
                elif change=='changed-project':output.with_suffix('.kicad_pro').write_text('{}')
                else:output.write_text('(kicad_pcb changed)')
                with self.assertRaisesRegex(ValueError,'context changed'):self.profiles.read_profiles(output)

    def test_intentionally_absent_rules_remain_absent(self):
        with tempfile.TemporaryDirectory() as folder:
            source,output=self.fixture(folder,rules=False);expected=self.profiles.read_profiles(source)
            self.assertIsNone(expected['.kicad_dru']);self.profiles.copy_profiles(source,output,expected)
            self.assertFalse(output.with_suffix('.kicad_dru').exists());self.assertEqual(self.profiles.read_profiles(output),expected)

    def test_stale_destination_rule_is_rejected_before_writing_project(self):
        with tempfile.TemporaryDirectory() as folder:
            source,output=self.fixture(folder,rules=False);rule=output.with_suffix('.kicad_dru');rule.write_text('(stale)')
            with self.assertRaisesRegex(ValueError,'stale custom rules'):self.profiles.copy_profiles(source,output,self.profiles.read_profiles(source))
            self.assertFalse(output.with_suffix('.kicad_pro').exists());self.assertEqual(rule.read_text(),'(stale)')

    def test_source_change_during_search_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            source,output=self.fixture(folder);expected=self.profiles.read_profiles(source);source.with_suffix('.kicad_pro').write_text('{}')
            with self.assertRaisesRegex(ValueError,'changed during search'):self.profiles.copy_profiles(source,output,expected)
            self.assertFalse(output.with_suffix('.kicad_pro').exists())

    def test_all_search_entry_points_reject_missing_or_changed_context_before_kicad(self):
        entries=[('search-native-control-profiled.py','DISPLAY_HEARTBEAT'),('search-routing-closure-profiled.py','DISPLAY_HEARTBEAT'),('search-u36-stage-profiled.py','GND')]
        for filename,net in entries:
            for problem in ['missing-project','changed-rule']:
                with self.subTest(tool=filename,problem=problem), tempfile.TemporaryDirectory() as folder:
                    source,output=self.fixture(folder)
                    if problem=='missing-project':source.with_suffix('.kicad_pro').unlink()
                    else:
                        self.profiles.copy_profiles(source,output,self.profiles.read_profiles(source));source=output
                        source.with_suffix('.kicad_dru').write_text('(changed)')
                    result=subprocess.run([sys.executable,str(ROOT/'tools'/filename),'--source',str(source),'--nets',net],capture_output=True,text=True)
                    self.assertEqual(result.returncode,2,result.stderr)
                    self.assertIn('project profile' if problem=='missing-project' else 'context changed',result.stderr)
                    self.assertNotIn('ModuleNotFoundError',result.stderr)

    def test_source_context_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as folder:
            source,_=self.fixture(folder);expected=self.profiles.read_profiles(source)
            with self.assertRaisesRegex(ValueError,'overwrite'):self.profiles.copy_profiles(source,source,expected)
            self.assertEqual(self.profiles.read_profiles(source),expected)


if __name__ == '__main__':
    unittest.main()
