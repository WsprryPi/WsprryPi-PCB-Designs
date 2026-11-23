"""Dual THS3491RGT with catalog-valued filters and per-band drive calibration.
No KiCad design edits. Vendor model text remains in ignored generated/ storage.
"""
from pathlib import Path
import argparse,json,sys,re,hashlib,subprocess,concurrent.futures,os
ap=argparse.ArgumentParser();ap.add_argument('--research',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--board-runs',type=Path,required=True);ap.add_argument('--single-runs',type=Path,required=True);ap.add_argument('--case');a=ap.parse_args()
sys.path[:0]=[str(a.research/'python-packages'),str(a.research)]
import numpy as np
from scipy.optimize import root
import simulate as s
import ths3491_optimized_filters as of
PARTS={r["f_Hz"]:r for r in json.loads((Path(__file__).resolve().parents[1]/"docs/ths3491-optimized-parts.json").read_text())}
p=Path(__file__).resolve().parents[1];out=a.output.resolve();out.mkdir(exist_ok=True,parents=True);(out/'runs').mkdir(exist_ok=True)
s.ROOT=out;sp=s.Spice()
for cm in Path('/Applications/KiCad/KiCad.app/Contents/PlugIns/sim/ngspice').glob('*.cm'):sp.lib.ngSpice_Command(('codemodel '+str(cm)).encode())
sp.lib.ngSpice_Command(b'set ngbehavior=psa')
model=out/'models/THS3491RGT.lib';original=model.read_text()
old='GOUTN GNDF VEE VALUE = {IF(V(VIMON,GNDF) <= 0, V(VIMON,GNDF)*V(SHDN,GNDF),0)}'
assert original.count(old)==1
corrected=out/'models/THS3491RGT-current-sign.lib'
design=out/'models/THS3491RGT-design.lib'
designtext=original.replace(old,old.replace('<= 0, V(', '<= 0, -V(')).replace('RFB           OUT FB 1u','RFB           OUT FB 1.5')
if not design.exists() or design.read_text()!=designtext:
 tmp=design.with_suffix(f'.{os.getpid()}.tmp');tmp.write_text(designtext);tmp.replace(design)
corrected=design
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
def matching_values(f):
 # Lossless 50-ohm Butterworth ladder, then synthesize a positive L/C
 # section whose input is exactly 25+j0 ohms at the operating frequency.
 w=2*np.pi*f;wc=1.5*w;g=[.61803398875,1.61803398875,2.,1.61803398875,.61803398875]
 ladder=[50*x/wc if j%2==0 else x/(50*wc) for j,x in enumerate(g)]
 z=complex(50)
 for j in range(4,-1,-1):z=z+1j*w*ladder[j] if j%2==0 else 1/(1/z+1j*w*ladder[j])
 y=1/z;B=np.sqrt(y.real/25-y.real**2)
 C=(B-y.imag)/w;L=25*B/y.real/w
 assert L>0 and C>0
 return [L,C,*ladder]
def matching_filter(prefix,src,dst,f,Q,tol):
 vals=np.array(matching_values(f))*tol;lines=[];node=src;w=2*np.pi*f
 for j,x in enumerate(vals):
  if j%2==0:
   nxt=dst if j==6 else f'{prefix}n{j}';mid=f'{prefix}m{j}';R=w*x/Q;Cp=min(2e-12,1/((5*1.5*w)**2*x))
   lines += [f'R{prefix}{j} {node} {mid} {R:.14g}',f'L{prefix}{j} {mid} {nxt} {x:.14g}',f'C{prefix}p{j} {mid} {nxt} {Cp:.14g}'];node=nxt
  else:
   mid=f'{prefix}c{j}';Rp=1000/(w*x)
   lines += [f'L{prefix}c{j} {node} {mid} 0.3n',f'C{prefix}{j} {mid} 0 {x:.14g}',f'R{prefix}p{j} {mid} 0 {Rp:.14g}']
 return lines
def run_case(f,alpha=.5,loss=.5,Q=50,step=1000,tol=None,offset=0,hot=1,scale=1):
 n=2;branch=2.49;common=0;shunt=0
 tol=[1.]*13 if tol is None else tol
 parts=PARTS[f]
 T=1/f;name=f'opt_f{f:g}_a{alpha:g}_loss{loss:g}_q{Q:g}_step{step}_t'+hashlib.sha256(json.dumps(tol).encode()).hexdigest()[:10]+(f'_off{offset:g}' if offset else '')+f'_hot{hot:g}_scale{scale:g}';board=a.board_runs.resolve();src=board/'runs'/f'f{f:g}_det1_skew0_step1400.cir';base=src.read_text().splitlines();fit=board/f'f{f:g}_det1_skew0_step1400_c4.mod';fittext=fit.read_text();fitlocal=out/(name+'_c4.mod')
 lines=[]
 for z in base[1:]:
  if z.startswith(('.end','.tran','.options','Rload ')):continue
  if z.startswith('.include'):z=f'.include "{fitlocal}"'
  lines.append(z)
 # Sense the current entering the input filter and leaving the PA.
 lines += ['Vinfilter load fin 0',*of.netlist('fi','fin','fiout',parts['input'],f,tol[:5],hot),*pad('pi','fiout','divin',loss),f'Rdivin divin 0 {50/(1-alpha*scale):.14g}',f'Rdivseries divin pa_in {50*(1/(alpha*scale)-1):.14g}','Rdivout pa_in 0 50',f'.include "{corrected}"','Ven en 0 3.3']
 for j in range(n):
  # Datasheet Fig 10-2: independent gain-5 feedback and 24.9-ohm input resistors.
  # Optional +/- offset is input-referred, scaled for +/-22.5mV output sensitivity.
  voff=(offset if j==0 else -offset)/(1+576/143)
  lines += [f'Rdeq{j} pa_in pinpre{j} 24.9',f'Voffset{j} pinpre{j} pin{j} {voff:.14g}',f'Vplus{j} vp{j} 0 15',f'Vminus{j} vm{j} 0 -15',f'Xpa{j} pin{j} inn{j} fb{j} pa_out{j} en vp{j} vm{j} 0 THS3491RGT',f'Rf{j} fb{j} inn{j} 576',f'Rg{j} inn{j} 0 143',f'Vpaout{j} pa_out{j} out_sense{j} 0',f'Rbranch{j} out_sense{j} bl{j} {branch:.14g}',f'Lbranch{j} bl{j} join 5n',f'Cstrayin{j} pin{j} 0 1p']
 lines += [f'Rcommon join acout {max(common,1e-6):.14g}']
 if shunt:lines += [f'Rshunt acout 0 {shunt:.14g}']
 lines += [f'Cout acout cout_mid {of.COUT["nominal"]*tol[12]:.14g}',f'Rcout cout_mid cout_l {of.elements(of.COUT,f,tol[12],hot)["esr"]:.14g}',f'Lcout cout_l of_in {of.COUT["esl"]:.14g}',*of.netlist('fo','of_in','of_out',parts['output'],f,tol[5:12],hot),*pad('po','of_out','rload',loss),'Vload rload final 0','Rfinal final 0 50']
 # Current drawn from the 5V rail by the IBIS pull-up tables; excludes internal crossover.
 for j in [0,1]:
  z=next(z for z in lines if z.startswith(f'Bdrv{j} '));expr=z.split(' I=',1)[1];pullup=expr.split(f'+v(w{j})*',1)[1]
  lines += [f'Brail{j} rail5 0 I=-v(w{j})*{pullup}']
 lines+=['Vrail5 rail5 0 5']
 initial=[float(re.search(r'C5 .* IC=(\S+)',src.read_text())[1]),float(re.search(r'C6 .* IC=(\S+)',src.read_text())[1]),float(re.search(r'Cs a n0 \S+ IC=(\S+)',fittext)[1])]
 warm=a.single_runs/(f'f{f:g}_a0.5_loss0.5_q50_step1000_t072d618c72.json')
 if not warm.exists():warm=a.single_runs/(f'f{f:g}_a0.5_loss0.5_q50_step1000_t072d618c72.json')
 if warm.exists():initial=json.loads(warm.read_text()).get('periodic_initial_state_V',initial)
 screens=list(out.glob(f'f{f:g}_a0.5_loss0.2_q50_step1000_*.json'))
 if screens:initial=json.loads(screens[0].read_text()).get('periodic_initial_state_V',initial)
 # The source divider stays near 50 ohms across gain settings; reuse the
 # closest completed state for the same filter/corner rather than restarting
 # from a different filter study. Every run still passes the drift checks.
 warm_options=[]
 for candidate in out.glob(f'opt_f{f:g}_*.json'):
  try:r=json.loads(candidate.read_text())
  except (ValueError,OSError):continue
  score=abs(r['divider_voltage_ratio']-alpha)+10*abs(r['additional_loss_dB_each']-loss)+sum(abs(x-y) for x,y in zip(r['component_multipliers'],tol))+abs(r.get('hot_loss_multiplier',1)-hot)
  warm_options.append((score,r))
 if warm_options:initial=min(warm_options,key=lambda x:x[0])[1]['periodic_initial_state_V']
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
 chip=[]
 for j in range(n):
  I=v(f'vpaout{j}#branch');Ifb=(v(f'fb{j}')-v(f'inn{j}'))/576;Itotal=I+Ifb;Ip=mean(-v(f'vplus{j}#branch'));Im=mean(v(f'vminus{j}#branch'));rf=mean(v(f'pa_out{j}')*I);pdc=15*(Ip+Im);feedback=mean(v(f'fb{j}')*Ifb)
  chip.append({'plus_mA':Ip*1000,'minus_mA':Im*1000,'plus_check_mA':(.0168+mean(np.maximum(Itotal,0)))*1000,'minus_check_mA':(.0168+mean(np.maximum(-Itotal,0)))*1000,'dc_W':pdc,'heat_W':pdc-rf-feedback,'external_real_output_W':rf,'feedback_loss_W':feedback,'pin_Vpp':float(np.ptp(v(f'pa_out{j}'))),'pin_mean_V':mean(v(f'pa_out{j}')),'peak_current_mA':peak(f'vpaout{j}#branch')*1000,'rms_current_mA':np.sqrt(mean(I*I))*1000,'mean_current_mA':mean(I)*1000})
 totalI=sum(v(f'vpaout{j}#branch') for j in range(n));load_ac=sum(x['external_real_output_W'] for x in chip)
 branch_loss=[mean(v(f'vpaout{j}#branch')**2)*branch for j in range(n)]
 circulating=np.minimum(np.maximum(v('vpaout0#branch'),0),np.maximum(-v('vpaout1#branch'),0))+np.minimum(np.maximum(v('vpaout1#branch'),0),np.maximum(-v('vpaout0#branch'),0)) if n==2 else np.zeros_like(q)
 node=amp('final');p1=node*node/100
 winding=[]
 for prefix,network in [('fi',parts['input']),('fo',parts['output'])]:
  for j,c in enumerate(network):
   if c['kind']!='L':continue
   cur=v(f'l{prefix}{j}#branch');count=c['count_parallel']
   winding.append({'network':prefix,'position':j+1,'mpn':c['mpn'],'count_parallel':count,'rms_each_A':float(np.sqrt(mean(cur*cur))/count),'peak_each_A':peak(f'l{prefix}{j}#branch')/count,'published_current_A':c['irms_each_A'],'published_isat_A':c['isat_each_A']})
 outrow={'case':name,'f_Hz':f,'chips':n,'feedback_trace_ohms':1.5,'branch_inductance_H':5e-9,'input_stray_cap_each_F':1e-12,'divider_voltage_ratio':alpha,'additional_loss_dB_each':loss,'branch_ohms':branch,'common_ohms':common,'shunt_ohms':shunt,'step_divisor':step,'hypothetical_output_offset_each_V':offset,'inductor_Q':Q,'component_multipliers':tol,'matching_values_SI':[z['nominal'] for z in parts['output']],'hot_loss_multiplier':hot,'drive_voltage_scale':scale,'catalog_parts':parts,'winding_currents':winding,'fundamental_output_mW':p1*1000,'total_load_mW':mean(v('final')**2/50)*1000,'pa_join_Vpp':float(np.ptp(v('join'))),'chip':chip,'plus_total_mA':sum(x['plus_mA'] for x in chip),'minus_total_mA':sum(x['minus_mA'] for x in chip),'dc_total_W':sum(x['dc_W'] for x in chip),'heat_total_W':sum(x['heat_W'] for x in chip),'branch_resistor_loss_W':branch_loss,'filter_real_input_W':mean(v('of_in')*totalI),'output_filter_and_pad_loss_W':mean(v('of_in')*totalI)-mean(v('final')**2/50),'matching_input_fundamental_V':amp('of_in'),'matching_input_fundamental_I':float(2*abs(np.trapezoid(totalI*np.exp(-2j*np.pi*f*q),q))/(8*T)),'output_network_loss_W':load_ac-mean(v('final')**2/50),'circulating_peak_mA':float(np.max(circulating))*1000,'circulating_rms_mA':np.sqrt(mean(circulating**2))*1000,'input_fundamental_equiv50_mW':amp('divin')**2*10,'logic_5V_pullup_mA':mean(-v('vrail5#branch'))*1000,'logic_led_3V3_mA':mean(-v('vrail#branch'))*1000,'logic_channel_peak_mA':[peak(f'vsense{j}#branch')*1000 for j in [0,1]],'load_H3_dBc':float(20*np.log10(max(amp('final',3),1e-20)/node)),'state_drift_V':list(map(float,drift)),'periodic_initial_state_V':last_state,'solver_runs':count,'transient_points':len(t),'input_shunt_first':False}
 power=[]
 for k in [0,1]:
  u=np.linspace((52+4*k)*T,(56+4*k)*T,8001);y=np.interp(u,t,sp.vec('final'));a1=2*abs(np.trapezoid(y*np.exp(-2j*np.pi*f*u),u))/(4*T);power.append(a1*a1/100)
 outrow['late_power_drift_percent']=100*(power[1]/power[0]-1);assert abs(outrow['late_power_drift_percent'])<.1
 if True:np.savez_compressed(out/(name+'.npz'),t=q-52*T,pa_in=v('pa_in'),pa_out=v('pa_out0'),final=v('final'),current=totalI,raw=v('out'),logic_load=v('load'))
 (out/(name+'.json')).write_text(json.dumps(outrow,indent=2)+'\n');print(json.dumps(outrow),flush=True)
if a.case:run_case(*json.loads(a.case))
else:
 tasks=[[f,.5,.2,50,1000] for f in freqs]
 (out/'plan.json').write_text(json.dumps(tasks,indent=2)+'\n');rows=[]
 cmd=[sys.executable,str(Path(__file__).resolve()),'--research',str(a.research),'--output',str(out),'--board-runs',str(a.board_runs),'--single-runs',str(a.single_runs)]
 def worker(case):
  run=subprocess.run(cmd+['--case',json.dumps(case)],capture_output=True,text=True,timeout=600)
  if run.returncode:raise RuntimeError(str(case)+'\n'+run.stdout[-500:]+run.stderr[-2000:])
  return json.loads(run.stdout.strip().splitlines()[-1])
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  for row in pool.map(worker,tasks):rows.append(row);(out/'results.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(row),flush=True)
 print('COMPLETE',len(rows),flush=True)
