# SPDX-License-Identifier: Apache-2.0
"""Preserve exact KiCad profile context when native probes are saved and reused."""
import hashlib
import json
from pathlib import Path

EXTENSIONS = ('.kicad_pro', '.kicad_dru')


def profile_hashes(profiles):
    return {ext: hashlib.sha256(data).hexdigest() if data is not None else None
            for ext, data in profiles.items()}


def read_profiles(board):
    board = Path(board).resolve()
    if not board.is_file() or not board.with_suffix('.kicad_pro').is_file():
        raise ValueError('Source PCB and its project profile are required: '+str(board))
    profiles = {ext: board.with_suffix(ext).read_bytes()
                if board.with_suffix(ext).is_file() else None for ext in EXTENSIONS}
    marker = board.with_suffix('.profiles.json')
    if marker.exists():
        manifest = json.loads(marker.read_text())
        if (manifest.get('board_sha256') != hashlib.sha256(board.read_bytes()).hexdigest()
                or manifest.get('profiles_sha256') != profile_hashes(profiles)):
            raise ValueError('Saved probe PCB/profile/rule context changed: '+str(board))
    return profiles


def copy_profiles(source, output, expected):
    source, output = (Path(p).resolve() for p in (source, output))
    if source == output:
        raise ValueError('A probe must not overwrite its source context')
    actual = read_profiles(source)
    if actual != expected:
        raise ValueError('Source profile/rules changed during search: '+str(source))
    if expected['.kicad_dru'] is None and output.with_suffix('.kicad_dru').exists():
        raise ValueError('Destination has stale custom rules: '+str(output))
    if not output.is_file():
        raise ValueError('Save the probe PCB before copying its context')
    for ext, data in expected.items():
        if data is not None:
            output.with_suffix(ext).write_bytes(data)
    output.with_suffix('.profiles.json').write_text(json.dumps({
        'SPDX-License-Identifier': 'CERN-OHL-S-2.0',
        'source_board_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'board_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
        'profiles_sha256': profile_hashes(expected),
        'fabrication_release_allowed': False,
    }, indent=2, sort_keys=True)+'\n')
