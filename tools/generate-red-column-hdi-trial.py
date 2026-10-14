#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Route all 16 coupon red cathode columns in a provisional HDI study.

This is a geometric experiment on a copy of the 120 mm staging PCB. The
0.3/0.1 mm via-in-pad F.Cu--In1.Cu microvias and stack-up are not selected for
manufacturing, and green/blue, driver fanout and current capacity remain open.
"""

from pathlib import Path
import uuid

import pcbnew as pcb


ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "hardware/coupon/rev-a/staging"
SOURCE = STAGING / "full-coupon-placement-trial-120mm.kicad_pcb"
OUTPUT = STAGING / "red-column-hdi-trial-120mm.kicad_pcb"
SCOPE = uuid.UUID("429fa924-fc75-5477-bb1a-f09f90c5a793")


def stable_id(item, name):
    item.SetUuid(pcb.KIID(str(uuid.uuid5(SCOPE, name))))


def generate():
    board = pcb.LoadBoard(str(SOURCE))
    if board is None or board.GetCopperLayerCount() != 6:
        raise ValueError("Expected the existing six-layer coupon staging board")
    parts = {part.GetReference(): part for part in board.GetFootprints()}
    assert len(parts) == 497
    old_track_count = len(list(board.GetTracks()))
    for col in range(16):
        pin_number = "2" if col < 8 else "4"
        pads = []
        for row in range(16):
            ref = f"D{row * 16 + col + 1}"
            part = parts[ref]
            pad = next(pad for pad in part.Pads() if pad.GetNumber() == pin_number)
            assert pad.GetNetname() == f"COL_{col:02d}_R", ref
            pads.append(pad)
        for row, pad in enumerate(pads):
            via = pcb.PCB_VIA(board)
            via.SetPosition(pad.GetPosition())
            via.SetViaType(pcb.VIATYPE_MICROVIA)
            via.SetLayerPair(pcb.F_Cu, pcb.In1_Cu)
            via.SetWidth(pcb.FromMM(0.3))
            via.SetDrill(pcb.FromMM(0.1))
            via.SetNet(pad.GetNet())
            stable_id(via, f"red-{col:02d}-{row:02d}-via")
            board.Add(via)
        for row, (start, end) in enumerate(zip(pads, pads[1:])):
            segment = pcb.PCB_TRACK(board)
            segment.SetStart(start.GetPosition())
            segment.SetEnd(end.GetPosition())
            segment.SetWidth(pcb.FromMM(0.2))
            segment.SetLayer(pcb.In1_Cu)
            segment.SetNet(start.GetNet())
            stable_id(segment, f"red-{col:02d}-{row:02d}-segment")
            board.Add(segment)
    assert len(list(board.GetTracks())) == old_track_count + 256 + 240
    assert pcb.SaveBoard(str(OUTPUT), board)
    loaded = pcb.LoadBoard(str(OUTPUT))
    assert len(list(loaded.GetFootprints())) == 497
    assert loaded.GetConnectivity().GetUnconnectedCount(False) == 1209
    print(f"Saved 256 microvias and 240 red-column segments to {OUTPUT}")
    print("1209 remaining KiCad connectivity edges; geometry/process still unqualified")


if __name__ == "__main__":
    generate()
