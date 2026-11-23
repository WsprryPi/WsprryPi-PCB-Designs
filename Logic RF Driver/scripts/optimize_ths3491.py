"""Calibrated band pads, passive tolerance/loss stresses, and numerical checks.
The target is a 650mW nominal capability setting with >=500mW stress margin.
It is not a closed-loop 500mW power regulator or a hardware qualification.
"""
from pathlib import Path
import sys,json,subprocess,concurrent.futures,math,argparse
ap=argparse.ArgumentParser();ap.add_argument('--research',type=Path,required=True);ap.add_argument('--runs',type=Path,required=True);a=ap.parse_args();p=Path(__file__).resolve().parents[1];g=a.runs.resolve();assessment=json.loads((g/'assessment.json').read_text());target=650
cmd=[sys.executable,str(p/'scripts/simulate_ths3491_optimized.py'),'--research',str(a.research),'--output',str(g),'--board-runs',str(p/'generated/board-rerun'),'--single-runs',str(p/'generated/ths3491-dual-matching')]
manifest=[]
def run(task):
 label,case=task
 c=subprocess.run(cmd+['--case',json.dumps(case)],capture_output=True,text=True,timeout=900)
 if c.returncode:raise RuntimeError(label+' '+str(case)+'\n'+c.stderr[-1800:])
 r=json.loads(c.stdout.strip().splitlines()[-1]);r['label']=label;r['arguments']=case
 return r
def batch(tasks):
 rows=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  for r in pool.map(run,tasks):
   rows.append(r);manifest.append(r);(g/'optimization-results.json').write_text(json.dumps(manifest,indent=2)+'\n');print(r['label'],r['f_Hz']/1e6,round(r['fundamental_output_mW'],2),round(max(c['pin_Vpp'] for c in r['chip']),3),round(max(c['heat_W'] for c in r['chip']),3),flush=True)
 return rows
def calibrated(label,f,alpha,tol=None):
 case=[f,alpha,.2,50,1000,tol];r=run((label+'-estimate',case));manifest.append(r)
 alpha*=math.sqrt(target/r['fundamental_output_mW']);r=run((label,[f,alpha,.2,50,1000,tol]));manifest.append(r)
 assert abs(r['fundamental_output_mW']/target-1)<.015,(label,r['fundamental_output_mW'])
 (g/'optimization-results.json').write_text(json.dumps(manifest,indent=2)+'\n');return r
# Parallelize one complete per-frequency calibration job at a time.
def caljob(x):
 f=x['f_Hz'];return calibrated('nominal',f,x['alpha_estimate']*math.sqrt(target/600))
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 nominal=list(pool.map(caljob,assessment))
for r in nominal:print('NOMINAL',r['f_Hz']/1e6,r['fundamental_output_mW'],flush=True)
# Shared manifest mutation in caljob is serialized by CPython; rewrite it from
# the returned results to ensure every final nominal row is retained.
manifest=[r for r in manifest if r['label'].endswith('-estimate')]+nominal
(g/'optimization-results.json').write_text(json.dumps(manifest,indent=2)+'\n')
tasks=[]
for x,n in zip(assessment,nominal):
 # Factory trim compensates the static component corner. The predicted trim
 # is verified by a complete transient. A second pass corrects residual error.
 for c in [x['corners'][0],x['corners'][2]]:
  tasks.append((x,n,c))
def cornerjob(t):
 x,n,c=t;return calibrated(c['label'],x['f_Hz'],n['divider_voltage_ratio']/math.sqrt(c['power_factor']),c['multipliers'])
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 corners=list(pool.map(cornerjob,tasks))
manifest=[r for r in manifest if r['label'].endswith('-estimate')]+nominal+corners
(g/'optimization-results.json').write_text(json.dumps(manifest,indent=2)+'\n')
stress=[]
for r in nominal+corners:
 case=r['arguments']+[0,1.25,.95] # opposing offset=0, 25% passive loss increase, 5% lower drive
 case[2]=.3 # additional PCB/contact loss per filter
 stress.append(('stress-'+r['label'],case))
batch(stress)
batch([('fine',[f,n['divider_voltage_ratio'],.2,50,2000,None]) for f in [137e3,145e6] for n in nominal if n['f_Hz']==f])
batch([('offset',[f,n['divider_voltage_ratio'],.2,50,1000,None,.0225]) for f in [137e3,145e6] for n in nominal if n['f_Hz']==f])
(g/'optimization-results.json').write_text(json.dumps(manifest,indent=2)+'\n');print('COMPLETE',len(manifest),flush=True)
