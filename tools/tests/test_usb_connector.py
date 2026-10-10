# SPDX-License-Identifier: Apache-2.0
"""Fault injection for connector mapping and mechanical release boundaries."""

from copy import deepcopy
from pathlib import Path
import runpy
import unittest

CHECK = runpy.run_path(str(Path(__file__).resolve().parents[1] / "check-usb-connector.py"))


class USBConnectorTests(unittest.TestCase):
    def footprint(self):
        return CHECK["HELP"]["footprint"](CHECK["PROJECT"], CHECK["FOOTPRINT"])

    def test_source_passes(self):
        CHECK["check_libraries"]()

    def test_mirrored_contact_positions_fail(self):
        root = self.footprint()
        for pad in CHECK["children"](root, "pad"):
            at = CHECK["one"](pad, "at", "pad")
            at[1] = str(-float(at[1]))
        with self.assertRaisesRegex(ValueError, "position/rotation"):
            CHECK["check_footprint"](root)

    def test_cc_swap_fails(self):
        lib = CHECK["parse"](CHECK["PROJECT"] / "symbols" / "rgb-badge-coupon.kicad_sym")
        symbol = next(s for s in CHECK["children"](lib, "symbol") if s[1] == CHECK["MPN"])
        pins = CHECK["HELP"]["library_pins"](symbol)
        CHECK["one"](pins["A5"], "name", "pin")[1] = "CC2"
        with self.assertRaisesRegex(ValueError, "contact function"):
            CHECK["check_symbol"](symbol)

    def test_shared_land_cannot_be_duplicated(self):
        root = self.footprint()
        pad = next(p for p in CHECK["children"](root, "pad") if p[1] == "A1_B12")
        extra = deepcopy(pad)
        pad[1], extra[1] = "A1", "B12"
        root.append(extra)
        with self.assertRaisesRegex(ValueError, "shared-land"):
            CHECK["check_footprint"](root)

    def test_slot_dimension_change_fails(self):
        root = self.footprint()
        pad = next(p for p in CHECK["children"](root, "pad") if p[1] == "S1")
        CHECK["one"](pad, "drill", "stake")[3] = "1.8"
        with self.assertRaisesRegex(ValueError, "slot mismatch"):
            CHECK["check_footprint"](root)

    def test_unqualified_edge_cut_fails(self):
        root = self.footprint()
        guide = next(g for g in CHECK["children"](root, "fp_line"))
        CHECK["one"](guide, "layer", "guide")[1] = "Edge.Cuts"
        with self.assertRaisesRegex(ValueError, "must not become Edge.Cuts"):
            CHECK["check_footprint"](root)
