#!/usr/bin/env python3
"""Generate local QLG3 KiCad assets. MIT; factual XY data supplied by Hans Summers.
Requires cadquery==2.8.0 for the colored STEP and VRML mesh export.
The JSON distinguishes dimensioned geometry from provisional height/envelope data.
"""
import json, math, re
from pathlib import Path
import cadquery as cq

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
D = json.loads((HERE / 'dimensions.json').read_text())
I, H, V = D['dimensioned_inches'], D['host_design_mm'], D['provisional_model_mm']
NAME = 'QLG3_GPS_UndersideHeader'
LIB = 'wsprrypico-synth-shield'
mm = lambda x: x * 25.4
W, L = mm(I['board_width']), mm(I['board_height'])
mounts = [(mm(x), mm(y)) for x, y in I['mounting_centers']]
hx, hy = map(mm, I['header_pin3'])
headers = [(hx + (n - 3) * mm(I['header_pitch']), hy) for n in range(1, 6)]
sx, sy = map(mm, I['sma_signal_center'])
# Turn Hans's board over about X: E108 side faces up, SMA still faces left.
# The male header is fitted on the opposite face from E108.
mounts = [(x, L-y) for x,y in mounts]
hy = L-hy
headers = [(x, L-y) for x,y in headers]
sy = L-sy
z = V['board_underside_above_host_top']
t = V['board_thickness']

# Solids use conventional right-handed XYZ, in the assembled E108-up view (Hans XY reflected in Y).
# Footprint Y is negated below because KiCad's PCB coordinates grow downward.
assembly = cq.Assembly(name=NAME)
solids = []
def add(name, shape, rgb):
    shape = shape.val() if isinstance(shape, cq.Workplane) else shape
    assert shape.isValid(), name
    assembly.add(shape, name=name, color=cq.Color(*rgb))
    solids.append((name, shape, rgb))
def box(x, y, zz, dx, dy, dz):
    return cq.Workplane('XY').box(dx, dy, dz, centered=(False, False, False)).translate((x, y, zz))

green, gold, black, white, steel = (.08,.32,.16), (.78,.58,.16), (.09,.09,.10), (.84,.84,.78), (.66,.68,.70)
board = box(0, 0, z, W, L, t)
for x,y in mounts:
    board = board.cut(cq.Workplane('XY').workplane(offset=z-0.1).center(x,y).circle(V['module_hole_diameter']/2).extrude(t+0.2))
for x,y in headers:
    board = board.cut(cq.Workplane('XY').workplane(offset=z-0.1).center(x,y).circle(.5).extrude(t+0.2))
add('QLG3_PCB_XY_verified_Z_provisional', board, green)
# Copper rings and plated header pads depict the supplied layout without reproducing its artwork.
for i,(x,y) in enumerate(mounts,1):
    ring = cq.Workplane('XY').workplane(offset=z+t).center(x,y).circle(2.5).circle(V['module_hole_diameter']/2).extrude(.035)
    add(f'mount_ring_{i}', ring, gold)
    spacer = cq.Workplane('XY').center(x,y).polygon(6,V['spacer_across_flats']/math.cos(math.pi/6)).extrude(V['spacer_length']).cut(cq.Workplane('XY').center(x,y).circle(1.5).extrude(V['spacer_length']))
    add(f'provisional_M3_spacer_{i}', spacer, white)
    head=cq.Workplane('XY').workplane(offset=z+t+.05).center(x,y).circle(2.5).extrude(1.8)
    head=head.cut(box(x-2.6,y-.4,z+t+1.2,5.2,.8,1))
    add(f'provisional_screw_head_{i}', head, white)
# Exact generic KiCad connector solids; mating side down on the daughterboard.
pitch=mm(I['header_pitch']);x0=headers[0][0]-pitch/2
model_dir=ROOT/f'{LIB}.3dshapes'
for kind,height in [('PinSocket',8.5),('PinHeader',2.54)]:
    raw=cq.importers.importStep(str(model_dir/f'{kind}_1x05_P2.54mm_Vertical.step')).val()
    plastic_box=box(-1.27,-11.43,0,2.54,12.7,height).val()
    body=raw.intersect(plastic_box);pins=raw.cut(plastic_box)
    for label,shape,color in [('body',body,black),('contacts',pins,gold)]:
        if kind=='PinSocket':
            shape=shape.rotate((0,0,0),(0,0,1),90).translate((headers[0][0],hy,0))
        else:
            shape=shape.rotate((0,0,0),(1,0,0),180).rotate((0,0,0),(0,0,1),-90).translate((headers[0][0],hy,z))
        add(f'KiCad_standard_{kind}_{label}',shape,color)
for i,(x,y) in enumerate(headers,1):
    add(f'header_pad_{i}',cq.Workplane('XY').workplane(offset=z+t).center(x,y).circle(.85).circle(.36).extrude(.04),gold)
# E108 side is now uppermost; convert its source-view Y coordinate.
gw,gl,gd=V['gnss_body_width'],V['gnss_body_length'],V['gnss_body_depth'];gx,gy=V['gnss_body_center']
gy=L-gy
add('E108_GN02_body_provisional',box(gx-gw/2,gy-gl/2,z+t,gw,gl,gd),steel)
# Right-angle SMA: dimensioned signal center anchors its illustrative body.
bl,bw,bd=V['sma_body_length'],V['sma_body_width'],V['sma_body_depth']
add('top_SMA_body_provisional',box(sx-bl/2,sy-bw/2,z+t,bl,bw,bd),gold)
barrel=cq.Solid.makeCylinder(V['sma_barrel_diameter']/2,V['sma_barrel_length'],cq.Vector(sx-bl/2,sy,z+t+bd/2),cq.Vector(-1,0,0))
bore=cq.Solid.makeCylinder(2.15,V['sma_barrel_length']+.1,cq.Vector(sx-bl/2+.05,sy,z+t+bd/2),cq.Vector(-1,0,0))
add('SMA_barrel_provisional',barrel.cut(bore),gold)
front=sx-bl/2-V['sma_barrel_length'];axis=z+t+bd/2
insulator=cq.Solid.makeCylinder(2.05,2,cq.Vector(front+2,sy,axis),cq.Vector(-1,0,0))
insulator=insulator.cut(cq.Solid.makeCylinder(.55,2.2,cq.Vector(front+2.1,sy,axis),cq.Vector(-1,0,0)))
add('SMA_dielectric_provisional',insulator,white)
for i in range(4):
    outer=cq.Solid.makeCylinder(V['sma_barrel_diameter']/2+.15,.25,cq.Vector(front+.7+i*.7,sy,axis),cq.Vector(1,0,0))
    inner=cq.Solid.makeCylinder(2.15,.27,cq.Vector(front+.69+i*.7,sy,axis),cq.Vector(1,0,0))
    add(f'SMA_thread_depiction_{i}',outer.cut(inner),gold)
# STEP is interchangeable CAD; VRML retains colors in KiCad and uses 2.54-mm units.
models=ROOT/f'{LIB}.3dshapes';models.mkdir(exist_ok=True)
assembly.save(str(models/f'{NAME}.step'))
lines=['#VRML V2.0 utf8','# QLG3 depiction includes KiCad connector geometry: CC BY-SA 4.0 with KiCad library exception. XY from Hans Summers; remaining envelopes approximate.']
for name,shape,rgb in solids:
    verts,tris=shape.tessellate(.08,.15)
    points=',\n'.join(f'{p.x/2.54:.6f} {p.y/2.54:.6f} {p.z/2.54:.6f}' for p in verts)
    indices=',\n'.join(' '.join(map(str,tri))+' -1' for tri in tris)
    lines.append(f'# {name}\nShape {{ appearance Appearance {{ material Material {{ diffuseColor {rgb[0]} {rgb[1]} {rgb[2]} }} }} geometry IndexedFaceSet {{ coord Coordinate {{ point [ {points} ] }} coordIndex [ {indices} ] solid TRUE creaseAngle 0.5 }} }}')
(models/f'{NAME}.wrl').write_text('\n'.join(lines)+'\n')
# Host footprint contains socket lands and two matching host clearance holes.
F=[f'(footprint "{NAME}" (version 20241229) (generator "qlg3_model_generator") (layer "F.Cu")',
'(descr "QLG3 E108 and SMA on top; male header underneath mates host socket. Hans XY reflected about X; standard socket; body envelopes approximate.")',
'(tags "QRP Labs QLG3 GNSS GPS 2.54mm daughterboard")','(attr through_hole exclude_from_bom exclude_from_pos_files)',
'(property "Reference" "REF**" (at 9.2 -20 0) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))',
f'(property "Value" "QLG3 GPS" (at 9.2 2.2 0) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))']
def rect(x1,y1,x2,y2,layer,width):
    F.append(f'(fp_rect (start {x1:.6f} {-y1:.6f}) (end {x2:.6f} {-y2:.6f}) (stroke (width {width}) (type default)) (fill none) (layer "{layer}"))')
rect(0,0,W,L,'F.Fab',.1)
rect(-.2,-.2,W+.2,L+.2,'F.SilkS',.12)
# Socket body, marking pin 1 on the host top view.
rect(x0,hy-1.27,x0+5*pitch,hy+1.27,'F.Fab',.1)
F.append(f'(fp_circle (center {headers[0][0]:.6f} {-hy-1.9:.6f}) (end {headers[0][0]+.3:.6f} {-hy-1.9:.6f}) (stroke (width .12) (type default)) (fill none) (layer "F.SilkS"))')
# SMA signal center and provisional projected outline are fab graphics, never host electrical pads.
rect(sx-bl/2,sy-bw/2,sx+bl/2,sy+bw/2,'F.Fab',.1)
rect(sx-bl/2-V['sma_barrel_length'],sy-V['sma_barrel_diameter']/2,sx-bl/2,sy+V['sma_barrel_diameter']/2,'F.Fab',.1)
F.append(f'(fp_circle (center {sx:.6f} {-sy:.6f}) (end {sx+.25:.6f} {-sy:.6f}) (stroke (width .1) (type default)) (fill none) (layer "F.Fab"))')
# Restrict only host-contact hardware; leave the elevated module interior usable.
# 7.4 mm squares enclose a 5.5 mm AF hex post at any rotation + >=0.5 mm.
margin=H['courtyard_margin'];radius=H['mount_hardware_keepout_square']/2
socket=(x0-margin,hy-1.27-margin,x0+5*pitch+margin,hy+1.27+margin)
def points_for_rect(bounds):
    x1,y1,x2,y2=bounds
    return [(x1,y1),(x2,y1),(x2,y2),(x1,y2)]
def courtyard(points):
    for a,b in zip(points,points[1:]+points[:1]):
        F.append(f'(fp_line (start {a[0]:.6f} {-a[1]:.6f}) (end {b[0]:.6f} {-b[1]:.6f}) (stroke (width .05) (type default)) (layer "F.CrtYd"))')
def component_keepout(name,points):
    xy=' '.join(f'(xy {x:.6f} {-y:.6f})' for x,y in points)
    F.append(f'(zone (layers "F.Cu") (name "{name}") (hatch edge 0.5) (connect_pads (clearance 0)) (min_thickness .25) (keepout (tracks allowed) (vias allowed) (pads allowed) (copperpour allowed) (footprints not_allowed)) (fill (thermal_gap .5) (thermal_bridge_width .5)) (polygon (pts {xy})))')
component_keepout('QLG3 socket component keepout',points_for_rect(socket))
# Adjacent post and socket clearance envelopes overlap: merge their courtyard
# outlines, rather than making an invalid self-overlapping courtyard.
for index,(x,y) in enumerate(mounts,1):
    post=(x-radius,y-radius,x+radius,y+radius)
    component_keepout(f'QLG3 mounting hardware {index} component keepout',points_for_rect(post))
    if abs(y-hy)<1e-6:
        a,b,c,e=post;sl,sb,sr,st=socket
        assert a<sl<c<sr and b<sb<st<e
        courtyard([(a,b),(c,b),(c,sb),(sr,sb),(sr,st),(c,st),(c,e),(a,e)])
    else:
        courtyard(points_for_rect(post))
for i,(x,y) in enumerate(headers,1):
    F.append(f'(pad "{i}" thru_hole {"rect" if i==1 else "circle"} (at {x:.6f} {-y:.6f}) (size {H["socket_pad_diameter"]} {H["socket_pad_diameter"]}) (drill {H["socket_drill"]}) (layers "*.Cu" "*.Mask"))')
for x,y in mounts:
    F.append(f'(pad "" np_thru_hole circle (at {x:.6f} {-y:.6f}) (size {H["mounting_clearance_drill"]} {H["mounting_clearance_drill"]}) (drill {H["mounting_clearance_drill"]}) (layers "*.Cu" "*.Mask"))')
    F.append(f'(fp_circle (center {x:.6f} {-y:.6f}) (end {x+V["spacer_across_flats"]/(2*math.cos(math.pi/6)):.6f} {-y:.6f}) (stroke (width .1) (type default)) (fill none) (layer "F.Fab"))')
F.append(f'(model "${{KIPRJMOD}}/{LIB}.3dshapes/{NAME}.wrl" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))\n)')
(ROOT/f'{LIB}.pretty'/f'{NAME}.kicad_mod').write_text('\n'.join(F)+'\n')
# Explicit electrical module symbol; no invented sixth header pin for hand-wired RX.
S=[f'(symbol "{NAME}" (pin_names (offset 1.016)) (exclude_from_sim no) (in_bom no) (on_board yes) (in_pos_files no)',
'(property "Reference" "A" (at 0 10.16 0) (effects (font (size 1.27 1.27))))',
'(property "Value" "QLG3 GPS" (at 0 7.62 0) (effects (font (size 1.27 1.27))))',
f'(property "Footprint" "{LIB}:{NAME}" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))',
'(property "Datasheet" "https://qrp-labs.com/qlg3.html" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))',
'(property "Description" "QRP Labs QLG3 GNSS module; E108 and SMA up, five-pin header down; optional RX requires hand wire to module pin3" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))',
f'(property "ki_fp_filters" "{NAME}" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))',
f'(symbol "{NAME}_0_1" (rectangle (start -10.16 5.08) (end 10.16 -5.08) (stroke (width .254) (type default)) (fill (type background))))']
S.append(f'(symbol "{NAME}_1_1"')
for num,nm,typ,x,y,ang in [(1,'VCC_3V3','power_in',-15.24,2.54,0),(2,'VBAT','power_in',-15.24,-2.54,0),(3,'PPS','output',15.24,2.54,180),(4,'TXD','output',15.24,-2.54,180),(5,'GND','power_in',0,-10.16,90)]:
    S.append(f'(pin {typ} line (at {x} {y} {ang}) (length 5.08) (name "{nm}" (effects (font (size 1.27 1.27)))) (number "{num}" (effects (font (size 1.27 1.27)))))')
S.append('))');symbol='\n'.join(S)
# Replace just this definition on regeneration; preserve all unrelated library text.
p=ROOT/f'{LIB}.kicad_sym';text=p.read_text();needle=f'(symbol "{NAME}"';pos=text.find(needle)
if pos>=0:
    depth=0;quoted=False;escaped=False;end=None
    for i,c in enumerate(text[pos:],pos):
        if quoted:
            if escaped:escaped=False
            elif c=='\\':escaped=True
            elif c=='"':quoted=False
        elif c=='"':quoted=True
        elif c=='(':depth+=1
        elif c==')':
            depth-=1
            if depth==0:end=i+1;break
    assert end is not None;text=text[:pos]+symbol+text[end:]
else:
    end=text.rfind(')');text=text[:end]+symbol+'\n'+text[end:]
p.write_text(text)
print(json.dumps({'board_mm':[W,L],'mounts_mm':mounts,'header_mm':headers,'sma_center_mm':[sx,sy],'solids':len(solids)},indent=2))
