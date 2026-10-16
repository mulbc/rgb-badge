#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Report complete KiCad connectivity for the staged coupon PCB.

Run with KiCad's bundled Python; the CLI DRC JSON truncates the large
unconnected list in this early board study.
"""

import argparse
import json
from pathlib import Path

import pcbnew as pcb


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BOARD = ROOT / "hardware/coupon/rev-a/staging/full-coupon-placement-trial-120mm.kicad_pcb"


def report(path):
    board = pcb.LoadBoard(str(path))
    if board is None:
        raise ValueError(f"KiCad could not load {path}")
    tracks = list(board.GetTracks())
    return {
        "SPDX-License-Identifier": "Apache-2.0",
        "board": str(path.resolve()),
        "footprints": len(list(board.GetFootprints())),
        "copper_layers": board.GetCopperLayerCount(),
        "track_segments": sum(isinstance(item, pcb.PCB_TRACK) and not isinstance(item, pcb.PCB_VIA)
                              for item in tracks),
        "vias": sum(isinstance(item, pcb.PCB_VIA) for item in tracks),
        "open_connection_edges": board.GetConnectivity().GetUnconnectedCount(False),
        "interpretation": "KiCad connectivity/ratsnest edges, not a completed-board DRC pass",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("board", nargs="?", type=Path, default=DEFAULT_BOARD)
    args = parser.parse_args()
    print(json.dumps(report(args.board), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
