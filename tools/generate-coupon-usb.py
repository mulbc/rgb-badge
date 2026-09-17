#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate the staged USB interface sheet into a new directory."""

import argparse
from pathlib import Path
import runpy

BASE = runpy.run_path(str(Path(__file__).with_name('generate-coupon-permission.py')))


def interface():
    s = BASE['Sheet']('usb-interface', 'Coupon Rev A - USB detection, data and logic supply')
    s.note('USB interface: connector, CC / BC1.2 detection, switched data and USB-only logic supply',20.32,20.32,'title',2)
    s.note('VBUS_CONNECTOR and +5V_USB are NOT bridged: input protection is still missing. No charger is connected.',20.32,30.48,'boundary')
    s.note('Draft +5V_USB boundary: 4.80-5.25 V only; this is a capture assumption, not a compliant input stage.',20.32,38.10,'voltage')
    s.component('J1','USB4505-03-0-A',60.96,91.44,{
        'A1_B12':'GND','A4_B9':'VBUS_CONNECTOR','A5':'USB_CC1',
        'B7':'USB_CONN_DM','A6':'USB_CONN_DP','A7':'USB_CONN_DM','B6':'USB_CONN_DP',
        'B5':'USB_CC2','B4_A9':'VBUS_CONNECTOR','B1_A12':'GND','S1':'GND'})
    s.note('SBU1/2 unused; shell bonded to GND.',20.32,127,'connector')
    s.component('TP32','TestPoint_Pad',60.96,157.48,{'1':'VBUS_CONNECTOR'},'VBUS_CONNECTOR')
    s.component('U33','TPD4E05U06DQAR',238.76,91.44,{
        '1':'USB_CONN_DP','2':'USB_CONN_DM','3':'GND','4':'USB_CC1','5':'USB_CC2','8':'GND'})
    s.note('Shunt ESD channels; NC lands are not series paths.',187.96,119.38,'esd',1.016)
    for ref,y,a,b in [('R73',142.24,'USB_CONN_DP','USB_BC_DP'),('R74',165.10,'USB_CONN_DM','USB_BC_DM')]:
        s.component(ref,'ERJ-2RCF2R20X',238.76,y,{'1':a,'2':b},'2.2R 1%')
    s.component('U31','TUSB320LAIRWBR',449.58,96.52,{
        '1':'USB_CC1','2':'USB_CC2','3':'GND','4':'USB_VBUS_DET',
        '7':'USB_RAW_OUT1','8':'USB_RAW_OUT2','10':'GND','11':'GND','12':'+3V3_USB'})
    s.note('PORT low = UFP; ADDR NC = GPIO; EN_N low.',391.16,127,'cc-mode',1.016)
    s.component('R71','ERJ-2RKF8873X',449.58,147.32,{'1':'VBUS_CONNECTOR','2':'USB_VBUS_DET'},'887k 1%')
    s.component('C36','GRM155R71C104KA88D',449.58,172.72,{'1':'+3V3_USB','2':'GND'},'100n 16V X7R')
    s.note('No external CC Rd: detector provides dead-battery Rd.',391.16,187.96,'cc-rd',1.016)
    s.note('USB-only LDO; never connect +3V3_APP here',20.32,215.90,'ldo',1.016)
    s.component('U29','TLV75533PDBVR',83.82,243.84,{'1':'+5V_USB','2':'GND','3':'+5V_USB','5':'+3V3_USB'})
    for ref,y in [('C30',276.86),('C31',299.72)]:
        s.component(ref,'GRM155C71A105KE11D',83.82,y,{'1':'+5V_USB','2':'GND'},'1u 10V X7S')
    s.component('C32','GRM188R60J106ME47D',83.82,325.12,{'1':'+3V3_USB','2':'GND'},'10u 6.3V X5R')
    s.component('R72','ERJ-2RCF2R20X',289.56,198.12,{'1':'+5V_USB','2':'USB_BC_VBUS'},'2.2R 1%')
    s.note('BC1.2: GOOD_BAT high prevents the dead-battery timer',220.98,215.90,'bc',1.016)
    s.component('U30','BQ24392RSER',289.56,243.84,{
        '1':'USB_RAW_SW_OPEN','2':'USB_BC_HOST_DM','3':'USB_BC_HOST_DP','4':'USB_RAW_CHG_AL_N',
        '5':'USB_BC_VBUS','6':'GND','7':'USB_BC_DP','8':'USB_BC_DM','9':'USB_BC_VBUS','10':'USB_RAW_CHG_DET'})
    for ref,y in [('C33',279.40),('C34',302.26)]:
        s.component(ref,'GRM155C71A105KE11D',289.56,y,{'1':'USB_BC_VBUS','2':'GND'},'1u 10V X7S')
    s.component('C35','GRM155R71C104KA88D',289.56,325.12,{'1':'USB_BC_VBUS','2':'GND'},'100n 16V X7R')
    s.note('Application-powered USB isolation',426.72,215.90,'data',1.016)
    s.component('U32','TS3USB31ERSER',492.76,243.84,{
        '1':'GND','2':'USB_D+','3':'USB_BC_HOST_DP','4':'GND','5':'USB_BC_HOST_DM','6':'USB_D-','8':'+3V3_APP'})
    s.component('C37','GRM155R71C104KA88D',492.76,279.40,{'1':'+3V3_APP','2':'GND'},'100n 16V X7R')
    s.note('D pins face detector; HSD pins face ESP32.',426.72,299.72,'direction',1.016)
    s.note('OFF isolation specified at VCC = 0; ramp testing pending.',426.72,309.88,'ramp',1.016)
    s.component('TP33','TestPoint_Pad',83.82,355.60,{'1':'+5V_USB'},'5V_USB_BOUNDARY')
    s.component('#FLG05','PWR_FLAG',289.56,355.60,{'1':'+5V_USB'})
    s.component('#FLG06','PWR_FLAG',492.76,355.60,{'1':'USB_BC_VBUS'})
    s.note('#FLG06: ERC power annotation after R72; not another source.',426.72,370.84,'derived-flag',1.016)
    s.note('Effective capacitance, inrush, total-port current, undervoltage/ramp behavior and input protection remain open.',20.32,381,'limits')
    s.note('R60/R61/R62/R64 on usb-conditioning provide detector pull-ups. Supervisors and charger actuators are not captured.',20.32,391.16,'pullups',1.016)
    return s


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    args.output.mkdir(parents=True,exist_ok=False)
    s=interface()
    text=s.output().replace('Staged logic; supervisors, startup inhibit and charger actuation remain open',
                            'Input protection, supervisors and charger actuation remain open')
    path=args.output/(s.name+'.kicad_sch')
    path.write_text(text)
    print(f'{path}: sheet UUID {s.sheet_uuid}, file UUID {s.file_uuid}')


if __name__=='__main__':main()
