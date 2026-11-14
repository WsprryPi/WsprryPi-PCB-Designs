#!/usr/bin/env python3
"""Generate the original low-support T61 footprint, preview and drawing.

No project PCB is read or written. Models are nominal assembly illustrations,
not qualified winding paths, tolerances, adhesive strength or RF performance.
"""
from pathlib import Path
import json,math,uuid
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph,Table,TableStyle
ROOT=Path(__file__).resolve().parent;PROJECT=ROOT.parent.parent
LIB='wsprrypico-gpio-shield-with-gps-torroid-edition'
NAME='T61_FairRite_5977000621_Upright_Bumper_4Pin';MODEL=NAME+'_Preview.wrl'
PADS=[(1,5.0,5.3,'A start / dot','AMP_XFMR_FEED'),(2,-5.6,-4.6,'A finish','AMP_DRAIN'),(3,-5.6,-4.6,'B start / dot','AMP_DRAIN'),(4,-5.0,5.3,'B finish','AMP_RF_XFMR')]
PHYSICAL_HOLES=[1,2,4]
PAD_DIMS={1:(1.0,2.0),2:(1.2,2.4),3:(1.2,2.4),4:(1.0,2.0)}
COURTYARD=[25,13.5]
SUPPORT_DIAMETER=8.0;SUPPORT_RADIUS=SUPPORT_DIAMETER/2
SUPPORT_HEIGHT=1.25;BEDDING_X=4.0;BEDDING_Y=6.0;BEDDING_HEIGHT=.5;CORE_BOTTOM=SUPPORT_HEIGHT+BEDDING_HEIGHT
LEAD_DROP=6-CORE_BOTTOM
def dress(x,y,z):return (x,y,z-LEAD_DROP)
LEAD_PATHS={1:[dress(3.4,-4.15,6.8),dress(6.2,-5.3,6.3),dress(6.2,5.3,6.3),dress(5,5.3,6.3),(5,5.3,1),(5,5.3,-3.1)],2:[dress(-6.2,4.6,6.3),dress(-6.2,-4.6,6.3),dress(-5.6,-4.6,6.3),(-5.82,-4.6,1),(-5.82,-4.6,-3.1)],3:[dress(3.4,-4.65,6.8),dress(2,-5.3,6.3),dress(-4.8,-5.3,6.3),dress(-5.6,-4.6,6.3),(-5.38,-4.6,1),(-5.38,-4.6,-3.1)],4:[dress(-3.4,4.15,6.8),dress(-5,5.3,6.3),(-5,5.3,1),(-5,5.3,-3.1)]}
PAD_UUID={1:'5e8c63f9-2a0b-5e23-b4f6-433c875dea9f',2:'35cb7abb-ef99-5155-9a90-e9253da4e860',3:'19288744-56f5-5373-8aa5-24caaa3f590c',4:'137ac396-eb33-515c-a4df-bb5ad3bf0523'}
CORE=dict(od_max=21.85,id_min=12.4,axial_max=7.1,nominal_bottom=CORE_BOTTOM)
SOURCES={'core':'https://fair-rite.com/product/toroids-5977000621/'}
seq=0
isometric_note='Original nominal preview; 1.25mm illustrative insulating support and 0.5mm bedding allowance. Mounting materials and retention are builder-selected; validate the actual assembly.'
def uid():
 global seq
 seq+=1;return str(uuid.uuid5(uuid.NAMESPACE_URL,'wsprrypico-t61-silicone-bumper-v1:'+str(seq)))
def n(v):return f'{v:.6f}'.rstrip('0').rstrip('.') if v else '0'
def q(v):return json.dumps(v)
def prop(k,v,x,y,l,hide=False):return f'\t(property {q(k)} {q(v)} (at {n(x)} {n(y)} 0) (layer {q(l)})'+(' (hide yes)' if hide else '')+f' (uuid {q(uid())}) (effects (font (size 1 1) (thickness 0.15))))'
def rect(x0,y0,x1,y1,l,w=.05):return f'\t(fp_rect (start {n(x0)} {n(y0)}) (end {n(x1)} {n(y1)}) (stroke (width {n(w)}) (type default)) (fill no) (layer {q(l)}) (uuid {q(uid())}))'
def text(v,x,y,l='F.Fab'):return f'\t(fp_text user {q(v)} (at {n(x)} {n(y)} 0) (layer {q(l)}) (uuid {q(uid())}) (effects (font (size 0.8 0.8) (thickness 0.12))))'
descr='Upright Fair-Rite 5977000621, 15+15 AWG26 turns, builder-selected insulating support; model shows 1.25mm pad and 0.5mm bedding allowance; three side-positioned PTH holes for four winding ends; 1 and 4 on +Y face, common 2/3 on -Y face; common hole 1.2mm, others 1.0mm; 25x13.5mm front courtyard, 30mm top and 1.5mm finished-joint underside reservation; no ties or slots. Prototype fit/retention/RF tests required.'
fp=[f'(footprint {q(NAME)}','\t(version 20260206)','\t(generator "pcbnew")','\t(generator_version "10.0")','\t(layer "F.Cu")',f'\t(descr {q(descr)})','\t(tags "T61 bifilar toroid upright builder-selected support manual")',prop('Reference','REF**',0,-6.7,'F.SilkS'),prop('Value','T61 15T+15T TYPE77',0,6.7,'F.Fab',True),prop('Datasheet',SOURCES['core'],0,0,'F.Fab',True),prop('Description','Original low-support preview; mounting materials selected by builder; see design/t61-mount/README.md',0,0,'F.Fab',True),'\t(attr through_hole exclude_from_pos_files exclude_from_bom)','\t(duplicate_pad_numbers_are_jumpers no)',rect(-12.5,-6.75,12.5,6.75,'F.CrtYd'),rect(-12,-5.7,12,5.7,'F.Fab',.1),rect(-10.925,-3.55,10.925,3.55,'F.Fab',.1),text('${REFERENCE}',7,0),text('UPRIGHT / 30mm MAX',0,-5.2),text('BUILDER SUPPORT',1,4.9)]
fp.append(f'\t(fp_circle (center 0 0) (end {n(SUPPORT_RADIUS)} 0) (stroke (width 0.1) (type default)) (fill no) (layer "F.Fab") (uuid {q(uid())}))')
for num,x,y,_,_ in PADS:
 drill,land=PAD_DIMS[num]
 if num==3:
  # Logical end 3 shares end 2's plated hole and pad 2's plated barrel.
  # A drill-free connect pad preserves schematic pin mapping without a duplicate drill.
  fp.append(f'\t(pad "3" connect circle (at {n(x)} {n(y)}) (size {n(land)} {n(land)}) (layers "F.Cu") (uuid {q(PAD_UUID[num])}))')
 else:
  fp.append(f'\t(pad "{num}" thru_hole {"rect" if num==1 else "circle"} (at {n(x)} {n(y)}) (size {n(land)} {n(land)}) (drill {n(drill)}) (layers "*.Cu" "*.Mask") (remove_unused_layers no) (uuid {q(PAD_UUID[num])}))')

 if num!=3:
  label='2/3' if num==2 else str(num)
  label_dx=-2.7 if num==2 else -2 if num==4 else 2
  fp.append(text(label,x+label_dx,y,'F.SilkS'))
  fp.append(text(('A*' if num==1 else 'A + B*' if num==2 else 'B'),x+label_dx,y))
fp.extend([f'\t(model "${{KIPRJMOD}}/{LIB}.3dshapes/{MODEL}" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))','\t(embedded_fonts no)',')'])
# Omit fabrication annotations while retaining the historical UUID sequence.
# Keep required value metadata hidden; silkscreen reference and terminal IDs stay.
fp=[item for item in fp if not (item.startswith('\t(fp_text ') and '(layer "F.Fab")' in item)]
fp_path=PROJECT/(LIB+'.pretty')/(NAME+'.kicad_mod');fp_path.write_text('\n'.join(fp)+'\n')
wrl=['#VRML V2.0 utf8','# Original repository MIT preview, coordinates in 0.1-inch units.','# '+isometric_note]
def mesh(ps,fs,col):
 # KiCad footprint +Y points down; VRML/CAD +Y points up. Reflect only at export.
 # Parameter paths stay in footprint XY so terminal coordinates are auditable.
 pts=', '.join(' '.join(n((v if axis!=1 else -v)/2.54) for axis,v in enumerate(p)) for p in ps);ids=', '.join(' '.join(map(str,f))+', -1' for f in fs)
 wrl.append(f'Shape {{ appearance Appearance {{ material Material {{ diffuseColor {col} }} }} geometry IndexedFaceSet {{ solid FALSE coord Coordinate {{ point [{pts}] }} coordIndex [{ids}] }} }}')
def box(cx,cy,cz,sx,sy,sz,col):
 ps=[(cx+a*sx/2,cy+b*sy/2,cz+c*sz/2) for a,b,c in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]];mesh(ps,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],col)
def tube(path,r,col,sides=10):
 ps=[]
 for i,p in enumerate(path):
  a=path[max(i-1,0)];b=path[min(i+1,len(path)-1)];d=[b[k]-a[k] for k in range(3)];mag=math.sqrt(sum(v*v for v in d));d=[v/mag for v in d];g=(0,1,0) if abs(d[1])<.9 else (1,0,0);u=(d[1]*g[2]-d[2]*g[1],d[2]*g[0]-d[0]*g[2],d[0]*g[1]-d[1]*g[0]);mag=math.sqrt(sum(v*v for v in u));u=[v/mag for v in u];v=(d[1]*u[2]-d[2]*u[1],d[2]*u[0]-d[0]*u[2],d[0]*u[1]-d[1]*u[0])
  for j in range(sides):
   a=2*math.pi*j/sides;ps.append(tuple(p[k]+r*(u[k]*math.cos(a)+v[k]*math.sin(a)) for k in range(3)))
 fs=[tuple(reversed(range(sides))),tuple((len(path)-1)*sides+j for j in range(sides))]
 for i in range(len(path)-1):
  for j in range(sides):fs.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
 mesh(ps,fs,col)
# Catalog core envelope and illustrative continuous winding paths; real winding qualification remains open.
N=96;cz=CORE['nominal_bottom']+10.925;ps=[]
for y,r in [(-3.55,10.925),(-3.55,6.2),(3.55,10.925),(3.55,6.2)]:
 for i in range(N):a=2*math.pi*i/N;ps.append((r*math.sin(a),y,cz+r*math.cos(a)))
fs=[]
for i in range(N):
 j=(i+1)%N;fs.extend([(i,j,N+j,N+i),(2*N+i,3*N+i,3*N+j,2*N+j),(i,2*N+i,2*N+j,j),(N+i,N+j,3*N+j,3*N+i)])
mesh(ps,fs,'0.25 0.28 0.32')
# Fifteen inner-window passages, with the last passage finishing on +Y.
# Tangential separation keeps the two nominal AWG26 heavy-build wires apart.
WINDING_PATHS={}
for k,col in [(0,'0.78 0.27 0.06'),(1,'0.10 0.35 0.72')]:
 path=[];offset=-.23 if k==0 else .23
 for i in range(473):
  t=i/32;phase=t%1;angle=math.radians(165-330*t/14.75)
  if phase<.25:r=11.525-(11.525-5.6)*phase*4;y=-4.15
  elif phase<.5:r=5.6;y=-4.15+8.3*(phase-.25)*4
  elif phase<.75:r=5.6+(11.525-5.6)*(phase-.5)*4;y=4.15
  else:r=11.525;y=4.15-8.3*(phase-.75)*4
  if i==472:r=11.525;y=4.15
  path.append((r*math.sin(angle)+offset*math.cos(angle),y,cz+r*math.cos(angle)-offset*math.sin(angle)))
 WINDING_PATHS['A' if k==0 else 'B']=path
 wrl.append('# Part: winding '+('A' if k==0 else 'B'));tube(path,.2235,col,sides=8)
LEAD_PATHS[1].insert(0,WINDING_PATHS['A'][0]);LEAD_PATHS[2].insert(0,WINDING_PATHS['A'][-1])
LEAD_PATHS[3].insert(0,WINDING_PATHS['B'][0]);LEAD_PATHS[4].insert(0,WINDING_PATHS['B'][-1])
# A generic insulating support, not a selected catalog component.
wrl.append('# Part: illustrative support')
ps=[(SUPPORT_RADIUS*math.cos(i*2*math.pi/N),SUPPORT_RADIUS*math.sin(i*2*math.pi/N),z) for z in [0,SUPPORT_HEIGHT] for i in range(N)];fs=[tuple(reversed(range(N))),tuple(range(N,2*N))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)];mesh(ps,fs,'0.65 0.72 0.76')
wrl.append('# Part: illustrative bedding allowance')
box(0,0,SUPPORT_HEIGHT+BEDDING_HEIGHT/2,BEDDING_X,BEDDING_Y,BEDDING_HEIGHT,'0.78 0.80 0.81')
for num,path in LEAD_PATHS.items():
 wrl.append('# Part: lead '+str(num));tube(path,.2235,'0.78 0.27 0.06' if num in [1,2] else '0.10 0.35 0.72')
(PROJECT/(LIB+'.3dshapes')/MODEL).write_text('\n'.join(wrl)+'\n')
# Conservative round-wire envelopes around the piecewise-linear illustrated paths.
# Distance to either convex support solid is convex on each segment. Minimize
# over the complete segment, including endpoints, then subtract the wire radius.
def pad_distance(p):
 dr=max(math.hypot(p[0],p[1])-SUPPORT_RADIUS,0)
 dz=max(-p[2],p[2]-SUPPORT_HEIGHT,0)
 return math.hypot(dr,dz)
def bedding_distance(p):
 return math.sqrt(max(abs(p[0])-BEDDING_X/2,0)**2+max(abs(p[1])-BEDDING_Y/2,0)**2+max(SUPPORT_HEIGHT-p[2],p[2]-CORE_BOTTOM,0)**2)
def capsule_gap(paths,distance):
 best=float('inf')
 for path in paths.values():
  for a,b in zip(path,path[1:]):
   def at(t):return distance([a[k]+t*(b[k]-a[k]) for k in range(3)])
   lo,hi=0.,1.
   for _ in range(55):
    left=(2*lo+hi)/3;right=(lo+2*hi)/3
    if at(left)<at(right):hi=right
    else:lo=left
   best=min(best,at(0),at(1),at((lo+hi)/2))
 return best-.2235
CLEARANCE=dict(winding_to_pad=capsule_gap(WINDING_PATHS,pad_distance),lead_to_pad=capsule_gap(LEAD_PATHS,pad_distance),winding_to_bedding=capsule_gap(WINDING_PATHS,bedding_distance),lead_to_bedding=capsule_gap(LEAD_PATHS,bedding_distance))
dims=dict(footprint=NAME,coordinate_convention=dict(paths="Footprint XY in mm; +Y down",native_vrml="X,-Y,Z in 0.1-inch units",front_surface_z_mm=0),core=CORE,turns_per_wire=15,winding_arc_degrees=330,wound_body_reserved_mm=[24,10,30],assembly_acceptance_max_xy_mm=[24,11.4],front_courtyard_mm=COURTYARD,physical_hole_count=3,common_drain_ends=[2,3],lead_paths_mm=LEAD_PATHS,winding_paths_mm=WINDING_PATHS,illustrated_wire_diameter_mm=.447,backside_finished_joint_max_mm=1.5,board_size_mm=[53.33,22.85],position_mm=[146.75,89.8],rotation_degrees=0,body_side_overhang_mm=0,pads=[dict(number=a,x=b,y=c,end=d,net=e,finished_hole=PAD_DIMS[a][0] if a!=3 else 0,pad_size=PAD_DIMS[a][1],physical_hole=2 if a==3 else a) for a,b,c,d,e in PADS],npth_slots=[],support=dict(selection='Builder-selected; no required MPN',illustrative_only=True,illustrated_diameter_mm=SUPPORT_DIAMETER,illustrated_height_mm=SUPPORT_HEIGHT,material_requirement='Electrically insulating; compatible with coating, PCB and operating temperature'),attachment=dict(selection='Builder-selected; no required adhesive or MPN',illustrative_only=True,bedding_allowance_mm=BEDDING_HEIGHT,illustrated_envelope_mm=[BEDDING_X,BEDDING_Y,BEDDING_HEIGHT],retention='Select and verify actual support and attachment. Maintain winding/lead clearance; winding leads are not the primary retainer.'),sources=SOURCES)
dims['nominal_clearance_mm']=CLEARANCE
(ROOT/'dimensions.json').write_text(json.dumps(dims,indent=2)+'\n')
# Four-page reference; the support is illustrative and materials are builder-selected.
OUT=ROOT/'output/pdf/t61-mounting.pdf';OUT.parent.mkdir(parents=True,exist_ok=True)
C=canvas.Canvas(str(OUT),pagesize=(612,792));C.setTitle('T61 low support and side terminals - Torroid Edition')
INK=colors.HexColor('#172b3a');BLUE=colors.HexColor('#144d71');GRAY=colors.HexColor('#52626d')
STYLE=ParagraphStyle('body',fontName='Helvetica',fontSize=9.5,leading=13,textColor=INK)
def page(i,title):
 C.setFillColor(BLUE);C.rect(0,750,612,42,fill=1,stroke=0);C.setFillColor(colors.white);C.setFont('Helvetica-Bold',10);C.drawString(36,766,'WsprryPico GPIO Shield with GPS - Torroid Edition')
 C.setFillColor(INK);C.setFont('Helvetica-Bold',18);C.drawString(36,718,title);C.setFillColor(GRAY);C.setFont('Helvetica',8);C.drawString(36,27,'2026-10-21 | Illustrative support; physical assembly and RF qualification pending');C.drawRightString(576,27,f'{i} / 4')
def para(s,y):
 p=Paragraph(s,STYLE);_,h=p.wrap(540,700);p.drawOn(C,36,y-h);return y-h-11
def table(rows,y,widths):
 t=Table(rows,colWidths=widths);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e7eff4')),('FONTNAME',(0,0),(-1,-1),'Helvetica'),('FONTSIZE',(0,0),(-1,-1),8.5),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,-1),.3,GRAY)]));_,h=t.wrap(540,700);t.drawOn(C,36,y-h);return y-h-15
page(1,'Terminals alongside the toroid')
y=para('Fair-Rite <b>5977000621 material 77, 15+15 AWG26 turns</b>. Separate ends <b>1 and 4 are on +Y</b>; <b>2 and 3 share one hole on -Y</b>. Core selection, electrical connection, board outline and terminal coordinates are unchanged. The model shows an <b>8 mm diameter, 1.25 mm high support pad</b>. Its diameter is reduced from 11 mm to clear the lower winding; the short height is retained. Mounting materials are selected by the builder.',682)
sc=16;cx=306;cy=480
C.setStrokeColor(BLUE);C.setDash(3,3);C.rect(cx-12.5*sc,cy-6.75*sc,25*sc,13.5*sc);C.setDash();C.setFillColor(colors.HexColor('#b9c2c7'));C.setStrokeColor(INK);C.rect(cx-12*sc,cy-5*sc,24*sc,10*sc,fill=1)
C.setFillColor(colors.HexColor('#e0e8eb'));C.circle(cx,cy,SUPPORT_RADIUS*sc,fill=1)
for num,x,z,_,_ in PADS:
 if num==3:continue
 C.setFillColor(colors.HexColor('#c4a35d'))
 if num==1:C.rect(cx+(x-1)*sc,cy+(-z-1)*sc,2*sc,2*sc,fill=1)
 else:C.circle(cx+x*sc,cy-z*sc,PAD_DIMS[num][1]/2*sc,fill=1)
 C.setFillColor(colors.white);C.circle(cx+x*sc,cy-z*sc,PAD_DIMS[num][0]/2*sc,fill=1);C.setFillColor(INK);C.setFont('Helvetica',9);C.drawRightString(cx+x*sc-PAD_DIMS[num][1]/2*sc-8,cy-z*sc-3,('2/3' if num==2 else str(num)))
C.setFillColor(INK);C.setFont('Helvetica',9);C.drawString(106,cy-6.75*sc-20,'Component-side plan: +X right, +Y down; dimensions mm');C.setFont('Helvetica-Bold',9);C.drawCentredString(cx,cy+6.75*sc+12,'-Y FACE: COMMON 2/3');C.drawCentredString(cx,cy-6.75*sc-36,'+Y FACE: SEPARATE 1 AND 4')
y=para('<b>Support and attachment:</b> no catalog bumper, adhesive, pack quantity or price is specified. Use an electrically insulating support and a compatible retention method chosen for the actual build. The 8 mm pad diameter, 1.25 mm pad height and 4 x 6 x 0.5 mm bedding allowance are illustrative geometry, not a required product or a guaranteed tolerance stack.',319)
y=para('<b>Board fit:</b> center (146.75,89.80) mm, rotation 0 degrees. Front courtyard 25 x 13.5 mm, within the 53.33 x 22.85 mm board. Finished assembly remains within 24 x 11.4 mm in plan and 30 mm above the board. All factory SMT stays underneath. No daughterboard, tie slots or underside straps.',y)
y=para('<b>Builder check:</b> keep winding and leads clear of the board, support and nearby parts; provide independent retention. Do not rely on soldered winding leads to retain the core. Verify the actual support thickness and winding build before committing to assembly.',y);assert y>45,y
C.showPage();page(2,'Narrower support: dimensioned elevation')
y=para('Illustrative front elevation; winding omitted to expose the support stack. The support material and any bedding or attachment method are builder-selected. Terminal XY positions and underside lead limit stay fixed.',682)
sc=13;cx=292;by=322;cz=by+(CORE_BOTTOM+10.925)*sc
C.setStrokeColor(INK);C.setLineWidth(.8);C.setFillColor(colors.HexColor('#b9c2c7'));C.circle(cx,cz,10.925*sc,fill=1);C.setFillColor(colors.white);C.circle(cx,cz,6.2*sc,fill=1)
C.setFillColor(colors.HexColor('#d8e3e7'));C.rect(cx-SUPPORT_RADIUS*sc,by,SUPPORT_DIAMETER*sc,SUPPORT_HEIGHT*sc,fill=1)
C.setFillColor(colors.HexColor('#edf1f3'));C.rect(cx-2*sc,by+SUPPORT_HEIGHT*sc,4*sc,BEDDING_HEIGHT*sc,fill=1)
C.setFillColor(colors.HexColor('#c4d4ca'));C.rect(cx-14*sc,by-1.6*sc,28*sc,1.6*sc,fill=1)
C.setFillColor(INK);C.setFont('Helvetica',9);C.drawCentredString(cx,cz+10,'21.85 OD / 12.40 ID');C.drawCentredString(cx,cz-5,'7.10 axial max');C.drawString(cx+14*sc+8,by-.8*sc-3,'PCB: 1.60')
def callout(x,y,ex,ey,text):
 C.setStrokeColor(GRAY);C.line(x,y,ex-8,ey);C.line(ex-8,ey,ex,ey);C.setFillColor(INK);C.setFont('Helvetica',9);C.drawString(ex+4,ey-3,text)
callout(cx+2*sc,by+(SUPPORT_HEIGHT+BEDDING_HEIGHT/2)*sc,446,385,'Bedding allowance: 0.50')
callout(cx+SUPPORT_RADIUS*sc,by+SUPPORT_HEIGHT/2*sc,446,357,'Pad height: 1.25')
callout(cx,by+CORE_BOTTOM*sc,446,412,'Bare core bottom: 1.75')
dy=by-1.6*sc-10
C.setStrokeColor(GRAY);C.line(cx-SUPPORT_RADIUS*sc,dy,cx+SUPPORT_RADIUS*sc,dy);C.line(cx-SUPPORT_RADIUS*sc,dy-3,cx-SUPPORT_RADIUS*sc,dy+3);C.line(cx+SUPPORT_RADIUS*sc,dy-3,cx+SUPPORT_RADIUS*sc,dy+3);C.setFillColor(INK);C.setFont('Helvetica',9);C.drawCentredString(cx,dy-13,'Pad diameter: 8.0, illustrative')
y=para('<b>Diameter change:</b> pad 11.00 to 8.00 mm; bedding plan 4 x 7.1 to 4 x 6.0 mm. Pad height stays 1.25 mm and bedding allowance stays 0.50 mm. Bare core bottom/top remain 1.75/23.60 mm. Winding, lead dressing, three solder holes and finished underside joints do not move.',261)
y=para(f'<b>Low-turn clearance:</b> conservative nominal wire-radius envelopes clear the pad by {min(CLEARANCE["winding_to_pad"],CLEARANCE["lead_to_pad"]):.2f} mm and bedding by {min(CLEARANCE["winding_to_bedding"],CLEARANCE["lead_to_bedding"]):.2f} mm. Bedding corners stay within the pad. Check actual winding variation, support compression and retention; these nominal gaps are not manufacturing tolerance guarantees.',y)
y=para('<b>Acceptance envelope:</b> remain within 24 x 11.4 mm in plan and 30 mm above the board. Keep total finished lead/solder projection below the board at or below 1.5 mm, subject to sound solder joints. The smaller illustrated stack does not reduce the permitted enclosure or assembly envelope.',y);assert y>45,y
C.showPage();page(3,'Winding ends and builder assembly')
y=table([['Pad','Local X / Y (mm)','Winding end','Net']]+[[str(a),f'{b:.2f} / {c:+.2f}',d,e] for a,b,c,d,e in PADS],682,[35,115,140,250])
for textline in [
 '<b>Wind:</b> identify starts 1/3 and finishes 2/4, twist the two wires initially 8-10 twists/inch and wind 15 window passages per wire over about 330 degrees. Leave about 30 degrees bare at the bottom. Check continuity, phase, coating and inductance before mounting.',
 '<b>Dress outside the window:</b> end 1 returns around the lower-right exterior to +Y. After the final window passage, end 2 returns around the lower-left exterior to -Y. End 3 crosses below the window on -Y, above the support, to meet 2. End 4 drops on +Y beside 1. No dressing route passes through the window again. The preview omits wire twists and is not proof of an actual winding.',
 '<b>Three holes:</b> ends 1/4 use separate 1.00 mm finished holes and 2.00 mm lands. Ends 2/3 enter one 1.20 mm finished hole and 2.40 mm land together. Pad 2 creates the barrel; logical pad 3 is coincident drill-free copper. Strip enamel completely, tin lightly and check actual wire-pair and finished-hole tolerance.',
 '<b>Mount:</b> select an insulating support and compatible attachment method. Check winding and lead clearance in the actual assembly, fixture with slack tails and complete any preparation/cure needed for the chosen materials. The winding leads are not the primary retainer. Do not add a conductive closed loop through the window.',
 '<b>Solder and inspect:</b> solder the shared 2/3 pair in one hole and 1/4 separately. Keep final underside projection at or below 1.5 mm including solder. Check the nearby C62 body and control solder spread. Confirm socket/Pico engagement, handling strength, warm operation and vibration on a sample.',
 '<b>Parts records:</b> T61 purchases the core only; T61-WIRE remains a separate wire purchase. T61-SUPPORT and T61-ADHESIVE are builder-choice reminders with no required manufacturer, MPN, supplier or quantity. They are not circuit references or factory assembly positions.'
]:y=para(textline,y)
y=para('<link href="https://fair-rite.com/product/toroids-5977000621/" color="#144d71">Core specification: Fair-Rite 5977000621</link>',y);assert y>45,y
C.showPage();page(4,'Checks and remaining acceptance')
y=para('The core, 15+15 turns, schematic and copper routing are unchanged. Nominal primary L remains 285.75 uH; AL-minimum zero-bias L remains 200.025 uH. Changing the support diameter does not establish RF, thermal or DC-biased performance.',682)
for textline in [
 '<b>CAD checks:</b> run KiCad 10.0.6 full DRC with all severities, all track errors, zone refill and schematic parity, and ERC without changing existing ignored categories. Verify exactly three T61 drills, unchanged pad coordinates/nets, unchanged copper, and 21 factory positions all on the underside.',
 '<b>3D clearance:</b> inspect the updated native model, nearby Q61/SW11/D11 bodies, sockets and antenna opening. Compare conservative capacitor and 1.5 mm finished-joint envelopes against the fitted official Pico W mechanical reference. Retain its 11.00, 10.65 and 8.30 mm board-gap scenarios and stated compatibility limits.',
 '<b>Mounting fit:</b> check actual winding, lower turns, support compression/shape, insulation, finished holes, solder fillets and retention. The low-support preview is illustrative. Its nominal dimensions and a clean CAD result do not establish a safe tolerance stack, adhesive compatibility or mechanical strength.',
 '<b>Records:</b> workbook and CSV leave mounting materials to the builder. No mandatory bumper or adhesive ordering code, pack quantity, supplier link or cost is retained. Winding wire and all electronic component selections remain unchanged.',
 '<b>Electrical acceptance:</b> measure primary inductance and impedance at 0/50/100/200/300 mA; initial target is at least 100 uH at 200 mA. Verify loss, matching, ringing, output, harmonics, stability, bias, USB droop, Pico/Wi-Fi coexistence and temperature from 135.7 kHz through 29.7 MHz with the real amplifier, external LPF and 50-ohm load. 300 mA is a screening point, not an approved continuous BS170 current.'
]:y=para(textline,y)
assert y>45,y
C.save();print(json.dumps(dict(footprint=str(fp_path),model=MODEL,drawing=str(OUT),support_height=SUPPORT_HEIGHT,bedding_allowance=BEDDING_HEIGHT,core_bottom=CORE_BOTTOM,physical_hole_count=3),indent=2))
