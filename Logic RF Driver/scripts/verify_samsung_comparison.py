"""Additional timestep and small bias-recentering checks; local research sources required."""
from pathlib import Path
import json,subprocess,concurrent.futures,sys
import argparse
args=argparse.ArgumentParser();args.add_argument('--project',type=Path,required=True);args.add_argument('--research',type=Path,required=True);args=args.parse_args()
p=args.project;d=p/'generated/comparison-samsung';research=args.research
command=[sys.executable,str(p/'scripts/rerun_samsung_comparison.py'),'--research',str(research),'--source',str(p/'generated/samsung-c4-check'),'--output',str(d)]
rows=json.loads((d/'results.json').read_text());checks=[];fail=[]
tasks=[(r,[r['kind'],r['f_Hz'],r['model_rg'],r['c4_model'],1400], 'extra_timestep') for r in rows if r['kind']=='choke' and r['model_rg']==270 and r['f_Hz'] in (3.5e6,7e6,10e6)]
tasks += [(r,[r['kind'],r['f_Hz'],r['model_rg'],r['c4_model'],r['step_factor'],r['mean_capacitor_V']],'bias_recenter') for r in rows if r['c4_model']=='dc_bias' and r['model_rg']==270 and r['f_Hz'] in (137e3,7e6,145e6)]
def run(t):
 r,task,kind=t
 try:
  out=subprocess.run(command+['--case',json.dumps(task)],capture_output=True,text=True,timeout=40);assert out.returncode==0,out.stdout[-250:]+out.stderr[-250:];v=json.loads(out.stdout.split('CASE_RESULT ')[-1]);v['check_type']=kind;v['power_change_percent']=100*(v['p1_W']/r['p1_W']-1);return v,None
 except Exception as e:return None,{'task':task,'check_type':kind,'reason':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for r,f in pool.map(run,tasks):
  if r:checks.append(r)
  else:fail.append(f)
  (d/'extra-verification.json').write_text(json.dumps({'checks':checks,'failures':fail},indent=2)+'\n')
print('extra checks',len(checks),'failures',len(fail));print([(r['kind'],r['f_Hz'],r['c4_model'],r['check_type'],r['power_change_percent']) for r in checks])
