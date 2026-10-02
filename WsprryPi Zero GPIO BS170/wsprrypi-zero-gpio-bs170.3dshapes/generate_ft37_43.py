"""Generate an illustrative upright 25-turn FT37-43 VRML model.

Repository MIT license. Dimensions from https://www.amidoncorp.com/ft-37-43/.
No third-party mesh. Run with Python 3; output is adjacent to this script.
VRML coordinates use KiCad's 2.54 mm unit and Z-up board coordinates. Not an MCAD STEP solid.
"""
from pathlib import Path
from math import sin, cos, pi, sqrt

OUTER, INNER, THICKNESS, WIRE = 9.525, 4.7498, 3.175, 0.32
TURNS, PITCH, GAP = 25, 5.08, 0.5
RO, RI, H, WR = OUTER/2, INNER/2, THICKNESS/2, WIRE/2
ZC = RO + WIRE + GAP
YC = -PITCH/2

def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def mul(a,k): return tuple(x*k for x in a)
def cross(a,b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def unit(a): return mul(a,1/sqrt(sum(x*x for x in a)))
def shape(points,faces,color):
    vertices=',\n'.join(' '.join(f'{v/2.54:.7f}' for v in p) for p in points)
    indices=',\n'.join(' '.join(map(str,f))+ ' -1' for f in faces)
    return f'Shape {{ appearance Appearance {{ material Material {{ diffuseColor {color} specularColor 0.25 0.25 0.25 shininess 0.4 }} }} geometry IndexedFaceSet {{ solid FALSE creaseAngle 0.6 coord Coordinate {{ point [\n{vertices}\n] }} coordIndex [\n{indices}\n] }} }}\n'

# Four surfaces of an annular cylindrical ferrite core, axis along Y.
points=[]
N=128
for r,y in [(RO,-H),(RO,H),(RI,-H),(RI,H)]:
    for i in range(N):
        a=2*pi*i/N;points.append((r*cos(a),YC+y,ZC+r*sin(a)))
faces=[]
for a,b in [(0,1),(2,3),(0,2),(1,3)]:
    for i in range(N):
        j=(i+1)%N
        face=(a*N+i,a*N+j,b*N+j,b*N+i)
        if (a,b) in [(0,1),(1,3)]: face=tuple(reversed(face))
        faces.append(face)
parts=[shape(points,faces,'0.11 0.12 0.13')]

# Rounded rectangular winding path clears the four core cross-section corners.
# Each pass through the center advances one of the 25 turns around the core.
A=(RO-RI)/2; B=H; R=(RO+RI)/2
corners=[(A,B,0),( -A,B,pi/2),(-A,-B,pi),(A,-B,3*pi/2)]
segments=[]
for i,(x,y,a) in enumerate(corners):
    arc=[(x+WR*cos(a+pi*j/32),y+WR*sin(a+pi*j/32)) for j in range(17)]
    segments.extend(arc)
    nx,ny,na=corners[(i+1)%4]
    end=(nx+WR*cos(na),ny+WR*sin(na))
    start=arc[-1]
    for j in range(1,17): segments.append((start[0]+(end[0]-start[0])*j/16,start[1]+(end[1]-start[1])*j/16))
lengths=[0.0]
for i in range(1,len(segments)):
    d=sub(segments[i],segments[i-1]);lengths.append(lengths[-1]+sqrt(sum(x*x for x in d)))
from bisect import bisect_right

def section(f):
    d=(f%1)*lengths[-1];i=min(bisect_right(lengths,d)-1,len(segments)-2)
    q=(d-lengths[i])/(lengths[i+1]-lengths[i]);return add(segments[i],mul(sub(segments[i+1],segments[i]),q))
path=[]
for i in range(TURNS*128+1):
    t=i/(TURNS*128);rad,y=section(t*TURNS)
    a=-pi/2+0.10+(2*pi-0.20)*t
    path.append(((R+rad)*cos(a),YC+y,ZC+(R+rad)*sin(a)))
# Illustrative hand-formed leads connect winding ends to the two existing pads.
path=[(0,0,-2.2),(0,0,0.2),path[0]]+path[1:-1]+[path[-1],(0,-PITCH,0.2),(0,-PITCH,-2.2)]
points=[];faces=[];M=10
for i,p in enumerate(path):
    tangent=unit(sub(path[min(i+1,len(path)-1)],path[max(i-1,0)]))
    reference=(0,0,1) if abs(tangent[2])<0.9 else (1,0,0)
    n=unit(cross(tangent,reference));b=cross(tangent,n)
    for j in range(M):
        a=2*pi*j/M;points.append(add(p,mul(add(mul(n,cos(a)),mul(b,sin(a))),WR)))
for i in range(len(path)-1):
    for j in range(M):faces.append((i*M+j,i*M+(j+1)%M,(i+1)*M+(j+1)%M,(i+1)*M+j))
faces.extend([tuple(reversed(range(M))),tuple((len(path)-1)*M+j for j in range(M))])
parts.append(shape(points,faces,'0.65 0.27 0.075'))
f=Path(__file__).with_name('FT37-43_25T_Upright.wrl')
f.write_text('#VRML V2.0 utf8\n# Original illustrative model; repository MIT license.\n'+''.join(parts))
print(f)
