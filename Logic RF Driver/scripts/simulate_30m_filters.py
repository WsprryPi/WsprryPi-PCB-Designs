"""30 m filter comparison driven by retained Logic RF Driver behavioral decks.

Requires the external research helper/model dependencies used by run_board_simulation.
Raw decks and vendor models remain in ignored generated storage. No CAD edits.
"""
from pathlib import Path
import argparse,sys,json,re,csv,hashlib,shutil
ap=argparse.ArgumentParser()
ap.add_argument('--research',type=Path,required=True)
ap.add_argument('--output',type=Path,required=True)
ap.add_argument('--reuse-l-first',type=Path,help='Reuse validated unchanged L-first and bare-load cases')
a=ap.parse_args()
sys.path[:0]=[str(a.research/'python-packages'),str(a.research)]
import numpy as np
from scipy.optimize import root
import simulate as s
p=Path(__file__).resolve().parents[1];out=a.output.resolve();out.mkdir(parents=True,exist_ok=True);(out/'runs').mkdir(exist_ok=True)
s.ROOT=out;sp=s.Spice();f=10.1401e6;T=1/f
src=p/'generated/board-rerun/runs/f1e+07_det1_skew0_step1400.cir'
fit=p/'generated/board-rerun/f1e+07_det1_skew0_step1400_c4.mod'
base=src.read_text().splitlines();fittext=fit.read_text()
values=p.parent/'WsprryPi LPF-LCL/model/minimum-loss-values.csv'
r=next(r for r in csv.DictReader(values.open()) if r['Band']=='30 & 40m')
L=[float(r['L1_L5_H']),float(r['C2_C4_F']),float(r['L3_H']),float(r['C2_C4_F']),float(r['L1_L5_H'])]
oldvalues=p.parent/'WsprryPi LPF-LCL/model/results.json'
C=next(r['C_first_SI'] for r in json.loads(oldvalues.read_text())['bands'] if r['band']=='30 & 40m')
assert len(C)==7 and len(L)==5
cached={}
if a.reuse_l_first:
 hashes=json.loads((a.reuse_l_first/'inputs.json').read_text())
 for x in [src,fit,values,p/'Logic RF Driver.kicad_sch',p/'Logic RF Driver.kicad_pcb']:
  assert hashes[str(x)]==hashlib.sha256(x.read_bytes()).hexdigest(), x
 cached={r['case']:r for r in json.loads((a.reuse_l_first/'results.json').read_text()) if r['first'] in ['L','bare']}
results=[]
for first,Q,length,step in [('bare',50,0,1400)]+[(x,q,.05,1400) for x in ['L','C'] for q in [25,50,100]]+[(x,50,ell,1400) for x in ['L','C'] for ell in [0,.2]]+[(x,50,.05,2800) for x in ['L','C']]:
 name=f'{first}_q{Q}_line{length:g}_step{step}';local=out/(name+'_c4.mod');lines=[]
 if name in cached:
  row=cached[name].copy();assert row['frequency_Hz']==f
  row.update(filter_values_SI=L if first=='L' else [],filter_elements=5 if first=='L' else 0,reused_from=str(a.reuse_l_first))
  shutil.copyfile(a.reuse_l_first/(name+'.npz'),out/(name+'.npz'))
  results.append(row);(out/'results.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(row),flush=True);continue
 for z in base[1:]:
  if z.startswith(('.end','.tran','.options','Rload ')):continue
  if z.startswith('.include'):z=f'.include "{local}"'
  if z.startswith(('Vw0 ','Vw1 ')):
   j=int(z[2]);pts=s.weights(f,50,2,0,j)[0]
   z=f'Vw{j} w{j} 0 PWL('+ ' '.join(f'{t:.14g} {v}' for t,v in pts)+')'
  lines.append(z)
 for j in [0,1]:
  z=next(z for z in lines if z.startswith(f'Bdrv{j} '));expr=z.split(' I=',1)[1];up=expr.split(f'+v(w{j})*',1)[1]
  lines.append(f'Brail{j} rail5 0 I=-v(w{j})*{up}')
 lines+=['Vrail5 rail5 0 5']
 if first=='bare':lines+=['Rload load 0 50'];final='load'
 else:
  if length:
   # Ten-section lossless pi ladder for a 50-ohm line; avoids ideal-delay solver failures.
   td=length/1.7e8;node='load'
   lines += [f'Cfeedstart load 0 {td/50/20:.14g}']
   for k in range(10):
    nxt='fin' if k==9 else f'feed{k}'
    lines += [f'Lfeed{k} {node} {nxt} {50*td/10:.14g}',f'Cfeed{k} {nxt} 0 {td/50/(20 if k==9 else 10):.14g}'];node=nxt
  else:lines+=['Vfeed load fin 0']
  node='fin';vals=L if first=='L' else C
  for j,vv in enumerate(vals):
   kind=first if j%2==0 else ('C' if first=='L' else 'L')
   if kind=='L':
    nxt='final' if j==len(vals)-1 or (first=='C' and j==len(vals)-2) else f'n{j}'
    lines += [f'Rcoil{j} {node} m{j} {2*np.pi*f*vv/Q:.14g}',f'Lcoil{j} m{j} {nxt} {vv:.14g}'];node=nxt
   else:lines += [f'Cfilter{j} {node} 0 {vv:.14g}']
  lines+=['Rload final 0 50'];final='final'
 initial=[2.13,.69,2.51];last=initial
 def execute(x):
  global last
  last=list(map(float,x));local.write_text(re.sub(r'(Cs a n0 \S+ IC=)\S+',lambda m:m[1]+f'{x[2]:.14g}',fittext))
  deck=[]
  for z in lines:
   if z.startswith('C5 '):z=re.sub(r'IC=\S+',f'IC={x[0]:.14g}',z)
   if z.startswith('C6 '):z=re.sub(r'IC=\S+',f'IC={x[1]:.14g}',z)
   if z.startswith('.ic '):z=f'.ic V(out)={x[2]:.14g} V(load)=0 V(base)={x[1]:.14g} V(com)={x[2]-x[0]:.14g} V(detin)={x[2]:.14g}'
   deck.append(z)
  deck+=['.options method=gear reltol=0.0001 abstol=1e-12',f'.tran {T/1000:.14g} {60*T:.14g} 0 {T/step:.14g} uic','.end']
  sp.run([name,*deck],name);t=sp.vec('time');assert t[-1]>=59.999*T
  return np.array([np.interp(60*T,t,y)-np.interp(40*T,t,y) for y in [sp.vec('detin')-sp.vec('com'),sp.vec('base'),sp.vec('out')-sp.vec('xc4.n0')]])
 class Settled(Exception):pass
 def objective(x):
  d=execute(x)
  if max(abs(d))<2e-6:raise Settled(d)
  return d*1e6
 try:
  sol=root(objective,initial,options={'eps':1e-6,'maxfev':60});drift=execute(sol.x)
 except Settled as done:drift=done.args[0]
 assert max(abs(drift))<5e-5,(name,drift)
 t=sp.vec('time');u=np.linspace(52*T,60*T,32001);v=lambda n:np.interp(u,t,sp.vec(n));mean=lambda y:float(np.trapezoid(y,u)/(8*T))
 amp=lambda node,h:float(2*abs(np.trapezoid(v(node)*np.exp(-2j*np.pi*f*h*u),u))/(8*T))
 a1=amp(final,1);harmonics={str(h):20*np.log10(max(amp(final,h),1e-16)/a1) for h in range(2,10)}
 row={'case':name,'first':first,'filter_values_SI':(L if first=='L' else C) if first!='bare' else [],'filter_elements':len(L if first=='L' else C) if first!='bare' else 0,'inductor_Q':Q,'line_m':length,'line_Z0_ohms':50,'line_velocity_m_per_s':1.7e8,'step_divisor':step,'frequency_Hz':f,'fundamental_mW':a1*a1*10,'harmonics_dBc':harmonics,'load_Vpp':float(np.ptp(v(final))),'mean_5V_pullup_mA':-mean(v('vrail5#branch'))*1e3,'mean_3V3_LED_mA':-mean(v('vrail#branch'))*1e3,'channel_peak_mA':[float(max(abs(sp.vec(f'vsense{j}#branch')[t>52*T]))*1e3) for j in [0,1]],'channel_rms_mA':[float(np.sqrt(mean(v(f'vsense{j}#branch')**2))*1e3) for j in [0,1]],'state_drift_V':list(map(float,drift))}
 powers=[]
 for low in [52,56]:
  q=np.linspace(low*T,(low+4)*T,16001);y=np.interp(q,t,sp.vec(final));z=2*abs(np.trapezoid(y*np.exp(-2j*np.pi*f*q),q))/(4*T);powers.append(z*z)
 row['late_power_drift_percent']=100*(powers[1]/powers[0]-1);assert abs(row['late_power_drift_percent'])<.1
 np.savez_compressed(out/(name+'.npz'),t_s=u-52*T,load_V=v(final),raw_V=v('out'),channel0_A=v('vsense0#branch'))
 results.append(row);(out/'results.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(row),flush=True)
(out/'inputs.json').write_text(json.dumps({str(x):hashlib.sha256(x.read_bytes()).hexdigest() for x in [src,fit,values,oldvalues,Path(__file__),p/'Logic RF Driver.kicad_sch',p/'Logic RF Driver.kicad_pcb']},indent=2)+'\n')
sp.lib.ngSpice_Command(b'version');(out/'engine.txt').write_text('\n'.join(sp.logs[-12:])+'\n')
