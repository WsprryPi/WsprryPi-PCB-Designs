#!/usr/bin/env python3
"""Route the reconstructed carrier on two copper layers; not an RF optimizer.

Run only after generate.py, with KiCad's Python. CAD DRC and RF qualification
remain separate checks. Local ground/output-return planes are filled last.
"""
from pathlib import Path
import heapq
import math
import numpy as np
import pcbnew as p
import wx
APP=wx.App(False)
ROOT=Path(__file__).resolve().parents[1]
FILE=ROOT/'Relay-Switched LPF.kicad_pcb'
b=p.LoadBoard(str(FILE))
if len(b.GetTracks()):
    raise SystemExit('Run generate.py first; routing over existing tracks is intentionally refused.')
step=.1
nx,ny=801,371
grid=np.zeros((2,ny,nx),dtype=np.int16)
via_block=np.zeros((ny,nx),dtype=bool)
def block_via(x,y,r):
    x0=max(0,int(x-r)-1); x1=min(nx,int(x+r)+2)
    y0=max(0,int(y-r)-1); y1=min(ny,int(y+r)+2)
    yy,xx=np.ogrid[y0:y1,x0:x1]
    via_block[y0:y1,x0:x1] |= (xx-x)**2+(yy-y)**2<=r*r
def xy(pos): return ((p.ToMM(pos.x)-50)/step,(p.ToMM(pos.y)-50)/step)
def node(pos):
    x,y=xy(pos); return (round(x),round(y))
def mark(x,y,rx,ry,net,layers=(0,1),rect=False):
    x0=max(0,int(x-rx)-1); x1=min(nx,int(x+rx)+2)
    y0=max(0,int(y-ry)-1); y1=min(ny,int(y+ry)+2)
    yy,xx=np.ogrid[y0:y1,x0:x1]
    mask=(abs(xx-x)<=rx)&(abs(yy-y)<=ry) if rect else ((xx-x)/rx)**2+((yy-y)/ry)**2<=1
    for z in layers:
        sub=grid[z,y0:y1,x0:x1]
        # Shared clearance areas remain unavailable to either of their owners.
        overlap=mask&(sub!=0)&(sub!=net)
        sub[mask]=net; sub[overlap]=-1

# Keep copper at least 0.25 mm from the outline (track half width included).
edge=7
grid[:,:edge,:]=-1; grid[:,-edge:,:]=-1; grid[:,:,:edge]=-1; grid[:,:,-edge:]=-1
pads={}
for fp in b.GetFootprints():
    for pd in fp.Pads():
        x,y=xy(pd.GetPosition()); code=pd.GetNetCode()
        size=pd.GetSize(); sx,sy=p.ToMM(size.x)/2,p.ToMM(size.y)/2
        drill=p.ToMM(pd.GetDrillSize().x)
        if drill: block_via(x,y,(drill/2+.15+.25+.03)/step)
        # All selected THT pads are square or circular; edge SMA pads are rectangular.
        rect=pd.GetShape()==p.PAD_SHAPE_RECT
        orientation=round(pd.GetOrientationDegrees())%180
        if orientation==90: sx,sy=sy,sx
        for z,layer in enumerate([p.F_Cu,p.B_Cu]):
            if pd.IsOnLayer(layer): mark(x,y,(sx+.44)/step,(sy+.44)/step,code if code else -1,(z,),rect)
        if code:
            # The exact center can be closer than the conservative clearance raster.
            pads.setdefault(code,[]).append((pd,node(pd.GetPosition())))

# Reserve the X2 layer transitions before routing other nets around them.
# Repeated same-number surface pads on opposite sides are not plated holes.
x2=next(fp for fp in b.GetFootprints() if fp.GetReference()=='X2')
rfpad=next(pd for pd in x2.Pads() if pd.GetNumber()=='1')
gp=min((pd for pd in x2.Pads() if pd.GetNumber()=='2'),key=lambda pd:pd.GetPosition().y)
cx,cy=p.ToMM(rfpad.GetPosition().x),p.ToMM(rfpad.GetPosition().y)
for vx,vy,tx,ty,net in [
    (cx-2.5,cy,cx,cy,rfpad.GetNetCode()),
    (cx+.5,cy-1.5,cx+.5,p.ToMM(gp.GetPosition().y),gp.GetNetCode()),
]:
    at=p.VECTOR2I(p.FromMM(vx),p.FromMM(vy))
    v=p.PCB_VIA(b);v.SetPosition(at);v.SetWidth(p.FromMM(.65));v.SetDrill(p.FromMM(.3))
    v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNetCode(net);b.Add(v)
    gx,gy=xy(at);mark(gx,gy,.825/step,.825/step,net);block_via(gx,gy,.58/step)
    end=p.VECTOR2I(p.FromMM(tx),p.FromMM(ty))
    for z,layer in enumerate([p.F_Cu,p.B_Cu]):
        t=p.PCB_TRACK(b);t.SetStart(at);t.SetEnd(end);t.SetWidth(p.FromMM(.3));t.SetLayer(layer);t.SetNetCode(net);b.Add(t)
        a=xy(at);bb=xy(end);steps=max(1,math.ceil(math.dist(a,bb)*2))
        for i in range(steps+1):
            frac=i/steps
            mark(a[0]+frac*(bb[0]-a[0]),a[1]+frac*(bb[1]-a[1]),.59/step,.59/step,net,(z,))

def free(x,y,z,net):
    return edge<=x<nx-edge and edge<=y<ny-edge and grid[z,y,x] in (0,net)
def viafree(x,y,net):
    if x<9 or x>=nx-9 or y<9 or y>=ny-9: return False
    if via_block[y,x]: return False
    for z in [0,1]:
        sub=grid[z,y-2:y+3,x-2:x+3]
        if np.any((sub!=0)&(sub!=net)): return False
    return True
dirs=[(1,0,1),(-1,0,1),(0,1,1),(0,-1,1),(1,1,1.414),(1,-1,1.414),(-1,1,1.414),(-1,-1,1.414)]
def astar(start,end,net,slayers,elayers):
    ex,ey=end
    def heuristic(x,y):
        dx,dy=abs(x-ex),abs(y-ey)
        return max(dx,dy)+.414*min(dx,dy)
    heap=[]; dist={}; parent={}
    for z in slayers:
        key=(start[0],start[1],z); dist[key]=0; heapq.heappush(heap,(heuristic(*start),0,key))
    count=0
    while heap:
        _,cost,key=heapq.heappop(heap)
        if cost!=dist.get(key): continue
        x,y,z=key
        if (x,y)==end and z in elayers:
            result=[key]
            while key in parent: key=parent[key]; result.append(key)
            return result[::-1]
        count+=1
        if count>800000: break
        for dx,dy,w in dirs:
            xx,yy=x+dx,y+dy
            if not free(xx,yy,z,net): continue
            if dx and dy and (not free(xx,y,z,net) or not free(x,yy,z,net)): continue
            # Gentle layer preference reduces needless crossings.
            cc=cost+w+(0.03 if (z==0 and dy) or (z==1 and dx) else 0)
            kk=(xx,yy,z)
            if cc<dist.get(kk,1e20):
                dist[kk]=cc; parent[kk]=key; heapq.heappush(heap,(cc+heuristic(xx,yy),cc,kk))
        if viafree(x,y,net):
            kk=(x,y,1-z); cc=cost+30
            if cc<dist.get(kk,1e20):
                dist[kk]=cc; parent[kk]=key; heapq.heappush(heap,(cc+heuristic(x,y),cc,kk))
    return None

def pos(node): return p.VECTOR2I(p.FromMM(50+node[0]*step),p.FromMM(50+node[1]*step))
def track(a,bb,z,net):
    if a==bb:return
    t=p.PCB_TRACK(b); t.SetStart(a); t.SetEnd(bb); t.SetWidth(p.FromMM(.3)); t.SetLayer(p.F_Cu if z==0 else p.B_Cu); t.SetNetCode(net); b.Add(t)
def layers(pd): return [z for z,layer in enumerate([p.F_Cu,p.B_Cu]) if pd.IsOnLayer(layer)]
fail=[]; total=0
# Short local signal nets first, control supply busses next, ground last.
def priority(n):
    name=b.FindNet(n).GetNetname().lstrip('/')
    band_priority=-int(name[4]) if name.startswith('BAND') else 0
    return (name in ['GND','GND_OUT'],name not in ['RELAY_VPLUS','+5V'],not name.startswith('BAND'),band_priority,len(pads[n])>7,len(pads[n]),name)
order=sorted(pads,key=priority)
for net in order:
    entries=pads[net]
    todo=set(range(1,len(entries))); tree={0}
    while todo:
        _,a,bb=min((math.dist(entries[a][1],entries[bb][1]),a,bb) for a in tree for bb in todo)
        pa,st=entries[a]; pb,en=entries[bb]
        # Recover exact same-net pad interiors after conservative raster overlaps.
        for pd,pt in [(pa,st),(pb,en)]:
            xx,yy=pt
            for z in layers(pd): grid[z,yy,xx]=net
        path=astar(st,en,net,layers(pa),layers(pb))
        if path is None:
            fail.append((b.FindNet(net).GetNetname(),pa.GetParentFootprint().GetReference()+'.'+pa.GetNumber(),pb.GetParentFootprint().GetReference()+'.'+pb.GetNumber()))
            todo.remove(bb); tree.add(bb); continue
        total+=1
        track(pa.GetPosition(),pos(path[0]),path[0][2],net)
        track(pos(path[-1]),pb.GetPosition(),path[-1][2],net)
        # Compress adjacent collinear grid steps to native CAD segments.
        begin=path[0]; previous=path[0]; direction=None
        for point in path[1:]:
            x,y,z=point; px,py,pz=previous
            if z!=pz:
                track(pos(begin),pos(previous),pz,net)
                v=p.PCB_VIA(b); v.SetPosition(pos(point)); v.SetWidth(p.FromMM(.65)); v.SetDrill(p.FromMM(.3)); v.SetViaType(p.VIATYPE_THROUGH); v.SetLayerPair(p.F_Cu,p.B_Cu); v.SetNetCode(net); b.Add(v)
                block_via(x,y,.58/step)
                mark(x,y,.825/step,.825/step,net)
                begin=point; direction=None
            else:
                d=(x-px,y-py)
                if direction is not None and d!=direction:
                    track(pos(begin),pos(previous),z,net); begin=previous
                direction=d
                # Track raster includes clearance, next track radius, and rounding guard.
                mark(x,y,.59/step,.59/step,net,(z,))
            previous=point
        track(pos(begin),pos(previous),previous[2],net)
        todo.remove(bb); tree.add(bb)
    print(b.FindNet(net).GetNetname(),len(entries),'pads',flush=True)
b.BuildConnectivity()
p.ZONE_FILLER(b).Fill(b.Zones())
p.SaveBoard(str(FILE),b)
print('Routed connections:',total,'; failed:',fail,flush=True)
