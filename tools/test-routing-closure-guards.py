#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Inject isolated geometric/control faults into ignored copies; never edit source."""
import json
from pathlib import Path
import shutil
import pcbnew as p
import routing_closure as policy

BUILD=policy.ROOT/'hardware/coupon/rev-a/build/routing-closure/faults'


def main():
    plan=policy.load_plan();BUILD.mkdir(parents=True,exist_ok=True)
    source=policy.OUTPUT if policy.OUTPUT.exists() else policy.ROOT/'hardware/coupon/rev-a/build/zero-open-routing/replay-a.kicad_pcb'
    before=policy.sha(source)
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
                if t.GetNetname()!=net or list(policy.signature(b,t)) not in plan['added_copper']:continue
                b.Remove(t);b.BuildConnectivity()
                if len({cluster(q) for q in pads})>1:
                    held.append(t);return
                b.Add(t);b.BuildConnectivity()
            raise AssertionError('No independent native disconnection fixture found')
        return apply
    held=[]
    case('timing-control-disconnected',remove_critical('USB_LOGIC_CT',[('U34','4'),('R77','2')]))
    case('iref-disconnected',remove_critical('LED_IREF',[('U1','1'),('R1','1')]))
    case('ilim-disconnected',remove_critical('E1_ILM',[('U44','9'),('R96','1')]))
    case('remote-iref-resistor',lambda b:b.FindFootprintByReference('R1').SetPosition(p.VECTOR2I(44750000,4250000)))
    def narrow(b):
        t=next(t for t in b.GetTracks() if not isinstance(t,p.PCB_VIA) and list(policy.signature(b,t)) in plan['added_copper'])
        t.SetWidth(120000)
    case('unreviewed-narrowing',narrow)
    def mode_net(b):
        q=next(q for q in b.FindFootprintByReference('U36').Pads() if q.GetNumber()=='6')
        q.SetNetCode(b.FindNet('+3V3_APP').GetNetCode())
    case('mode-default-net-changed',mode_net)
    def old_lx(b):
        t=next(t for t in b.GetTracks() if not isinstance(t,p.PCB_VIA) and t.GetNetname()=='Net-(U36-LX1)')
        b.Remove(t);held.append(t)
    case('previous-converter-copper-removed',old_lx)
    assert policy.sha(source)==before and len(results)==7
    report={'SPDX-License-Identifier':'CERN-OHL-S-2.0','source_sha256':before,'cases':results,'fabrication_release_allowed':False}
    (BUILD/'results.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print('PASS seven isolated closure guards, including three native disconnection fixtures',flush=True)


if __name__=='__main__':main()
