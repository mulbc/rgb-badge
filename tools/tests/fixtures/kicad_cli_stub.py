#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Test-only CLI stub. Its output is not a KiCad render or ERC result."""

import os
from pathlib import Path
import sys


def fabrication_svg():
    # Minimal KiCad-shaped text structure for wrapper/overlay tests. The paths
    # are deliberately dummy strokes, not a real LED footprint or digit font.
    groups = "".join(
        f'<g style="fill:none;stroke:#000000;stroke-width:0.012500;stroke-linecap:round">'
        f'<g class="stroked-text"><desc>{number}</desc>'
        f'<path d="M{x} {y} L{x + 0.1} {y + 0.15}"/></g></g>'
        for number, x, y in ((1, 1.3, 0.4), (2, 1.3, 1.3), (3, 0.4, 1.3), (4, 0.4, 0.4))
    )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="2.000000mm" '
        'height="2.000000mm" viewBox="0.000000 0.000000 2.000000 2.000000">'
        '<title>Stub only, not a KiCad render</title>' + groups + '</svg>\n'
    )


def main():
    args = sys.argv[1:]
    if args == ["version"]:
        print(os.environ.get("RGB_BADGE_TEST_VERSION", "10.0.6"))
        return 0

    output = Path(args[args.index("--output") + 1])
    stage = "/".join(args[:2])
    if args[:3] == ["sym", "export", "svg"]:
        names = ["EAST10105RGBA0_unit1.svg", "QBLP1515A-RGB2A_unit1.svg"]
    elif args[:3] == ["fp", "export", "svg"]:
        layers = args[args.index("--layers") + 1]
        if output.name == "fabrication":
            assert layers == "F.Fab,F.SilkS,F.CrtYd", "Fabrication view must exclude solid pad layers"
            assert "--sketch-pads-on-fab-layers" in args
        elif output.name == "copper":
            assert layers == "F.Cu", "Copper view must exclude non-copper outlines"
            assert "--sketch-pads-on-fab-layers" not in args
        else:
            raise AssertionError(f"Unexpected footprint export destination: {output}")
        stage = output.name
        names = ["LED_Everlight_EAST10105RGBA0.svg", "LED_QTBrightek_QBLP1515A-RGB2A.svg"]
    elif args[:2] == ["sch", "erc"]:
        assert "--severity-all" in args and "--exit-code-violations" in args
        if os.environ.get("RGB_BADGE_TEST_FAIL") == stage:
            return 5
        output.write_text("Stub only: no real ERC was run.\n", encoding="utf-8")
        return 0
    else:
        raise AssertionError(f"Unexpected command: {args}")

    if os.environ.get("RGB_BADGE_TEST_FAIL") == stage:
        return 7
    for name in names:
        file = output / name
        # Always exercise a missing/empty export of the second copper part.
        target = stage == "copper" and "QTBrightek" in name
        if target and os.environ.get("RGB_BADGE_TEST_MISSING") == "1":
            continue
        svg = '<svg xmlns="http://www.w3.org/2000/svg"><desc>Test stub, not a KiCad render</desc></svg>\n'
        if stage == "fabrication":
            svg = fabrication_svg()
            if os.environ.get("RGB_BADGE_TEST_BAD_LABELS") == "1":
                svg = svg.replace('<desc>4</desc>', '<desc>3</desc>')
        if target and os.environ.get("RGB_BADGE_TEST_EMPTY") == "1":
            svg = ""
        file.write_text(svg, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
