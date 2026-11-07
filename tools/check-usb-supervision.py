#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Static TPS3808 logic-rail divider audit; not a startup/transient proof."""

from decimal import Decimal as D
from itertools import product
from pathlib import Path
import runpy

TOOLS=Path(__file__).resolve().parent
LIB=runpy.run_path(str(TOOLS/'check-power-libraries.py'))


def resistor_interval(nominal, tolerance='.01', tcr='.0001', delta_t='65'):
    """Initial tolerance at 25 C, then TCR relative to that actual resistance.

    The 65 K displacement covers -40..85 C. Aging, reflow shifts and local
    heating outside this interval are not included or implied qualified.
    """
    r,t,c,d=map(D,(nominal,tolerance,tcr,delta_t))
    if not all(v.is_finite() for v in (r,t,c,d)) or r<=0 or not 0<=t<1 or c<0 or d<0 or c*d>=1:
        raise ValueError('Invalid resistance/tolerance/temperature envelope')
    return r*(1-t)*(1-c*d),r*(1+t)*(1+c*d)


def threshold_bounds(upper='620000',lower='100000'):
    """All resistor, threshold and signed input-bias corners.

    TPS3808G01: 0.405 V ±2%, 25 nA maximum SENSE bias, 3% maximum
    hysteresis. Applying 3% to the high actual threshold is conservative.
    """
    falling=[];rising=[]
    for rt,rb,vit,bias in product(resistor_interval(upper),resistor_interval(lower),
                                 (D('.405')*D('.98'),D('.405')*D('1.02')),
                                 (-D('25e-9'),D('25e-9'))):
        falling.append(vit*(1+rt/rb)+bias*rt)
        rising.append(vit*D('1.03')*(1+rt/rb)+bias*rt)
    return min(falling),max(falling),max(rising)


def check(project=LIB['PROJECT']):
    symbols={s[1]:s for s in LIB['children'](LIB['parse'](project/'symbols/rgb-badge-coupon.kicad_sym'),'symbol')}
    mpn='ERJ2RKF6203X'
    import json
    # Reuse the audited passive shape/pin map while checking all exact identity
    # fields and the manufacturer source URL against the controlled template.
    if json.dumps(symbols[mpn]).replace(mpn,'ERJ2RKF1003X')!=json.dumps(symbols['ERJ2RKF1003X']):
        raise ValueError('Supervisor divider resistor identity/geometry mismatch')
    reset_pull=symbols['ERJ2RKF1004X']
    props=LIB['property_map'](reset_pull)
    if any(props.get(key)!=value for key,value in {
        'Value':'ERJ2RKF1004X', 'MPN':'ERJ2RKF1004X',
        'Manufacturer':'Panasonic',
        'Footprint':'rgb-badge-coupon:R_Panasonic_ERJ2_0402',
        'Datasheet':'https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ2RKF1004X',
    }.items()):
        raise ValueError('RESET 1M resistor identity mismatch')
    pins=[pin for unit in LIB['children'](reset_pull,'symbol') for pin in LIB['children'](unit,'pin')]
    pin_numbers={LIB['one'](pin,'number','pin number')[1] for pin in pins}
    if pin_numbers!={'1','2'} or any(pin[1]!='passive' for pin in pins):
        raise ValueError('RESET 1M resistor pin map mismatch')
    lo,hi,release=threshold_bounds()
    if not D('2.7')<lo<hi<release<D('3.2'):
        raise ValueError('Logic supervisor divider outside static design window')
    # TI specifies the long fixed delay with 40..200 kohm from CT to VDD.
    ct_lo,ct_hi=resistor_interval('100000')
    if not D('40000')<=ct_lo<=ct_hi<=D('200000'):
        raise ValueError('CT resistor outside fixed-delay selection interval')
    return lo,hi,release


if __name__=='__main__':
    lo,hi,release=check()
    print(f'Logic supervisor static corners: trip {lo:.4f}..{hi:.4f} V; release threshold <= {release:.4f} V, then 180..420 ms delay.')
    print('Not a VBUS-valid, loaded-logic-level, fast-brownout or actuator-startup proof.')
