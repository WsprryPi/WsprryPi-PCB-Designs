from pathlib import Path
import math
p=Path(__file__).resolve().parent
def shape(pts,faces,c):
 return 'Shape { appearance Appearance { material Material { diffuseColor '+c+' specularColor 0.25 0.25 0.25 shininess 0.4 } } geometry IndexedFaceSet { solid FALSE creaseAngle 0.6 coord Coordinate { point [\n'+',\n'.join(' '.join(f'{x/2.54:.7f}' for x in v) for v in pts)+'\n] } coordIndex [\n'+',\n'.join(' '.join(map(str,f))+' -1' for f in faces)+'\n] } }\n'
def box(x,y,z,a,b,c,col):
 pts=[(x+i*a/2,y+j*b/2,z+k*c/2) for i in [-1,1] for j in [-1,1] for k in [-1,1]];fs=[[0,1,3,2],[4,6,7,5],[0,4,5,1],[2,3,7,6],[0,2,6,4],[1,5,7,3]];return shape(pts,[(f[0],f[i],f[i+1]) for f in fs for i in [1,2]],col)
def cyl(x,y,z,r,h,col,axis):
 pts=[]
 for u in [-h/2,h/2]:
  for i in range(64):
   a=r*math.cos(i*math.tau/64);b=r*math.sin(i*math.tau/64);pts.append((x+a,y+b,z+u) if axis=='z' else (x+a,y+u,z+b))
 pts.extend([(x,y,z-h/2),(x,y,z+h/2)] if axis=='z' else [(x,y-h/2,z),(x,y+h/2,z)])
 fs=[]
 for i in range(64):
  j=(i+1)%64;fs += [(128,j,i),(129,i+64,j+64),(i,j,j+64),(i,j+64,i+64)]
 return shape(pts,fs,col)
h='#VRML V2.0 utf8\n# Original illustrative model; repository MIT license.\n'
s=h+box(-.1,0,.75,3.8,3,1.3,'0.15 0.17 0.2')+cyl(0,0,1.45,1.45,.25,'0.8 0.8 0.75','z')+box(0,0,1.59,1.8,.3,.03,'0.15 0.15 0.15')
for x,y in [(-1.8,1),(-1.8,-1),(1.45,0)]:s+=box(x,y,.1,1,1,.2,'0.7 0.7 0.7')
(p/'TC33X_Preview.wrl').write_text(s)
s=h+box(0,-.9,1.45,6.5,1.8,4.5,'0.75 0.65 0.32')+cyl(0,-5.65,1.45,3.05,7.7,'0.75 0.65 0.32','y')+cyl(0,-9.51,1.45,2.2,.03,'0.88 0.88 0.78','y')+cyl(0,-9.54,1.45,.55,.03,'0.12 0.12 0.12','y')
for x in [-2.75,2.75]:
 for z in [.15,-1.75]:s+=box(x,1.95,z,1,3.9,.3,'0.75 0.65 0.32')
s+=box(0,1.95,.15,.8,3.9,.3,'0.75 0.65 0.32');(p/'SMA_Adafruit_1865_Preview.wrl').write_text(s)
