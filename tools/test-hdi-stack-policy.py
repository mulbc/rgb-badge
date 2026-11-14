#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Physical eligibility and rejection tests independent of native KiCad."""
import copy
import json
from pathlib import Path
import unittest
from hdi_stack_policy import validate_plan, via_findings

PLAN = json.loads((Path(__file__).resolve().parents[1] / 'manufacturing/planning/coupon-six-layer-stack.json').read_text())


class StackPolicy(unittest.TestCase):
    def test_sum_rejects_old_1p6_label(self):
        self.assertEqual(validate_plan(PLAN), 800)
        bad = copy.deepcopy(PLAN); bad['laminate_and_copper_sum_um'] = 1600
        with self.assertRaisesRegex(ValueError, 'thickness'):
            validate_plan(bad)

    def test_outer_and_second_build_up_pass_nominal_geometry(self):
        for span in [['F.Cu','In1.Cu'], ['In1.Cu','In2.Cu'], ['In3.Cu','In4.Cu'], ['In4.Cu','B.Cu']]:
            self.assertEqual(via_findings(PLAN, dict(kind='microvia', layers=span, pad_um=300, hole_um=100)), [])

    def test_central_laser_via_is_forbidden(self):
        self.assertEqual(via_findings(PLAN, dict(kind='microvia', layers=['In2.Cu','In3.Cu'], pad_um=300, hole_um=100)),
                         ['VIA_KIND_OR_SPAN_NOT_ALLOWED'])

    def test_central_mechanical_requires_real_pad_and_drill(self):
        span = ['In2.Cu','In3.Cu']
        self.assertEqual(via_findings(PLAN, dict(kind='buried', layers=span, pad_um=500, hole_um=300)), [])
        errors = via_findings(PLAN, dict(kind='buried', layers=span, pad_um=300, hole_um=100))
        self.assertIn('VIA_PAD_TOO_SMALL', errors)
        self.assertIn('VIA_HOLE_DIFFERS', errors)

    def test_nominal_depth_and_annulus_are_enforced(self):
        bad = copy.deepcopy(PLAN); bad['dielectric_um'][0] = 81
        self.assertIn('NOMINAL_ASPECT_RATIO_EXCEEDED', via_findings(bad, dict(kind='microvia', layers=['F.Cu','In1.Cu'], pad_um=300, hole_um=100)))
        self.assertIn('ANNULAR_RING_TOO_SMALL', via_findings(PLAN, dict(kind='microvia', layers=['F.Cu','In1.Cu'], pad_um=250, hole_um=100)))

    def test_unknown_spans_nan_and_permission_fail_closed(self):
        self.assertEqual(via_findings(PLAN, dict(kind='blind', layers=['F.Cu','In2.Cu'], pad_um=500, hole_um=300)), ['VIA_KIND_OR_SPAN_NOT_ALLOWED'])
        self.assertEqual(via_findings(PLAN, dict(kind='microvia', layers=['F.Cu','In1.Cu'], pad_um=float('nan'), hole_um=100)), ['INVALID_VIA_DIMENSIONS'])
        bad = copy.deepcopy(PLAN); bad['fabrication_release_allowed'] = True
        with self.assertRaisesRegex(ValueError, 'fabrication'):
            validate_plan(bad)

    def test_through_via_is_distinct_from_buried_span(self):
        self.assertEqual(via_findings(PLAN, dict(kind='through', layers=['F.Cu','B.Cu'], pad_um=500, hole_um=300)), [])
        self.assertEqual(via_findings(PLAN, dict(kind='through', layers=['In2.Cu','In3.Cu'], pad_um=500, hole_um=300)), ['VIA_KIND_OR_SPAN_NOT_ALLOWED'])


if __name__ == '__main__':
    unittest.main()
