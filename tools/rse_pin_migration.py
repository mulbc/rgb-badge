# SPDX-License-Identifier: Apache-2.0
"""ADR 0117 functional terminal permutation; never renumber physical RSE lands."""
MPN = 'SN74LVC1G74RSER'
FOOTPRINT = 'rgb-badge-coupon:UQFN_TI_RSE0008A_1.5x1.5mm_P0.5mm'
FORWARD = {'1':'7', '2':'6', '3':'5', '4':'4', '5':'3', '6':'2', '7':'1', '8':'8'}
LEGACY = {
    'U49': {'1':'HEARTBEAT_FALL_CLK', '2':'+3V3_APP', '3':'', '4':'GND',
            '5':'HEARTBEAT_SEEN', '6':'DISPLAY_CLEAR_OK', '7':'+3V3_APP', '8':'+3V3_APP'},
    'U50': {'1':'DISPLAY_ARM_CLK', '2':'HEARTBEAT_SEEN', '3':'', '4':'GND',
            '5':'ARM_LATCH', '6':'DISPLAY_CLEAR_OK', '7':'+3V3_APP', '8':'+3V3_APP'},
}
CORRECTED = {ref: {FORWARD[n]:net for n,net in pins.items()} for ref,pins in LEGACY.items()}


def is_exact_legacy(ref, part):
    """Only the complete documented historical assignment may be normalized."""
    return (ref in LEGACY and part['value'] == MPN and part['mpn'] in ('', MPN)
            and part['footprint'] == FOOTPRINT and len(part['pads']) == 8
            and {q['number']:q['net'] for q in part['pads']} == LEGACY[ref])
