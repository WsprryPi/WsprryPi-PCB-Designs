"""Select rounded parts, rank tolerance corners, and size per-band drive range."""
from pathlib import Path
import sys,json,itertools
import numpy as np
import ths3491_optimized_filters as m
p=Path(__file__).resolve().parents[1];g=p/'generated/ths3491-optimized';rows=[];plans=[]
def transfer(r,signs,hot=1,db=.2):
 f=r['f_Hz'];ip=r['input'];op=r['output'];mi=[1+s*x['tol'] for s,x in zip(signs[:5],ip)];mo=[1+s*x['tol'] for s,x in zip(signs[5:12],op)];cout=1+signs[12]*.05
 A=m.matrix(ip,f,mi,hot)@m.pad_matrix(db);hin=1/(A[0,0]+A[0,1]/50+7*(A[1,0]+A[1,1]/50));z,h=m.response(op,f,db,mo,hot);zs=1.245+m.impedance(m.COUT,f,cout,hot);vload=h*z/(z+zs);pi=abs(hin*5*vload)**2/100
 return pi,abs(z+zs),mo,mi,cout
# 13 components: five input, seven output, and the coupling-capacitor pair.
signs=list(itertools.product([-1,1],repeat=13))
for f in m.FREQS:
 r=m.select(f);rows.append(r);nom=transfer(r,[0]*13);corners=[transfer(r,s)[:2] for s in signs];lo=min(range(len(corners)),key=lambda i:corners[i][0]);hi=max(range(len(corners)),key=lambda i:corners[i][0]);vol=max(range(len(corners)),key=lambda i:corners[i][1]);scenarios=[]
 for label,idx in [('min_power',lo),('max_power',hi),('max_required_voltage',vol)]:
  ss=signs[idx];v=transfer(r,ss);scenarios.append({'label':label,'multipliers':v[3]+v[2]+[v[4]],'power_factor':v[0]/nom[0],'output_impedance_magnitude_ohms':v[1]})
 # Starting drive estimate from 5V square fundamental and a 7-ohm source.
 alpha=float(np.sqrt(.60/(nom[0]*(10/np.pi)**2)));plans.append({'f_Hz':f,'alpha_estimate':alpha,'nominal_W_per_source_Vpeak2_alpha2':nom[0],'corners':scenarios,'corner_count':len(signs)})
 print(f/1e6,'alpha',round(alpha,3),'corner min/max',round(min(x[0] for x in corners)/nom[0],3),round(max(x[0] for x in corners)/nom[0],3),flush=True)
(p/'docs/ths3491-optimized-parts.json').write_text(json.dumps(rows,indent=2)+'\n');(g/'assessment.json').write_text(json.dumps(plans,indent=2)+'\n')
