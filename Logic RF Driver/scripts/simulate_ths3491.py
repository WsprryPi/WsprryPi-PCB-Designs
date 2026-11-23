"""Candidate THS3491 chain; external TI model and retained Logic RF Driver decks.
No KiCad design edits. Vendor model text remains in ignored generated/ storage.
"""
from pathlib import Path
import argparse,json,sys,re,hashlib,subprocess,concurrent.futures
ap=argparse.ArgumentParser();ap.add_argument('--research',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--board-runs',type=Path,required=True);ap.add_argument('--case');a=ap.parse_args()
sys.path[:0]=[str(a.research/'python-packages'),str(a.research)]
import numpy as np
from scipy.optimize import root
import simulate as s
p=Path(__file__).resolve().parents[1];out=a.output.resolve();out.mkdir(exist_ok=True,parents=True);(out/'runs').mkdir(exist_ok=True)
s.ROOT=out;sp=s.Spice()
for cm in Path('/Applications/KiCad/KiCad.app/Contents/PlugIns/sim/ngspice').glob('*.cm'):sp.lib.ngSpice_Command(('codemodel '+str(cm)).encode())
sp.lib.ngSpice_Command(b'set ngbehavior=psa')
model=out/'models/THS3491DDA.lib';original=model.read_text()
old='GOUTN GNDF VEE VALUE = {IF(V(VIMON,GNDF) <= 0, V(VIMON,GNDF)*V(SHDN,GNDF),0)}'
assert original.count(old)==1
corrected=out/'models/THS3491DDA-current-sign.lib'
if not corrected.exists():corrected.write_text(original.replace(old,old.replace('<= 0, V(', '<= 0, -V(')))
freqs=[137e3,475e3,1.8e6,3.5e6,7e6,10e6,14e6,21e6,28e6,50e6,70e6,100e6,145e6]
def filt(prefix,src,dst,f,Q,shunt_first=False):
 # Fifth-order Butterworth low-pass, 50-ohm design impedance, fc=1.5*f.
 # Inductor ESR set from Q at the test frequency; capacitor Q=1000.
 # Illustrative parasitics: 0.3nH per cap; inductor SRF=5*fc.
 g=[.61803398875,1.61803398875,2.,1.61803398875,.61803398875];w=2*np.pi*1.5*f;lines=[];node=src
 for j,x in enumerate(g):
  if (j%2==0) != shunt_first:
   nxt=dst if j==4 else f'{prefix}n{j}';mid=f'{prefix}m{j}';L=50*x/w;R=2*np.pi*f*L/Q;Cp=min(2e-12,1/((5*w)**2*L))
   lines += [f'R{prefix}{j} {node} {mid} {R:.14g}',f'L{prefix}{j} {mid} {nxt} {L:.14g}',f'C{prefix}p{j} {mid} {nxt} {Cp:.14g}'];node=nxt
  else:
   C=x/(50*w);Rp=1000/(2*np.pi*f*C);mid=f'{prefix}c{j}'
   lines += [f'L{prefix}c{j} {node} {mid} 0.3n',f'C{prefix}{j} {mid} 0 {C:.14g}',f'R{prefix}p{j} {mid} 0 {Rp:.14g}']
 if shunt_first:lines += [f'R{prefix}end {node} {dst} 1u']
 return lines
def pad(prefix,src,dst,db):
 if not db:return [f'R{prefix}wire {src} {dst} 1u']
 K=10**(db/20);rp=50*(K+1)/(K-1);rs=50*(K*K-1)/(2*K)
 return [f'R{prefix}a {src} 0 {rp:.14g}',f'R{prefix}s {src} {dst} {rs:.14g}',f'R{prefix}b {dst} 0 {rp:.14g}']
def run_case(f,loss=.5,Q=50,alpha=.5,riso=1,step=1000,original_sign=False,shunt_first=False):
 T=1/f;name=f'f{f:g}_loss{loss:g}_q{Q:g}_a{alpha:g}_r{riso:g}_step{step}_orig{int(original_sign)}_cin{int(shunt_first)}_cp2p';board=a.board_runs.resolve();src=board/'runs'/f'f{f:g}_det1_skew0_step1400.cir';base=src.read_text().splitlines();fit=board/f'f{f:g}_det1_skew0_step1400_c4.mod';fittext=fit.read_text();fitlocal=out/(name+'_c4.mod')
 lines=[]
 for z in base[1:]:
  if z.startswith(('.end','.tran','.options','Rload ')):continue
  if z.startswith('.include'):z=f'.include "{fitlocal}"'
  lines.append(z)
 # Sense the current entering the input filter and leaving the PA.
 lines += ['Vinfilter load fin 0',*filt('fi','fin','fiout',f,Q,shunt_first),*pad('pi','fiout','divin',loss),f'Rdivin divin 0 {50/(1-alpha):.14g}',f'Rdivseries divin pa_in {50*(1/alpha-1):.14g}','Rdivout pa_in 0 50',f'.include "{model if original_sign else corrected}"','Vplus vp 0 15','Vminus vm 0 -15','Ven en 0 3.3','Xpa pa_in inn pa_out 0 en vp vm 0 THS3491DDA','Rf pa_out inn 798','Rg inn 0 200','Vpaout pa_out out_sense 0',f'Riso out_sense acout {riso:.14g}','Cout acout cout_mid 1u','Rcout cout_mid cout_l .03','Lcout cout_l of_in .5n',*filt('fo','of_in','of_out',f,Q),*pad('po','of_out','rload',loss),'Vload rload final 0','Rfinal final 0 50']
 # Current drawn from the 5V rail by the IBIS pull-up tables; excludes internal crossover.
 for j in [0,1]:
  z=next(z for z in lines if z.startswith(f'Bdrv{j} '));expr=z.split(' I=',1)[1];pullup=expr.split(f'+v(w{j})*',1)[1]
  lines += [f'Brail{j} rail5 0 I=-v(w{j})*{pullup}']
 lines+=['Vrail5 rail5 0 5']
 initial=[float(re.search(r'C5 .* IC=(\S+)',src.read_text())[1]),float(re.search(r'C6 .* IC=(\S+)',src.read_text())[1]),float(re.search(r'Cs a n0 \S+ IC=(\S+)',fittext)[1])]
 warm=out/f'f{f:g}_loss0.5_q50_a0.5_r1_step1000_orig0_cin0_cp2p.json'
 if warm.exists():initial=json.loads(warm.read_text()).get('periodic_initial_state_V',initial)
 if (out/'warm-states.json').exists():initial=json.loads((out/'warm-states.json').read_text()).get(str(int(f)),initial)
 own=out/(name+'.json')
 if own.exists():initial=json.loads(own.read_text()).get('periodic_initial_state_V',initial)
 last_state=initial.copy();count=0
 def execute(x):
  nonlocal count,last_state
  last_state=list(map(float,x));count+=1;fitlocal.write_text(re.sub(r'(Cs a n0 \S+ IC=)\S+',lambda m:m[1]+f'{x[2]:.14g}',fittext))
  deck=[]
  for z in lines:
   if z.startswith('C5 '):z=re.sub(r'IC=\S+',f'IC={x[0]:.14g}',z)
   if z.startswith('C6 '):z=re.sub(r'IC=\S+',f'IC={x[1]:.14g}',z)
   if z.startswith('.ic '):z=re.sub(r'V\(out\)=\S+',f'V(out)={x[2]:.14g}',z)+f' V(base)={x[1]:.14g} V(com)={x[2]-x[0]:.14g} V(detin)={x[2]:.14g}'
   deck.append(z)
  deck+=['.options method=gear reltol=0.0001 abstol=1e-12',f'.tran {T/500:.14g} {60*T:.14g} 0 {T/step:.14g}','.end']
  sp.run([name,*deck],name);t=sp.vec('time');assert t[-1]>=59.999*T
  ys=[sp.vec('detin')-sp.vec('com'),sp.vec('base'),sp.vec('out')-sp.vec('xc4.n0')]
  delta=np.array([np.interp(60*T,t,y)-np.interp(40*T,t,y) for y in ys]);print(name,count,list(map(float,delta)),file=sys.stderr,flush=True);return delta
 drift=execute(initial)
 if max(abs(drift))>=5e-5:
  class Settled(Exception):pass
  def objective(x):
   delta=execute(x)
   if max(abs(delta))<5e-5:raise Settled(delta)
   return delta*1e6
  try:
   sol=root(objective,initial,options={'eps':1e-6,'xtol':1e-8,'maxfev':30});drift=execute(sol.x)
  except Settled as done:drift=done.args[0]
 assert max(abs(drift))<5e-5,(name,drift)
 t=sp.vec('time');native=(t>=52*T)&(t<=60*T);peak=lambda n:float(np.max(np.abs(sp.vec(n)[native])));q=np.linspace(52*T,60*T,16001);v=lambda n:np.interp(q,t,sp.vec(n));mean=lambda y:float(np.trapezoid(y,q)/(8*T))
 amp=lambda n,h=1:2*abs(np.trapezoid(v(n)*np.exp(-2j*np.pi*f*h*q),q))/(8*T)
 I=v('vpaout#branch');Ifb=(v('pa_out')-v('inn'))/798;Itotal=I+Ifb;Ip=mean(-v('vplus#branch'));Im=mean(v('vminus#branch'));rf=mean(v('pa_out')*I);pdc=15*(Ip+Im)
 # Independent physical Class-B load-current bookkeeping, plus modeled nominal quiescent current.
 ipcheck=.0168+mean(np.maximum(Itotal,0));imcheck=.0168+mean(np.maximum(-Itotal,0));feedback=mean(v('pa_out')*Ifb)
 node=amp('final');p1=node*node/100;pin=amp('divin')**2/100
 outrow={'case':name,'f_Hz':f,'additional_loss_dB_each':loss,'inductor_Q':Q,'divider_voltage_ratio':alpha,'Riso_ohms':riso,'step_divisor':step,'inductor_parallel_cap_limit_F':2e-12,'original_vendor_current_sign':original_sign,'input_shunt_first':shunt_first,'fundamental_output_mW':p1*1000,'total_load_mW':mean(v('final')**2/50)*1000,'pa_pin_fundamental_mW_equiv50':amp('pa_out')**2*10,'pa_pin_Vpp':float(np.ptp(v('pa_out'))),'pa_pin_max_dvdt_V_per_us':float(np.max(np.abs(np.gradient(v('pa_out'),q)))/1e6),'pa_pin_peak_current_mA':float(np.max(np.abs(I))*1000),'pa_plus_mA':Ip*1000,'pa_minus_mA':Im*1000,'pa_plus_independent_mA':ipcheck*1000,'pa_minus_independent_mA':imcheck*1000,'pa_dc_W':pdc,'pa_real_output_W':rf,'pa_heat_W':pdc-rf-feedback,'pa_feedback_loss_mW':mean((v('pa_out')-v('inn'))**2/798+v('inn')**2/200)*1000,'output_network_loss_mW':(rf-mean(v('final')**2/50))*1000,'input_fundamental_equiv50_mW':pin*1000,'logic_5V_pullup_mA':mean(-v('vrail5#branch'))*1000,'logic_led_3V3_mA':mean(-v('vrail#branch'))*1000,'peak_sampling':'native_final_8_periods','logic_filter_peak_mA':peak('vinfilter#branch')*1000,'logic_filter_real_mW':mean(v('load')*v('vinfilter#branch'))*1000,'logic_channel_peak_mA':[peak(f'vsense{j}#branch')*1000 for j in [0,1]],'load_H3_dBc':float(20*np.log10(max(amp('final',3),1e-20)/node)),'load_H5_dBc':float(20*np.log10(max(amp('final',5),1e-20)/node)),'pa_H3_dBc':float(20*np.log10(max(amp('pa_out',3),1e-20)/amp('pa_out'))),'state_drift_V':list(map(float,drift)),'periodic_initial_state_V':last_state,'solver_runs':count,'transient_points':len(t)}
 power=[]
 for k in [0,1]:
  u=np.linspace((52+4*k)*T,(56+4*k)*T,8001);y=np.interp(u,t,sp.vec('final'));a1=2*abs(np.trapezoid(y*np.exp(-2j*np.pi*f*u),u))/(4*T);power.append(a1*a1/100)
 outrow['late_power_drift_percent']=100*(power[1]/power[0]-1);assert abs(outrow['late_power_drift_percent'])<.1
 if f in [137e3,145e6]:np.savez_compressed(out/(name+'.npz'),t=q-52*T,pa_in=v('pa_in'),pa_out=v('pa_out'),final=v('final'),current=I,raw=v('out'),logic_load=v('load'))
 (out/(name+'.json')).write_text(json.dumps(outrow,indent=2)+'\n');print(json.dumps(outrow),flush=True)
if a.case:run_case(*json.loads(a.case))
else:
 # All three loss budgets, full-band nominal divider, plus higher-drive endpoint checks.
 tasks=[[f,.5,50,.5,1,1000] for f in freqs]
 tasks += [[f,l,50,.5,1,1000] for f in [137e3,145e6] for l in [0,1]]
 tasks += [[f,.5,50,.6,1,1000] for f in freqs]
 tasks += [[f,.5,Q,.5,1,1000] for f in [137e3,145e6] for Q in [25,100]]
 tasks += [[f,.5,50,al,1,2000] for f in [137e3,145e6] for al in [.5,.6]]
 tasks += [[145e6,.5,50,.5,1,1000,True]]
 tasks += [[f,.5,50,.5,1,1000,False,True] for f in [137e3,145e6]]
 (out/'plan.json').write_text(json.dumps(tasks,indent=2)+'\n');rows=[]
 cmd=[sys.executable,str(Path(__file__).resolve()),'--research',str(a.research),'--output',str(out),'--board-runs',str(a.board_runs)]
 def worker(case):
  run=subprocess.run(cmd+['--case',json.dumps(case)],capture_output=True,text=True,timeout=600)
  if run.returncode:raise RuntimeError(str(case)+'\n'+run.stdout[-500:]+run.stderr[-2000:])
  return json.loads(run.stdout.strip().splitlines()[-1])
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  for row in pool.map(worker,tasks):rows.append(row);(out/'results.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(row),flush=True)
 print('COMPLETE',len(rows),flush=True)
