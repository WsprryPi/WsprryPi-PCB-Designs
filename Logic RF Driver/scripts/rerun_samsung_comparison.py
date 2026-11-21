"""Rerun retained amplifier decks with passive fits to local Samsung graph exports.
No manufacturer transistor/IBIS sources are bundled. Requires numpy/scipy and
retained research simulate.py, models/, practical-bs/ decks (hashes in manifest).
Usage: python3 script.py --research DIR --source DIR --output DIR
"""
from pathlib import Path
import argparse,sys,csv,json,re,hashlib
p=argparse.ArgumentParser();p.add_argument('--research',type=Path,required=True);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument("--case");a=p.parse_args()
sys.path[:0]=[str(a.research/'python-packages'),str(a.research)]
import numpy as np
from scipy.optimize import nnls
import simulate as base
D=a.output;D.mkdir(exist_ok=True);(D/'runs').mkdir(exist_ok=True);base.ROOT=D
F=[137e3,475e3,1.8e6,3.5e6,7e6,10e6,14e6,21e6,28e6,50e6,70e6,100e6,145e6]
tau=1/(2*np.pi*np.geomspace(1,1e11,70));fits={};fitstats={}
for bias in (0,2.5,5):
 text=(a.source/f'graph-{bias}V.csv').read_text(encoding='utf-8-sig')
 data=np.array([[float(x) for x in r] for r in csv.reader(text.split('Frequency(MHz),|Z|(ohm),ESR(ohm)\n')[1].splitlines()) if len(r)==3]);f=data[:,0]*1e6;s=2j*np.pi*f
 # Magnitude-only exports do not supply phase. Assume one series resonance:
 # capacitive below minimum |Z|, inductive above. Validate against |Z| AND ESR.
 sign=np.where(np.arange(len(f))<np.argmin(data[:,1]),-1,1)
 z=data[:,2]+1j*sign*np.sqrt(np.maximum(0,data[:,1]**2-data[:,2]**2))
 B=np.array([1/s,np.ones(len(s)),s]+[1/(1+s*t) for t in tau]+[s*t/(1+s*t) for t in tau]).T
 w=1/np.maximum(abs(z),.008);A=np.r_[B.real*w[:,None],B.imag*w[:,None]];y=np.r_[z.real*w,z.imag*w];scale=np.linalg.norm(A,axis=0)
 c=nnls(A/scale,y,maxiter=50000)[0]/scale;c[1]=max(c[1],.0001);fit=B@c;fits[bias]=c
 band=(f>=137e3)&(f<=145e6);err=abs(abs(fit)-data[:,1]);er=abs(fit.real-data[:,2]);rel=err/data[:,1]
 fitstats[str(bias)]={'max_magnitude_error_ohm_band':float(max(err[band])),'max_magnitude_error_percent_band':float(max(rel[band])*100),'max_ESR_error_ohm_band':float(max(er[band])),'max_magnitude_error_percent_100Hz_6GHz':float(max(rel)*100),'rms_magnitude_error_percent_100Hz_6GHz':float(np.sqrt(np.mean(rel**2))*100),'assumed_resonance_sample_Hz':float(f[np.argmin(data[:,1])]),'coefficients':c.tolist()}
 np.savez_compressed(D/f'fit-{bias}V.npz',frequency=f,Z_source=z,Z_fit=fit)
(D/'fit-summary.json').write_text(json.dumps(fitstats,indent=2)+'\n')
print('FITS', {b:{k:v for k,v in st.items() if k!='coefficients'} for b,st in fitstats.items()},flush=True)
def network(bias,path,mid):
 bias=float(np.clip(bias,0,5));lo,hi=(0,2.5) if bias<=2.5 else (2.5,5);t=(bias-lo)/(hi-lo);c=fits[lo]*(1-t)+fits[hi]*t
 net=['* Passive fit/interpolation of Samsung precise-model graph; not vendor SPICE','.subckt C4_samsung a b',f'Cs a n0 {1/c[0]:.14g} IC={mid:.14g}','Rleak a n0 100meg']
 branches=[('R',c[1],0),('L',c[2],0)]
 branches += [('RC',v,t) for v,t in zip(c[3:3+len(tau)],tau) if v>1e-10]
 branches += [('RL',v,t) for v,t in zip(c[3+len(tau):],tau) if v>1e-10]
 for i,(kind,v,t) in enumerate(branches):
  n=f'n{i}';m='b' if i==len(branches)-1 else f'n{i+1}'
  if kind in ('R','L'):net.append(f'{kind}{i} {n} {m} {max(v,1e-18):.14g}')
  else:net += [f'R{i} {n} {m} {v:.14g}',f'{kind[-1]}{i} {n} {m} {(t/v if kind=="RC" else t*v):.14g}']
 net+=['.ends C4_samsung'];path.write_text('\n'.join(net)+'\n');return bias
sp=base.Spice()
def run(kind,f,rg,model,step=700,bias_override=None):
 name=f'{kind}_{f:g}_{rg}_{model}_{step}'+('' if bias_override is None else f'_bias{bias_override:.9g}');text=(a.research/'practical-bs'/f'practical_{kind}_{f:g}_50_{rg}.cir').read_text();mid=float(re.search(r'Cc \S+ ce 1u IC=(\S+)',text)[1]);node='out' if kind=='logic' else 'drain'
 lines=[l for l in text.splitlines() if not l.startswith(('Cc ','Rc ','Lc ','Rload ','.ic ','.end','.tran ','.options '))];lines[0]=name;lines+=['.temp 25','.options method=gear reltol=0.001 abstol=1e-10']
 bias=0 if model=='zero_bias' else (mid if bias_override is None else bias_override)
 lib=D/(name+'.mod');effective_bias=network(bias,lib,mid)
 lines +=[f'.include "{lib}"',f'XC4 {node} load C4_samsung',f'.ic V({node})={mid:.14g} V(load)=0','Rload load 0 50',f'.tran {1/f/1000:.14g} {60/f:.14g} 0 {1/f/step:.14g} uic','.end']
 sp.run(lines,name);t=sp.vec('time');assert t[-1]>=59.999/f
 tt=np.linspace(52/f,60/f,32001);v=np.interp(tt,t,sp.vec('load'));vr=np.interp(tt,t,sp.vec(node));period=8/f
 assert max(abs(v))<30,(name,'unphysical voltage',float(max(abs(v))))
 power=lambda ts,vs:abs(2/(ts[-1]-ts[0])*np.trapezoid(vs*np.exp(-2j*np.pi*f*ts),ts))**2/100
 pp=power(tt,v);halves=[power(tt[k*16000:(k+1)*16000+1],v[k*16000:(k+1)*16000+1]) for k in (0,1)]
 r=dict(kind=kind,f_Hz=f,model_rg=rg,c4_model=model,p1_W=float(pp),mean_load_V=float(np.trapezoid(v,tt)/period),mean_capacitor_V=float(np.trapezoid(vr-v,tt)/period),fit_bias_V=effective_bias,initialized_midpoint_V=mid,late_window_power_change_percent=float(100*(halves[1]/halves[0]-1)),vpp=float(np.ptp(v)),step_factor=step)
 assert abs(r['mean_load_V'])<.05,(name,'DC offset',r['mean_load_V'])
 assert abs(r['late_window_power_change_percent'])<.1,(name,'not stationary',r['late_window_power_change_percent'])
 return r
if a.case:
    task=json.loads(a.case)
    try:r=run(*task);print('CASE_RESULT '+json.dumps(r),flush=True)
    except Exception as e:print('CASE_ERROR '+str(e),flush=True);sys.exit(1)
    sys.exit(0)
import subprocess, concurrent.futures
command=[sys.executable,str(Path(__file__).resolve()),'--research',str(a.research),'--source',str(a.source),'--output',str(D)]
def bounded(task,step=700):
    attempt=task+[step]
    result=subprocess.run(command+['--case',json.dumps(attempt)],capture_output=True,text=True,timeout=30)
    if result.returncode:raise RuntimeError(result.stdout[-500:]+result.stderr[-500:])
    return json.loads(result.stdout.split('CASE_RESULT ')[-1])
rows=json.loads((D/'results.json').read_text()) if (D/'results.json').exists() else [];failures=[]
keys=lambda r:(r['kind'],r['f_Hz'],r['model_rg'],r['c4_model'])
tasks=[[kind,f,rg,model] for f in F for kind,rg in [('logic',270),('resistor',270),('choke',270),('resistor',5),('choke',5)] for model in ('zero_bias','dc_bias')]
def evaluate(task):
    for step in (700,1400):
        try:return bounded(task,step),None
        except Exception as e:reason=str(e)
    return None,dict(task=task,reason=reason)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    pending={pool.submit(evaluate,t):t for t in tasks if tuple(t) not in {keys(r) for r in rows}}
    for future in concurrent.futures.as_completed(pending):
        r,fail=future.result()
        if r:rows.append(r)
        else:failures.append(fail)
        (D/'results.json').write_text(json.dumps(rows,indent=2)+'\n');(D/'failures.json').write_text(json.dumps(failures,indent=2)+'\n')
        print('PROGRESS',len(rows),len(failures),pending[future],flush=True)
checks=[]
selected=[r for r in rows if r['f_Hz'] in (137e3,145e6) or (r['f_Hz']==7e6 and r['model_rg']==5)]
def verify(row):
    try:
        r=bounded(list(keys(row)),row['step_factor']*2);r['power_change_percent']=100*(r['p1_W']/row['p1_W']-1);return r,None
    except Exception as e:return None,dict(verification=True,case=row,reason=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    for r,fail in pool.map(verify,selected):
        if r:checks.append(r)
        else:failures.append(fail)
        (D/'verification.json').write_text(json.dumps(checks,indent=2)+'\n')
(D/'failures.json').write_text(json.dumps(failures,indent=2)+'\n')
print('COMPLETE',len(rows),'cases',len(checks),'checks',len(failures),'failures',flush=True)
