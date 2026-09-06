<!-- SPDX-License-Identifier: Apache-2.0 -->

# Software tools

Host-side utilities will include the deterministic content compiler, schema validation, release-manifest generation and analysis of power/runtime logs. Tools must be testable without a connected badge and must not rewrite measured evidence.

`check-led-libraries.py` audits the exact Coupon Rev A LED symbol pin maps, source drawing layout, footprint pads, polarity geometry and the nominal 1.95 mm checkerboard-clearance calculation. `check-kicad.sh` runs that audit, loads and exports the project-local libraries through KiCad 10, and runs schematic ERC. Numbered fabrication views and solid copper-only views are exported into separate directories.

Run the wrapper regression tests without KiCad:

```bash
python3 -m unittest discover -s tools/tests -p 'test_*.py' -v
```

These tests use a stub executable to check CLI arguments, output separation and failure handling. They do not render KiCad files, run real ERC, prove legibility or approve hardware. The actual `./tools/check-kicad.sh` run and human inspection remain required.
