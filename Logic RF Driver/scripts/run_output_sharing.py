"""Per-output series-resistor and channel-sharing sensitivity study.

Manufacturer model text is not bundled. --research supplies simulate.py and its
model/package dependencies; --decks and --c4-models supply the retained Samsung
comparison decks and passive C4 fits. No electromagnetic layout extraction.
"""
from pathlib import Path
import argparse,sys,json,re,hashlib
ap=argparse.ArgumentParser();ap.add_argument('--research',type=Path,required=True);ap.add_argument('--decks',type=Path,required=True);ap.add_argument('--c4-models',type=Path,required=True);ap.add_argument('--models',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--case');ap.add_argument('--plan',type=Path);ap.add_argument('--baseline',type=Path,required=True);a=ap.parse_args()
sys.path[:0]=[str(a.research/'python-packages'),str(a.research)]
import numpy as np
from scipy.optimize import least_squares
import simulate as s
out=a.output.resolve();out.mkdir(parents=True,exist_ok=True);(out/'runs').mkdir(exist_ok=True);s.ROOT=out;sp=s.Spice();rows=[];inputs={}
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
freqs=[137e3,475e3,1.8e6,3.5e6,7e6,10e6,14e6,21e6,28e6,50e6,70e6,100e6,145e6]
def case(f,series,skew=0,step=1400,mismatch=0,parasitics=False):
 loaded=True
 name=f'f{f:g}_r{series:g}_skew{skew:g}_step{step}_m{mismatch:g}_p{int(parasitics)}';T=1/f
 deck=a.decks/f'logic_{f:g}_270_dc_bias_700.cir';text=deck.read_text();inputs[str(deck.resolve())]=sha(deck)
 lines=[]
 for line in text.splitlines()[1:]:
  if line.startswith(('.end','.tran','.options')):continue
  if line.startswith('.include'):
   fit=a.c4_models/Path(re.search(r'"([^"]+)"',line)[1]).name;assert fit.exists();inputs[str(fit.resolve())]=sha(fit);fit_text=fit.read_text();fit_local=out/(name+'_c4.mod');line=f'.include "{fit_local}"'
  if line.startswith('Vw1 ') and skew:
   head,points=line.split('PWL(');v=list(map(float,points.rstrip(')').split()));pairs=list(zip(v[::2],v[1::2]));line=head+'PWL('+' '.join(f'{(t+skew if t else 0):.14g} {y:.14g}' for t,y in pairs)+')'
  if series and line.startswith('Vsense'):
   j=int(line.split()[0][-1]);line=line.replace(' out 0',f' pin{j} 0');rv=series*(1+(-.01 if j==0 else .01) if mismatch else 1)
   if parasitics:
    lines += [line,f'Riso{j} pin{j} iso{j} {rv:.12g}',f'Liso{j} iso{j} out .5n',f'Ciso{j} pin{j} out .05p'];continue
   lines += [line,f'Riso{j} pin{j} out {rv:.12g}'];continue
  if mismatch and line.startswith('Bdrv'):
   j=int(line.split()[0][-1]);head,body=line.split(' I=');line=head+' I='+f'{1+(mismatch if j==0 else -mismatch):.12g}*('+body+')'
  lines.append(line)
 for file in ['BAT54S.txt','MMBT3904.txt']:
  mf=a.models/file;inputs[str(mf.resolve())]=sha(mf);lines+=mf.read_text().splitlines()
 lines+=['Vrail rail 0 3.3','R5 rail powerled 680','Dpower powerled 0 LED_APPROX','.model LED_APPROX D(IS=1e-20 N=2 RS=5 CJO=2p)']
 n=0
 def run(x):
  nonlocal n
  n+=1
  fit_local.write_text(re.sub(r'(Cs a n0 \S+ IC=)\S+',lambda m:m[1]+f'{x[2]:.14g}',fit_text))
  deck=[name,*[re.sub(r'V\(out\)=\S+',f'V(out)={x[2]:.14g}',z) if z.startswith('.ic ') else z for z in lines]]
  if loaded:
   deck += ['R2 out detin 220',f'C5 detin com 10n IC={x[0]:.14g}','Dlow 0 com DI_BAT54S','Dhigh com base DI_BAT54S',f'C6 base 0 10n IC={x[1]:.14g}','R3 base 0 1meg','Q1 collector base 0 DI_MMBT3904','R4 rail ledtop 680','Vled ledtop leda 0','Dled leda collector LED_APPROX']
  deck+=['.options method=gear reltol=0.0001 abstol=1e-12',f'.tran {T/1000:.14g} {60*T:.14g} 0 {T/step:.14g} uic','.end'];sp.run(deck,name)
  t=sp.vec('time');assert t[-1]>=59.999*T
  if not loaded:return np.zeros(3)
  return np.array([np.interp(60*T,t,y)-np.interp(40*T,t,y) for y in [sp.vec('detin')-sp.vec('com'),sp.vec('base'),sp.vec('out')-sp.vec('xc4.n0')]])*1e6
 if loaded:
  initial=[2.1,.7,2.51458238133]
  warm=a.baseline/'runs'/f'f{f:g}_det1_skew0_step1400.cir';warmfit=a.baseline/f'f{f:g}_det1_skew0_step1400_c4.mod'
  if warm.exists() and warmfit.exists():
   old=warm.read_text();initial=[float(re.search(r'C5 .* IC=(\S+)',old)[1]),float(re.search(r'C6 .* IC=(\S+)',old)[1]),float(re.search(r'Cs a n0 .* IC=(\S+)',warmfit.read_text())[1])]
  candidates=[]
  for completed in out.glob('f*.json'):
   q=json.loads(completed.read_text())
   if not isinstance(q,dict) or 'f_Hz' not in q:continue
   if q['strength_mismatch_fraction']==mismatch and q['resistor_parasitics']==parasitics:
    distance=20*abs(float(np.log(q['f_Hz']/f)))+abs(q['series_ohms']-series)/max(series,10)+10*abs(q['skew_s']-skew)*1e9
    candidates.append((distance,completed.stem))
  if candidates:
   _,stem=min(candidates);warm=out/'runs'/(stem+'.cir');warmfit=out/(stem+'_c4.mod')
   if warm.exists() and warmfit.exists():
    old=warm.read_text();initial=[float(re.search(r'C5 .* IC=(\S+)',old)[1]),float(re.search(r'C6 .* IC=(\S+)',old)[1]),float(re.search(r'Cs a n0 .* IC=(\S+)',warmfit.read_text())[1])]
  opt=least_squares(run,initial,bounds=([0,0,0],[5,1,5]),diff_step=.0001,xtol=1e-10,ftol=1e-10,gtol=1e-8,max_nfev=60);drift=run(opt.x)/1e6
  if max(abs(drift))>=5e-5:
   from scipy.optimize import root
   retry=root(run,opt.x,options={'eps':1e-8,'xtol':1e-8});drift=run(retry.x)/1e6
  assert max(abs(drift))<5e-5,(name,drift)
 else:run([0,0,2.51458238133]);drift=np.zeros(3)
 t=sp.vec('time');u=np.r_[52*T,t[(t>52*T)&(t<60*T)],60*T];v=lambda n:np.interp(u,t,sp.vec(n));mean=lambda y:float(np.trapezoid(y,u)/(8*T))
 vv=v('load');raw=v('out');amp=lambda n:2*abs(np.trapezoid(vv*np.exp(-2j*np.pi*f*n*u),u))/(8*T)
 currents=[v(f'vsense{j}#branch') for j in [0,1]]
 result={'f_Hz':f,'detector':loaded,'series_ohms':series,'strength_mismatch_fraction':mismatch,'resistor_tolerance_fraction':.01 if mismatch else 0,'resistor_parasitics':parasitics,'skew_s':skew,'step_factor':step,'fundamental_mW':float(amp(1)**2*10),'third_harmonic_dBc':float(20*np.log10(amp(3)/amp(1))),'fifth_harmonic_dBc':float(20*np.log10(amp(5)/amp(1))),'raw_min_V':float(raw.min()),'raw_max_V':float(raw.max()),'load_Vrms':float(np.sqrt(mean(vv**2))),'load_Vpp':float(np.ptp(vv)),'channel_peak_mA':[float(max(abs(i))*1e3) for i in currents],'channel_rms_mA':[float(np.sqrt(mean(i*i))*1e3) for i in currents],'power_led_mA':mean((3.3-v('powerled'))/680)*1e3,'led_rail_mA':mean(-v('vrail#branch'))*1e3,'state_drift_V':list(map(float,drift)) if loaded else None,'solver_evaluations':n}
 if loaded:
  det=(raw-v('detin'))/220
  result.update(activity_led_mA=mean(v('vled#branch'))*1e3,R2_mean_mW=mean(det*det*220)*1e3,detector_peak_mA=float(max(abs(det))*1e3))
 result['resistor_mean_mW']=[]
 for j in [0,1]:
  rv=series*(1+(-.01 if j==0 else .01) if mismatch else 1)
  ir=(v(f'pin{j}')-v(f'iso{j}' if parasitics else 'out'))/rv if rv else np.zeros_like(raw)
  result['resistor_mean_mW'].append(mean(ir*ir)*rv*1e3)
 result['circulating_peak_mA']=float(max(np.minimum(np.abs(currents[0]),np.abs(currents[1]))*np.where(currents[0]*currents[1]<0,1,0))*1e3)
 result['circulating_rms_mA']=float(np.sqrt(mean((np.minimum(np.abs(currents[0]),np.abs(currents[1]))*np.where(currents[0]*currents[1]<0,1,0))**2))*1e3)
 result['channel_current_difference_rms_mA']=float(np.sqrt(mean((currents[0]-currents[1])**2))*1e3)
 # Independent late-window fundamental check.
 powers=[]
 for k in [0,1]:
  lo=(52+4*k)*T;hi=lo+4*T;q=np.r_[lo,t[(t>lo)&(t<hi)],hi];w=np.interp(q,t,sp.vec('load'));z=2*abs(np.trapezoid(w*np.exp(-2j*np.pi*f*q),q))/(4*T);powers.append(z*z*10)
 result['late_power_drift_percent']=100*(powers[1]/powers[0]-1);assert abs(result['late_power_drift_percent'])<.1
 if f in [137e3,145e6]:np.savez_compressed(out/(name+'.npz'),t_s=u-52*T,load_V=vv,raw_V=raw,i0_A=currents[0],i1_A=currents[1])
 rows.append(result);(out/(name+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
if a.case:
 case(*json.loads(a.case))
else:
 import subprocess,concurrent.futures
 tasks=json.loads(a.plan.read_text())
 retained=json.loads((out/'inputs.json').read_text()) if (out/'inputs.json').exists() else {}
 cache_valid=bool(retained) and all(Path(file).exists() and sha(Path(file))==digest for file,digest in retained.items())
 cache_valid=cache_valid and retained.get(str(Path(__file__).resolve()))==sha(Path(__file__))

 command=[sys.executable,str(Path(__file__).resolve()),'--research',str(a.research),'--decks',str(a.decks),'--c4-models',str(a.c4_models),'--models',str(a.models),'--output',str(out),'--baseline',str(a.baseline)]
 def worker(task):
  name=f'f{task[0]:g}_r{task[1]:g}_skew{task[2]:g}_step{task[3]}_m{task[4]:g}_p{int(task[5])}'
  cached=out/(name+'.json')
  if cache_valid and cached.exists():return json.loads(cached.read_text())
  job=subprocess.run(command+['--case',json.dumps(task)],capture_output=True,text=True,timeout=600)
  if job.returncode:raise RuntimeError(str(task)+' '+job.stdout[-300:]+job.stderr[-1000:])
  return json.loads(job.stdout.strip().splitlines()[-1])
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  for result in pool.map(worker,tasks):
   rows.append(result);(out/'results.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(result),flush=True)
 print('COMPLETE',len(rows),'cases',flush=True)
 # Source files are external; record their hashes without bundling model text.
 for source in list(a.decks.glob('logic_*_270_dc_bias_700.cir'))+list(a.c4_models.glob('logic_*_270_dc_bias_700.mod'))+list(a.models.glob('*.txt'))+[a.research/'simulate.py',a.research/'models/SN74LVC2T45.ibs',a.baseline/'results.json',Path(__file__)]:
  inputs[str(source.resolve())]=sha(source)
 (out/'inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
 sp.lib.ngSpice_Command(b'version');(out/'engine.txt').write_text('\n'.join(sp.logs[-12:])+'\n')
