#!/usr/bin/env python3
"""Rebuild the independent Rev-5 circuit reconstruction with KiCad's Python.

Run using KiCad 10's bundled Python. This overwrites this project's CAD files;
do not run over hand edits. No QRP Labs artwork is embedded.
"""
from pathlib import Path
import json
import math
import uuid
import subprocess
import sys
import pcbnew as p
import wx

APP = wx.App(False)

ROOT = Path(__file__).resolve().parents[1]
NAME = 'Relay-Switched LPF'
project_file=ROOT/(NAME+'.kicad_pro')
shared_text_variables=json.loads(project_file.read_text()).get('text_variables',{}) if project_file.exists() else {}
LIB = 'relay-switched-lpf'
PRETTY = ROOT / (LIB + '.pretty')
PRETTY.mkdir(exist_ok=True)
NS = uuid.UUID('8cc6c727-f708-4d78-9495-848629294835')
def uid(s): return str(uuid.uuid5(NS, s))
def q(s): return json.dumps(str(s))
def eff(size=1.0, extra=''): return f'(effects (font (size {size} {size})) {extra})'
def prop(k, v, x=0, y=0, hide=False):
    return f'(property {q(k)} {q(v)} (at {x} {y} 0) {eff(1.0, "(hide yes)" if hide else "")})'
def line(x1,y1,x2,y2):
    return f'(polyline (pts (xy {x1} {y1}) (xy {x2} {y2})) (stroke (width 0.254) (type default)) (fill (type none)))'
def rect(x1,y1,x2,y2):
    return f'(rectangle (start {x1} {y1}) (end {x2} {y2}) (stroke (width 0.254) (type default)) (fill (type none)))'
def pin(n,name,x,y,a):
    return f'(pin passive line (at {x} {y} {a}) (length 2.54) (name {q(name)} {eff(.9)}) (number {q(n)} {eff(.9)}))'

symbols = {}
pinmaps = {}
def symbol(name, prefix, pins, graphics, description):
    pinmaps[name] = {str(n):(x,y,a) for n,_,x,y,a in pins}
    s = f'''(symbol {q(name)} (pin_names (offset .5) (hide yes)) (exclude_from_sim yes) (in_bom yes) (on_board yes)
    {prop('Reference',prefix,0,17.78)} {prop('Value',name,0,15.24)}
    {prop('Footprint','',hide=True)} {prop('Datasheet','',hide=True)} {prop('Description',description,hide=True)}
    (symbol {q(name+'_0_1')} {graphics})
    (symbol {q(name+'_1_1')} {''.join(pin(*t) for t in pins)}))'''
    symbols[name] = s

# Whole DPDT relay. Numbering agrees with QRP Labs' schematic and TX standard terminals.
rp = [(1,'COIL+',-12.7,7.62,0),(12,'COIL-',-12.7,-7.62,0),
      (8,'NO_A',12.7,12.7,180),(9,'COM_A',12.7,7.62,180),(10,'NC_A',12.7,2.54,180),
      (5,'NO_B',12.7,-2.54,180),(4,'COM_B',12.7,-7.62,180),(3,'NC_B',12.7,-12.7,180)]
g = rect(-7.62,5.08,-2.54,-5.08)+line(-10.16,7.62,-5.08,7.62)+line(-5.08,7.62,-5.08,5.08)+line(-10.16,-7.62,-5.08,-7.62)+line(-5.08,-7.62,-5.08,-5.08)
for yy in [7.62,-7.62]:
    g += line(10.16,yy,7.62,yy)+line(7.62,yy,4.445,yy-3.81)
    g += line(10.16,yy+5.08,3.81,yy+5.08)+line(10.16,yy-5.08,3.81,yy-5.08)
symbol('TX2_5V','RL',rp,g,'Panasonic TX2-5V single-side stable DPDT; NC shown at rest')
for n in [2,3,4,10]:
    ys=[(n-1)*1.27-i*2.54 for i in range(n)]
    symbol('Port_'+str(n),'J',[(i+1,str(i+1),-7.62,y,0) for i,y in enumerate(ys)],
           rect(-5.08,max(ys)+1.27,5.08,min(ys)-1.27), 'Numbered physical connector or wire-link pads; see README pin map')
symbol('1N4148','D',[(1,'K',-7.62,0,0),(2,'A',7.62,0,180)],
       line(-5.08,0,-1.27,0)+line(1.27,0,5.08,0)+line(-1.27,-2.54,-1.27,2.54)+line(-1.27,0,1.27,2.54)+line(1.27,2.54,1.27,-2.54)+line(1.27,-2.54,-1.27,0),
       '1N4148 relay flyback diode, cathode pin 1')

def fp_text(kind,text,x,y,layer='F.SilkS',size=.85,hide=False):
    return f'(fp_text {kind} {q(text)} (at {x} {y}) (layer {q(layer)}) {"hide" if hide else ""} (effects (font (size {size} {size}) (thickness .13))))'
def fp_line(x1,y1,x2,y2,layer='F.SilkS',width=.15):
    return f'(fp_line (start {x1} {y1}) (end {x2} {y2}) (stroke (width {width}) (type default)) (layer {q(layer)}))'
def fp_rect(x1,y1,x2,y2,layer):
    return ''.join(fp_line(*t,layer) for t in [(x1,y1,x2,y1),(x2,y1,x2,y2),(x2,y2,x1,y2),(x1,y2,x1,y1)])
def pad(n,x,y,size=1.8,drill=1.0):
    return f'(pad {q(n)} thru_hole {"rect" if str(n)=="1" else "circle"} (at {x} {y}) (size {size} {size}) (drill {drill}) (layers "*.Cu" "*.Mask"))'
def footprint(name,pads,box,refy=-2,descr='Independent reconstruction; geometry limits in README'):
    x1,y1,x2,y2=box
    text=f'''(footprint {q(name)} (version 20260206) (generator "pcbnew") (layer "F.Cu")
    (descr {q(descr)}) (attr through_hole)
    {fp_text('reference','REF**',0,refy)} {fp_text('value',name,0,y2+1.5,'F.Fab',hide=True)}
    {'' if name.startswith('SMA_') else fp_rect(*box,'F.SilkS')}{fp_rect(x1-.25,y1-.25,x2+.25,y2+.25,'F.CrtYd')}{fp_rect(*box,'F.Fab')}
    {''.join(pad(*t) for t in pads)})'''
    (PRETTY/(name+'.kicad_mod')).write_text(text+'\n')

footprint('TX2_5V',[(1,-2.54,-5.08),(3,-2.54,0),(4,-2.54,2.54),(5,-2.54,5.08),
                      (12,2.54,-5.08),(10,2.54,0),(9,2.54,2.54),(8,2.54,5.08)],(-3.7,-7.5,3.7,7.5),-8.4,
          'TX2 standard PC terminals; 15 x 7.4 mm body; 5.08 mm rows; 1 mm holes. Pin 1 top left in component view.')
for n in [2,3,4]:
    footprint('Socket_1x'+str(n),[(i+1,0,i*2.54) for i in range(n)],(-1.3,-1.3,1.3,(n-1)*2.54+1.3),-2)
for n in [2,3]:
    name='Wire_1x'+str(n)
    body=f'(footprint "{name}" (version 20260206) (generator "pcbnew") (layer "F.Cu") (attr through_hole)'
    body+=fp_text('reference','REF**',0,-2,'F.Fab')+fp_text('value',name,0,-3.5,'F.Fab',hide=True)
    body+=fp_rect(-1.15,-1.15,1.15,(n-1)*2.54+1.15,'F.CrtYd')
    body+=fp_rect(-1.15,-1.15,1.15,(n-1)*2.54+1.15,'F.Fab')
    body+=''.join(pad(i+1,0,i*2.54) for i in range(n))
    (PRETTY/(name+'.kicad_mod')).write_text(body+')\n')
footprint('Host_2x05',[(2*i+1,0,i*2.54) for i in range(5)]+[(2*i+2,-2.54,i*2.54) for i in range(5)],(-3.84,-1.3,1.3,11.46),-2,
          'Bottom-side socket; mirrored library columns give odd pins at board-left and even pins at board-right in top view. Confirm mating host before assembly.')
footprint('D_DO35_P7.62',[(1,0,0,1.6,.8),(2,7.62,0,1.6,.8)],(1.5,-1,6.1,1),-1.8)
# Output groups have semantic contact numbers: 1 RF, 2 isolated output return.
footprint('SMA_Vertical_Generic',[(1,0,0,2.2,1.2)]+[(2,x,y,2.2,1.2) for x in [-2.54,2.54] for y in [-2.54,2.54]],(-3.5,-3.5,3.5,3.5),-4.4)
edge = f'''(footprint "SMA_Edge_Generic" (version 20260206) (generator "pcbnew") (layer "F.Cu") (attr smd)
{fp_text('reference','REF**',-4,0)} {fp_text('value','SMA edge option',0,0,'F.Fab',hide=True)}
{fp_rect(-2.5,-4,1,4,'F.CrtYd')}
'''
for layer in ['F','B']:
    for n,y,w,h in [(1,0,4,1.5),(2,-3,4,1.5),(2,3,4,1.5)]:
        edge+=f'(pad "{n}" smd rect (at -1 {y}) (size {w} {h}) (layers "{layer}.Cu" "{layer}.Mask"))'
(PRETTY/'SMA_Edge_Generic.kicad_mod').write_text(edge+')\n')

components=[]
def comp(ref,sym,value,fp,x,y,nets,px,py,angle=0,bottom=False):
    c=dict(ref=ref,sym=sym,value=value,fp=fp,x=x,y=y,nets={str(k):v for k,v in nets.items()},px=px,py=py,angle=angle,bottom=bottom,uuid=uid(ref))
    components.append(c)
    return c

# Board coordinates are local to the 80 x 37 outline, later translated to (50,50).
host={1:'+5V',2:'BAND5_N',3:'BAND3_N',4:'BAND4_N',5:'BAND1_N',6:'BAND2_N',7:'GND',8:'RFI',9:'GND',10:'RFO'}
comp('J1','Port_10','HOST (underside)','Host_2x05',34.29,254,host,2.54,8.26,bottom=True)
comp('W1','Port_2','FIT: +5V to coils','Wire_1x2',100.33,246.38,{1:'+5V',2:'RELAY_VPLUS'},7.4,8.4,90)
for i in range(1,6):
    sx=39.37+(5-i)*69.85
    bx=12.7+(5-i)*13.97
    # Switched input is pole A; switched output is pole B.
    rnets={1:'RELAY_VPLUS',12:f'BAND{i}_N',8:'RFI',9:f'LPF{i}_IN',10:'GND' if i>1 else 'FINAL_NC',
           3:'GND',4:f'LPF{i}_OUT' if i>1 else 'FINAL_RELAY_COM',5:f'RELAY{i}_OUT'}
    comp(f'RL{i}','TX2_5V','TX2-5V','TX2_5V',sx,99.06,rnets,bx-(.762 if i==1 else 0),18.62)
    comp(f'D{i}','1N4148','1N4148','D_DO35_P7.62',sx,175.26,{1:'+5V',2:f'BAND{i}_N'},bx-3.81,5.8)
    comp(f'J{i*2}','Port_4',f'LPF{i} IN','Socket_1x4',sx,55.88,{1:'GND',2:'GND',3:f'LPF{i}_IN',4:f'LPF{i}_IN'},bx-3.81,1.99,90)
    # Two signal pads and two return pads; slot 1's entire output return floats.
    comp(f'J{i*2+1}','Port_4',f'LPF{i} OUT','Socket_1x4',sx,144.78,{1:f'LPF{i}_OUT',2:f'LPF{i}_OUT',3:'GND_OUT' if i==1 else 'GND',4:'GND_OUT' if i==1 else 'GND'},bx+3.81,35.01,-90)
    comp(f'W{i+1}','Port_3',f'OUTPUT {i}: link 1-2*','Wire_1x3',sx,209.55,{1:f'RELAY{i}_OUT',2:'RFO',3:f'ANT{i}'},bx-5.97,25.4)
    comp(f'J{20+i}','Port_2',f'ANT {i}','Wire_1x2',sx,229.87,{1:f'ANT{i}',2:'GND'},bx-6.55,33.02)
comp('W7','Port_3','FINAL INPUT: link 1-2','Wire_1x3',176.53,246.38,{1:'RFO',2:'FINAL_NC',3:'GND'},62.61,13.97)
comp('W8','Port_2','OPEN: ground bypass','Wire_1x2',246.38,246.38,{1:'GND',2:'GND_OUT'},68.4,28,90)
comp('W9','Port_2','OPEN: relay-1 output link','Wire_1x2',374.65,246.38,{1:'LPF1_OUT',2:'FINAL_RELAY_COM'},74.8,18,90)
comp('J26','Port_2','RF OUT / isolated return','Wire_1x2',316.23,246.38,{1:'LPF1_OUT',2:'GND_OUT'},76.2,30.48,-90)
comp('X1','Port_2','SMA vertical option','SMA_Vertical_Generic',374.65,203.2,{1:'LPF1_OUT',2:'GND_OUT'},75.819,23)
comp('X2','Port_2','SMA edge option','SMA_Edge_Generic',374.65,223.52,{1:'LPF1_OUT',2:'GND_OUT'},78.5,12)

# Write independent local symbol library and its project tables.
(ROOT/(LIB+'.kicad_sym')).write_text('(kicad_symbol_lib (version 20241209) (generator "kicad_symbol_editor")\n'+'\n'.join(symbols.values())+')\n')
(ROOT/'sym-lib-table').write_text(f'(sym_lib_table (version 7) (lib (name "{LIB}") (type "KiCad") (uri "${{KIPRJMOD}}/{LIB}.kicad_sym") (options "") (descr "Independent reconstruction symbols")))\n')
(ROOT/'fp-lib-table').write_text(f'(fp_lib_table (version 7) (lib (name "{LIB}") (type "KiCad") (uri "${{KIPRJMOD}}/{LIB}.pretty") (options "") (descr "Independent reconstruction footprints")))\n')
sheetuid=uid('sheet')
sch=f'''(kicad_sch (version 20260306) (generator "eeschema") (generator_version "10.0") (uuid "{sheetuid}") (paper "A3")
(title_block (title "Relay-Switched LPF") (date "2026-11-13") (rev "A - unqualified") (company "QRP Labs Rev 5 circuit; independent reconstruction") (comment 1 "80 x 37 mm; drawing-derived geometry; NOT fabrication qualified"))
(lib_symbols {''.join(s.replace('(symbol '+q(name), '(symbol '+q(LIB+':'+name),1) for name,s in symbols.items())})
'''
def note(text,x,y,size=1.27):
    return f'(text {q(text)} (at {x} {y} 0) {eff(size,"(justify left)")} (uuid "{uid("note"+text)}"))'
sch+=note('Five plug-in filters; slot 1 is the highest-frequency LPF and is always in series.',20.32,16.51,1.7)
sch+=note('One active-low relay at a time. 5 V coils need an external sink driver for Pi/Pico GPIO.',20.32,22.86)
sch+=note('* Fit W1 1-2, W3/W4/W5/W6 1-2, and W7 1-2. Leave W2, W8, and W9 OPEN.',20.32,29.21)
sch+=note('W2-W6: pin 1 relay output, pin 2 common RFO bus, pin 3 separate antenna. Slot 1 output is direct.',20.32,35.56)
for c in components:
    x,y=c['x'],c['y']; ref=c['ref']; sym=c['sym']; cu=c['uuid']
    refy=y-17.78 if sym=='TX2_5V' else y-(len(pinmaps[sym])+1)*1.27-2.54
    if sym=='1N4148': refy=y-6.35
    sch+=f'''(symbol (lib_id "{LIB}:{sym}") (at {x} {y} 0) (unit 1) (exclude_from_sim yes) (in_bom yes) (on_board yes) (dnp no) (uuid "{cu}")
    {prop('Reference',ref,x,refy)} {prop('Value',c['value'],x,refy+2.54)}
    {prop('Footprint',LIB+':'+c['fp'],x,y,True)} {prop('Datasheet','',x,y,True)}
    {''.join('(pin '+q(n)+' (uuid "'+uid(ref+'pin'+n)+'"))' for n in pinmaps[sym])}
    (instances (project "{NAME}" (path "/{sheetuid}" (reference "{ref}") (unit 1)))))'''
    for n,(dx,dy,a) in pinmaps[sym].items():
        xx,yy=round(x+dx,4),round(y-dy,4)
        endx=round(xx+(-5.08 if a==0 else 5.08),4)
        net=c['nets'][n]
        sch+=f'(wire (pts (xy {xx} {yy}) (xy {endx} {yy})) (stroke (width 0) (type default)) (uuid "{uid(ref+n+"wire")}"))'
        sch+=f'(label {q(net)} (at {endx} {yy} 0) {eff(.9, "(justify "+("right" if a==0 else "left")+" bottom)")} (uuid "{uid(ref+n+"label")}"))'
sch+=')\n'
(ROOT/(NAME+'.kicad_sch')).write_text(sch)
# Normal KiCad defaults: no exclusions and no weakened severities.
project={'meta':{'filename':NAME+'.kicad_pro','version':3},'erc':{'erc_exclusions':[], 'meta':{'version':0}},
         'board':{'design_settings':{'rules':{'min_clearance':.2,'min_track_width':.25,'min_via_diameter':.6,'min_through_hole_diameter':.3,'min_copper_edge_clearance':.25},'drc_exclusions':[]}},
         'net_settings':{'classes':[{'name':'Default','description':'Default','clearance':.2,'track_width':.3,'via_diameter':.65,'via_drill':.3,'microvia_diameter':.3,'microvia_drill':.1,'diff_pair_width':.25,'diff_pair_gap':.25,'diff_pair_via_gap':.25}],'meta':{'version':4}}}
(ROOT/(NAME+'.kicad_pro')).write_text(json.dumps(project,indent=2)+'\n')

b=p.BOARD()
mm=p.FromMM
def vec(x,y): return p.VECTOR2I(mm(x),mm(y))
netnames=sorted({n for c in components for n in c['nets'].values()})
nets={}
for n in netnames:
    nn=p.NETINFO_ITEM(b,'/'+n); b.Add(nn); nets[n]=nn
fps={}
for c in components:
    fp=p.FootprintLoad(str(PRETTY),c['fp'])
    fp.SetReference(c['ref']); fp.SetValue(c['value']); fp.SetFPID(p.LIB_ID(LIB,c['fp']))
    fp.SetPath(p.KIID_PATH('/'+sheetuid+'/'+c['uuid']))
    fp.SetPosition(vec(50+c['px'],50+c['py'])); fp.SetOrientationDegrees(c['angle'])
    b.Add(fp)
    if c['bottom']: fp.Flip(fp.GetPosition(),False)
    # References are kept on fab for this densely stacked carrier; channel numbers are silk.
    fp.Reference().SetLayer(p.B_Fab if c['bottom'] else p.F_Fab)
    fp.Value().SetVisible(False)
    for pd in fp.Pads(): pd.SetNet(nets[c['nets'][pd.GetNumber()]])
    fps[c['ref']]=fp

for a,bb in [((50,50),(130,50)),((130,50),(130,87)),((130,87),(50,87)),((50,87),(50,50))]:
    s=p.PCB_SHAPE(); s.SetShape(p.SHAPE_T_SEGMENT); s.SetStart(vec(*a)); s.SetEnd(vec(*bb)); s.SetLayer(p.Edge_Cuts); s.SetWidth(mm(.05)); b.Add(s)
for idx,(x,y) in enumerate([(3,3),(77,3),(3,34),(77,34)],1):
    fp=p.FOOTPRINT(b); fp.SetReference('H'+str(idx)); fp.SetValue('Mount 3.2 mm (inferred)'); fp.SetPosition(vec(50+x,50+y)); fp.SetAttributes(p.FP_BOARD_ONLY|p.FP_EXCLUDE_FROM_BOM|p.FP_EXCLUDE_FROM_POS_FILES)
    mask=p.LSET()
    for layer in [p.F_Cu,p.B_Cu,p.F_Mask,p.B_Mask]: mask.AddLayer(layer)
    pd=p.PAD(fp); pd.SetAttribute(p.PAD_ATTRIB_NPTH); pd.SetShape(p.PAD_SHAPE_CIRCLE); pd.SetSize(vec(3.2,3.2)); pd.SetDrillSize(vec(3.2,3.2)); pd.SetLayerSet(mask); pd.SetPosition(fp.GetPosition()); fp.Add(pd); fp.Reference().SetVisible(False); fp.Value().SetVisible(False); b.Add(fp)
def text(t,x,y,size=.85,layer=p.F_SilkS):
    s=p.PCB_TEXT(b); s.SetText(t); s.SetPosition(vec(50+x,50+y)); s.SetTextSize(vec(max(.8,size),max(.8,size))); s.SetTextThickness(mm(.13)); s.SetLayer(layer); s.SetMirrored(layer==p.B_SilkS); b.Add(s)
for i in range(1,6):
    x=12.7+(5-i)*13.97
    text(str(i),x,30.5,2.1); text('IN',x+6,2.0,.75); text('OUT',x,32.6,.75)
text('Relay-Switched LPF  /  A',40,8.2,.95)
text('Rev 5 circuit reconstruction - UNQUALIFIED',40,9.7,.65)
text('RF OUT',76,28.9,.8)
text('J1 bottom',4,22.8,.8,p.B_SilkS)
text('1 +5V / 2 B5 / 3 B3 / 4 B4 / 5 B1',40,11,.8,p.B_SilkS)
text('6 B2 / 7 GND / 8 RFI / 9 GND / 10 RFO',40,16,.75,p.B_SilkS)

# Zones are bounded away from the isolated slot-1 output region.
def zone(net,layer,points):
    z=p.ZONE(b); z.SetLayer(layer); z.SetNet(nets[net]); z.SetLocalClearance(mm(.25)); z.SetThermalReliefGap(mm(.25)); z.SetThermalReliefSpokeWidth(mm(.3)); z.SetMinThickness(mm(.2))
    poly=z.Outline(); poly.NewOutline()
    for x,y in points: poly.Append(mm(50+x),mm(50+y))
    b.Add(z)
for layer in [p.F_Cu,p.B_Cu]:
    zone('GND',layer,[(.5,.5),(79.5,.5),(79.5,7.4),(72,7.4),(72,20.4),(63.2,20.4),(63.2,36.5),(.5,36.5)])
    zone('GND_OUT',layer,[(72.5,8),(79.5,8),(79.5,32),(68.6,32),(68.6,36.5),(63.7,36.5),(63.7,30.2),(72.5,30.2)])

b.BuildConnectivity()
p.SaveBoard(str(ROOT/(NAME+'.kicad_pcb')),b)
(ROOT/'design'/'connections.json').write_text(json.dumps({c['ref']:c['nets'] for c in components},indent=2)+'\n')
# KiCad's board save can write project defaults; restore user-owned shared
# drawing-sheet values before applying the Letter schematic presentation.
saved_project=json.loads(project_file.read_text())
saved_project['text_variables']=shared_text_variables
project_file.write_text(json.dumps(saved_project,indent=2)+'\n')
subprocess.run([sys.executable, str(ROOT/'design'/'redraw_schematic.py')], check=True)
subprocess.run([sys.executable, str(ROOT/'design'/'finish_mechanics.py')], check=True)
print(f'Generated {len(components)} components, {len(nets)} nets; routing follows in route.py')
