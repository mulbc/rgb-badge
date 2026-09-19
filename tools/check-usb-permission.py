#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""ADR 0013 stable Type-C-only charge policy; not a transient qualification."""
from itertools import product

# TUSB320LAI SLLSEQ8D Table 3, GPIO/UFP mode.
TYPE_C_PINS = {'unattached':(1,1),'default':(1,0),'1.5A':(0,1),'3A':(0,0)}

def permission(*, out1, out2, vbus_valid, logic_ready):
    for value in (out1,out2):
        if type(value) is not int or value not in (0,1):
            raise ValueError('Detector pins must be resolved 0 or 1')
    if type(vbus_valid) is not bool or type(logic_ready) is not bool:
        raise ValueError('Supply qualification inputs must be booleans')
    charge=bool(vbus_valid and logic_ready and not out1)
    return {'charge':charge, 'mode':'external-fixed' if charge else 'standby',
            'en2':1, 'en1':int(not charge)}

def check():
    count=0
    for a,b,v,l in product((0,1),repeat=4):
        state=permission(out1=a,out2=b,vbus_valid=bool(v),logic_ready=bool(l))
        # Independent membership definition from the manufacturer code table.
        expected=(a,b) in (TYPE_C_PINS['1.5A'],TYPE_C_PINS['3A']) and bool(v and l)
        if state['charge']!=expected or state['en1']!=int(not expected):
            raise ValueError('Type-C-only policy mismatch')
        count+=1
    return count

if __name__=='__main__':
    print(f'USB permission contract passed: {check()} Type-C/supply states; no BC1.2, firmware grant or boost selection. Not transient qualification.')
