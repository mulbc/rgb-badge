# SPDX-License-Identifier: Apache-2.0
"""Distinct native target groups for opt-in additive routing exploration."""

def other_group_representatives(source, pads, identity):
    """Retain caller order; exclude the live source group and repeated groups."""
    seen = {identity(source)}
    result = []
    for pad in pads:
        group = identity(pad)
        if group not in seen:
            seen.add(group)
            result.append(pad)
    return result
