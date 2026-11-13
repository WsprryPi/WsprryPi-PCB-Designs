#!/usr/bin/env python3
"""Apply local 3D assets, populated wire-link variants, and R3 board corners.

Run with KiCad 10's Python in the logged-in graphics session. Preserves copper,
pin assignments, component placement, shared fields, and design-rule settings.
"""
from pathlib import Path
import hashlib
import json
import math
import re
import subprocess
import sys
import pcbnew as p
import wx

APP=wx.App(False)
ROOT=Path(__file__).resolve().parents[1]
NAME='Relay-Switched LPF';LIB='relay-switched-lpf'
PRETTY=ROOT/(LIB+'.pretty');MODELS=ROOT/(LIB+'.3dshapes')
BOARD=ROOT/(NAME+'.kicad_pcb')
project_path=ROOT/(NAME+'.kicad_pro')
project_settings=json.loads(project_path.read_text())
# Match the documented 25 mil connection grid of the compact Letter schematic.
project_settings.setdefault('schematic',{})['connection_grid_size']=25.0
project_bytes=(json.dumps(project_settings,indent=2)+'\n').encode()
MODELS.mkdir(exist_ok=True)
subprocess.run([sys.executable,str(MODELS/'generate_previews.py')],check=True)
imports={
    'D_DO-35_SOD27_P7.62mm_Horizontal.step':'Diode_THT.3dshapes',
    'PinSocket_1x04_P2.54mm_Vertical.step':'Connector_PinSocket_2.54mm.3dshapes',
    'PinSocket_2x05_P2.54mm_Vertical.step':'Connector_PinSocket_2.54mm.3dshapes',
}
manifest_path=MODELS/'sources.json'
manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
for name,folder in imports.items():
    target=MODELS/name
    if not target.exists():raise FileNotFoundError(f'Restore bundled local model {name}; see KICAD-LIBRARY-LICENSE.md')
    digest=hashlib.sha256(target.read_bytes()).hexdigest()
    if name in manifest:assert digest==manifest[name]['sha256'],f'Local model differs from recorded source: {name}'
    else:manifest[name]={'source':folder+'/'+name,'kicad_version':'10.0.6','sha256':digest}
manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
models={
    'TX2_5V':'TX2_5V_Nominal.wrl',
    'D_DO35_P7.62':'D_DO-35_SOD27_P7.62mm_Horizontal.step',
    'Socket_1x4':'PinSocket_1x04_P2.54mm_Vertical.step',
    'Host_2x05':'PinSocket_2x05_P2.54mm_Vertical.step',
    'SMA_Vertical_Generic':'SMA_Vertical_Generic_Preview.wrl',
    'SMA_Edge_Generic':'SMA_Edge_Generic_Preview.wrl',
    'Wire_1x2_Link12':'Wire_Link_P2.54mm.wrl',
    'Wire_1x3_Link12':'Wire_Link_P2.54mm.wrl',
}
for variant,base in [('Wire_1x2_Link12','Wire_1x2'),('Wire_1x3_Link12','Wire_1x3')]:
    if not (PRETTY/(variant+'.kicad_mod')).exists():
        text=(PRETTY/(base+'.kicad_mod')).read_text()
        text=text.replace('(footprint "'+base+'"','(footprint "'+variant+'"',1)
        (PRETTY/(variant+'.kicad_mod')).write_text(text)
mount=PRETTY/'MountingHole_3.2mm.kicad_mod'
if not mount.exists():
    mount.write_text('''(footprint "MountingHole_3.2mm" (version 20260206) (generator "pcbnew") (layer "F.Cu")
      (descr "Original project-local 3.2 mm non-plated mounting hole; no selected hardware")
      (attr board_only exclude_from_pos_files exclude_from_bom)
      (property "Reference" "H**" (at 0 0) (layer "F.SilkS") (hide yes) (effects (font (size 1.27 1.27))))
      (property "Value" "Mount 3.2 mm (inferred)" (at 0 0) (layer "F.Fab") (hide yes) (effects (font (size 1.27 1.27))))
      (pad "" np_thru_hole circle (at 0 0) (size 3.2 3.2) (drill 3.2) (layers "*.Cu" "*.Mask")))\n''')
def attach(fp,name):
    fp.Models().clear()
    if name in models:
        model=p.FP_3DMODEL();model.m_Filename='${KIPRJMOD}/'+LIB+'.3dshapes/'+models[name]
        model.m_Scale=p.VECTOR3D(1,1,1);model.m_Rotation=p.VECTOR3D(0,0,0);model.m_Offset=p.VECTOR3D(0,0,0);model.m_Show=True
        fp.Add3DModel(model)
for name in models:
    fp=p.FootprintLoad(str(PRETTY),name)
    attach(fp,name);fp.SetFPID(p.LIB_ID(LIB,name))
    p.FootprintSave(str(PRETTY),fp)

b=p.LoadBoard(str(BOARD))
fitted={'W1','W3','W4','W5','W6','W7'}
symbol_values={}

# Wire-link variants have identical pads and describe the default population.
# Update only the corresponding footprint field, leaving schematic layout intact.
def replace_symbols(text):
    edits=[];depth=0;quoted=False;escaped=False;start=None
    for i,c in enumerate(text):
        if quoted:
            if escaped:escaped=False
            elif c=='\\':escaped=True
            elif c=='"':quoted=False
            continue
        if c=='"':quoted=True
        elif c=='(':
            if depth==1 and text.startswith('(symbol',i) and text[i+7] in ' \n\t':start=i
            depth+=1
        elif c==')':
            depth-=1
            if depth==1 and start is not None:
                record=text[start:i+1];match=re.search(r'\(property "Reference" "([^"]+)"',record)
                value=re.search(r'\(property "Value" ("(?:\\.|[^"\\])*")',record)
                if match and value:symbol_values[match[1]]=json.loads(value[1])
                if match and match[1] in fitted:
                    name='Wire_1x2_Link12' if match[1]=='W1' else 'Wire_1x3_Link12'
                    record=re.sub(r'(\(property "Footprint" ")[^"]*(")',lambda m:m[1]+LIB+':'+name+m[2],record,count=1)
                    edits.append((start,i+1,record))
                start=None
    for a,z,record in reversed(edits):text=text[:a]+record+text[z:]
    return text
sch=ROOT/(NAME+'.kicad_sch');sch.write_text(replace_symbols(sch.read_text()))
for fp in b.GetFootprints():
    ref=fp.GetReference();name=str(fp.GetFPID().GetLibItemName())
    if ref.startswith('H'):name='MountingHole_3.2mm'
    elif ref in fitted:name='Wire_1x2_Link12' if ref=='W1' else 'Wire_1x3_Link12'
    fp.SetFPID(p.LIB_ID(LIB,name));attach(fp,name)
    if ref in symbol_values and fp.GetValue()!=symbol_values[ref]:fp.SetValue(symbol_values[ref])

# Shorten the four original edges and join them with true tangent R3 arcs.
edges=[item for item in b.GetDrawings() if item.GetLayer()==p.Edge_Cuts]
lines=[item for item in edges if item.GetShape()==p.SHAPE_T_SEGMENT]
assert len(lines)==4,'Expected the four existing straight outline edges'
def vec(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
for line in lines:
    a,c=line.GetStart(),line.GetEnd()
    if a.y==c.y:
        y=p.ToMM(a.y);line.SetStart(vec(53,y));line.SetEnd(vec(127,y))
    elif a.x==c.x:
        x=p.ToMM(a.x);line.SetStart(vec(x,53));line.SetEnd(vec(x,84))
    else:raise ValueError('Outline is not rectangular')
if not any(item.GetShape()==p.SHAPE_T_ARC for item in edges):
    d=3/math.sqrt(2)
    for idx,(a,m,c) in enumerate([
        ((127,50),(127+d,53-d),(130,53)),
        ((130,84),(127+d,84+d),(127,87)),
        ((53,87),(53-d,84+d),(50,84)),
        ((50,53),(53-d,53-d),(53,50)),
    ]):
        arc=p.PCB_SHAPE();arc.SetShape(p.SHAPE_T_ARC);arc.SetArcGeometry(vec(*a),vec(*m),vec(*c))
        arc.SetLayer(p.Edge_Cuts);arc.SetWidth(p.FromMM(.05))
        b.Add(arc)
b.BuildConnectivity();p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(BOARD),b)
# Keep user project fields/settings, which the drawing-only operation does not own.
project_path.write_bytes(project_bytes)
print('Applied R3 fillets, localized all footprints, and assigned project-local model assets.')
