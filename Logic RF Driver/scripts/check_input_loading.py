"""Transient input-loading study; manufacturer models are separate local inputs."""
from pathlib import Path
import argparse,ctypes as ct,json,sys,re,hashlib,time
p=argparse.ArgumentParser();p.add_argument('--models',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--packages',type=Path);p.add_argument('--library',default='/Applications/KiCad/KiCad.app/Contents/Frameworks/libngspice.0.dylib');p.add_argument('--case',required=True);a=p.parse_args()
if a.packages:sys.path.insert(0,str(a.packages))
import numpy as np
case=json.loads(a.case);f=case['f_Hz'];rs=case.get('source_ohms',50);loaded=case.get('detector',True);tt=case.get('tt_scale',1);cscale=case.get('cjo_scale',1);r2=case.get('r2_ohms',100);edge=case.get('edge_s',.5e-9);step=case.get('step_factor',160);settle=case.get('settle_s',20e-6);T=1/f;end=max(40*T,settle) if 'periods' not in case else case['periods']*T;end=(np.ceil(end/T)+.23)*T
name=case.get('name',f'f{f:g}_r{rs:g}_d{int(loaded)}_tt{tt:g}_c{cscale:g}_r2{r2:g}_s{step}')
out=a.output;out.mkdir(parents=True,exist_ok=True)
logs=[]
CB=ct.CFUNCTYPE(ct.c_int,ct.c_char_p,ct.c_int,ct.c_void_p);EC=ct.CFUNCTYPE(ct.c_int,ct.c_int,ct.c_bool,ct.c_bool,ct.c_int,ct.c_void_p)
cb=CB(lambda s,*args:logs.append(s.decode(errors='replace')) or 0);ec=EC(lambda *args:0)
lib=ct.CDLL(a.library);lib.ngSpice_Init.argtypes=[ct.c_void_p]*7;lib.ngSpice_Init(cb,None,ec,None,None,None,None);lib.ngSpice_Command.argtypes=[ct.c_char_p];lib.ngSpice_Circ.argtypes=[ct.POINTER(ct.c_char_p)]
class Vec(ct.Structure):_fields_=[('name',ct.c_char_p),('type',ct.c_int),('flags',ct.c_short),('real',ct.POINTER(ct.c_double)),('comp',ct.c_void_p),('length',ct.c_int)]
lib.ngGet_Vec_Info.argtypes=[ct.c_char_p];lib.ngGet_Vec_Info.restype=ct.POINTER(Vec)
def vec(n):
 v=lib.ngGet_Vec_Info(n.encode());assert v and v.contents.length>0,(n,logs[-12:]);return np.ctypeslib.as_array(v.contents.real,shape=(v.contents.length,)).copy()
models=[]
for n in ['BAT54S.txt','MMBT3904.txt']:
 t=(a.models/n).read_text()
 if n=='BAT54S.txt':
  t=re.sub(r'CJO=13.3p',f'CJO={13.3e-12*cscale:.12g}',t,flags=re.I);t=re.sub(r'TT=7.20n',f'TT={7.2e-9*tt:.12g}',t,flags=re.I)
 models.extend(t.splitlines())
lines=[name,f'Vdrive src 0 PULSE(0 3.3 0 {edge:.12g} {edge:.12g} {T/2-edge:.12g} {T:.12g})',f'Rsource src clock {rs}','R1 clock 0 10k',f'Cin clock 0 {case.get("input_pf",14):g}p','Vrail rail 0 3.3',*models]
if loaded:
 lines += [f'R2 clock capin {r2}','Resr5 capin esr5 .05','Lesl5 esr5 c5left .7n',f'C5 c5left com 10n IC={case.get("ic5",1.1):.12g}','Rleadcom com lc .1','Ldcom lc dc 1n','Rleadground 0 lg .1','Ldground lg da 1n','Rleadout dk lo .1','Ldout lo base 1n','Dlow da dc DI_BAT54S','Dhigh dc dk DI_BAT54S','Resr6 base esr6 .05','Lesl6 esr6 c6top .7n',f'C6 c6top 0 10n IC={case.get("ic6",.65):.12g}','R3 base 0 1meg','Q1 collector base 0 DI_MMBT3904','R4 rail ledtop 680','Vled ledtop leda 0','Dled leda collector LED_APPROX','.model LED_APPROX D(IS=1e-20 N=2 RS=5 CJO=2p)']
if not case.get('parasitics',False):
 lines=[re.sub(r'^L(\w+) (\S+) (\S+) \S+$',r'RzeroL\1 \2 \3 1m',line) for line in lines]
lines += ['.options method=gear maxord=2 reltol=0.0001 abstol=1e-12',f'.tran {T/200:.12g} {end:.12g} 0 {min(T/step,1e-9):.12g} uic','.end']
(out/f'{name}.cir').write_text('\n'.join(lines)+'\n');arr=(ct.c_char_p*(len(lines)+1))(*[s.encode() for s in lines],None);start=time.monotonic();lib.ngSpice_Command(b'destroy all');lib.ngSpice_Circ(arr);lib.ngSpice_Command(b'run');(out/f'{name}.log').write_text('\n'.join(logs))
if any('aborted' in s.lower() or s.startswith('stderr Error') for s in logs):raise RuntimeError(logs[-20:])
t=vec('time');assert t[-1]>=end*(1-1e-8),'Integration incomplete'
lo=end-8*T
u=np.r_[lo,t[(t>lo)&(t<end)],end];v=np.interp(u,t,vec('clock'));src=np.interp(u,t,vec('src'));i=-np.interp(u,t,vec('vdrive#branch'));mean=lambda y:float(np.trapezoid(y,u)/(8*T))
def fraction_above(level):
 x=v[:-1];y=v[1:];fraction=np.where((x>=level)&(y>=level),1.,0.);cross=(x-level)*(y-level)<0;z=np.divide(level-x,y-x,out=np.zeros_like(x),where=y!=x);fraction=np.where(cross,np.where(y>x,1-z,z),fraction);return float(np.sum(np.diff(u)*fraction)/(8*T))
phase=u%T
result={**case,'name':name,'periods':float(end/T),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'duration_s':float(end),'v_min':float(v.min()),'v_max':float(v.max()),'source_peak_mA':float(i.max()*1000),'source_sink_peak_mA':float(-i.min()*1000),'source_rail_equivalent_mA':mean(src*i/3.3)*1000,'time_above_2V_fraction':fraction_above(2),'time_below_0p8V_fraction':1-fraction_above(.8),'runtime_s':time.monotonic()-start,'timestep_max_s':min(T/step,1e-9)}
def crossing(level,direction):
 mask=u>=end-T;q=u[mask];w=v[mask];idx=np.flatnonzero((w[:-1]<level)&(w[1:]>=level)) if direction=='r' else np.flatnonzero((w[:-1]>level)&(w[1:]<=level))
 if len(idx)!=1:return None
 k=idx[0];return float(q[k]+(level-w[k])/(w[k+1]-w[k])*(q[k+1]-q[k]))
for direction,key in [('r','rise_20_80_ns'),('f','fall_80_20_ns')]:
 x=crossing(.66 if direction=='r' else 2.64,direction);y=crossing(2.64 if direction=='r' else .66,direction);result[key]=None if x is None or y is None else ((y-x)%T)*1e9
trace_t=np.linspace(end-2*T,end,8001)
trace={'t_s':trace_t-(end-2*T),'clock_V':np.interp(trace_t,u,v),'source_V':np.interp(trace_t,u,src),'source_A':np.interp(trace_t,u,i)}
if loaded:
 base=np.interp(u,t,vec('base'));com=np.interp(u,t,vec('com'));left=np.interp(u,t,vec('c5left'));il=np.interp(u,t,vec('vled#branch'));branch=(v-np.interp(u,t,vec('capin')))/r2
 result.update(base_mean_V=mean(base),c5_mean_V=mean(left-com),led_mean_mA=mean(il)*1000,detector_positive_charge_mA=mean(np.maximum(branch,0))*1000,detector_peak_mA=float(np.max(abs(branch)))*1000)
 # Compare separate late windows using their own time axes.
 def win_mean(node,lo,hi):
  q=np.r_[lo,t[(t>lo)&(t<hi)],hi];return float(np.trapezoid(np.interp(q,t,vec(node)),q)/(hi-lo))
 result['base_late_drift_mV']=1000*(win_mean('base',end-4*T,end)-win_mean('base',end-8*T,end-4*T))
 result['c5_late_drift_mV']=1000*((win_mean('c5left',end-4*T,end)-win_mean('com',end-4*T,end))-(win_mean('c5left',end-8*T,end-4*T)-win_mean('com',end-8*T,end-4*T)))
 trace['detector_A']=np.interp(trace_t,u,branch);trace['base_V']=np.interp(trace_t,u,base)
 states=[vec('c5left')-vec('com'),vec('c6top')]
 result['state_end_V']=[float(np.interp(end,t,y)) for y in states]
 result['state_drift_V']=[float(np.interp(end,t,y)-np.interp(end-20*T,t,y)) for y in states]
np.savez_compressed(out/f'{name}.npz',**trace);(out/f'{name}.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
