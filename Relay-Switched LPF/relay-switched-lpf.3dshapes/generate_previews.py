#!/usr/bin/env python3
"""Original nominal relay, SMA, and wire previews, licensed MIT.

Coordinates below are millimetres, converted to KiCad's 0.1-inch VRML units.
These are visible mechanical envelopes, not manufacturer CAD or fit approval.
"""
from pathlib import Path
import math

ROOT=Path(__file__).resolve().parent
METAL=(.68,.69,.72);GOLD=(.72,.56,.2);BLACK=(.055,.065,.08);WHITE=(.9,.88,.8)
def v(values):return ' '.join(f'{x/2.54:.7f}' for x in values)
def appearance(color):return 'appearance Appearance { material Material { diffuseColor '+' '.join(map(str,color))+' specularColor .25 .25 .25 shininess .4 } }'
def box(center,size,color):
    return f'Transform {{ translation {v(center)} children [ Shape {{ {appearance(color)} geometry Box {{ size {v(size)} }} }} ] }}\n'
def cylinder(center,radius,height,color,axis='z'):
    direction={'x':(1,0,0),'y':(0,1,0),'z':(0,0,1)}[axis]
    a=[center[i]-height*direction[i]/2 for i in range(3)]
    b=[center[i]+height*direction[i]/2 for i in range(3)]
    return rod(a,b,radius,color)
def rod(a,b,radius,color):
    d=[b[i]-a[i] for i in range(3)];length=math.sqrt(sum(x*x for x in d))
    unit=[x/length for x in d]
    helper=(0,0,1) if abs(unit[2])<.9 else (0,1,0)
    def cross(x,y):return (x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0])
    u=cross(helper,unit);norm=math.sqrt(sum(x*x for x in u));u=[x/norm for x in u];w=cross(unit,u)
    count=32;points=[]
    for endpoint in [a,b]:
        for j in range(count):
            t=2*math.pi*j/count
            points.append([endpoint[i]+radius*(math.cos(t)*u[i]+math.sin(t)*w[i]) for i in range(3)])
    points.extend([a,b]);faces=[]
    for j in range(count):
        k=(j+1)%count
        faces.extend([(j,k,k+count,j+count),(2*count,k,j),(2*count+1,j+count,k+count)])
    coords=',\n'.join(v(point) for point in points)
    indices=',\n'.join(' '.join(map(str,face))+' -1' for face in faces)
    return f'Shape {{ {appearance(color)} geometry IndexedFaceSet {{ solid TRUE creaseAngle .7 coord Coordinate {{ point [ {coords} ] }} coordIndex [ {indices} ] }} }}\n'
def save(name,body):
    (ROOT/name).write_text('#VRML V2.0 utf8\n# Copyright 2026 WsprryPi contributors. MIT license.\n# Original nominal preview; not qualified manufacturer geometry.\n'+body)

relay=box((0,0,4.25),(7.4,15,7.9),BLACK)
relay+=box((0,6.2,8.23),(5.8,.7,.06),(.72,.74,.77))
for x in [-2.54,2.54]:
    for y in [-5.08,0,2.54,5.08]:relay+=box((x,-y,-1.35),(.5,.25,4.1),METAL)
save('TX2_5V_Nominal.wrl',relay)

vertical=cylinder((0,0,3.8),3.0,7.0,GOLD)
vertical+=cylinder((0,0,7.35),2.65,.6,GOLD)
vertical+=cylinder((0,0,7.68),2.05,.08,WHITE)
vertical+=cylinder((0,0,7.74),.4,.12,METAL)
for x in [-2.54,2.54]:
    for y in [-2.54,2.54]:vertical+=box((x,y,-1.3),(.65,.65,3.2),GOLD)
vertical+=cylinder((0,0,-1.3),.4,3.2,METAL)
save('SMA_Vertical_Generic_Preview.wrl',vertical)

edge=box((1.5,0,-.8),(1,6.4,6.0),GOLD)
edge+=cylinder((5.5,0,-.8),3.0,7.0,GOLD,'x')
edge+=cylinder((9.05,0,-.8),2.2,.1,WHITE,'x')
edge+=cylinder((9.13,0,-.8),.4,.15,METAL,'x')
for y in [-3,0,3]:
    for z in [.1,-1.7]:edge+=box((-1,y,z),(4,1,.2),GOLD)
save('SMA_Edge_Generic_Preview.wrl',edge)

points=[(0,0,-1.2),(0,0,.5),(0,-.4,.9),(0,-2.14,.9),(0,-2.54,.5),(0,-2.54,-1.2)]
wire=''.join(rod(a,b,.175,METAL) for a,b in zip(points,points[1:]))
save('Wire_Link_P2.54mm.wrl',wire)
print('Generated four original nominal VRML models.')
