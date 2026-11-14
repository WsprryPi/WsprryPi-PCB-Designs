#!/usr/bin/env python3
"""Redraw the saved carrier as a wired circuit, without changing its PCB.

Standard-library-only. Retains references, pin numbers, electrical nets, the
root-sheet UUID, and each component's original UUID for PCB association.
"""
from pathlib import Path
import copy
import json
import re
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
NAME = 'Relay-Switched LPF'
LIB = 'relay-switched-lpf'
NS = uuid.UUID('8cc6c727-f708-4d78-9495-848629294835')
def uid(text): return str(uuid.uuid5(NS, text))
def q(text): return json.dumps(str(text))
class Atom(str): pass
def parse(text):
    stack=[]; result=None
    for token in re.findall(r'\(|\)|"(?:\\.|[^"\\])*"|[^\s()]+', text):
        if token == '(':
            item=[]
            if stack: stack[-1].append(item)
            stack.append(item)
        elif token == ')': result=stack.pop()
        else: stack[-1].append(json.loads(token) if token.startswith('"') else Atom(token))
    return result
def kids(obj,key): return [v for v in obj if isinstance(v,list) and v and v[0]==key]
def child(obj,key): return kids(obj,key)[0]
def dump(obj,depth=0):
    if not isinstance(obj,list): return str(obj) if isinstance(obj,Atom) else q(obj)
    flat='('+' '.join(dump(v,depth+1) for v in obj)+')'
    if '\n' not in flat and len(flat)<115: return flat
    prefix=[]
    while obj and not isinstance(obj[len(prefix)],list):
        prefix.append(obj[len(prefix)])
        if len(prefix)==len(obj): break
    rest=obj[len(prefix):]
    return '('+' '.join(dump(v,depth+1) for v in prefix)+''.join('\n'+'  '*(depth+1)+dump(v,depth+1) for v in rest)+')'
def eff(size=1.0,extra=''): return f'(effects (font (size {size} {size})) {extra})'
def prop(key,value,x,y,hide=False):
    return f'(property {q(key)} {q(value)} (at {x} {y} 0) {eff(1.0,"(hide yes)" if hide else "")})'
def poly(points,width=.254):
    return '(polyline (pts '+''.join(f'(xy {x} {y})' for x,y in points)+f') (stroke (width {width}) (type default)) (fill (type none)))'
def rectangle(x1,y1,x2,y2):
    return f'(rectangle (start {x1} {y1}) (end {x2} {y2}) (stroke (width .254) (type default)) (fill (type none)))'
def circle(x,y,r=.635):
    return f'(circle (center {x} {y}) (radius {r}) (stroke (width .254) (type default)) (fill (type none)))'
def pin(n,x,y,angle,length=2.54):
    return f'(pin passive line (at {x} {y} {angle}) (length {length}) (name "~" {eff(.9)}) (number "{n}" {eff(.9)}))'
def symbol(name,prefix,units):
    return parse(f'''(symbol "{name}" (pin_names (offset .5) (hide yes))
      (exclude_from_sim yes) (in_bom yes) (on_board yes)
      {prop('Reference',prefix,0,10.16)} {prop('Value',name,0,12.7)}
      {prop('Footprint','',0,0,True)} {prop('Datasheet','',0,0,True)}
      {''.join(f'(symbol "{name}_{i}_1" {graphics}{pins})' for i,(graphics,pins) in enumerate(units,1))})''')

sch_path=ROOT/(NAME+'.kicad_sch')
old=parse(sch_path.read_text())
sheet_uuid=child(old,'uuid')[1]
original={}
for instance in kids(old,'symbol'):
    ref=next(v[2] for v in kids(instance,'property') if v[1]=='Reference')
    if ref not in original or child(instance,'unit')[1]=='1': original[ref]=instance
assert len(original)==38
library=parse((ROOT/(LIB+'.kicad_sym')).read_text())
library[:]=[v for v in library if not (isinstance(v,list) and v[0]=='symbol' and v[1] in ['TX2_5V','LPF_IN','LPF_OUT','Selector3','Link2','Terminal2','InputSelector3','Port_2','Port_3','Port_4','Port_10','1N4148','AntennaConnector2','OutputConnector2','Conn_Coaxial'])]
# Canonical unscaled definitions make repeated Letter redraws idempotent.
for n in [2,3,4]:
    ys=[(n-1)*1.27-i*2.54 for i in range(n)]
    library.append(symbol('Port_'+str(n),'J',[(rectangle(-5.08,max(ys)+1.27,5.08,min(ys)-1.27),''.join(pin(i+1,-7.62,y,0) for i,y in enumerate(ys)))]))
def host_connector():
    # KiCad Conn_01x10 boxed artwork adapted to the existing J1 pin endpoints.
    # The actual host footprint remains the existing 2x5 socket.
    ys=[9*1.27-i*2.54 for i in range(10)]
    graphics=rectangle(-3.81,max(ys)+1.27,-1.27,min(ys)-1.27).replace('(type none)', '(type background)')
    for y in ys:
        graphics+=(f'(rectangle (start -3.81 {y+.127}) (end -2.54 {y-.127}) '
                   '(stroke (width .1524) (type default)) (fill (type none)))')
    return symbol('Port_10','J',[(graphics,''.join(pin(i+1,-7.62,y,0,3.81) for i,y in enumerate(ys)))])
library.append(host_connector())
diode=poly([(-5.08,0),(-1.27,0)])+poly([(1.27,0),(5.08,0)])
diode+=poly([(-1.27,-2.54),(-1.27,2.54)])+poly([(-1.27,0),(1.27,2.54),(1.27,-2.54),(-1.27,0)])
library.append(symbol('1N4148','D',[(diode,pin(1,-7.62,0,0)+pin(2,7.62,0,180))]))
coil=rectangle(-2.54,3.81,2.54,-3.81)+poly([(-2.54,-3.81),(2.54,3.81)])
coil+=poly([(0,5.08),(0,3.81)])+poly([(0,-3.81),(0,-5.08)])
input_contact=poly([(0,-5.08),(0,-3.81),(5.08,0)])
output_contact=poly([(0,5.08),(0,3.81),(5.08,0)])
library.append(symbol('TX2_5V','RL',[
    (coil,pin(1,0,7.62,270)+pin(12,0,-7.62,90)),
    (input_contact,pin(8,0,7.62,270)+pin(10,0,-7.62,90)+pin(9,7.62,0,180)),
    (output_contact,pin(3,0,7.62,270)+pin(5,0,-7.62,90)+pin(4,7.62,0,180))]))
def lpf_connector(name, output=False):
    # Adapt KiCad Connector_Generic:Conn_01x04 to the existing pin endpoints.
    # Source: KiCad 10.0.6 Connector_Generic.kicad_sym; see KICAD-LIBRARY-LICENSE.md.
    # Rotate/reflect the standard boxed body and four contact marks, retaining
    # the compact sheet's pin numbering and 2.54 mm pre-scaling pitch.
    sign = -1 if output else 1
    def point(x, y): return (round(sign*(-y-1.27), 4), round(sign*(-x+2.54), 4))
    rectangles = [(-1.27,3.81,1.27,-6.35)]
    rectangles += [(-1.27,y+.127,0,y-.127) for y in [2.54,0,-2.54,-5.08]]
    graphics = ''
    for i,(x1,y1,x2,y2) in enumerate(rectangles):
        x1,y1=point(x1,y1);x2,y2=point(x2,y2)
        graphics += (f'(rectangle (start {x1} {y1}) (end {x2} {y2}) '
                     f'(stroke (width {.254 if i==0 else .1524}) (type default)) '
                     f'(fill (type {"background" if i==0 else "none"})))')
    pins=''.join(pin(n,sign*(n-2.5)*2.54,sign*7.62,90 if output else 270,3.81) for n in range(1,5))
    return symbol(name,'J',[(graphics,pins)])
library.append(lpf_connector('LPF_IN'))
library.append(lpf_connector('LPF_OUT', output=True))
def boxed_wire_symbol(name):
    # KiCad Conn_01x02/Conn_01x03 boxed style, adapted to existing wire-link pins.
    # Pin endpoints remain fixed; these graphics do not bridge adjacent pins.
    if name=='Link2':
        body=(-3.81,2.54,3.81,5.08)
        contacts=[(-2.54,2.54,-2.54,3.81),(2.54,2.54,2.54,3.81)]
        pins=pin(1,-2.54,0,90)+pin(2,2.54,0,90)
    elif name=='Selector3':
        body=(2.54,1.27,5.08,-11.43)
        contacts=[(2.54,-i*5.08,3.81,-i*5.08) for i in range(3)]
        pins=''.join(pin(i+1,0,-i*5.08,0) for i in range(3))
    else:
        assert name=='InputSelector3'
        body=(-6.35,-2.54,6.35,-5.08)
        contacts=[(x,-2.54,x,-3.81) for x in [-5.08,0,5.08]]
        pins=''.join(pin(i+1,x,0,270) for i,x in enumerate([-5.08,0,5.08]))
    graphics=rectangle(*body).replace('(type none)', '(type background)')
    for x1,y1,x2,y2 in contacts:
        if x1==x2:x1-=.127;x2+=.127
        else:y1+=.127;y2-=.127
        graphics+=(f'(rectangle (start {x1} {y1}) (end {x2} {y2}) '
                   '(stroke (width .1524) (type default)) (fill (type none)))')
    return symbol(name,'W',[(graphics,pins)])
library.append(boxed_wire_symbol('Selector3'))
library.append(boxed_wire_symbol('Link2'))
library.append(symbol('Terminal2','J',[(rectangle(-2.54,-2.54,10.16,-5.08),pin(1,0,0,270)+pin(2,7.62,0,270))]))
# Two-pin boxed connector artwork adapted from KiCad Conn_01x02; see attribution.
# Preserve the existing 7.62 mm pre-scaling terminal pin separation.
def antenna_connector():
    graphics=rectangle(-1.27,-2.54,8.89,-5.08).replace('(type none)', '(type background)')
    for x in [0,7.62]:
        graphics += (f'(rectangle (start {x-.127} -2.54) (end {x+.127} -3.81) '
                     '(stroke (width .1524) (type default)) (fill (type none)))')
    return symbol('AntennaConnector2','J',[(graphics,pin(1,0,0,270)+pin(2,7.62,0,270))])
library.append(antenna_connector())
def output_connector():
    # Standard Conn_01x02 box/contact geometry, translated to existing Port_2 pins.
    graphics=rectangle(-3.81,2.54,-1.27,-2.54).replace('(type none)', '(type background)')
    for y in [1.27,-1.27]:
        graphics += (f'(rectangle (start -3.81 {y+.127}) (end -2.54 {y-.127}) '
                     '(stroke (width .1524) (type default)) (fill (type none)))')
    return symbol('OutputConnector2','J',[(graphics,pin(1,-7.62,1.27,0,3.81)+pin(2,-7.62,-1.27,0,3.81))])
library.append(output_connector())

def coax_connector():
    # KiCad 10.0.6 Connector:Conn_Coaxial artwork; see library attribution.
    # Translate center contact onto the old pin-1 endpoint. Shield exits below.
    definition=symbol('Conn_Coaxial','X',[('(polyline (pts (xy -2.54 0) (xy -0.508 0)) (stroke (width 0) (type default)) (fill (type none)))(arc\n  (start 1.778 0)\n  (mid 0.222 -1.8079)\n  (end -1.778 -0.508)\n  (stroke (width 0.254) (type default))\n  (fill (type none)))(arc\n  (start -1.778 0.508)\n  (mid 0.2221 1.8084)\n  (end 1.778 0)\n  (stroke (width 0.254) (type default))\n  (fill (type none)))(circle (center 0 0) (radius 0.508) (stroke (width 0.2032) (type default)) (fill (type none)))(polyline (pts (xy 0 -2.54) (xy 0 -1.778)) (stroke (width 0) (type default)) (fill (type none)))','(pin passive line\n  (at -5.08 0 0)\n  (length 2.54)\n  (name "In" (effects (font (size 1.27 1.27))))\n  (number "1" (effects (font (size 1.27 1.27)))))(pin passive line\n  (at 0 -5.08 90)\n  (length 2.54)\n  (name "Ext" (effects (font (size 1.27 1.27))))\n  (number "2" (effects (font (size 1.27 1.27)))))')])
    def translate(obj):
        if not isinstance(obj,list):return
        if obj and obj[0] in ['xy','at','start','mid','end','center']:
            obj[1]=Atom(str(round(float(obj[1])-2.54,4)))
            obj[2]=Atom(str(round(float(obj[2])+1.27,4)))
        for value in obj:translate(value)
    for unit in kids(definition,'symbol'):translate(unit)
    return definition
library.append(coax_connector())

definitions={s[1]:s for s in kids(library,'symbol')}
embedded=[]
for name,definition in definitions.items():
    s=copy.deepcopy(definition);s[1]=LIB+':'+name;embedded.append(dump(s))
parts=[];segments=[];dots=set();labels=set();extras=[]
def wire(*points):
    for a,b in zip(points,points[1:]):
        if a!=b:
            assert a[0]==b[0] or a[1]==b[1],(a,b)
            segments.append((a,b))
def dot(x,y): dots.add((x,y))
def label(net,x,y,angle=0,justify='left'):
    if (net,x,y) in labels:return
    labels.add((net,x,y))
    extras.append(f'(label {q(net)} (at {x} {y} {angle}) {eff(1.0,f"(justify {justify} bottom)")} (uuid "{uid(f"label:{net}:{x}:{y}")}"))')
def note(text,x,y,size=1.27):
    extras.append(f'(text {q(text)} (at {x} {y} 0) {eff(size,"(justify left)")} (uuid "{uid("text:"+text)}"))')
def ground(x,y,net='GND'):
    wire((x,y),(x,y+5.08))
    extras.append(poly([(x-2.54,y+5.08),(x+2.54,y+5.08)],.254)[:-1]+f' (uuid "{uid(f"groundbar:{x}:{y}")}"))')
    # Schematic polylines use absolute points and require a UUID, like wires.
    extras.append(poly([(x-1.27,y+6.35),(x+1.27,y+6.35)],.254)[:-1]+f' (uuid "{uid(f"groundbar2:{x}:{y}")}"))')
    label(net,x,y+5.08,justify='right')
def place(ref,sym,x,y,unit=1,angle=0,refpos=None,valuepos=None):
    inst=copy.deepcopy(original[ref])
    child(inst,'lib_id')[1]=LIB+':'+sym
    child(inst,'at')[1:]=[Atom(str(x)),Atom(str(y)),Atom(str(angle))]
    child(inst,'unit')[1]=Atom(str(unit))
    if unit>1: child(inst,'uuid')[1]=uid(ref+':unit'+str(unit))
    for v in kids(inst,'property'):
        if ref=='W9' and v[1]=='Value':v[2]='OPEN: relay-1 COM'
        if v[1]=='Reference':
            xx,yy=refpos or (x+5.08,y-3.81)
        elif v[1]=='Value':
            xx,yy=valuepos or (x+5.08,y-1.27)
        else: xx,yy=x,y
        field_angle=90 if angle==270 and v[1] in ['Reference','Value'] else 0
        child(v,'at')[1:]=[Atom(str(xx)),Atom(str(yy)),Atom(str(field_angle))]
        if v[1] in ['Reference','Value']:
            effects=child(v,'effects')
            effects[:]=[item for item in effects if not (isinstance(item,list) and item[0]=='justify')]
            effects.append([Atom('justify'),Atom('left')])
        if unit>1 and v[1]=='Value':
            child(v,'effects').append([Atom('hide'),Atom('yes')])
    inst[:]=[v for v in inst if not (isinstance(v,list) and v[0]=='pin')]
    for sub in kids(definitions[sym],'symbol'):
        if sub[1].endswith(f'_{unit}_1'):
            for pd in kids(sub,'pin'):
                n=child(pd,'number')[1]
                inst.append(parse(f'(pin "{n}" (uuid "{uid(ref+"pin"+n)}"))'))
    child(child(child(inst,'instances'),'project'),'path')[:] = parse(f'(path "/{sheet_uuid}" (reference "{ref}") (unit {unit}))')
    parts.append(dump(inst))

note('Relay-Switched LPF - five-channel carrier',20.32,17.78,1.7)
note('Rev. 5 circuit arrangement: coils above, RF switching and filter sockets below.',20.32,24.13,1.0)
wire((30.48,30.48),(332.74,30.48));label('+5V',30.48,30.48)
wire((50.8,40.64),(314.96,40.64));label('RELAY_VPLUS',50.8,40.64)
place('W1','Link2',35.56,40.64,refpos=(33.02,45.72),valuepos=(33.02,48.26))
wire((33.02,40.64),(30.48,40.64),(30.48,30.48));dot(30.48,30.48)
wire((38.1,40.64),(50.8,40.64));dot(50.8,40.64)
wire((30.48,90.17),(314.96,90.17));label('RFI',30.48,90.17)
wire((30.48,215.90),(309.88,215.90));label('RFO',30.48,215.90)

for i in range(5,0,-1):
    x=round(50.8+(5-i)*66.04,2)
    def xx(offset=0):return round(x+offset,2)
    place(f'RL{i}','TX2_5V',x,60.96,refpos=(xx(-17.78),58.42),valuepos=(xx(-17.78),60.96))
    place(f'RL{i}','TX2_5V',x,105.41,2,refpos=(xx(10.16),105.41))
    place(f'RL{i}','TX2_5V',x,201.93,3,refpos=(xx(-15.24),201.93) if i==1 else (xx(10.16),199.39))
    place(f'D{i}','1N4148',xx(17.78),60.96,angle=270,refpos=(xx(21.59),58.42),valuepos=(xx(21.59),60.96))
    wire((x,40.64),(x,53.34));dot(x,40.64)
    wire((xx(17.78),30.48),(xx(17.78),53.34));dot(xx(17.78),30.48)
    wire((x,68.58),(xx(17.78),68.58));wire((x,68.58),(x,76.2));dot(x,68.58)
    label(f'BAND{i}_N',x,76.2)
    wire((x,90.17),(x,97.79));dot(x,90.17)
    place(f'J{i*2}','LPF_IN',xx(3.81),135.89,refpos=(xx(12.7),130.81),valuepos=(xx(12.7),133.35))
    wire((x,128.27),(x,123.19),(xx(2.54),123.19),(xx(2.54),128.27))
    wire((xx(5.08),128.27),(xx(5.08),123.19),(xx(7.62),123.19));dot(xx(7.62),123.19)
    wire((xx(7.62),105.41),(xx(7.62),128.27));label(f'LPF{i}_IN',xx(7.62),118.11)
    wire((x,123.19),(xx(-7.62),123.19));dot(x,123.19);ground(xx(-7.62),123.19)
    if i>1: wire((x,113.03),(x,123.19))
    note(str(i),xx(1.27),154.94,5.08)
    place(f'J{i*2+1}','LPF_OUT',xx(3.81),171.45,refpos=(xx(12.7),172.72),valuepos=(xx(12.7),175.26))
    wire((x,179.07),(x,184.15),(xx(2.54),184.15),(xx(2.54),179.07))
    wire((xx(5.08),179.07),(xx(5.08),184.15),(xx(7.62),184.15));dot(xx(7.62),184.15)
    if i>1:
        wire((x,184.15),(x,194.31));dot(x,184.15)
        wire((x,184.15),(xx(-7.62),184.15));ground(xx(-7.62),184.15)
        wire((xx(7.62),179.07),(xx(7.62),201.93));label(f'LPF{i}_OUT',xx(7.62),189.23)
    else:
        wire((xx(7.62),179.07),(xx(7.62),184.15),(360.68,184.15));label('LPF1_OUT',337.82,184.15)
        wire((x,184.15),(x,190.5),(365.76,190.5));dot(x,184.15);dot(365.76,190.5)
        wire((x,194.31),(x,191.77),(307.34,191.77));ground(307.34,191.77)
    selector=f'W{i+1}'
    place(selector,'Selector3',x,219.71,refpos=(xx(-10.16),218.44),valuepos=(xx(7.62),222.25))
    wire((x,209.55),(x,219.71));label(f'RELAY{i}_OUT',x,212.09)
    wire((xx(-5.08),215.90),(xx(-5.08),224.79),(x,224.79));dot(xx(-5.08),215.90)
    place(f'J{20+i}','AntennaConnector2',x,242.57,refpos=(xx(-7.62),245.11),valuepos=(xx(-7.62),247.65))
    wire((x,229.87),(x,242.57));label(f'ANT{i}',x,236.22)
    wire((xx(7.62),242.57),(xx(7.62),238.76),(xx(15.24),238.76));ground(xx(15.24),238.76)

# Slot 1 keeps the selected common output in series through its NC contact.
# A horizontal three-pad option represents RFO / FINAL_NC / ground.
defs=boxed_wire_symbol('InputSelector3')
library.append(defs);definitions['InputSelector3']=defs
em=copy.deepcopy(defs);em[1]=LIB+':InputSelector3';embedded.append(dump(em))
place('W7','InputSelector3',294.64,118.11,refpos=(281.94,102.87),valuepos=(281.94,105.41))
wire((314.96,113.03),(314.96,115.57),(294.64,115.57),(294.64,118.11));label('FINAL_NC',294.64,115.57)
wire((289.56,118.11),(284.48,118.11),(284.48,215.90));dot(284.48,215.90)
wire((299.72,118.11),(307.34,118.11));ground(307.34,118.11)
place('W8','Link2',339.09,158.75,refpos=(331.47,148.59),valuepos=(331.47,151.13))
ground(336.55,158.75)
wire((341.63,158.75),(341.63,190.5));dot(341.63,190.5)
place('W9','Link2',339.09,204.47,refpos=(326.39,191.77),valuepos=(326.39,194.31))
wire((322.58,201.93),(334.01,201.93),(334.01,198.12),(344.17,198.12),(344.17,204.47),(341.63,204.47));label('FINAL_RELAY_COM',334.01,198.12)
wire((336.55,204.47),(336.55,207.01),(353.06,207.01),(353.06,194.31),(360.68,194.31));dot(360.68,194.31)
for ref,y in [('X1',165.1),('X2',187.96),('J26',210.82)]:
    place(ref,'OutputConnector2' if ref=='J26' else 'Conn_Coaxial',375.92,y,refpos=(370.84,y-6.35) if ref=='J26' else (379.73,y-3.81),valuepos=(370.84,y-3.81) if ref=='J26' else (379.73,y-1.27))
    wire((360.68,round(y-1.27,2)),(368.3,round(y-1.27,2)));dot(360.68,round(y-1.27,2))
    shield_y=round(y+(1.27 if ref=='J26' else 3.81),2)
    shield_x=368.3 if ref=='J26' else 373.38
    wire((365.76,shield_y),(shield_x,shield_y));dot(365.76,shield_y)
wire((360.68,163.83),(360.68,209.55));dot(360.68,184.15)
wire((365.76,168.91),(365.76,212.09));label('GND_OUT',365.76,219.71)
wire((365.76,212.09),(365.76,219.71))
place('J1','Port_10',50.8,276.86,refpos=(45.72,260.35),valuepos=(45.72,262.89))
for n,net in json.loads((ROOT/'design/connections.json').read_text())['J1'].items():
    y=round(276.86-(11.43-(int(n)-1)*2.54),2)
    wire((43.18,y),(25.4,y));label(net,25.4,y,justify='right')
note('Default links: W1, W3-W6, W7 pins 1-2. Leave W2, W8, and W9 open.',83.82,260.35)
note('Drive one BAND input low at a time; use an external coil driver for Pi/Pico.',83.82,266.7)
note('Slot 1: highest-frequency LPF. GND_OUT remains isolated on the carrier.',83.82,273.05)

# Split wires at explicit junctions so every T connection is unambiguous.
def rounded(point):return tuple(round(v,4) for v in point)
segments=[(rounded(a),rounded(b)) for a,b in segments]
dots={rounded(v) for v in dots}
pieces=set()
for a,b in segments:
    points={a,b}
    for point in dots:
        if a[0]==b[0]==point[0] and min(a[1],b[1])<=point[1]<=max(a[1],b[1]):points.add(point)
        if a[1]==b[1]==point[1] and min(a[0],b[0])<=point[0]<=max(a[0],b[0]):points.add(point)
    points=sorted(points)
    for aa,bb in zip(points,points[1:]): pieces.add((aa,bb))
wires=[]
for a,b in sorted(pieces):
    wires.append(f'(wire (pts (xy {a[0]} {a[1]}) (xy {b[0]} {b[1]})) (stroke (width 0) (type default)) (uuid "{uid(str((a,b)))}"))')
for x,y in sorted(dots):
    wires.append(f'(junction (at {x} {y}) (diameter 0) (color 0 0 0 0) (uuid "{uid(f"junction:{x}:{y}")}"))')
header=[copy.deepcopy(v) for v in old if not (isinstance(v,list) and v[0] in ['lib_symbols','symbol','wire','label','junction','text','polyline'])]
out='(kicad_sch\n'+'\n'.join(dump(v) for v in header[1:])+'\n(lib_symbols\n'+'\n'.join(embedded)+')\n'+'\n'.join(parts+wires+extras)+')\n'

# Compact the drawing for the user's selected US Letter landscape sheet.
# Symbols shrink to half size on a normal 25 mil connection grid. Additional
# horizontal space between filter columns keeps the field text readable.
def scale_local(obj,pin_context=False):
    if not isinstance(obj,list):return
    pin_context=pin_context or bool(obj and obj[0]=='pin')
    if obj and obj[0] in ['at','start','mid','end','xy','center','size']:
        for i in [1,2]:
            if i<len(obj) and isinstance(obj[i],Atom):
                factor=.5
                obj[i]=Atom(str(round(float(obj[i])*factor,4)))
        if obj[0]=='size':
            obj[1:3]=[Atom(str(max(.7 if pin_context else .9,float(v)))) for v in obj[1:3]]
    elif obj and obj[0] in ['length','radius','width','offset'] and len(obj)>1:
        obj[1]=Atom(str(round(float(obj[1])*.5,4)))
    for item in obj:scale_local(item,pin_context)
def page_x(x):
    # Boundaries sit between symbols, so local pin/body geometry stays rigid.
    columns=sum(x>=bound for bound in [83.82,149.86,215.90,281.94,347.98])
    return round(x*.5+columns*6.35+10.16,4)
def page_y(y):return round(y*.5+5.08,4)
def scale_page(obj):
    if not isinstance(obj,list):return
    if obj and obj[0] in ['at','xy','start','end','center']:
        obj[1]=Atom(str(page_x(float(obj[1]))));obj[2]=Atom(str(page_y(float(obj[2]))))
    elif obj and obj[0]=='size':
        obj[1:3]=[Atom(str(max(.9,float(v)*.5))) for v in obj[1:3]]
    elif obj and obj[0] in ['diameter','width']:
        obj[1]=Atom(str(round(float(obj[1])*.5,4)))
    for item in obj:scale_page(item)
sheet=parse(out)
child(sheet,'paper')[:]=parse('(paper "A")')
for item in sheet:
    if not isinstance(item,list):continue
    if item[0]=='lib_symbols':
        for definition in kids(item,'symbol'):scale_local(definition)
    elif item[0] in ['symbol','wire','label','junction','text','polyline']:
        scale_page(item)
for definition in kids(library,'symbol'):scale_local(definition)
sch_path.write_text(dump(sheet)+'\n')
(ROOT/(LIB+'.kicad_sym')).write_text(dump(library)+'\n')
project_path=ROOT/(NAME+'.kicad_pro')
project=json.loads(project_path.read_text())
project.setdefault('schematic',{})['connection_grid_size']=25.0
project_path.write_text(json.dumps(project,indent=2)+'\n')
subprocess.run([sys.executable,str(ROOT/'design/shared_fields.py')],check=True)
print(f'Redrawn: {len(parts)} units / {len(original)} components; {len(wires)} wire/junction records, {len(labels)} net labels.')
