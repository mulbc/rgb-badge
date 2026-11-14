#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Inject isolated geometric/control faults into ignored copies; never edit source."""
import json
from pathlib import Path
import shutil
import pcbnew as p
import u36_stage_checkpoint as policy

BUILD=policy.ROOT/'hardware/coupon/rev-a/build/u36-stage-checkpoint/faults'


def main():
    plan=policy.load_plan();BUILD.mkdir(parents=True,exist_ok=True)
    source=policy.OUTPUT if policy.OUTPUT.exists() else policy.ROOT/'hardware/coupon/rev-a/build/u36-stage-checkpoint/replay-a.kicad_pcb'
    before=policy.sha(source);c=policy.base.native_helpers()
    results=[]
    def case(name,mutate):
        b=p.LoadBoard(str(source));mutate(b)
        out=BUILD/(name+'.kicad_pcb');p.SaveBoard(str(out),b)
        for ext in ('.kicad_pro','.kicad_dru'):shutil.copyfile(source.with_suffix(ext),out.with_suffix(ext))
        try:policy.audit(out,plan)
        except AssertionError as error:results.append({'case':name,'rejected':True,'reason':str(error)})
        else:raise AssertionError('Fault accepted: '+name)
    def remove_critical(net,entries):
        def apply(b):
            parts={f.GetReference():f for f in b.GetFootprints()}
            pads=[next(q for q in parts[ref].Pads() if q.GetNumber()==n) for ref,n in entries]
            cluster=lambda q:frozenset(z.m_Uuid.AsString() for z in b.GetConnectivity().GetConnectedItems(q) if isinstance(z,p.PAD))
            for t in list(b.GetTracks()):
                if t.GetNetname()!=net or list(c['signature'](b,t)) not in plan['added_copper']:continue
                b.Remove(t);b.BuildConnectivity()
                if len({cluster(q) for q in pads})>1:
                    held.append(t);return
                b.Add(t);b.BuildConnectivity()
            raise AssertionError('No independent native disconnection fixture found')
        return apply
    held=[]
    case('feedback-disconnected',remove_critical('APP_3V3_FB',[('U36','8'),('R81','2'),('R82','1')]))
    case('enable-pulldown-disconnected',remove_critical('APP_ON_SW_DRAFT',[('U36','5'),('R83','1')]))
    case('remote-input-cap',lambda b:b.FindFootprintByReference('C40').SetPosition(p.VECTOR2I(39750000,4000000)))
    def narrow(b):
        t=next(t for t in b.GetTracks() if not isinstance(t,p.PCB_VIA) and t.GetNetname()=='+SYS_APP_IN_DRAFT' and list(c['signature'](b,t)) in plan['added_copper'])
        t.SetWidth(120000)
    case('narrow-power-copper',narrow)
    def mode_net(b):
        pad=next(q for q in b.FindFootprintByReference('U36').Pads() if q.GetNumber()=='6')
        pad.SetNetCode(b.FindNet('+3V3_APP').GetNetCode())
    case('mode-default-net-changed',mode_net)
    assert policy.sha(source)==before and len(results)==5
    report={'SPDX-License-Identifier':'CERN-OHL-S-2.0','source_sha256':before,'cases':results,'fabrication_release_allowed':False}
    (BUILD/'results.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print('PASS five isolated U36 stage guards, including native FB/EN disconnection fixtures',flush=True)


if __name__=='__main__':main()
