"""Independent complex-impedance check and all 128 +/-5% output-filter corners."""
from pathlib import Path
import argparse, ast, json, itertools, sys
ap=argparse.ArgumentParser();ap.add_argument('--research',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();sys.path.insert(0,str(a.research/'python-packages'))
import numpy as np
script=Path(__file__).with_name('simulate_ths3491_matching.py');tree=ast.parse(script.read_text());scope={'np':np};exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='matching_values'],type_ignores=[]),str(script),'exec'),scope);values=scope['matching_values']
def network(f,tol,real=True):
 w=2*np.pi*f;M=np.eye(2,dtype=complex)
 for j,x in enumerate(np.array(values(f))*tol):
  if j%2==0:
   cp=min(2e-12,1/((7.5*w)**2*x)) if real else 0
   z=(w*x/50 if real else 0)+1/(1/(1j*w*x)+1j*w*cp)
   M=M@np.array([[1,z],[0,1]])
  else:
   y=1/(1/(1j*w*x)+(1j*w*.3e-9 if real else 0))+(w*x/1000 if real else 0)
   M=M@np.array([[1,0],[y,1]])
 if real:
  K=10**(.5/20);rp=50*(K+1)/(K-1);rs=50*(K*K-1)/(2*K)
  M=M@np.array([[1,0],[1/rp,1]])@np.array([[1,rs],[0,1]])@np.array([[1,0],[1/rp,1]])
 zin=(M[0,0]*50+M[0,1])/(M[1,0]*50+M[1,1]);h=1/(M[0,0]+M[0,1]/50)
 # Include output coupling and isolation; 1-V peak ideal PA voltage.
 zseries=2.49+.03+1/(1j*w*1e-6)+1j*w*.5e-9 if real else 0
 ip=1/(zin+zseries);vload=h*zin*ip;P=abs(vload)**2/100
 return {'Zin_real_ohms':zin.real,'Zin_imag_ohms':zin.imag,'load_W_per_Vpeak_squared':P,'current_A_per_Vpeak':abs(ip),'filter_efficiency':(abs(h)**2/50)/(1/zin).real}
rows=[];cases=[]
for f in [137e3,145e6]:
 ideal=network(f,[1]*7,False);assert abs(ideal['Zin_real_ohms']-25)<1e-10 and abs(ideal['Zin_imag_ohms'])<1e-10
 corners=[dict(network(f,t),multipliers=list(t)) for t in itertools.product([.95,1.05],repeat=7)]
 lo=min(corners,key=lambda x:x['load_W_per_Vpeak_squared']);hi=max(corners,key=lambda x:x['load_W_per_Vpeak_squared']);hot=max(corners,key=lambda x:x['current_A_per_Vpeak'])
 rows.append({'f_Hz':f,'ideal':ideal,'nominal':network(f,[1]*7),'min_power_corner':lo,'max_power_corner':hi,'max_current_corner':hot,'corner_count':len(corners),'matching_values_SI':values(f)})
 for x in [lo,hi,hot]:
  case=[f,.5,.5,50,1000,x['multipliers']]
  if case not in cases:cases.append(case)
a.output.mkdir(parents=True,exist_ok=True);(a.output/'network-check.json').write_text(json.dumps(rows,indent=2)+'\n');(a.output/'tolerance-plan.json').write_text(json.dumps(cases,indent=2)+'\n');print(json.dumps(rows,indent=2))
