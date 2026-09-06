#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Make a legible review copy of a four-pad KiCad 10 fabrication SVG.

The original export is never rewritten. Copy KiCad's own numbered glyph paths
above the drawing with a white halo; never infer a pin number or move geometry.
This derived view is for review, not manufacturing or dimensional measurement.
"""

import argparse
from copy import deepcopy
import hashlib
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)


def tag(name):
    return f"{{{SVG}}}{name}"


def numbered_review(source):
    root = ET.fromstring(source)
    if root.tag != tag("svg") or root.find(".//*[@id='review-pad-labels']") is not None:
        raise ValueError("Expected an unprocessed KiCad fabrication SVG")

    labels = {}
    # KiCad 10 writes untransformed, stroked-text groups inside root-level
    # style groups. Reject a changed structure rather than misplace a label.
    for parent in root.findall(tag("g")):
        for glyph in parent.findall(tag("g")):
            number = glyph.findtext(tag("desc"), "")
            if not number.isdigit():
                continue
            if number not in {"1", "2", "3", "4"} or number in labels:
                raise ValueError("Expected each pad number 1, 2, 3, 4 exactly once")
            if any("transform" in item.attrib for item in (root, parent, *glyph.iter())):
                raise ValueError("Transformed pad text requires a new review")
            if glyph.get("class") != "stroked-text" or not glyph.findall(tag("path")):
                raise ValueError("Expected KiCad's stroked pad-number glyph paths")
            if any(item.tag not in {tag("desc"), tag("path")} for item in glyph):
                raise ValueError("Unexpected pad-number glyph content")
            if any(set(path.attrib) != {"d"} for path in glyph.findall(tag("path"))):
                raise ValueError("Unexpected styled pad-number path")
            style = dict(item.strip().split(":", 1) for item in parent.get("style", "").split(";") if item.strip())
            width = float(style.get("stroke-width", "nan"))
            if style.get("stroke") != "#000000" or not 0 < width < 0.05:
                raise ValueError("Expected black pad-number strokes in millimetres")
            labels[number] = (glyph, parent.get("style"), width)
    if set(labels) != {"1", "2", "3", "4"}:
        raise ValueError("Expected each pad number 1, 2, 3, 4 exactly once")

    title = root.find(tag("title"))
    if title is not None:
        title.text = "Numbered review copy — " + (title.text or "")
    metadata = ET.SubElement(root, tag("metadata"))
    metadata.text = (
        "Derived review only; original KiCad glyphs overlaid with white halos. "
        "Source SVG SHA-256: " + hashlib.sha256(source).hexdigest()
    )
    overlay = ET.SubElement(root, tag("g"), {"id": "review-pad-labels"})
    for number in sorted(labels):
        glyph, style, width = labels[number]
        layer = ET.SubElement(overlay, tag("g"), {"data-pad": number, "style": style})
        halo = deepcopy(glyph)
        halo.set("class", "review-label-halo")
        halo.set("style", f"fill:none;stroke:#ffffff;stroke-width:{width + 0.05:.6f};stroke-opacity:1")
        layer.append(halo)
        layer.append(deepcopy(glyph))

    # Give the courtyard/marker strokes room at the edge without moving them.
    x, y, width, height = map(float, root.get("viewBox", "").split())
    if root.get("width") != f"{width:.6f}mm" or root.get("height") != f"{height:.6f}mm":
        raise ValueError("Expected the KiCad millimetre viewBox and dimensions")
    margin = 0.1
    root.set("viewBox", f"{x-margin:.6f} {y-margin:.6f} {width+2*margin:.6f} {height+2*margin:.6f}")
    root.set("width", f"{width+2*margin:.6f}mm")
    root.set("height", f"{height+2*margin:.6f}mm")
    serialized = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    return b"\n".join(line.rstrip() for line in serialized.splitlines()) + b"\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path, help="New derived SVG; must not already exist")
    args = parser.parse_args()
    try:
        result = numbered_review(args.source.read_bytes())
        with args.output.open("xb") as output:
            output.write(result)
    except (OSError, ValueError, ET.ParseError) as error:
        print(f"Numbered footprint review failed: {error}", file=sys.stderr)
        return 1
    print(f"Created derived numbered review: {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
