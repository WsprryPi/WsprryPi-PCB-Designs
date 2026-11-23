"""Orderable filter candidates; Coilcraft model coefficients evaluated at each tone.
Numerical parameters transcribed from the cited manufacturer model tables.
These per-tone RLC networks are not broadband causal fits of variable elements.
"""
import numpy as np
from scipy.optimize import minimize
FREQS=[137e3,475e3,1.8e6,3.5e6,7e6,10e6,14e6,21e6,28e6,50e6,70e6,100e6,145e6]
# code, L(uH), R1, R2, Cp(pF), k2, k4, k5, Isat(A), Irms(A)
PS=[['102',1,60,.054,.15,.064,1e-6,1e-6,2.5,2.7],['122',1.2,55,.06,.21,.075,.000803,.000062,2.2,2.6],['152',1.5,55,.06,.18,.076,.000781,.0000616,2,2.6],['222',2.2,90,.07,.2,.137,1e-6,.0000517,1.7,2.4],['272',2.7,60,.08,.22,.158,1e-6,.0000516,1.4,2.3],['332',3.3,35,.09,.27,.220,1e-6,.0000515,1.4,2.3],['392',3.9,25,.11,.22,.306,.00148,.0000514,1.2,2.2],['472',4.7,25,.11,.32,.355,.00147,.0000516,1.15,2.1],['562',5.6,22,.12,.29,.494,.00145,.0000514,1.1,2.1],['682',6.8,26,.13,.24,.518,.00141,.000051,1,1.9],['103',10,29,.17,.28,.741,.00140,.0000509,.9,1.7],['153',15,65,.26,.26,1.30,1e-6,.0000331,.7,1.45],['223',22,45,.33,.60,2.28,1e-6,.0000351,.54,1.2],['333',33,30,.40,.97,3.37,.278,.000000839,.46,1.1],['393',39,55,.56,1.08,4.10,.683,.000009,.4,1],['473',47,30,.87,.83,4.63,.647,.00000972,.35,.8],['683',68,35,1.1,1.13,7.52,1e-6,1e-6,.32,.67],['823',82,55,1.3,.84,7.51,1e-6,1e-6,.28,.65],['154',150,70,2.2,1.81,18.4,1e-6,1e-6,.20,.51]]
# code, nominal nH, R1, R2, Cp(pF), model nH, k, Irms(A)
CS=[['100',10,8,.1,.065,9.8,1.96e-5,1],['120',12,7,.1,.1,12,2.40e-5,1],['150',15,7,.1,.153,15,3.12e-5,1],['180',18,7,.1,.083,18,3.16e-5,1],['220',22,8,.1,.124,22,3.69e-5,1],['270',27,8,.1,.185,27,4.41e-5,1],['330',33,9,.1,.117,33,5.18e-5,1],['390',39,9,.2,.149,39,5.5e-5,1],['470',47,9,.2,.118,47,6.4e-5,1],['560',56,7,.2,.16,56,7.4e-5,1],['680',68,6,.2,.137,68,9.2e-5,1],['820',82,12,.2,.179,81,1.15e-4,1],['101',100,13,.6,.135,100,1.25e-4,.65],['121',120,13,.6,.136,120,1.51e-4,.65],['151',150,14,.7,.136,150,1.1e-4,.58],['181',180,18,.8,.13,180,1.4e-4,.62],['221',220,18,.8,.147,224,1.9e-4,.5],['271',270,19,.9,.144,265,2.32e-4,.5],['331',330,20,1.1,.132,330,2.84e-4,.45],['391',390,27,1.1,.138,380,3.49e-4,.47],['471',470,31,1.2,.156,465,4.27e-4,.47],['561',560,36,1.3,.172,550,5.18e-4,.4],['681',680,37,1.5,.139,665,6.10e-4,.4],['751',750,44,1.5,.138,740,6.90e-4,.36],['821',820,41,1.6,.135,810,8.10e-4,.4],['911',910,53,1.7,.155,895,7.80e-4,.38]]
CS += [['102',1000,90,1.8,.209,975,8.2e-4,.37],['122',1200,73,2,.201,1215,1.05e-3,.31],['152',1500,83,2.3,.249,1515,1.71e-3,.33],['182',1800,85,2.6,.278,1825,2.04e-3,.30],['222',2200,84,2.8,.258,2200,2.46e-3,.28],['272',2700,112,3.2,.398,2700,2.55e-3,.29],['332',3300,134,3.4,.285,3300,3.27e-3,.29],['392',3900,121,3.6,.401,3900,4.23e-3,.26],['472',4700,163,4,.381,4600,5e-3,.26],['562',5600,64,4,5.304,5250,3.04e-3,.24],['682',6800,148,4.9,1.357,6800,3.54e-3,.20],['822',8200,134,6,2.911,8200,4.38e-3,.17]]
# Bourns published Q is specified at its test frequency, not every tone.
# This engineering model uses that Q, DCR max, and SRF min; hot-loss
# sensitivities explicitly cover lower Q. Actual RF impedance is unmeasured.
BF=[['1R0',1,.15,40,180,.815],['1R2',1.2,.18,40,165,.740],['1R5',1.5,.20,50,150,.700],['1R8',1.8,.23,50,125,.655],['2R2',2.2,.25,50,110,.630],['2R7',2.7,.28,50,95,.595],['3R3',3.3,.30,50,60,.575],['3R9',3.9,.32,45,50,.555],['4R7',4.7,.35,45,38,.530],['5R6',5.6,.40,45,32,.500],['6R8',6.8,.45,40,28,.470],['8R2',8.2,.55,40,20,.425]]
def coil(target,output=False,frequency=0):
 if .95e-6<=target<=8.2e-6 and frequency<=10e6:
  x=min(BF,key=lambda x:abs(np.log(x[1]*1e-6/target)));suffix='K' if x[1]<3.3 else 'J'
  return {'kind':'L','family':'78F','code':x[0],'mpn':f'78F{x[0]}{suffix}-RC','count_parallel':1,'nominal':x[1]*1e-6,'tol':.1 if suffix=='K' else .05,'params':x[2:5],'isat_each_A':None,'irms_each_A':x[5]}
 if target>8.2e-6:
  count=2 if output and target>60e-6 else 1
  x=min(PS,key=lambda x:abs(np.log(x[1]*1e-6/count/target)))
  return {'kind':'L','family':'1812PS','code':x[0],'mpn':f'1812PS-{x[0]}JRC','count_parallel':count,'nominal':x[1]*1e-6/count,'tol':.05,'params':x[2:8],'isat_each_A':x[8],'irms_each_A':x[9]}
 x=min(CS,key=lambda x:abs(np.log(x[1]*1e-9/target)))
 return {'kind':'L','family':'1008CS','code':x[0],'mpn':f'1008CS-{x[0]}XGRC','count_parallel':1,'nominal':x[1]*1e-9,'tol':.02,'params':x[2:7],'isat_each_A':None,'irms_each_A':x[7]}
def cap(C):
 if C<=100e-12:
  e=[10,11,12,13,15,16,18,20,22,24,27,30,33,36,39,43,47,51,56,62,68,75,82,91,100];v=min(e,key=lambda x:abs(np.log(x*1e-12/C)));code=f'{int(v*10):03d}' if v<100 else '101';return {'kind':'C','mpn':f'GJM1555C1H{code}GB01D','nominal':v*1e-12,'tol':.02,'esl':.2e-9,'esr_floor':.05,'count_parallel':1}
 e=[m*10**n*1e-12 for n in range(1,5) for m in [10,12,15,18,22,27,33,39,47,56,68,82]];v=min(e,key=lambda x:abs(np.log(x/C)));pf=round(v*1e12);exp=0
 while pf>=100:pf=round(pf/10);exp+=1
 return {'kind':'C','mpn':f'C1206C{pf:02d}{exp}J5GACTU','nominal':v,'tol':.05,'esl':.6e-9,'esr_floor':.05,'count_parallel':1}
def elements(part,f,m=1,hot=1):
 if part['kind']=='C':return {'C':part['nominal']*m,'esl':part['esl'],'esr':hot*(part['esr_floor']+.001/(2*np.pi*f*part['nominal']*m))}
 n=part['count_parallel'];q=part['params']
 if part['family']=='78F':
  dc,qual,srf=q;L=part['nominal']*m
  return {'L':L,'Rs':hot*(dc+2*np.pi*f*L/qual),'Rp':1e30,'Cp':1/((2*np.pi*srf*1e6)**2*part['nominal']),'Rcp':.01}
 if part['family']=='1812PS':
  r1,r2,cp,k2,k4,k5=q;L=(part['nominal']*n*1e6-k4*np.log(k5*f))*1e-6*m;skin=1e-6*np.sqrt(f);core=k2*np.sqrt(f)/hot
 else:r1,r2,cp,l,k=q;L=l*1e-9*m;skin=k*np.sqrt(f);core=1e30
 return {'L':L/n,'Rs':hot*(r2+skin)/n,'Rp':core/n,'Cp':cp*1e-12*n,'Rcp':r1/n}
def impedance(part,f,m=1,hot=1,model_f=None):
 w=2*np.pi*f;e=elements(part,f if model_f is None else model_f,m,hot)
 if part['kind']=='C':return e['esr']+1j*w*e['esl']+1/(1j*w*e['C'])
 return e['Rs']+1/(1/(1j*w*e['L'])+1/e['Rp']+1/(e['Rcp']+1/(1j*w*e['Cp'])))
def matrix(parts,f,mults=None,hot=1,model_f=None):
 M=np.eye(2,dtype=complex)
 for j,part in enumerate(parts):
  z=impedance(part,f,1 if mults is None else mults[j],hot,model_f)
  M=M@ (np.array([[1,z],[0,1]]) if part['kind']=='L' else np.array([[1,0],[1/z,1]]))
 return M
def pad_matrix(db):
 if db==0:return np.eye(2,dtype=complex)
 k=10**(db/20);rp=50*(k+1)/(k-1);rs=50*(k*k-1)/(2*k)
 return np.array([[1,0],[1/rp,1]])@np.array([[1,rs],[0,1]])@np.array([[1,0],[1/rp,1]])
def response(parts,f,db=.2,mults=None,hot=1,model_f=None):
 M=matrix(parts,f,mults,hot,model_f)@pad_matrix(db);z=(M[0,0]*50+M[0,1])/(M[1,0]*50+M[1,1]);h=1/(M[0,0]+M[0,1]/50)
 return z,h
COUT={'kind':'C','nominal':200e-9,'tol':.05,'esl':.575e-9,'esr_floor':.003,'count_parallel':2,'mpn':'C3216C0G1H104J160AA'}
def ladder(f):
 g=[.61803398875,1.61803398875,2.,1.61803398875,.61803398875];w=2*np.pi*1.5*f
 return [50*x/w if j%2==0 else x/(50*w) for j,x in enumerate(g)]
def select(f):
 vals=ladder(f);w=2*np.pi*f
 inp=[coil(v,frequency=f) if j%2==0 else cap(v) for j,v in enumerate(vals)]
 z=50+0j
 for j in range(4,-1,-1):z=z+1j*w*vals[j] if j%2==0 else 1/(1/z+1j*w*vals[j])
 y=1/z;b=np.sqrt(y.real/25-y.real**2);lm=25*b/y.real/w+1/(w*w*COUT['nominal']);cm=(b-y.imag)/w
 out=[coil(lm,True,f),cap(cm),*[coil(v,True,f) if j%2==0 else cap(v) for j,v in enumerate(vals)]]
 # Discrete coordinate search of catalog capacitor values with fixed chosen coils.
 def score(ps):
  zin,h=response(ps,f);zt=zin+impedance(COUT,f);return abs((zt-25)/25)**2+ .03*abs(h)**-2
 for loop in range(4):
  for j in [1,3,5]:
   base=out[j]['nominal'];choices=[cap(base*k) for k in [.8,.9,1,1.1,1.2]];out[j]=min(choices,key=lambda c:score(out[:j]+[c]+out[j+1:]))
 return {'f_Hz':f,'input':inp,'output':out,'coupling':COUT,'extra_loss_each_dB':.2}
def netlist(prefix,src,dst,parts,f,mults=None,hot=1):
 lines=[];node=src
 for j,part in enumerate(parts):
  e=elements(part,f,1 if mults is None else mults[j],hot)
  if part['kind']=='L':
   end=dst if j==len(parts)-1 else f'{prefix}n{j}';mid=f'{prefix}m{j}';cp=f'{prefix}p{j}'
   lines += [f'R{prefix}s{j} {node} {mid} {e["Rs"]:.14g}',f'L{prefix}{j} {mid} {end} {e["L"]:.14g}',f'R{prefix}core{j} {mid} {end} {e["Rp"]:.14g}',f'C{prefix}{j} {mid} {cp} {e["Cp"]:.14g}',f'R{prefix}cp{j} {cp} {end} {e["Rcp"]:.14g}'];node=end
  else:
   c=f'{prefix}c{j}';l=f'{prefix}l{j}';lines += [f'R{prefix}{j} {node} {l} {e["esr"]:.14g}',f'L{prefix}c{j} {l} {c} {e["esl"]:.14g}',f'C{prefix}{j} {c} 0 {e["C"]:.14g}']
 return lines
