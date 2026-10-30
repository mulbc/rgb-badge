#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Report complete KiCad connectivity for the staged coupon PCB.

Run with KiCad's bundled Python; the CLI DRC JSON truncates the large
unconnected list in this early board study.
"""

import argparse
from collections import defaultdict
import hashlib
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


def open_edges_by_net(path):
    """Count connected pad clusters per net using KiCad's native connectivity."""
    board = pcb.LoadBoard(str(path))
    connected = board.GetConnectivity()
    nets = defaultdict(list)
    for footprint in board.GetFootprints():
        for pad in footprint.Pads():
            if pad.GetNetname():
                nets[pad.GetNetname()].append(pad)
    counts = {}
    for name, pads in nets.items():
        clusters = {
            tuple(sorted(item.m_Uuid.AsString()
                         for item in connected.GetConnectedItems(pad)
                         if isinstance(item, pcb.PAD)))
            for pad in pads
        }
        if len(clusters) > 1:
            counts[name] = len(clusters) - 1
    return {
        "SPDX-License-Identifier": "CERN-OHL-S-2.0",
        "board": str(path.resolve().relative_to(ROOT)),
        "board_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "native_open_edges": connected.GetUnconnectedCount(False),
        "pad_cluster_open_edges": sum(counts.values()),
        "by_net": dict(sorted(counts.items(), key=lambda item: (-item[1], item[0]))),
        "interpretation": "Unconnected pad clusters minus one per net; no electrical or manufacturability qualification",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("board", nargs="?", type=Path, default=DEFAULT_BOARD)
    parser.add_argument("--by-net", action="store_true",
                        help="show the native open-edge count for each pad net")
    args = parser.parse_args()
    result = open_edges_by_net(args.board) if args.by_net else report(args.board)
    print(json.dumps(result, indent=2, sort_keys=not args.by_net))


if __name__ == "__main__":
    main()
