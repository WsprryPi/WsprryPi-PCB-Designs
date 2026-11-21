"""Publish derived Samsung rerun results; vendor sources remain local.
Usage: python3 script.py --project DIR --research DIR
"""
from pathlib import Path
import argparse,sys,json,csv,shutil,hashlib
p=argparse.ArgumentParser();p.add_argument('--project',type=Path,required=True);p.add_argument('--research',type=Path,required=True);a=p.parse_args();sys.path.insert(0,str(a.research/'python-packages'))
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=a.project;D=R/'generated/comparison-samsung';doc=R/'docs'
allrows=json.loads((D/'results.json').read_text());rows=[r for r in allrows if r['kind']!='choke'];assert len(rows)==78
checks=json.loads((D/'verification.json').read_text());extra=json.loads((D/'extra-verification.json').read_text());fit=json.loads((D/'fit-summary.json').read_text());fail=json.loads((D/'failures.json').read_text())
# Ideal-choke circuits are diagnostic-only after failed robustness checks.
for r in allrows:r['report_status']='retained_main_comparison' if r['kind']!='choke' else 'diagnostic_only_ideal_choke'
for name,data in [('simulation-samsung-results',rows),('simulation-samsung-diagnostics',allrows)]:
 (doc/(name+'.json')).write_text(json.dumps(data,indent=2)+'\n')
 with (doc/(name+'.csv')).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(allrows[0]),lineterminator='\n');w.writeheader();w.writerows(data)
mainchecks=[r for r in checks if r['kind']!='choke'];biaschecks=[r for r in extra['checks'] if r['kind']!='choke' and r['check_type']=='bias_recenter']
changes=[]
for r in rows:
 if r['c4_model']=='dc_bias':
  z=next(v for v in rows if (v['kind'],v['f_Hz'],v['model_rg'],v['c4_model'])==(r['kind'],r['f_Hz'],r['model_rg'],'zero_bias'));changes.append(dict(kind=r['kind'],f_Hz=r['f_Hz'],model_rg=r['model_rg'],power_change_percent=100*(r['p1_W']/z['p1_W']-1)))
verification={'main_cases':len(rows),'successful_diagnostic_runs':len(allrows)-len(rows),'planned_base_cases':130,'main_timestep_checks':mainchecks,'extra_bias_checks':biaschecks,'max_main_timestep_power_change_percent':max(abs(r['power_change_percent']) for r in mainchecks),'max_main_bias_recenter_power_change_percent':max(abs(r['power_change_percent']) for r in biaschecks),'max_main_late_window_power_change_percent':max(abs(r['late_window_power_change_percent']) for r in rows),'max_main_mean_load_voltage_V':max(abs(r['mean_load_V']) for r in rows),'bias_power_changes':changes,'fit':{k:{n:v for n,v in s.items() if n!='coefficients'} for k,s in fit.items()},'base_failures':fail,'ideal_choke_extra_checks':extra,'scope':'All ideal-choke runs excluded from main quantitative conclusions because robustness checks failed; original/modified-gate resistor circuits and logic retained.'}
(doc/'simulation-samsung-verification.json').write_text(json.dumps(verification,indent=2)+'\n')
F=sorted({r['f_Hz'] for r in rows});fig,(ax,delta)=plt.subplots(2,1,figsize=(9,7),sharex=True,gridspec_kw={'height_ratios':[3,1]},layout='constrained')
for kind,rg,color,label,style in [('logic',270,'#1769aa','Paralleled SN74LVC2T45','-'),('resistor',270,'#d45d00','BS170, 51-ohm drain resistor','-'),('resistor',5,'#777777','BS170, hypothetical 5-ohm internal gate R','--')]:
 selected=sorted([r for r in rows if r['kind']==kind and r['model_rg']==rg and r['c4_model']=='dc_bias'],key=lambda r:r['f_Hz']);zero=sorted([r for r in rows if r['kind']==kind and r['model_rg']==rg and r['c4_model']=='zero_bias'],key=lambda r:r['f_Hz'])
 x=np.array(F)/1e6;y=np.array([r['p1_W'] for r in selected])*1000;z=np.array([r['p1_W'] for r in zero])*1000
 ax.loglog(x,y,style,color=color,label=label,lw=2);ax.fill_between(x,np.minimum(y,z),np.maximum(y,z),color=color,alpha=.2);delta.semilogx(x,100*(y/z-1),style,color=color,lw=1.5)
ax.set(ylabel='Fundamental power into 50 ohms (mW)',title='Samsung C15849 C4: bias-dependent passive-fit simulation');ax.legend(loc='lower left',fontsize=9);ax.grid(True,which='both',alpha=.18)
delta.set(xlabel='Frequency (MHz)',ylabel='Bias effect (%)');delta.grid(True,which='both',alpha=.18);delta.axhline(0,color='black',lw=.5)
fig.savefig(doc/'comparison-samsung.png',dpi=180);plt.close(fig)
manifest={'engine':'ngspice','temperature_C':25,'part':'Samsung CL10A105KB8NNNC / C15849','conditions':'0/2.5/5 V precise graph exports; passive Foster fits, linear interpolation of common-basis coefficients at initialized periodic capacitor midpoint; 0..5 V bounded range; 60 periods, last eight Fourier integration, Gear, reltol=.001, 700/1400 step factors and additional verification.', 'provenance':'Original vendor sources and generated transistor-model decks remain local/ignored. Derived results and project scripts are published. No manufacturer SPICE execution or measured validation is claimed.','sha256':{}}
paths=[R/'scripts/rerun_samsung_comparison.py',R/'scripts/report_samsung_comparison.py',R/'scripts/check_samsung_c4.py',R/'scripts/verify_samsung_comparison.py',a.research/'simulate.py',a.research/'models/bs170.lib',a.research/'models/SN74LVC2T45.ibs']+[R/f'generated/samsung-c4-check/graph-{b}V.csv' for b in (0,2.5,5)]
for file in paths:manifest['sha256'][str(file.relative_to(R)) if file.is_relative_to(R) else str(file.relative_to(a.research))]=hashlib.sha256(file.read_bytes()).hexdigest()
manifest['retained_amplifier_deck_sha256']={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in (a.research/'practical-bs').glob('practical_*.cir')}
(doc/'comparison-samsung-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Published',len(rows),'main cases;',len(allrows)-len(rows),'diagnostic-only cases;',len(mainchecks),'main timestep checks;',len(biaschecks),'bias recenter checks')
